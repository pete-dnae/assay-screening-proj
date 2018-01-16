import draggable from 'vuedraggable';
import _ from 'lodash';
import {
  mapActions, mapGetters,
} from 'vuex';
import {
  spinner,
} from 'vue-strap';


export default {
  name: 'AllocationRules',
  components: {
    draggable,
    spinner,
  },
  data() {
    return {
      msg: 'Welcome',
    };
  },
  computed: {
    ...mapGetters({
      spin: 'getPostingStatus',
    }),
    rules: {
      get() {
        return this.$store.state.experiment.currentPlate.allocation_instructions.rule_list.rules;
      },
      set(value) {
        this.updateAllocationRules({
          data: {
            new_rules: _.map(value, 'id'),
          },
          url: this.$store.state.experiment.currentPlate.allocation_instructions.rule_list.url,
        }).then(() => {
          this.fetchExperiment('1').then((res) => {
            this.$store.commit('SET_CURRENT_PLATE', res.plates[parseInt(this.$route.params.plateId, 10)]);
            this.$emit('ruleChanged');
          });
        });
      },
    },
  },
  methods: {
    ...mapActions(['updateAllocationRules', 'fetchExperiment']),
    handleSelect(evt) {
      this.$emit('selectedRule', this.rules[evt.oldIndex]);
    },
    handleDelete(evt) {
      this.updateAllocationRules({
        data: {
          new_rules: _.map(_.filter(this.rules, (x, i) => i !== evt.oldIndex), 'id'),
        },
        url: this.$store.state.experiment.currentPlate.allocation_instructions.rule_list.url,
      }).then(() => {
        this.fetchExperiment('1').then((res) => {
          this.$store.commit('SET_CURRENT_PLATE', res.plates[parseInt(this.$route.params.plateId, 10)]);
          this.$emit('ruleChanged');
        });
      });
    },
    handleAddRule() {
      this.$emit('requestNewRule');
    },
  },
};
