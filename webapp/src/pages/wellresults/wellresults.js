import { mapGetters, mapActions } from 'vuex';
import wellResultsSummary from '@/components/table/table.vue';
import {
  RESULTS_SUMMARY_HEADERS,
  RESULTS_COLOR_CONFIG,
} from '@/models/tableConfiguration';

export default {
  name: 'wellresults',
  data() {
    return {
      msg: 'Welcome',
      headers: RESULTS_SUMMARY_HEADERS,
      columnsToColor: RESULTS_COLOR_CONFIG,
    };
  },
  components: {
    wellResultsSummary,
  },
  computed: {
    ...mapGetters({
      resultList: 'getResultList',
    }),
  },
  methods: {
    ...mapActions(['fetchWellResultSummary', 'fetchWellSummary']),
    getSummary({ experiment_id, qpcr_plate_id, wells }) {
      const wellArray = JSON.stringify(wells.split(','));
      this.fetchWellSummary({
        wellArray,
        experimentId: experiment_id,
        qpcrPlateId: qpcr_plate_id,
      });
    },
  },
  mounted() {
    this.fetchWellResultSummary();
  },
};
