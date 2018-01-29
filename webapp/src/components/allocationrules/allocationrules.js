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
      defaultRule: 'getDefaultRule',
    }),
    rules: {
      get() {
        return this.$store.state.plate.currentPlate.data.allocation_instructions
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
      this.$emit('ruleDeleted');
    },
    async handleAddRule({ copy, id }) {
      try {
        const newRule = await this.addAllocationRule({
          data: copy
            ? {
                ..._.find(this.rules, {
                  id,
                }),
                payload_csv: _.find(this.rules, {
                  id,
                }).payload_csv.toString(),
              }
            : this.defaultRule,
          url: 'http://localhost:8000/api/allocrules/',
        });

        await this.updateAllocationRules({
          data: {
            new_rules: _.map(this.rules, 'id').concat(newRule.id),
          },
          url: this.$store.state.plate.currentPlate.data.allocation_instructions
            .rule_list.url,
        });
        const experiment = await this.fetchExperiment(this.$route.params.expt);
        this.$store.commit(
          'SET_CURRENT_PLATE',
          experiment.plates[parseInt(this.$route.params.plateId, 10)],
        );
        this.$emit('ruleChanged');
      } catch (err) {
        this.$emit('error', err);
      }
    },
    async handleUpdateAllocation(data) {
      try {
        await this.updateAllocationRules({
          data: {
            new_rules: data,
          },
          url: this.$store.state.plate.currentPlate.data.allocation_instructions
            .rule_list.url,
        });
        const experiment = await this.fetchExperiment(this.$route.params.expt);
        this.$store.commit(
          'SET_CURRENT_PLATE',
          experiment.plates[parseInt(this.$route.params.plateId, 10)],
        );
        this.$emit('ruleChanged');
      } catch (err) {
        this.$emit('error', err);
      }
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
