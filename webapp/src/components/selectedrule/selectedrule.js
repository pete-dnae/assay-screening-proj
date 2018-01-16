import Vue from 'vue';
import draggable from 'vuedraggable';
import _ from 'lodash';
import {
  zoomIn,
  zoomOut,
  getNewIndex,
} from '@/models/utils';
import {
  modal,
} from 'vue-strap';


Vue.component('modal', modal);
export default {
  name: 'selectedRule',
  components: {
    draggable,
  },
  props: {
    element: Object,
    allocationResults: Array,
    image: String,
  },
  data() {
    return {
      msg: 'Welcome',
      showModal: false,
      textElem: '',
      options: [{
        text: 'AAAA BBBB CCCC',
        value: 'In Blocks',
      },
      {
        text: 'ABCD ABCD ABCD',
        value: 'Consecutive',
      },
      ],
      types: [{
        text: 'Template Copies',
        value: 'Template Copies',
      },
      {
        text: 'ID Primers',
        value: 'ID Primers',
      },
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
    validateRowRange() {},
    validateColRange() {},
    handleAddValue() {
      const newIndex = getNewIndex('id', this.element.value);
      this.element.value.push({
        id: newIndex,
        value: this.textElem,
      });
      this.textElem = '';
    },
    handleDeleteValue(evt) {
      this.element.value = _.filter(this.element.value, (x, i) => i !== evt.oldIndex);
    },
  },

};
