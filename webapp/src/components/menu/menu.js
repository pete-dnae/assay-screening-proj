import Vue from 'vue';
import { mapGetters, mapActions } from 'vuex';
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
  computed: {
    ...mapGetters({
      designerName: 'getDesignerName',
      experimentName: 'getExperimentName',
    }),
  },
  methods: {
    handleExptChange(expt) {
      this.currentExpt = expt;
    },
  },
};
