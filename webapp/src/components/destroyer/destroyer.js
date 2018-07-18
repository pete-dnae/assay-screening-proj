import { modal } from 'vue-strap';
import * as api from '@/models/api';

export default {
  props: {
    show: Boolean,
    experimentName: String,
    plateName: String,
  },
  components: {
    modal,
  },
  data() {
    return { DeleteFeedBack: null };
  },
  methods: {
    handleExit() {
      this.$emit('exit');
    },
    handleLabchipDelete() {
      this.DeleteFeedBack = null;
      api
        .removeLabchipWells({
          plate_id: this.plateName,
          experiment_id: this.experimentName,
        })
        .then(({ data }) => {
          this.DeleteFeedBack = data.msg;
        }, (response) => {
          this.DeleteFeedBack = response;
        });
    },
    handleQpcrDelete() {
      this.DeleteFeedBack = null;
      api
        .removeQpcrWells({
          plate_id: this.plateName,
          experiment_id: this.experimentName,
        })
        .then(({ data }) => {
          this.DeleteFeedBack = data.msg;
        }, (response) => {
          this.DeleteFeedBack = response;
        });
    },
  },
};
