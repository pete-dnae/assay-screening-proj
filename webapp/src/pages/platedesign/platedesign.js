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
  beforeRouteLeave(to, from, next) {
    const answer = window.confirm('Do you really want to leave? you have unsaved changes!');
    if (answer) {
      next();
    } else {
      next(false);
    }
  },
  computed: {
    ...mapGetters({
      plateInfo: 'getPlateInfo',
      allocationRules: 'getAllocationRules',
      allocationResults: 'getAllocationResults',
      designerName: 'getDesignerName',
      experimentName: 'getExperimentName',
      plateImage: 'getPlateImage',
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

    handleDoubleClick() {
      const dl = document.createElement('a');
      document.body.appendChild(dl);
      dl.setAttribute('href', this.plateImage);
      dl.setAttribute('download', 'test.svg');
      dl.click();
    },
  },
  mounted() {
    this.$store.commit('SET_RULE_ID', this.$route.params.plateId);
  },
};
