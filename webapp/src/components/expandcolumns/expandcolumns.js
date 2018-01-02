import _ from 'lodash';
import { isConcentrationValid } from '@/models/rules.js';

export default {
  name: 'ExpandColumns',
  props: {
    type: String,
    columnBlocks: Number,
  },
  data() {
    return {
      msg: 'This is ExpandColumns',
      options: [
        { text: 'A', value: 'A' },
        { text: 'B', value: 'B' },
        { text: 'C', value: 'C' },
        { text: 'D', value: 'D' },
        { text: 'E', value: 'E' },
        { text: 'F', value: 'F' },
        { text: 'G', value: 'G' },
        { text: 'H', value: 'H' },
      ],
      rows: [],
      data: {},
    };
  },
  methods: {
    handleRowAdd() {
      const currentRowId = this.rows.length - 1;
      const newRowId = this.rows.length == 0 ? 0 : this.rows[currentRowId] + 1;
      if (
        newRowId != 0 &&
        !isConcentrationValid(this.columnBlocks, this.data[currentRowId].concentration)
      ) {
        $(`#popup${this.type}`).show();
        const popper = new Popper(
          document.getElementById((newRowId - 1).toString() + this.type),
          this.$refs.popup,
          {
            placement: 'top',
          },
        );
      } else {
        this.rows.push(newRowId);
        this.data[newRowId] = {
          startAt: '',
          allRows: '',
          concentration: '',
          blocks: this.columnBlocks,
        };
      }
    },
    handleRowDelete(rowId) {
      this.rows = this.rows.filter(x => x != rowId);
      delete this.data[rowId];
      $(`#popup${this.type}`).hide();
      this.changeAllocationRules();
    },
    changeAllocationRules() {
      this.rows.map((rowId) => {
        const rowNames = this.options.map(x => x.value);
        const currentStart = rowNames.indexOf(this.data[rowId].startAt);
        const nextStart = this.data[rowId + 1]
          ? rowNames.indexOf(this.data[rowId + 1].startAt)
          : rowNames.length;
        this.data = Object.assign({}, this.data, {
          [rowId]: {
            ...this.data[rowId],
            allRows: rowNames.slice(currentStart, nextStart),
          },
        });
      });
      if (!_.isEmpty(_.filter(this.data, x => x.startAt != ''))) {
        this.$emit('ruleChange', this.type, JSON.parse(JSON.stringify(_.map(this.data, x => x))));
      }
    },
  },
  mounted() {
    $(`#popup${this.type}`).hide();
    $(`#popup${this.type}`).click(() => {
      $(`#popup${this.type}`).hide();
    });
  },
};
