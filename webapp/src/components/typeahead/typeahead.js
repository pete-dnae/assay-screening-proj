import _ from 'lodash';

export default {
  name: 'TypeaheadComponent',
  data() {
    return {
      msg: 'Welcome',
      result: [],
      val: null,
      showDropdown: false,
    };
  },
  props: {
    options: Array,
    prop: String,
  },
  watch: {
    val() {
      if (!_.isEmpty(this.val)) {
        this.showDropdown = true;
        this.result = this.options.filter(
          x => x[this.prop].indexOf(this.val) > -1,
        );
      } else {
        this.result = null;
      }
    },
  },
  methods: {
    handleSelection(dat) {
      this.val = dat;
    },
    handleBack() {
      this.$emit('typeaheadBack');
    },
  },
};
