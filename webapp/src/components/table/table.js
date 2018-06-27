import _ from 'lodash';

export default {
  name: 'TableComponene',
  props: {
    options: Object,
    data: Array,
    selectedRowProps: {
      default: () => [],
      type: Array,
    },
    columnsToColor: {
      default: () => [],
      type: Array,
    },
    searchByColumns: {
      default: () => false,
      type: Boolean,
    },
  },
  data() {
    return {
      msg: 'Welcome',
      lastSelectedRow: null,
      highlightRows: [],
      search: {},
      lastSortedKey: null,
      lastSortedOrder: null,
      filteredRows: [],
    };
  },
  watch: {
    data() {
      this.filteredRows = this.data;
    },
    search: {
      handler(newVal) {
        for (const propName in newVal) {
          if (
            newVal[propName] === null ||
            newVal[propName] === undefined ||
            newVal[propName] === ''
          ) {
            delete newVal[propName];
          }
        }

        this.filteredRows = _.filter(this.data, (row) => {
          const keyWiseSearchPass = _.map(newVal, (val, key) => {
            if (typeof row[key] === 'object') {
              return row[key].toString().indexOf(val) > -1;
            }
            return row[key].indexOf(val) > -1;
          });
          return keyWiseSearchPass.every(value => value);
        });
      },
      deep: true,
    },
  },
  methods: {
    handleSortBy(key) {
      if (key !== this.lastSortedKey) {
        this.filteredRows = _.orderBy(this.filteredRows, key, 'asc');
        this.lastSortedOrder = 'asc';
      } else if (this.lastSortedOrder === 'asc') {
        this.filteredRows = _.orderBy(this.filteredRows, key, 'desc');
        this.lastSortedOrder = 'desc';
      } else {
        this.filteredRows = _.orderBy(this.filteredRows, key, 'asc');
        this.lastSortedOrder = 'asc';
      }
      this.lastSortedKey = key;
    },
    pickProps(obj) {
      return Object.assign(
        {},
        ...this.selectedRowProps.map(prop => ({
          [prop]: obj[prop],
        })),
      );
    },
    determineClass(data, options) {
      const bootstrapClass = {};
      if (options.colorOn) {
        if (data[options.colorOn]) {
          bootstrapClass['table-danger'] = true;
        }
      }
      if (options.title.indexOf('Comment') > -1) {
        bootstrapClass['overflow-wrap'] = true;
      }
      return bootstrapClass;
    },
    handleTableRowClick(id) {
      if (!_.isEmpty(this.selectedRowProps)) {
        const props = this.filteredRows[id];
        this.$emit('tableRowSelected', props);
        this.handleRowClick(props);
      }
    },
    handleRoundOff(value) {
      if (typeof value === 'number') return value.toFixed(2);
      return value;
    },
    handleRowClick(props) {
      if (window.event.ctrlKey) {
        this.toggleRow(props);
      }

      if (window.event.button === 0) {
        if (!window.event.ctrlKey && !window.event.shiftKey) {
          this.highlightRows = [];
          this.toggleRow(props);
        }

        if (window.event.shiftKey) {
          const [start, end] = [
            _.findIndex(this.filteredRows, this.lastSelectedRow),
            _.findIndex(this.filteredRows, props),
          ].sort((a, b) => a - b);
          this.highlightRows = _.uniq(
            this.highlightRows.concat(
              _.range(start, end + 1).map(idx => this.filteredRows[idx]),
            ),
          );
        }
      }
      this.$emit('multipleSelection', this.highlightRows);
    },
    checkRowSelected(id) {
      const elem = this.filteredRows[id];
      const value = _.find(this.highlightRows, { ...elem });
      return typeof value !== 'undefined';
    },
    toggleRow(props) {
      this.lastSelectedRow = props;
      if (_.find(this.highlightRows, { ...props })) {
        this.highlightRows.splice(_.findIndex(this.filteredRows, props), 1);
      } else {
        this.highlightRows.push(props);
      }
    },
  },
  mounted() {
    document.getElementById('table').onselectstart = () => false;
    this.filteredRows = this.data;
  },
};
