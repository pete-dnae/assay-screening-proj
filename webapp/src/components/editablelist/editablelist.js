import Vue from 'vue';
import { modal } from 'vue-strap';

Vue.component('modal', modal);
export default {
  name: 'EditableList',
  data() {
    return {
      msg: 'This is EditableList',
      rows: [],
      showModal: false,
      modalText: '',
      listItem: {},
    };
  },
  methods: {
    handleListAdd(modalText) {
      const newId = this.rows.length == 0 ? 0 : this.rows[this.rows.length - 1] + 1;
      this.rows.push(newId);
      this.listItem[newId] = modalText;
    },
    handleListDelete(rowId) {
      this.rows = this.rows.filter(x => x != rowId);
    },
  },
};
