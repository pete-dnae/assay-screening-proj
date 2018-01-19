import draggable from 'vuedraggable';
import _ from 'lodash';
import { mapActions, mapGetters } from 'vuex';
import { spinner } from 'vue-strap';
import { prepareResultsTable, makeSVG, genCharArray } from '@/models/utils';

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
      allocationResults: 'getAllocationResults',
    }),
    rules: {
      get() {
        return this.$store.state.plate.currentPlate.allocation_instructions
          .rule_list.rules;
      },
      set(changedRules) {
        this.handleUpdateAllocation(_.map(changedRules, 'id'));
      },
    },
  },
  methods: {
    ...mapActions([
      'updateAllocationRules',
      'fetchExperiment',
      'addAllocationRule',
    ]),
    handleSelect(evt) {
      this.$emit('selectedRule', this.rules[evt.oldIndex]);
      this.drawTableImage({
        rows: genCharArray(
          this.rules[evt.oldIndex].start_row_letter,
          this.rules[evt.oldIndex].end_row_letter,
        ),
        cols: _.range(
          this.rules[evt.oldIndex].start_column - 1,
          this.rules[evt.oldIndex].end_column,
        ),
      });
    },
    handleDelete(deletedRule) {
      this.handleUpdateAllocation(
        _.map(_.filter(this.rules, (x, i) => i !== deletedRule.oldIndex), 'id'),
      );
    },
    handleAddRule() {
      this.addAllocationRule({
        data: {
          rule_to_copy: this.$store.state.rule.currentRule.id,
        },
        url: this.$store.state.plate.currentPlate.allocation_instructions
          .rule_list.url,
      }).then(() => {
        this.fetchExperiment('1').then(res => {
          this.$store.commit(
            'SET_CURRENT_PLATE',
            res.plates[parseInt(this.$route.params.plateId, 10)],
          );
          this.$emit('ruleChanged');
        });
      });
    },
    handleUpdateAllocation(data) {
      this.updateAllocationRules({
        data: {
          new_rules: data,
        },
        url: this.$store.state.plate.currentPlate.allocation_instructions
          .rule_list.url,
      }).then(() => {
        this.fetchExperiment('1').then(res => {
          this.$store.commit(
            'SET_CURRENT_PLATE',
            res.plates[parseInt(this.$route.params.plateId, 10)],
          );
          this.$emit('ruleChanged');
        });
      });
    },
    drawTableImage(currentSelection) {
      const url = makeSVG(
        window.URL || window.webkitURL || window,
        prepareResultsTable(this.allocationResults, currentSelection),
      );
      const element = document.getElementById('overlay');
      element.style.backgroundImage = `url('${url}')`;
      // document.getElementById('imgZoom').src = url;
      this.$store.commit('SET_PLATE_IMAGE_URL', url);
    },
  },
};
