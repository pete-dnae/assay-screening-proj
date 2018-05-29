import Vue from 'vue';
import Router from 'vue-router';

import experimenthome from '@/pages/experimenthome/experimenthome.vue';
import reagents from '@/pages/reagentshome/reagentshome.vue';
import wellresults from '@/pages/wellresults/wellresults.vue';
import wellSummary from '@/pages/wellsummary/wellsummary.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/experiment',
    },
    {
      path: '/maintenance',
      name: 'reagentHome',
      component: reagents,
    },
    {
      path: '/experiment',
      name: 'experimenthome',
      component: experimenthome,
      props: true,
    },
    {
      path: '/results',
      name: 'resultsHome',
      component: wellresults,
    },
    {
      path: '/summary',
      name: 'summaryHome',
      component: wellSummary,
    },
  ],
});
