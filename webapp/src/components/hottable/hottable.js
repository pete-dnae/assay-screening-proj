import HotTable from '@handsontable/vue';

export default {
  name: 'reagentshome',
  data() {
    return {
      root: 'test-hot',
      data: null,
    };
  },
  props: {
    hotSettings: Object,
  },
  components: {
    HotTable,
  },
  methods: {
    getData(event) {
      console.log(event);
      debugger;
    },
  },
};
