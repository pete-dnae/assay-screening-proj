import draggable from 'vuedraggable';
import { mapActions, mapGetters } from 'vuex';
import _ from 'lodash';
import {
  zoomIn,
  zoomOut,
  prepareResultsTable,
  genCharArray,
  makeSVG,
} from '@/models/utils';

export default {
  name: 'selectedRule',
  components: {
    draggable,
  },
  props: {
    allocationResults: Array,
    image: String,
  },
  data() {
    return {
      msg: 'Welcome',
      showModal: false,
      textElem: '',
      show: true,
      userText: {},
      textBoxNo: 3,
      selectMode: false,
    };
  },
  computed: {
    ...mapGetters({
      options: 'getPatternDropDown',
      types: 'getPayloadTypeDropDown',
      currentOptions: 'getCurrentPayloadOptions',
      rowOptions: 'getRowsDropDown',
      colOptions: 'getColsDropDown',
    }),
    rowStart: {
      get() {
        return this.$store.state.rule.currentRule.start_row_letter;
      },
      set(value) {
        this.$store.commit('SET_ROW_START', value);
        this.drawTableImage({
          rows: genCharArray(value, this.rowEnd),
          cols: _.range(this.colStart - 1, this.colEnd),
        });
        this.handleUpdateRule({
          start_row_letter: this.$store.state.rule.currentRule.start_row_letter,
        });
      },
    },
    rowEnd: {
      get() {
        return this.$store.state.rule.currentRule.end_row_letter;
      },
      set(value) {
        this.$store.commit('SET_ROW_END', value);
        this.drawTableImage({
          rows: genCharArray(this.rowStart, value),
          cols: _.range(this.colStart - 1, this.colEnd),
        });
        this.handleUpdateRule({
          end_row_letter: this.$store.state.rule.currentRule.end_row_letter,
        });
      },
    },
    colStart: {
      get() {
        return this.$store.state.rule.currentRule.start_column;
      },
      set(value) {
        this.$store.commit('SET_COL_START', value);
        this.drawTableImage({
          rows: genCharArray(this.rowStart, this.rowEnd),
          cols: _.range(value - 1, this.colEnd),
        });
        this.handleUpdateRule({
          start_column: this.$store.state.rule.currentRule.start_column,
        });
      },
    },
    colEnd: {
      get() {
        return this.$store.state.rule.currentRule.end_column;
      },
      set(value) {
        this.$store.commit('SET_COL_END', value);
        this.drawTableImage({
          rows: genCharArray(this.rowStart, this.rowEnd),
          cols: _.range(this.colStart - 1, value),
        });
        this.handleUpdateRule({
          end_column: this.$store.state.rule.currentRule.end_column,
        });
      },
    },
    distPattern: {
      get() {
        return this.$store.state.rule.currentRule.pattern;
      },
      set(value) {
        this.$store.commit('SET_DIST_PATTERN', value);
        this.handleUpdateRule({
          pattern: this.$store.state.rule.currentRule.pattern,
        });
      },
    },
    payloadType: {
      get() {
        return this.$store.state.rule.currentRule.payload_type;
      },
      set(value) {
        this.$store.commit('SET_PAYLOAD_TYPE', value);
        this.$store.commit('SET_PAYLOAD_OPTIONS', value);
        // this.$store.commit('DELETE_PAYLOAD');
        this.handleUpdateRule({
          payload_type: this.$store.state.rule.currentRule.payload_type,
        }).then(() => {
          this.$store.commit('DELETE_PAYLOAD');
        });
      },
    },
    payload: {
      get() {
        return this.$store.state.rule.currentRule.payload_csv;
      },
      set(value) {
        if (this.selectMode) {
          this.$store.commit('SET_PAYLOAD', value);

          this.handleUpdateRule({
            payload_csv: this.$store.state.rule.currentRule.payload_csv.toString(),
          });
        } else {
          this.$store.commit('REORDER_PAYLOAD', value);

          this.handleUpdateRule({
            payload_csv: this.$store.state.rule.currentRule.payload_csv.toString(),
          });
        }
      },
    },
  },
  methods: {
    ...mapActions([
      'updateRule',
      'fetchPlate',
      'addAllocationRule',
      'fetchExperiment',
    ]),
    zoomIn,
    zoomOut,
    drawTableImage(currentSelection) {
      const url = makeSVG(
        window.URL || window.webkitURL || window,
        prepareResultsTable(this.allocationResults, currentSelection),
      );
      const element = document.getElementById('overlay');
      element.style.backgroundImage = `url('${url}')`;
      this.$store.commit('SET_PLATE_IMAGE_URL', url);
    },
    handleDeleteValue(index) {
      const updatedRule = _.filter(this.payload, (x, i) => i !== index);
      this.$store.commit('UPDATE_PAYLOAD', updatedRule);

      this.handleUpdateRule({
        payload_csv: this.$store.state.rule.currentRule.payload_csv.toString(),
      });
    },
    async handleUpdateRule(data) {
      try {
        await this.updateRule({
          data,
          url: this.$store.state.rule.currentRule.url,
        });
        const plateData = await this.fetchPlate(
          parseInt(this.$route.params.plateId + 1, 10),
        );
        this.$store.commit('SET_CURRENT_PLATE', plateData);
        this.drawTableImage({
          rows: genCharArray(this.rowStart, this.rowEnd),
          cols: _.range(this.colStart - 1, this.colEnd),
        });
        this.$emit('plateRefresh');
      } catch (err) {
        this.$emit('error', JSON.stringify(err));
      }
    },
    handleUserInput(data) {
      this.$store.commit('SET_PAYLOAD', _.map(data, x => parseInt(x, 10)));
      if (!_.isEmpty(data)) {
        this.handleUpdateRule({
          payload_csv: this.$store.state.rule.currentRule.payload_csv.toString(),
        });
      }
    },
    handleTextBoxDel() {
      this.userText[this.textBoxNo] = undefined;
      this.textBoxNo -= 1;
    },
  },
};
