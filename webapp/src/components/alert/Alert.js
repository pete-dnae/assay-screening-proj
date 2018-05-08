import {
  coerce,
  delayer,
} from '../../../node_modules/vue-strap/src/utils/utils';

const DURATION = 0;
export default {
  props: {
    dismissable: { type: Boolean, default: false },
    duration: { default: DURATION },
    placement: { type: String },
    type: { type: String },
    value: { type: Boolean, default: true },
    width: { type: String },
  },
  data() {
    return {
      val: this.value,
    };
  },
  computed: {
    durationNum() {
      return coerce.number(this.duration, DURATION);
    },
  },
  watch: {
    val(val) {
      if (val && this.durationNum > 0) {
        this._delayClose();
      }
      this.$emit('input', val);
    },
    value(val) {
      if (this.val !== val) {
        this.val = val;
      }
    },
  },
  methods: {
    handleClose() {
      this.$emit('close');
    },
  },
  created() {
    this._delayClose = delayer(() => {
      this.val = false;
    }, 'durationNum');
  },
};
