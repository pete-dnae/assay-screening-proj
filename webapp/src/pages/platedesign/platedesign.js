import { mapGetters, mapActions } from 'vuex';
import allocationrules from '@/components/allocationrules/allocationrules.vue';
import selectedrule from '@/components/selectedrule/selectedrule.vue';
import { zoomIn, zoomOut, prepareResultsTable, makeSVG } from '@/models/utils';
import {
  spinner,
} from 'vue-strap';

export default {
  name: 'PlateDesign',
  components: {
    allocationrules,
    selectedrule,
    spinner,
  },
  data() {
    return {
      msg: 'Welcome',
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
      allocationRules: 'getAllocationRules',
      allocationResults: 'getAllocationResults',
      designerName: 'getDesignerName',
      experimentName: 'getExperimentName',
      plateImage: 'getPlateImage',
      spin: 'getPostingStatus',
    }),
  },
  methods: {
    ...mapActions(['fetchExperiment']),
    handleSelectedRule(ruleElem) {
      this.$store.commit('SET_CURRENT_RULE', ruleElem);
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
