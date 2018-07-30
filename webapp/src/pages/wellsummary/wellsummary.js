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
import annotator from '@/components/annotator/annotator.vue';

export default {
  name: 'wellsummary',
  data() {
    return {
      msg: 'Welcome',
      masterHeaders: MASTER_HEADERS,
      columnsToColor: SUMMARY_COLOR_CONFIG,
      summaryHeaders: null,
      experimentId: null,
      plateId: null,
      wells: null,
      showAnnotator: false,
    };
  },
  components: {
    calcTable,
    annotator,
  },
  computed: {
    ...mapGetters({
      resultMaster: 'getResultMaster',
      resultSummary: 'getResultSummary',
      ampGraphData: 'getAmpGraphData',
      meltGraphData: 'getMeltGraphData',
      copyCountGraphData: 'getCopyCountGraphData',
      labchipGraphData: 'getLabchiPGraphData',
      currentSelection: 'getCurrentSelection',
    }),
  },
  watch: {
    resultSummary: {
      handler(value) {
        this.summaryHeaders = this.removeHeadersWithNoData(SUMMARY_HEADERS, value);
      },
      deep: true,
    },
  },
  methods: {
    ...mapActions(['fetchWellSummary']),
    removeHeadersWithNoData(headers, resultSummary) {
      const headerValid = {};
      Object.keys(headers).forEach((head) => {
        resultSummary.forEach((row) => {
          if (headers[head].array) {
            if (!_.isEmpty(row[head])) {
              headerValid[head] = true;
            }
          } else if (row[head]) {
            headerValid[head] = true;
          }
        });
      });
      const filteredHeaders = _.reduce(headers, (acc, headVal, headKey) => {
        if (headerValid[headKey]) {
          acc[headKey] = headVal;
        }
        return acc;
      }, {});
      return filteredHeaders;
    },
    publishSummary() {
      const { Expt, Plate, Wells } = this.$route.params;
      this.experimentId = Expt;
      this.plateId = Plate;
      this.wells = Wells;
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
    handleWellSelection(wellList) {
      this.$store.commit('SET_CURRENT_SELECTION', wellList.map(well => ({
        'qPCR Well': well['qPCR Well'],
        'LC Well': well['LC Well'],
        'qPCR Well Id': well['qPCR Well Id'],
        'Labchip Well Id': well['Labchip Well Id'],
      })));
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
    this.publishSummary();
  },
};
