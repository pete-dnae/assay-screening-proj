import allocationholder from '@/components/allocationholder/allocationholder.vue';
import scriptinput from '@/components/scriptinput/scriptinput.vue';
import languageSpec from '@/components/languagespec.vue';

export default {
  name: 'ExperimentBody',
  components: {
    allocationholder,
    scriptinput,
    languageSpec,
  },
  data() {
    return {
      msg: 'Welcome',
    };
  },
};
