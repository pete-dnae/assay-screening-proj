import { dropdown } from 'vue-strap';
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
        autoColumnSize: false,
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
      this.generateData();
    },
    experimentImages() {
      this.generateData();
    },
  },
  methods: {
    updateTableData(data, colHeaders) {
      this.settings.data = data;
      this.settings.colHeaders = colHeaders;
      this.handsonTable.updateSettings(this.settings);
    },
    handleClose() {
      this.$emit('exit');
    },
    generateData() {
      const contentDict = this.experimentImages[this.selected];
      const data = _.reduce(
        contentDict,
        (acc, columnValues) => {
          const rows = _.map(columnValues, row => row.join(' '));
          acc.push(rows);
          return acc;
        },
        [],
      );
      const transposedData = _.zip(...data);
      this.updateTableData(transposedData, Object.keys(contentDict));
    },
  },
  mounted() {
    const container = document.getElementById('csvTable');
    this.handsonTable = new Handsontable(container, this.settings);
  },
};
