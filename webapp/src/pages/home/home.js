import Vue from 'vue';
import { mapGetters } from 'vuex';
import rules from '@/components/rules/rules.vue';
import footer from '@/components/footer/footer.vue';
import plate from '@/components/plate/plate.vue';

Vue.component('rulesdropdown', rules);
Vue.component('customfooter', footer);
Vue.component('plateLayout', plate);

export default {
  name: 'HelloWorld',
  data() {
    return {
      msg: 'Welcome Bitch',
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
};
