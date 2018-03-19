import Vue from 'vue';
import Router from 'vue-router';

import experimenthome from '@/pages/experimenthome/experimenthome.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/1',
    },

    {
      path: '/:ruleScript',
      name: 'experimenthome',
      component: experimenthome,
    },
  ],
});
