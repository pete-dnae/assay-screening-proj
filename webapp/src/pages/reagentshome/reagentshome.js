import { mapGetters, mapActions } from 'vuex';
import { modal } from 'vue-strap';
import reagentGroup from '@/components/reagentgroup/reagentgroup.vue';
import _ from 'lodash';
import alert from '@/components/alert/Alert.vue';
import reagentCreateForm from '@/components/addreagent/addreagent.vue';
import reagentEditForm from '@/components/editreagent/editreagent.vue';
import store from '@/store';

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
      showAddForm: false,
      tableHeaders: {
        name: 'Name',
        category: 'Category',
        opaque_json_payload: 'Metadata',
      },
    };
  },
  beforeRouteEnter(to, from, next) {
    store.dispatch('inspectToken').then(() => { next(); });
  },
  components: {
    reagentGroup,
    modal,
    alert,
    reagentCreateForm,
    reagentEditForm,
  },
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
      'inspectToken',
    ]),
    handleReagentEdit(data) {
      this.showEditForm = false;
      this.editReagent({
        data,
        reagentName: this.selectedReagent,
      }).then(() => this.fetchReagents());
    },
    handleReagentDelete(value) {
      this.selectedReagent = value.name;
      this.removeReagent(this.selectedReagent).then(() => this.fetchReagents());
    },
    handleReagentAdd(reagentData) {
      this.showAddForm = false;
      if (
        _.isEmpty(reagentData.name) ||
        _.isEmpty(reagentData.category) ||
        reagentData.categpry === 'null'
      ) {
        this.$store.commit('ADD_ERROR_MESSAGE', [
          'Please fill in Reagent Name as well as category',
        ]);
      } else {
        this.addReagent(reagentData).then(() => {
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
    stringToList(string) {
      const obj = JSON.parse(string);
      let list = _.map(obj, (value, key) => ({ key, value }));
      if (_.isEmpty(list)) {
        list = [{ key: 'None', value: '' }];
      }

      return list;
    },
  },
  mounted() {
    this.fetchReagentCategories();
  },
};
