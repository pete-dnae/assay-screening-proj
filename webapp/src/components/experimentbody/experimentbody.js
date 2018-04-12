import scriptinput from '@/components/scriptinput/scriptinput.vue';
import languageSpec from '@/components/languagespec';

export default {
  name: 'ExperimentBody',
  components: {
    scriptinput,
    languageSpec,
  },
  data() {
    return {
      msg: 'Welcome',
    };
  },
};
