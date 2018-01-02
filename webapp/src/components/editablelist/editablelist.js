import Vue from 'vue';
import { modal } from 'vue-strap';

Vue.component('modal', modal);
export default {
  name: 'EditableList',
  props: {
    type: String,
    columnBlocks: Number,
  },
  data() {
    return {
      msg: 'This is EditableList',
      rows: [],
      showModal: false,
      modalText: '',
      listItem: {},
      repeatOption: '',
      blockNo: '',
    };
  },
  methods: {
    handleListAdd(modalText) {
      if (modalText != '') {
        debugger;
        const newId = this.rows.length == 0 ? 0 : this.rows[this.rows.length - 1] + 1;
        this.rows.push(newId);
        this.listItem[newId] = modalText;
        const mutation = this.type == 'Strain' ? 'SET_STRAINS' : 'SET_ID_PRIMERS';
        this.$store.commit(mutation, {
          blocks: this.columnBlocks,
          byBlock: this.repeatOption == 'block',
          blockNo: this.blockNo,
          data: this.listItem,
        });
        this.$store.commit(`${mutation}_PLATE`, {
          blocks: this.columnBlocks,
          byBlock: this.repeatOption == 'block',
          blockNo: this.blockNo,
          data: this.listItem,
        });
      } else {
        alert('Please enter a valid name');
      }
    },
    handleListDelete(rowId) {
      this.rows = this.rows.filter(x => x != rowId);

      this.listItem = _.filter(this.listItem, (x, i) => this.rows.indexOf(parseInt(i)) != -1);
      const mutation = this.type == 'Strain' ? 'SET_STRAINS' : 'SET_ID_PRIMERS';
      this.$store.commit(mutation, {
        blocks: this.columnBlocks,
        byBlock: this.repeatOption == 'block',
        blockNo: this.blockNo,
        data: this.listItem,
      });

      this.$store.commit(`${mutation}_PLATE`, {
        blocks: this.columnBlocks,
        byBlock: this.repeatOption == 'block',
        blockNo: this.blockNo,
        data: this.listItem,
      });
    },
  },
};
