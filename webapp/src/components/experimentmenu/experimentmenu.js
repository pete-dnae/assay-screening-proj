import typeahead from '@/components/typeahead/Typeahead.vue';

export default {
  name: 'ExperimentMenu',
  data() {
    return {
      msg: 'Welcome to menu',
      USstate: ['Alabama', 'Alaska', 'Arizona'],
    };
  },
  components: {
    typeahead,
  },
};
