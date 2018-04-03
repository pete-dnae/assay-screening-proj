import { isItemInArray } from '@/models/visualizer';
import { tooltip } from 'vue-strap';

export default {
  name: 'HoverVisualizer',
  components: {
    tooltip,
  },
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
