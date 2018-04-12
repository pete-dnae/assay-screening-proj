export default {
  name: 'suggestionList',
  props: {
    suggestions: Array,
    toolTipPosition: Object,
  },
  methods: {
    handleAutoCompleteClick(text) {
      this.$emit('autoComplete', text);
    },
    hideSuggestion() {
      this.$emit('hideSuggestion');
    },
  },
};
