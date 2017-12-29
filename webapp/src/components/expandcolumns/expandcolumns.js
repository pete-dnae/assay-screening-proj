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
      rows: [],
      data: {},
    };
  },
  methods: {
    handleRowAdd() {
      const newRowId = this.rows.length == 0 ? 0 : this.rows[this.rows.length - 1] + 1;
      this.rows.push(newRowId);
      this.data[newRowId] = {
        startAt: '',
        allRows: '',
        concentration: '',
      };
    },
    handleRowDelete(rowId) {
      this.rows = this.rows.filter(x => x != rowId);
      delete this.data[rowId];
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
      this.$emit('ruleChange', this.data);
    },
  },
};
