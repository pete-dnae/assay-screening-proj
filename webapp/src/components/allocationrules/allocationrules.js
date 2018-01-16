import draggable from 'vuedraggable';
import _ from 'lodash';
import { mapActions } from 'vuex';

export default {
  name: 'AllocationRules',
  components: {
    draggable,
  },
  data() {
    return {
      msg: 'Welcome',
    };
  },
  computed: {
    rules: {
      get() {
        return this.$store.state.experiment.currentPlate.allocation_instructions.rule_list.rules;
      },
      set(value) {
        this.updateAllocationRules({
          data: _.map(value, 'id'),
          url: this.$store.state.experiment.currentPlate.url,
        });
      },
    },
  },
  methods: {
    ...mapActions(['updateAllocationRules']),
    handleSelect(evt) {
      this.$emit('selectedRule', this.rules[evt.oldIndex]);
    },
    handleDelete(evt) {
      this.$emit('deletedRule', this.rules[evt.oldIndex]);
    },
    handleAddRule() {
      this.$emit('requestNewRule');
    },
  },
};
