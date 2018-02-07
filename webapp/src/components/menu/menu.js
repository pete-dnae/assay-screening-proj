import Vue from 'vue';
import { mapGetters, mapActions } from 'vuex';
import experimentloader from '@/components/experimentloader/experimentloader.vue';
import { modal } from 'vue-strap';

export default {
  name: 'HelloWorld',
  components: {
    modal,
    experimentloader,
  },
  data() {
    return {
      msg: 'Welcome to Your Vue.js App ',
      currentExpt: '',
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
