import draggable from 'vuedraggable';
import { mapActions, mapGetters } from 'vuex';
import _ from 'lodash';
import {
  zoomIn,
  zoomOut,
  getNewIndex,
  prepareResultsTable,
  genCharArray,
  makeSVG,
} from '@/models/utils';
import { modal, dropdown } from 'vue-strap';

export default {
  name: 'selectedRule',
  components: {
    draggable,
    dropdown,
    modal,
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
    };
  },
  computed: {
    ...mapGetters({
      options: 'getPatternDropDown',
      types: 'getPayloadTypeDropDown',
      currentOptions: 'getCurrentPayloadOptions',
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
        this.handleUpdateRule();
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
        this.handleUpdateRule();
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
        this.handleUpdateRule();
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
        this.handleUpdateRule();
      },
    },
    distPattern: {
      get() {
        return this.$store.state.rule.currentRule.pattern;
      },
      set(value) {
        this.$store.commit('SET_DIST_PATTERN', value);
        this.handleUpdateRule();
      },
    },
    payloadType: {
      get() {
        return this.$store.state.rule.currentRule.payload_type;
      },
      set(value) {
        this.$store.commit('SET_PAYLOAD_TYPE', value);
        this.$store.commit('SET_PAYLOAD_OPTIONS', value);
        this.handleUpdateRule().then(() => {
          this.$store.commit('DELETE_PAYLOAD');
        });
      },
    },
    payload: {
      get() {
        return this.$store.state.rule.currentRule.payload_csv;
      },
      set(value) {
        this.$store.commit('SET_PAYLOAD', value);
        if (!_.isEmpty(value)) {
          this.handleUpdateRule();
        }
      },
    },
  },
  methods: {
    ...mapActions(['updateRule', 'fetchPlate']),
    zoomIn(event) {
      zoomIn(event);
    },
    zoomOut() {
      zoomOut();
    },
    validateRowRange() {},
    validateColRange() {},
    drawTableImage(currentSelection) {
      const url = makeSVG(
        window.URL || window.webkitURL || window,
        prepareResultsTable(this.allocationResults, currentSelection),
      );
      const element = document.getElementById('overlay');
      element.style.backgroundImage = `url('${url}')`;
      this.$store.commit('SET_PLATE_IMAGE_URL', url);
    },
    handleAddValue() {
      const newIndex = getNewIndex('id', this.element.value);
      this.element.value.push({
        id: newIndex,
        value: this.textElem,
      });
      this.textElem = '';
    },
    handleDeleteValue(evt) {
      const updatedRule = _.filter(this.payload, (x, i) => i !== evt.oldIndex);
      this.$store.commit('UPDATE_PAYLOAD', updatedRule);
      this.handleUpdateRule();
    },
    async handleUpdateRule() {
      try {
        await this.updateRule(this.$store.state.rule.currentRule.url);
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
        this.handleUpdateRule();
      }
    },
    handleTextBoxDel() {
      this.userText[this.textBoxNo] = undefined;
      this.textBoxNo -= 1;
    },
  },
};
