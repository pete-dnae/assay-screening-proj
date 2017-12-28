import _ from 'lodash';

export default {
  name: 'ExpandColumns',
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
      rows: [0],
      concentration: { 0: '' },
      rowRepeat: { 0: '' },
      selected: { 0: '' },
    };
  },
  methods: {
    handleRowAdd() {
      this.rows.push(this.rows.length == 0 ? 0 : this.rows[this.rows.length - 1] + 1);
    },
    handleRowDelete(rowId) {
      this.rows = this.rows.filter(x => x != rowId);
      delete this.concentration[rowId];
      delete this.rowRepeat[rowId];
      delete this.selected[rowId];
      this.handleDropDownChange();
    },
    handleDropDownChange() {
      this.rows.map((rowId) => {
        const rowNames = this.options.map(x => x.value);
        const currentStart = rowNames.indexOf(this.selected[rowId]);
        const nextStart = this.selected[rowId + 1]
          ? rowNames.indexOf(this.selected[rowId + 1])
          : rowNames.length;

        this.rowRepeat[rowId] = rowNames.slice(currentStart, nextStart);
      });
    },
  },
};
