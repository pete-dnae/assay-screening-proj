import { mapGetters, mapActions } from 'vuex';
import reagentGroup from '@/components/reagentgroup/reagentgroup.vue';
import _ from 'lodash';

export default {
  name: 'reagentshome',
  data() {
    return {};
  },
  components: { reagentGroup },
  computed: {
    ...mapGetters({}),
  },
  methods: {
    ...mapActions([]),
  },
  mounted() {},
};
