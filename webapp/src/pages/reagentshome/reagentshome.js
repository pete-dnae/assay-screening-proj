
import { mapGetters, mapActions } from 'vuex';
import hottable from '@/components/hottable/hottable.vue';

export default {
  name: 'reagentshome',
  data() {
    return {};
  },
  components: {
    hottable,
  },
  computed: {
    ...mapGetters({
      hotSettings: 'getHotSettings',
    }),
  },
  methods: {
    ...mapActions([
      'fetchAvailableSuggestions',
    ]),
  },
  mounted() {
    this.fetchAvailableSuggestions();
  },
};
