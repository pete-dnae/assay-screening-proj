import draggable from 'vuedraggable';
import { mapGetters } from 'vuex';
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
      },
    },
    distPattern: {
      get() {
        return this.$store.state.rule.currentRule.pattern;
      },
      set(value) {
        this.$store.commit('SET_DIST_PATTERN', value);
      },
    },
    payloadType: {
      get() {
        return this.$store.state.rule.currentRule.payload_type;
      },
      set(value) {
        this.$store.commit('SET_PAYLOAD_TYPE', value);
        this.$store.commit('SET_PAYLOAD_OPTIONS', value);
        this.$store.commit('SET_PAYLOAD', ['']);
      },
    },
    payload: {
      get() {
        return this.$store.state.rule.currentRule.payload_csv;
      },
      set(value) {
        this.$store.commit('SET_PAYLOAD', value);
      },
    },
  },
  methods: {
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
      this.$store.commit('SET_PAYLOAD', updatedRule);
    },
  },
};
