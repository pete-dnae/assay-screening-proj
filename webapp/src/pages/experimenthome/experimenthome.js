import experimentmenu from '@/components/experimentmenu/experimentmenu.vue';
import experimentbody from '@/components/experimentbody/experimentbody.vue';

export default {
  name: 'ExperimentHome',
  components: { experimentmenu, experimentbody },
  data() {
    return {
      msg: 'Welcome',
    };
  },
};
