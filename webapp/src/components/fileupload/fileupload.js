import { modal } from 'vue-strap';
import * as api from '@/models/api';

export default {
  name: 'pictures',
  components: {
    modal,
  },
  data() {
    return { showUpload: false, disableUpload: true, uploadFeedBack: null };
  },
  props: {
    show: Boolean,
    experimentName: String,
    plateName: String,
  },
  methods: {
    handleLabchipUpload() {
      this.uploadFeedBack = null;
      const formData = new FormData();
      const file = document.getElementById('fileLoad');
      formData.append('file', file.files[0]);
      formData.append('experimentName', this.experimentName);
      formData.append('plateName', this.plateName);
      api
        .postLabchipResults(formData)
        .then(({ data }) => {
          this.uploadFeedBack = `Upload sucessful for plate ${data.plate_id}
              Wells Extracted :  ${data.wells}`;
        }, ({ response }) => {
          this.uploadFeedBack = `Upload Failure 
                                    ${response.data}
                                `;
        })
        .catch((e) => {
          this.uploadFeedBack = `Upload Failure 
                                    ${e.toString()}
                                `;
        });
    },
    handleQpcrUpload() {
      this.uploadFeedBack = null;
      const formData = new FormData();
      const file = document.getElementById('fileLoad');
      formData.append('file', file.files[0]);
      formData.append('experimentName', this.experimentName);
      formData.append('plateName', this.plateName);
      api
        .postQpcrResults(formData)
        .then(
          ({ data }) => {
            this.uploadFeedBack = `Upload sucessful for plate ${data.plate_id}
              Wells Extracted :  ${data.wells}`;
          },
          ({ response }) => {
            this.uploadFeedBack = `Upload Failure 
                                    ${response.data}
                                `;
          },
        )
        .catch((e) => {
          this.uploadFeedBack = `Upload Failure 
                                    ${e.toString()}
                                `;
        });
    },
    handleExit() {
      this.$emit('exit');
    },
    getFileInfo() {
      const x = document.getElementById('fileLoad');
      let txt = '';
      if ('files' in x) {
        if (x.files.length !== 1) {
          this.disableUpload = true;
          txt = 'Select a file.';
        } else {
          this.disableUpload = false;
          for (let i = 0; i < x.files.length; i += 1) {
            txt += `<br><strong> ${i + 1}. file</strong><br>`;
            const file = x.files[i];
            if ('name' in file) {
              txt += `name: ${file.name}<br>`;
            }
            if ('size' in file) {
              txt += `size: ${file.size} bytes <br>`;
            }
          }
        }
      } else if (x.value === '') {
        this.disableUpload = true;
        txt += 'Select a file.';
      } else {
        txt += 'The files property is not supported by your browser!';
        txt += `<br>The path of the selected file:  ${x.value}`; // If the browser does not support the files property, it will return the path of the selected file instead.
      }
      document.getElementById('info').innerHTML = txt;
    },
  },
};
