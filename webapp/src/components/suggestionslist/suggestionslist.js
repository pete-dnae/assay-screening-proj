export default {
  name: 'suggestionList',
  props: {
    suggestions: Array,
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
