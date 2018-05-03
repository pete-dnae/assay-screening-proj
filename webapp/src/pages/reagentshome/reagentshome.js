import { mapGetters, mapActions } from 'vuex';
import { modal } from 'vue-strap';
import reagentGroup from '@/components/reagentgroup/reagentgroup.vue';
import _ from 'lodash';

export default {
  name: 'reagentshome',
  data() {
    return {
      searchField: null,
      searchText: null,
      showEditForm: false,
      selectedReagentData: {},
      selectedReagent: null,
    };
  },
  components: { reagentGroup, modal },
  computed: {
    ...mapGetters({ reagents: 'getReagents' }),
    filteredReagents() {
      if (this.searchField && !_.isEmpty(this.searchText)) {
        return this.reagents.filter(reagent =>
          reagent[this.searchField].includes(this.searchText),
        );
      }
      return this.reagents;
    },
  },
  methods: {
    ...mapActions([]),
    handleReagentEdit(value) {
      this.selectedReagentData = this.reagents.find(reagent => reagent === value);
      this.selectedReagent = value.name;
      this.showEditForm = true;
    },
    handleReagentDelete(value) {
      this.selectedReagent = value.name;
    },
    handleReagentAdd() {

    },
  },
  mounted() {},
};
