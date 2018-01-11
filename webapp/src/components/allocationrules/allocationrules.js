import Vue from 'vue';
import draggable from 'vuedraggable';
import { getNewIndex } from '@/models/utils';

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
        return this.$store.state.experiment.experiment.plates[this.$route.params.plateId]
          .allocation_instructions.allocation_rules;
      },
      set(value) {
        this.$store.commit('SET_RULE_ORDER_CHANGE', {
          data: value,
          plateId: this.$route.params.plateId,
        });
      },
    },
  },
  methods: {
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
