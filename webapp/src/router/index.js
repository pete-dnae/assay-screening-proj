import Vue from 'vue';
import Router from 'vue-router';

import experimenthome from '@/pages/experimenthome/experimenthome.vue';
import reagents from '@/pages/reagentshome/reagentshome.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/experiment',
    },
    {
      path: '/reagents',
      name: 'reagentHome',
      component: reagents,
    },
    {
      path: '/pools',
      name: 'reagentHome',
      component: reagents,
    },
    {
      path: '/experiment',
      name: 'experimenthome',
      component: experimenthome,
      props: true,
    },
  ],
});
