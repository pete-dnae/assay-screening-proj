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

export default {
  name: 'wellsummary',
  data() {
    return {
      msg: 'Welcome',
      masterHeaders: MASTER_HEADERS,
      columnsToColor: SUMMARY_COLOR_CONFIG,
      summaryHeaders: SUMMARY_HEADERS,
    };
  },
  components: {
    calcTable,
  },
  computed: {
    ...mapGetters({
      resultMaster: 'getResultMaster',
      resultSummary: 'getResultSummary',
      ampMeltGraphData: 'getAmpMeltGraphData',
      copyCountGraphData: 'getCopyCountGraphData',
      labchipGraphData: 'getLabchiPGraphData',
    }),
  },
  methods: {
    ...mapActions([]),

    handleWellSelection(wellList) {
      const qpcrWells = _.map(wellList, 'qPCR Well');
      const lcWells = _.map(wellList, 'LC Well');
      plotAmpGraph(
        _.filter(
          this.ampMeltGraphData.amp_data,
          row => qpcrWells.indexOf(row.meta.well_id) > -1,
        ),
      );
      plotMeltGraph(
        _.filter(
          this.ampMeltGraphData.melt_data,
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
    plotAmpGraph(this.ampMeltGraphData.amp_data);
    plotMeltGraph(this.ampMeltGraphData.melt_data);
    plotCopyCountGraph(this.copyCountGraphData);
    plotLabchipGraph(generateLabChipPlotTraces(this.labchipGraphData));
  },
};
