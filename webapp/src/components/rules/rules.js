import Vue from 'vue';
import expandColumns from '@/components/expandcolumns/expandcolumns.vue';
import editableList from '@/components/editablelist/editablelist.vue';
import { aside, dropdown } from 'vue-strap';
import { mapActions, mapGetters } from 'vuex';

Vue.component('expandColumns', expandColumns);
Vue.component('editableList', editableList);
Vue.component('sidebar', aside);
Vue.component('vue-drop', dropdown);

export default {
  name: 'rulesDropDown',
  data() {
    return {
      msg: 'loaded rules drop down',
      currentDisplayStyle: {
        display: 'relative',
        // 'background-color': 'rgba(0,0,0,0.7)',
        cursor: 'pointer',
      },
      currentDisplayClass: ['dropdown-menu', 'dropdown-menu-lg', 'w-100'],
      columnBlocks: 4,
      showDropDown: false,
      showRight: true,
      surpressColumns: '',
    };
  },
  computed: {
    ...mapGetters({
      strains: 'getStrainsRules',
      templates: 'getTemplateRules',
      idPrimers: 'getIdPrimersRules',
      hgDNA: 'gethgDNARules',
    }),
  },
  methods: {
    handleRuleClose() {
      this.currentDisplayClass.pop();
    },
    handleRuleChange(type, obj) {
      const mutation = type == 'template' ? 'SET_TEMPLATE' : 'SET_HGDNA';

      this.$store.commit(`${mutation}_RULES`, obj);
      this.$store.commit(`${mutation}_PLATE`, obj);
    },
  },
  mounted() {
    console.log(this.strains);
  },
};
