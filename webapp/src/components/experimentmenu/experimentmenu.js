import typeahead from '@/components/typeahead/Typeahead.vue';
import { mapGetters, mapActions } from 'vuex';
import { tooltip, modal } from 'vue-strap';

export default {
  name: 'ExperimentMenu',
  data() {
    return {
      msg: 'Welcome to menu',
      data: null,
      showModal: false,
      experiment: null,
    };
  },
  components: {
    typeahead,
    tooltip,
    modal,
  },
  computed: {
    ...mapGetters({
      experiments: 'getExperimentList',
      currentExperiment: 'getCurrentExperiment',
    }),
  },
  methods: {
    ...mapActions(['fetchExperimentList', 'saveExperimentAs']),
    handleLoadedExperiment(value) {
      this.currentExperiment = value;
    },
    handleSave(experimentName) {
      this.saveExperimentAs(experimentName).then((data) => {
        const exptNo = data.url.match('/[0-9]+/')[0].match(/[0-9]+/g)[0];
        this.$router.push({ path: '/experiment', params: { exptNo } });
      });
    },
  },
  mounted() {
    this.fetchExperimentList().then(() => {
      this.data = this.experiments.map(expObject => expObject.experiment_name);
    });
  },
};
