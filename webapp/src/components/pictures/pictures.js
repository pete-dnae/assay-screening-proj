import { dropdown } from 'vue-strap';
import Handsontable from 'handsontable';
import _ from 'lodash';
import { debug } from 'util';
import { Colors } from '@/models/colors';

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
      uniqFont: {},
      uniqBackground: {},
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
    hexToRgbNew(hex) {
      const arrBuff = new ArrayBuffer(4);
      const vw = new DataView(arrBuff);
      vw.setUint32(0, parseInt(hex, 16), false);
      const arrByte = new Uint8Array(arrBuff);

      return `rgba(${arrByte[1]},${arrByte[2]},${arrByte[3]},0.2)`;
    },
    generateData() {
      this.settings.data = [];
      this.handsonTable.updateSettings(this.settings);
      const contentDict = this.experimentImages[this.selected];
      _.forEach(contentDict, col =>
        _.forEach(col, row =>
          _.forEach(row, (elements) => {
            if (elements[3] === 'assay') {
              this.uniqFont[elements[0]] = Colors.random();
            }
            if (elements[3] === 'template') {
              this.uniqBackground[elements[0]] = Colors.random(true);
            }
          }),
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
      _.forEach(data, (row, iter) => {
        if (row) row[0] = iter;
        return row;
      });
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
          const rawColText = self.settings.data[row][col];

          if (
            typeof rawColText === 'string' &&
            (rawColText.indexOf('assay') > -1 ||
              rawColText.indexOf('template') > -1)
          ) {
            const elements = rawColText
              .split('\n')
              .map(entity => entity.split(' '));
            _.forEach(elements, (entity) => {
              if (entity[3] === 'assay') {
                td.style.color = self.uniqFont[entity[0]];
              }
              if (entity[3] === 'template') {
                td.style.background = `${self.uniqBackground[entity[0]]}`;
              }
            });
          }
        }
      }
    }
    Handsontable.renderers.registerRenderer('renderCell', cellRenderer);
    const container = document.getElementById('csvTable');
    this.handsonTable = new Handsontable(container, this.settings);
  },
};
