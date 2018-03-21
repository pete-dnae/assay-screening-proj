import typeahead from '@/components/typeahead/Typeahead';

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
