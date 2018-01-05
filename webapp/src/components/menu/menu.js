import Vue from 'vue';
import experimentloader from '@/components/experimentloader/experimentloader.vue';

Vue.component('ExptLoad', experimentloader);
export default {
  name: 'HelloWorld',
  data() {
    return {
      msg: 'Welcome to Your Vue.js App ',
      currentExpt: '',
      showDropDown: false,
    };
  },
  methods: {
    handleExptChange(expt) {
      this.currentExpt = expt;
    },
  },
};
