import { isItemInArray } from '@/models/visualizer';
import wellcontents from '@/components/wellcontents/wellcontents.vue';

export default {
  name: 'HoverVisualizer',
  components: {
    wellcontents,
  },
  props: {
    currentPlate: String,
    tableBoundaries: Array,
    allocationMapping: Object,
    highlightedLineNumber: Number,
    allocationData: Object,
  },
  data() {
    return {
      msg: 'Welcome',
      currentRow: null,
      currentCol: null,
    };
  },
  methods: {
    isItemInArray,
    handleShowCellContents([row, col]) {
      [this.currentRow, this.currentCol] = [row, col];
    },
  },
};
