import { mapGetters, mapActions } from 'vuex';
import Handsontable from 'handsontable';
import { modal } from 'vue-strap';
import _ from 'lodash';
import typeahead from '@/components/typeahead/Typeahead.vue';
import alert from '@/components/alert/Alert.vue';

export default {
  name: 'reagentgroup',
  data() {
    return {
      currentReagentGroup: null,
      show: false,
      groupName: null,
      currentText: null,
      showErrors: false,
      settings: {
        data: null,
        stretchH: 'all',
        colHeaders: ['ReagentName', 'Concentration', 'Unit'],
        columns: [
          { validator: 'reagent', type: 'dropdown', source: [], strict: true },
          { validator: 'numeric', allowInvalid: true },
          { type: 'dropdown', source: [], strict: true },
        ],
        startRows: 10,
        startCols: 3,
        minSpareRows: 1,
        contextMenu: true,
      },
    };
  },
  components: {
    modal,
    alert,
    typeahead,
  },
  computed: {
    ...mapGetters({
      reagents: 'getReagents',
      units: 'getUnits',
      reagentGroupList: 'getReagentGroupList',
      currentGroupReagents: 'getCurrentGroupReagents',
      errors: 'getReagentGroupsErrors',
    }),
  },
  watch: {
    reagents() {
      if (this.handsonTable) {
        this.settings.columns[0].source = _.map(this.reagents, 'name');
        this.handsonTable.updateSettings(this.settings);
      }
    },
    errors() {
      if (this.errors) this.showErrors = true;
    },
  },
  methods: {
    ...mapActions([
      'fetchReagents',
      'fetchUnits',
      'fetchAvailableReagentGroups',
      'fetchSelectedReagentGroup',
      'saveReagents',
      'deleteReagentGroup',
    ]),
    handleReagentGroupSelection(value) {
      this.loadSelectedReagentGroup(value);
      this.currentText = value;
    },
    handleCreateNew() {
      this.updateTableData(null);
      this.currentReagentGroup = null;
    },
    loadSelectedReagentGroup(reagentGroupName) {
      this.fetchSelectedReagentGroup({
        reagentGroupName,
      }).then(() => {
        const data = this.currentGroupReagents.map(reagentObj => [
          reagentObj.reagent,
          reagentObj.concentration,
          reagentObj.units,
        ]);
        this.updateTableData(data);
      });
    },
    updateTableData(data) {
      this.settings.data = data;
      this.handsonTable.updateSettings(this.settings);
    },
    loadSettings() {
      return Promise.all([this.fetchReagents(), this.fetchUnits()]).then(() => {
        this.settings.columns[0].source = _.map(this.reagents, 'name');
        this.settings.columns[2].source = _.map(this.units, 'abbrev');
      });
    },
    handleReagentGroupDelete() {
      this.deleteReagentGroup(this.currentText).then(() => {
        this.fetchAvailableReagentGroups();
        this.updateTableData(null);
      });
    },
    validateReagents(reagentName) {
      const usedReagents = this.handsonTable.getData().map(row => row[0]);
      if (
        !_.find(this.reagents, {
          name: reagentName,
        })
      ) {
        this.$store.commit(
          'ADD_ERROR_MESSAGE_REAGENT_GROUP',
          'Reagent Name not recogonized',
        );
        return false;
      }
      if (usedReagents.includes(reagentName)) {
        this.$store.commit(
          'ADD_ERROR_MESSAGE_REAGENT_GROUP',
          'Reagent Name already in use',
        );
        return false;
      }
      return true;
    },
    saveData() {
      const dataArray = this.handsonTable.getData();
      const groupName = this.groupName;
      const reagentGroupObjectList = dataArray
        .filter(row => !row.includes('') && !row.includes(null))
        .map(row => ({
          group_name: groupName,
          reagent: row[0],
          concentration: row[1],
          units: row[2],
        }));

      this.saveReagents(reagentGroupObjectList).then(() => {
        this.fetchAvailableReagentGroups();
        this.currentReagentGroup = groupName;
        this.currentText = groupName;
        this.loadSelectedReagentGroup(this.currentReagentGroup);
      });
    },
  },
  mounted() {
    Handsontable.validators.registerValidator('reagent', (query, callback) =>
      callback(this.validateReagents(query)),
    );
    this.loadSettings().then(() => {
      const container = document.getElementById('handsonTable');
      this.handsonTable = new Handsontable(container, this.settings);
      Handsontable.hooks.add('afterValidate', (success, value, row, prop, source) => {
        if (success) this.$store.commit('CLEAR_ERROR_MESSAGE_REAGENT_GROUP');
        if (prop === 1 && !success) {
          this.$store.commit('ADD_ERROR_MESSAGE_REAGENT_GROUP', 'Concentration should be numeric');
        }
        if (prop === 2 && !success) {
          this.$store.commit('ADD_ERROR_MESSAGE_REAGENT_GROUP', 'Unit Not Recogonized');
        }
      }, this.handsonTable);
    });
    this.fetchAvailableReagentGroups();
  },
};
