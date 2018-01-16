import { mapGetters, mapActions } from 'vuex';
import allocationrules from '@/components/allocationrules/allocationrules.vue';
import selectedrule from '@/components/selectedrule/selectedrule.vue';
import { zoomIn, zoomOut, prepareResultsTable, makeSVG } from '@/models/utils';

export default {
  name: 'PlateDesign',
  components: {
    allocationrules,
    selectedrule,
  },
  data() {
    return {
      msg: 'Welcome',
      selectedrule: null,
    };
  },
  beforeRouteUpdate(to, from, next) {
    const plateId = to.params.plateId;
    if (this.$store.state.experiment.experiment.data.plates[plateId]) {
      next();
    } else {
      next(false);
    }
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

    ...mapActions(['fetchExperiment']),
    handleSelectedRule(evt) {
      this.selectedrule = evt;
    },
    zoomIn(event) {
      zoomIn(event);
    },
    zoomOut(event) {
      zoomOut(event);
    },
    drawTableImage() {
      const url = makeSVG(
        window.URL || window.webkitURL || window,
        prepareResultsTable(this.allocationResults),
      );
      const element = document.getElementById('overlay');
      element.style.backgroundImage = `url('${url}')`;
      this.$store.commit('SET_PLATE_IMAGE_URL', url);
    },
    handleRuleChange() {
      this.drawTableImage();
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
    this.fetchExperiment('1').then((res) => {
      this.$store.commit('SET_CURRENT_PLATE', res.plates[parseInt(this.$route.params.plateId, 10)]);
      this.drawTableImage();
    });
  },
};
