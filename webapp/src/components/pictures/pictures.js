import { dropdown } from 'vue-strap';
import Handsontable from 'handsontable';
import _ from 'lodash';
import { debug } from 'util';

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
      coloring: false,
      uniqEntities: {},
      settings: {
        data: null,
        autoColumnSize: true,
        // stretchH: 'all',
        startRows: 8,
        startCols: 12,
        minSpareRows: 1,
        contextMenu: true,
        cells: (row, col) => {
          const cellProperties = {};
          cellProperties.renderer = 'renderCell';
          return cellProperties;
        },
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
      if (this.selected) this.generateData();
    },
    coloring() {
      this.handsonTable.render('cellRenderer');
      this.handsonTable.updateSettings(this.settings);
    },
  },
  methods: {
    updateTableData(data, colHeaders) {
      this.settings.data = data;
      this.settings.colHeaders = colHeaders;
      this.handsonTable.render('cellRenderer');
      this.handsonTable.updateSettings(this.settings);
    },
    handleClose() {
      this.$emit('exit');
    },
    getRandomColor() {
      const o = Math.round;
      const r = Math.random;
      const s = 255;
      return `rgba(${o(r() * s)},${o(r() * s)},${o(r() * s)},${0.4})`;
    },
    generateData() {
      this.settings.data = [];
      this.handsonTable.updateSettings(this.settings);
      const contentDict = this.experimentImages[this.selected];

      _.forEach(contentDict, col =>
        _.forEach(
          col,
          row =>
            (this.uniqEntities[
              _.map(row, elements => `${elements.join(' ')}`).join('\n')
            ] = this.getRandomColor()),
        ),
      );
      const data = _.reduce(
        contentDict,
        (acc, columnValues, iter) => {
          const rows = _.reduce(
            columnValues,
            (a, row, i) => {
              a[i] = _.map(row, elements => `${elements.join(' ')}`).join('\n');
              return a;
            },

            [],
          );
          acc[iter] = rows;
          return acc;
        },
        [],
      );
      _.forEach(data, (row, iter) => { if (row) row[0] = iter; return row; });
      const transposedData = _.zip(...data);
      this.updateTableData(transposedData, Object.keys(contentDict));
    },
  },
  mounted() {
    const self = this;
    function cellRenderer(instance, td, row, col, prop, value, cellProperties) {
      if (
        self.settings.data &&
        self.settings.data[row] &&
        self.settings.data[row][col]
      ) {
        td.innerText = self.settings.data[row][col];
        if (self.coloring) {
          td.style.background = self.uniqEntities[self.settings.data[row][col]];
        }
      }
    }
    Handsontable.renderers.registerRenderer('renderCell', cellRenderer);
    const container = document.getElementById('csvTable');
    this.handsonTable = new Handsontable(container, this.settings);
  },
};
