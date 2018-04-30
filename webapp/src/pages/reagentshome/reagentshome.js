
import { mapGetters, mapActions } from 'vuex';
import Handsontable from 'handsontable';

export default {
  name: 'reagentshome',
  data() {
    return {
      currentReagentGroup: null,
    };
  },
  computed: {
    ...mapGetters({
      hotSettings: 'getTableSettings',
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
    ]),
    handleReagentGroupSelection() {
      this.fetchSelectedReagentGroup({
        reagentGroupName: this.currentReagentGroup,
      });
    },
    getData() {
      this.data = this.handsonTable.getData();
      debugger;
    },
  },
  watch: {
    hotSettings: {
      handler(val, oldVal) {
        this.handsonTable.updateSettings(val);
      },
      deep: true,
    },
  },
  mounted() {
    this.fetchReagents();
    this.fetchUnits();
    this.fetchAvailableReagentGroups();
    const container = document.getElementById('handsonTable');
    this.handsonTable = new Handsontable(container, this.hotSettings);
  },
};
