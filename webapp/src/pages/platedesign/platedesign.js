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
      templateData: 'getTemplateOnPlate',
      hgDNAData: 'gethgDNAOnPlate',
      dilutionData: 'getDilutionOnPlate',
      strainData: 'getStrainsOnPlate',
      idPrimerData: 'getIdPrimersOnPlate',
    }),
  },
  methods: {
    handleSelectedRule(evt) {
      this.selectedrule = evt;
    },
    zoomIn(event) {
      zoomIn(event);
    },
  },
};
