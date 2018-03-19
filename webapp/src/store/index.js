import Vuex from 'vuex';
import Vue from 'vue';

import ui from './modules/ui/index';
import scriptparser from './modules/scriptparser/index';

Vue.use(Vuex);

export default new Vuex.Store({
  strict: !!(
    typeof process !== 'undefined' && process.env.NODE_ENV === 'development'
  ),
  modules: {
    ui,
    scriptparser,
  },
});
