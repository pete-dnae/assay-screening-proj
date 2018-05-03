import { mapGetters, mapActions } from 'vuex';
import reagentGroup from '@/components/reagentgroup/reagentgroup.vue';
import _ from 'lodash';

export default {
  name: 'reagentshome',
  data() {
    return {
      showReagents: false,
      searchField: null,
      searchText: null,
    };
  },
  components: { reagentGroup },
  computed: {
    ...mapGetters({ reagents: 'getReagents' }),
    filteredReagents() {
      if (this.searchField && !_.isEmpty(this.searchText)) {
        return this.reagents.filter(reagent => reagent[this.searchField].includes(this.searchText));
      }
      return this.reagents;
    },
  },
  methods: {
    ...mapActions([]),
  },
  mounted() {},
};
