import { dropdown } from 'vue-strap';
import SVGtoPNGDataURL from '@/models/SVGtoPNG';
import { makeSVG } from '@/models/visualizer';
import Handsontable from 'handsontable';
import _ from 'lodash';

export default {
  name: 'pictures',
  components: {
    dropdown,
    Handsontable,
  },
  data() {
    return {
      image: null,
      selected: null,
      settings: {
        data: null,
        stretchH: 'all',
        startRows: 8,
        startCols: 12,
        minSpareRows: 1,
        contextMenu: true,
      },
    };
  },
  props: {
    experimentImages: Object,
  },
  watch: {
    selected() {
      this.generateImage();
    },
    experimentImages() {
      this.generateImage();
    },
  },
  methods: {
    generateImage() {
      const contentDict = this.experimentImages[this.selected];
      const colLength = Object.keys(contentDict).length;
      _.reduce(contentDict, (acc, x) => {

      });
      debugger;
    },
  },
  mounted() {
    const container = document.getElementById('csvTable');
    this.handsonTable = new Handsontable(container, this.settings);
  },
};
