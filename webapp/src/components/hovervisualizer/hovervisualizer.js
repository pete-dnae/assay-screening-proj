import { isItemInArray } from '@/models/visualizer';


export default {
  name: 'HoverVisualizer',
  props: {
    currentPlate: String,
    tableColCount: Number,
    tableRowCount: Number,
    allocationMapping: Object,
    highlightedLineNumber: Number,
    hoverHighlight: Boolean,
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
      if (event.fromElement.id === 'monitorMouseLeave') this.$emit('hoverComplete');
    },
  },
};
