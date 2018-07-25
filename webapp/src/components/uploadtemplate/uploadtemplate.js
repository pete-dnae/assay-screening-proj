import { modal } from 'vue-strap';
import * as api from '@/models/api';
import loader from '@/components/loader';

export default {
  name: 'pictures',
  components: {
    modal,
    loader,
  },
  props: {
    show: Boolean,
    availablePools: Array,
  },
  data() {
    return {
      showUpload: false,
      disableUpload: true,
      paMastermix: null,
      idMastermix: null,
      paConc: null,
      paUnit: null,
      idConc: null,
      idUnit: null,
      dilution: null,
      uploadFeedBack: null,
      isPosting: false,
      posted: false,
      didInvalidate: false,
    };
  },
  methods: {
    handleTemplateUpload() {
      const formData = new FormData();
      const file = document.getElementById('templateFile');
      formData.append('file', file.files[0]);
      formData.append('pa_mastermix', this.paMastermix);
      formData.append('pa_primer_conc', this.paConc);
      formData.append('pa_primer_unit', this.paUnit);
      formData.append('id_mastermix', this.idMastermix);
      formData.append('id_primer_conc', this.idConc);
      formData.append('id_primer_unit', this.idUnit);
      formData.append('dilution', this.dilution);
      this.isPosting = true;
      this.posted = false;
      this.didInvalidate = false;
      api.postTemplateFile(formData).then(
        ({ data }) => {
          this.isPosting = false;
          this.posted = true;
          this.didInvalidate = false;
          this.$emit('ruleScript', data.join('\n'));
        },
        ({ response }) => {
          this.isPosting = false;
          this.posted = false;
          this.didInvalidate = true;
          this.uploadFeedBack = response.data;
        },
      ).catch((e) => {
        this.uploadFeedBack = `Upload Failure 
                                    ${e.toString()}
                                `;
      });
    },
    handleExit() {
      this.$emit('exit');
    },
  },
};
