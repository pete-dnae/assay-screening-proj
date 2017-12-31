import Vue from 'vue';
import { mapGetters, mapActions } from 'vuex';
import rules from '@/components/rules/rules.vue';
import footer from '@/components/footer/footer.vue';
import plate from '@/components/plate/plate.vue';
import '@/assets/sass/app.scss';

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
      templateData: 'getTemplate',
      hgDNAData: 'gethgDNA',
      dilutionData: 'getDilution',
      strainData: 'getStrains',
      idPrimerData: 'getIdPrimers',
    }),
  },
};
