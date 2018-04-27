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
      invalidExpName: false,
      experimentNameTaken: false,
    };
  },
  components: {
    typeahead,
    tooltip,
    modal,
  },
  watch: {
    experiment() {
      if (this.data.includes(this.experiment)) {
        this.experimentNameTaken = true;
      } else if (!this.experiment.match(/^[a-zA-Z0-9_ ]+$/)) {
        this.invalidExpName = true;
      } else {
        this.experimentNameTaken = false;
        this.invalidExpName = false;
      }
    },
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
      this.loadExperiment(value);
    },
    handleSave(experimentName) {
      this.saveExperimentAs(experimentName).then((data) => {
        this.loadExperiment(data.experiment_name);
        this.showModal = false;
        this.fetchExperimentList().then(() => {
          this.mapData();
        });
      });
    },
    loadExperiment(experimentName) {
      this.fetchExperiment({ experimentName });
    },
  },
  mounted() {
    this.fetchExperimentList().then(() => {
      this.mapData();
    });
  },
};
