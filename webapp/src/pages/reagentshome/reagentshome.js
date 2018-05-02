import { mapGetters, mapActions } from 'vuex';
import Handsontable from 'handsontable';
import { modal } from 'vue-strap';
import _ from 'lodash';

export default {
  name: 'reagentshome',
  data() {
    return {
      currentReagentGroup: null,
      show: false,
      groupName: null,
      settings: {
        data: null,
        stretchH: 'all',
        colHeaders: ['ReagentName', 'Concentration', 'Unit'],
        columns: [
          { type: 'dropdown', source: [], strict: true },
          {},
          { type: 'dropdown', source: [], strict: true },
        ],
        startRows: 10,
        startCols: 3,
      },
    };
  },
  components: {
    modal,
  },
  computed: {
    ...mapGetters({
      reagents: 'getReagents',
      units: 'getUnits',
      reagentGroupList: 'getReagentGroupList',
      currentGroupReagents: 'getCurrentGroupReagents',
    }),
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
    handleReagentGroupSelection() {
      this.loadSelectedReagentGroup(this.currentReagentGroup);
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
      this.deleteReagentGroup(this.currentReagentGroup).then(() => {
        this.fetchAvailableReagentGroups();
        this.updateTableData(null);
      });
    },
    saveData() {
      const dataArray = this.handsonTable.getData();
      const groupName = this.groupName;
      const reagentGroupObjectList = dataArray
        .filter(row => !row.includes(''))
        .map(row => ({
          group_name: groupName,
          reagent: row[0],
          concentration: row[1],
          units: row[2],
        }));
      this.saveReagents(reagentGroupObjectList).then(() => {
        this.fetchAvailableReagentGroups();
        this.currentReagentGroup = groupName;
        this.loadSelectedReagentGroup(this.currentReagentGroup);
      });
    },
  },
  mounted() {
    this.loadSettings().then(() => {
      const container = document.getElementById('handsonTable');
      this.handsonTable = new Handsontable(container, this.settings);
    });
    this.fetchAvailableReagentGroups();
  },
};
