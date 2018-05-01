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
        colHeaders: ['ReagentName', 'Concentration', 'Unit'],
        columns: [
          {
            type: 'dropdown',
            source: [],
            strict: true,
          },
          {},
          {
            type: 'dropdown',
            source: [],
            strict: true,
          },
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
    ]),
    handleReagentGroupSelection() {
      this.fetchSelectedReagentGroup({
        reagentGroupName: this.currentReagentGroup,
      }).then(() => {
        this.settings.data = this.currentGroupReagents.map(reagentObj => [
          reagentObj.reagent,
          reagentObj.concentration,
          reagentObj.units,
        ]);
        this.handsonTable.updateSettings(this.settings);
      });
    },
    getData() {
      const dataArray = this.handsonTable.getData();
      const groupName = this.groupName;
      const reagentGroupObjectList = dataArray.map(row => ({
        group_name: groupName,
        reagent: row[0],
        concentration: row[1],
        units: row[2],
      }));
      this.saveReagents(reagentGroupObjectList);
    },
  },
  mounted() {
    Promise.all([this.fetchReagents(), this.fetchUnits()]).then(() => {
      this.settings.columns[0].source = _.map(this.reagents, 'name');
      this.settings.columns[2].source = _.map(this.units, 'abbrev');
      const container = document.getElementById('handsonTable');
      this.handsonTable = new Handsontable(container, this.settings);
    });
    this.fetchAvailableReagentGroups();
  },
};
