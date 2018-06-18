import Vue from 'vue';
import Router from 'vue-router';


import reagents from '@/pages/reagentshome/reagentshome.vue';
import wellresults from '@/pages/wellresults/wellresults.vue';
import wellSummary from '@/pages/wellsummary/wellsummary.vue';
import login from '@/pages/login/login.vue';
import scriptInput from '@/pages/scriptinput/scriptinput.vue';

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
      component: scriptInput,
    },
    {
      path: '/results',
      name: 'resultsHome',
      component: wellresults,
    },
    {
      path: '/login',
      name: 'login',
      component: login,
    },
    {
      path: '/summary/:Expt/:Plate/:Wells',
      name: 'summaryHome',
      component: wellSummary,
    },
  ],
});
