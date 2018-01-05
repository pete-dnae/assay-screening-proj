import Vue from 'vue';
import draggable from 'vuedraggable';
import { zoomIn, zoomOut } from '@/models/utils';

export default {
  name: 'selectedRule',
  components: {
    draggable,
  },
  props: {
    element: Object,
  },
  data() {
    return {
      msg: 'Welcome',
      options: [
        { text: 'AAAA BBBB CCCC', value: 'In Blocks' },
        { text: 'ABCD ABCD ABCD', value: 'Consecutively' },
      ],
    };
  },
  methods: {
    zoomIn(event) {
      zoomIn(event);
    },
    zoomOut() {
      zoomOut();
    },
  },
};
