import { tooltip } from 'vue-strap';

export default {
  name: 'toolbar',
  props: {
    error: Object,
    showSpinner: Boolean,
  },
  components: {
    tooltip,
  },
  methods: {
    handleSwitchInfoVisiblity() {
      this.$emit('switchInfoVisiblity');
    },
    handleFormat() {
      this.$emit('formatText');
    },
    highlightError(errorPosition) {
      this.$emit('highlightError', errorPosition);
    },
  },
};
