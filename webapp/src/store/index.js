import Vuex from 'vuex';
import Vue from 'vue';

import experiment from './modules/experiment/index';

Vue.use(Vuex);

export default new Vuex.Store({
  strict: !!(typeof process !== 'undefined' && process.env.NODE_ENV === 'development'),
  modules: {
    experiment,
  },
});
