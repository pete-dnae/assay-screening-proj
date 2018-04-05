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
    }),
    currentExperiment: {
      get() {
        return this.$store.state.scriptparser.experiment.currentExperiment.name;
      },
    },
  },
  methods: {
    ...mapActions([
      'fetchExperimentList',
      'saveExperimentAs',
      'fetchExperiment',
    ]),
    mapData() {
      this.data = this.experiments.map(expObject => expObject.experiment_name);
    },
    loadExperimentFromName(value) {
      const exptNo = this.experiments.find(
        expObject => expObject.experiment_name === value,
      ).id;
      this.loadExperiment(exptNo);
    },
    handleSave(experimentName) {
      this.saveExperimentAs(experimentName).then((data) => {
        this.loadExperiment(data.id);
        this.showModal = false;
        this.fetchExperimentList().then(() => {
          this.mapData();
        });
      });
    },
    loadExperiment(exptNo) {
      this.fetchExperiment({ exptNo });
    },
  },
  mounted() {
    this.fetchExperimentList().then(() => {
      this.mapData();
    });
  },
};
