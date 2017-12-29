import Vue from 'vue';
import expandColumns from '@/components/expandcolumns/expandcolumns.vue';
import editableList from '@/components/editablelist/editablelist.vue';

Vue.component('expandColumns', expandColumns);
Vue.component('editableList', editableList);
export default {
  name: 'rulesDropDown',
  data() {
    return {
      msg: 'loaded rules drop down',
      currentDisplayStyle: {
        display: 'relative',
        'background-color': 'rgba(0,0,0,0.7)',
        cursor: 'pointer',
      },
      currentDisplayClass: ['dropdown-menu', 'dropdown-menu-lg', 'w-100'],
    };
  },
  methods: {
    handleRuleClose() {
      this.currentDisplayClass.pop();
    },
    handleRuleChange(obj) {
      this.$store.commit('SET_TEMPLATE_RULES', obj);
    },
  },
};
