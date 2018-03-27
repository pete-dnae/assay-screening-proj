import typeahead from '@/components/typeahead/Typeahead.vue';
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'ExperimentMenu',
  data() {
    return {
      msg: 'Welcome to menu',
      data: null,
    };
  },
  components: {
    typeahead,
  },
  computed: {
    ...mapGetters({
      experiments: 'getExperimentList',
      currentExperiment: 'getCurrentExperiment',
    }),
  },
  methods: {
    ...mapActions([
      'fetchExperimentList',
    ]),
    handleLoadedExperiment(value) {
      this.currentExperiment = value;
    },
  },
  mounted() {
    this.fetchExperimentList().then(() => {
      this.data = this.experiments.map(expObject => expObject.experiment_name);
    });
  },
};
