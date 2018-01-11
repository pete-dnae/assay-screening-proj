import Vue from 'vue';
import { mapGetters, mapActions } from 'vuex';
import allocationrules from '@/components/allocationrules/allocationrules.vue';
import selectedrule from '@/components/selectedrule/selectedrule.vue';
import { zoomIn, zoomOut } from '@/models/utils';

export default {
  name: 'PlateDesign',
  components: {
    allocationrules,
    selectedrule,
  },
  data() {
    return {
      msg: 'Welcome',
      selectedrule: {},
    };
  },
  computed: {
    ...mapGetters({
      plateInfo: 'getPlateInfo',
      allocationRules: 'getAllocationRules',
      allocationResults: 'getAllocationResults',
      designerName: 'getDesignerName',
      experimentName: 'getExperimentName',
    }),
  },
  methods: {
    handleSelectedRule(evt) {
      this.selectedrule = evt;
    },
    zoomIn(event) {
      zoomIn(event);
    },
    zoomOut(event) {
      zoomOut(event);
    },
  },
  mounted() {
    this.$store.commit('SET_RULE_ID', this.$route.params.plateId);
  },
};
