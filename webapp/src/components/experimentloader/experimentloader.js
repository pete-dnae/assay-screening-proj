import Vue from 'vue';
import typeahead from '@/components/typeahead/typeahead.vue';
import { mapActions, mapGetters } from 'vuex';

Vue.component('typeahead', typeahead);
export default {
  name: 'ExperimentLoader',
  components: {
    typeahead,
  },
  data() {
    return {
      msg: 'This is Experiment Loader',
      currentExpt: '',
      showTypehead: false,
    };
  },
  watch: {
    currentExpt() {
      this.$emit('experimentChange', this.currentExpt);
    },
  },
  methods: {
    ...mapActions(['fetchExperimentList', 'fetchExperiment']),
    handleTypeheadBack() {
      this.showTypehead = false;
    },
  },
  computed: {
    ...mapGetters({
      expts: 'getExperimentList',
    }),
  },
  mounted() {
    this.fetchExperimentList();
  },
};
