import Handsontable from 'handsontable';

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
    Handsontable,
  },
  methods: {
    getData() {
      this.data = this.handsonTable.getData();
    },
  },
  mounted() {
    const container = document.getElementById('handsonTable');
    this.handsonTable = new Handsontable(container, this.hotSettings);
  },
};
