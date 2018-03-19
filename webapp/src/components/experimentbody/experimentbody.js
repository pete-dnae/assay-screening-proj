import scriptinput from '@/components/scriptinput/scriptinput.vue';
import languageSpec from '@/components/languagespec.vue';

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
