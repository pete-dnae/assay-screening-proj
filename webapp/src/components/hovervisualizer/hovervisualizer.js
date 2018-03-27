import { isItemInArray } from '@/models/visualizer';


export default {
  name: 'HoverVisualizer',
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
    };
  },
  methods: {
    isItemInArray,
    handleShowCellContents([row, col]) {
      this.$emit('wellHovered', [row, col]);
    },
    handleHoverLeave() {
      this.$emit('hoverComplete');
    },
  },
};
