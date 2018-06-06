import { mapGetters, mapActions } from 'vuex';
import calcTable from '@/components/table/table.vue';
import {
  plotCopyCountGraph,
  plotMeltGraph,
  plotAmpGraph,
  plotLabchipGraph,
} from '@/models/plots';
import { generateLabChipPlotTraces } from '@/models/plotUtilities';
import {
  MASTER_HEADERS,
  SUMMARY_HEADERS,
  SUMMARY_COLOR_CONFIG,
} from '@/models/tableConfiguration';
import _ from 'lodash';
import VueDraggableResizable from 'vue-draggable-resizable';

export default {
  name: 'wellsummary',
  data() {
    return {
      msg: 'Welcome',
      masterHeaders: MASTER_HEADERS,
      columnsToColor: SUMMARY_COLOR_CONFIG,
      summaryHeaders: SUMMARY_HEADERS,
      showSummary: true,
    };
  },
  components: {
    calcTable,
    VueDraggableResizable,
  },
  computed: {
    ...mapGetters({
      resultMaster: 'getResultMaster',
      resultSummary: 'getResultSummary',
      ampGraphData: 'getAmpGraphData',
      meltGraphData: 'getMeltGraphData',
      copyCountGraphData: 'getCopyCountGraphData',
      labchipGraphData: 'getLabchiPGraphData',
    }),
  },
  methods: {
    ...mapActions(['fetchWellSummary']),
    handleWellSelection(wellList) {
      const qpcrWells = _.map(wellList, 'qPCR Well');
      const lcWells = _.map(wellList, 'LC Well');
      plotAmpGraph(
        _.filter(
          this.ampGraphData,
          row => qpcrWells.indexOf(row.meta.well_id) > -1,
        ),
      );
      plotMeltGraph(
        _.filter(
          this.meltGraphData,
          row => qpcrWells.indexOf(row.meta.well_id) > -1,
        ),
      );
      plotLabchipGraph(
        generateLabChipPlotTraces(
          _.reduce(
            this.labchipGraphData,
            (acc, val, wellId) => {
              if (lcWells.indexOf(wellId) > -1) {
                acc[wellId] = val;
              }
              return acc;
            },
            {},
          ),
        ),
      );
    },
  },
  mounted() {
    const { Expt, Plate, Wells } = this.$route.params;
    const wellArray = JSON.stringify(Wells.split(','));
    this.fetchWellSummary({
      wellArray,
      experimentId: Expt,
      qpcrPlateId: Plate,
    }).then(() => {
      plotAmpGraph(this.ampGraphData);
      plotMeltGraph(this.meltGraphData);
      plotCopyCountGraph(this.copyCountGraphData);
      plotLabchipGraph(generateLabChipPlotTraces(this.labchipGraphData));
    });
  },
};
