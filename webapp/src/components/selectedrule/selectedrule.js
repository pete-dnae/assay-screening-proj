import Vue from 'vue';
import draggable from 'vuedraggable';
import { zoomIn, zoomOut } from '@/models/utils';
import { modal } from 'vue-strap';
import { getNewIndex } from '@/models/utils';

Vue.component('modal', modal);
export default {
  name: 'selectedRule',
  components: {
    draggable,
  },
  props: {
    element: Object,
    allocationResults: Array,
  },
  data() {
    return {
      msg: 'Welcome',
      showModal: false,
      textElem: '',
      options: [
        { text: 'AAAA BBBB CCCC', value: 'In Blocks' },
        { text: 'ABCD ABCD ABCD', value: 'Consecutively' },
      ],
      types: [
        { text: 'Template Copies', value: 'Template Copies' },
        { text: 'ID Primers', value: 'ID Primers' },
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
    drawCanvas() {
      const tableHead = '<table class="table">';
      let tableBody = '';
      this.allocationResults.forEach((row) => {
        tableBody += '<tr>';
        row.forEach((col) => {
          tableBody += '<td style="width:200px;border: 1px solid black">';
          tableBody += `<span class="row" style="color:red">${col['ID Primers']}</span>`;
          tableBody += `<span class="row" style="color:blue">${col['PA Primers']}</span>`;
          tableBody += `<span class="row" style="color:red">${col['Strain Count']}cp</span>`;
          tableBody += `<span class="row" style="color:red">${'Dil'}${
            col['Dilution Factor']
          }</span>`;
          tableBody += '</td>';
        });
        tableBody += '</tr>';
      });
      const tableText = `${tableHead + tableBody}</table>`;
      const data =
        `${'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000">' +
          '<foreignObject width="1000" height="1000">' +
          '<div xmlns="http://www.w3.org/1999/xhtml" style="font-size:10px">'}${tableText}</div>` +
        '</foreignObject>' +
        '</svg>';

      const DOMURL = window.URL || window.webkitURL || window;
      const svg = new Blob([data], { type: 'image/svg+xml' });
      const url = DOMURL.createObjectURL(svg);
      const element = document.getElementById('overlay');

      document.getElementById('imgZoom').src = url;
      element.style.backgroundImage = `url('${url}')`;
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
      this.element.value = _.filter(this.element.value, (x, i) => i != evt.oldIndex);
    },
  },
  mounted() {
    this.drawCanvas();
  },
};
