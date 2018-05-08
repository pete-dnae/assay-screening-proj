import { mapGetters, mapActions } from 'vuex';
import { modal } from 'vue-strap';
import reagentGroup from '@/components/reagentgroup/reagentgroup.vue';
import _ from 'lodash';
import alert from '@/components/alert/Alert.vue';

export default {
  name: 'reagentshome',
  data() {
    return {
      searchField: null,
      searchText: null,
      showEditForm: false,
      showErrors: false,
      selectedReagentData: {},
      selectedReagent: null,
      addReagentData: { category: null },
    };
  },
  components: { reagentGroup, modal, alert },
  computed: {
    ...mapGetters({
      reagents: 'getReagents',
      errors: 'getReagentErrors',
      reagentCategories: 'getReagentCategories',
    }),
    filteredReagents() {
      if (this.searchField && !_.isEmpty(this.searchText)) {
        const filter = this.reagents.filter(reagent =>
          reagent[this.searchField].includes(this.searchText),
        );
        return filter;
      }

      return this.reagents;
    },
    reagentAddEmpty() {
      const keys = Object.keys(this.addReagentData);
      for (let i = 0; i < keys.length; i += 1) {
        const property = keys[i];

        if (
          !this.addReagentData[property] ||
          this.addReagentData[property] === 'null'
        ) {
          return true;
        }
      }
      return false;
    },
  },
  watch: {
    errors() {
      if (this.errors) this.showErrors = true;
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
      if (this.reagentAddEmpty) {
        this.$store.commit('ADD_ERROR_MESSAGE', [
          'Please fill in Reagent Name as well as category',
        ]);
      } else {
        this.addReagent(this.addReagentData).then(() => {
          this.fetchReagents();
          this.addReagentData = {};
        });
      }
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
