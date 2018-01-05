import Vue from 'vue';
import { typeahead } from 'vue-strap';

Vue.component('typeahead', typeahead);
export default {
  name: 'ExperimentLoader',
  data() {
    return {
      msg: 'This is Experiment Loader',
      expts: ['A81_E008', 'A81_E009', 'A81_E010'],
      currentExpt: '',
    };
  },
  watch: {
    currentExpt() {
      this.$emit('experimentChange', this.currentExpt);
    },
  },
};
