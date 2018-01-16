import Vue from 'vue';
import draggable from 'vuedraggable';
import _ from 'lodash';
import {
  zoomIn,
  zoomOut,
  getNewIndex,
  prepareResultsTable,
  makeSVG,
  genCharArray,
} from '@/models/utils';
import {
  modal,
} from 'vue-strap';


Vue.component('modal', modal);
export default {
  name: 'selectedRule',
  components: {
    draggable,
  },
  props: {
    element: Object,
    allocationResults: Array,
    image: String,
  },
  data() {
    return {
      msg: 'Welcome',
      showModal: false,
      textElem: '',
      options: [{
        text: 'AAAA BBBB CCCC',
        value: 'In Blocks',
      },
      {
        text: 'ABCD ABCD ABCD',
        value: 'Consecutive',
      },
      ],
      types: [{
        text: 'Template Copies',
        value: 'Template Copies',
      },
      {
        text: 'ID Primers',
        value: 'ID Primers',
      },
      ],
    };
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
      document.getElementById('imgZoom').src = url;
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
      this.element.value = _.filter(this.element.value, (x, i) => i !== evt.oldIndex);
    },
  },
  mounted() {
    document.getElementById('imgZoom').src = this.image;
    this.drawTableImage({
      rows: genCharArray(this.element.start_row_letter, this.element.end_row_letter),
      cols: _.range(this.element.start_column, this.element.end_column),
    });
  },
};
