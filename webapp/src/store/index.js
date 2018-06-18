import Vuex from 'vuex';
import Vue from 'vue';

import ui from './modules/ui/index';
import scriptparser from './modules/scriptparser/index';
import suggestions from './modules/suggestions/index';
import pictures from './modules/pictures/index';
import reagentgroups from './modules/reagentgroups/index';
import reagents from './modules/reagents/index';
import results from './modules/results/index';
import auth from './modules/auth/index';

Vue.use(Vuex);

export default new Vuex.Store({
  strict: !!(
    typeof process !== 'undefined' && process.env.NODE_ENV === 'development'
  ),
  modules: {
    ui,
    scriptparser,
    suggestions,
    pictures,
    reagentgroups,
    reagents,
    results,
    auth,
  },
});
