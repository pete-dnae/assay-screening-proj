import Vue from 'vue';
import expandColumns from '@/components/expandcolumns/expandcolumns.vue';

Vue.component('expandColumns', expandColumns);
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
  },
};
