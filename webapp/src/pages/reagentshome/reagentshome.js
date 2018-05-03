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
      addReagentData: {},
    };
  },
  components: { reagentGroup, modal },
  computed: {
    ...mapGetters({
      reagents: 'getReagents',
      errors: 'getReagentErrors',
      reagentCategories: 'getReagentCategories',
    }),
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
    ...mapActions([
      'addReagent',
      'removeReagent',
      'editReagent',
      'fetchReagents',
      'fetchReagentCategories',
    ]),
    handleReagentEdit() {
      this.editReagent({
        data: this.selectedReagentData,
        reagentName: this.selectedReagent,
      }).then(() => this.fetchReagents());
    },
    handleReagentDelete(value) {
      this.selectedReagent = value.name;
      this.removeReagent(this.selectedReagent).then(() => this.fetchReagents());
    },
    handleReagentAdd() {
      this.addReagent(this.addReagentData).then(() => {
        this.fetchReagents();
        this.addReagentData = {};
      });
    },
    prepReagentEdit(value) {
      this.selectedReagentData = _.clone(
        this.reagents.find(reagent => reagent === value),
      );
      this.selectedReagent = value.name;
      this.showEditForm = true;
    },
  },
  mounted() {
    this.fetchReagentCategories();
  },
};
