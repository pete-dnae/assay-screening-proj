export default {
  name: 'plateLayout',
  props: {
    templateData: Object,
    hgDNAData: Object,
    dilutionData: Object,
  },
  data() {
    return {
      msg: 'This is plateLayout',
      rows: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
      cols: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    };
  },
};
