import * as types from './mutation-types';

export const state = {
  template: {
    data: [],
  },
  hgDNA: {
    data: {},
  },
  dilution: {
    data: {},
  },
  plate: {
    data: { templateConcentration: {}, hgDNAConcentration: {} },
  },
};

const actions = {};
const mutations = {
  [types.SET_TEMPLATE_RULES](state, data) {
    state.template.data = data;
  },
  [types.SET_HGDNA_RULES](state, data) {
    state.hgDNA.data = data;
  },
  [types.SET_TEMPLATE_PLATE](state, data) {
    state.plate.data.templateConcentration = data.reduce((acc, x) => {
      x.allRows.map(
        y =>
          (acc[y] = _.times(x.repeat, () => x.concentration.split(',')).reduce((a, x) => {
            a = a.concat(x);
            return a;
          }, [])),
      );
      return acc;
    }, {});
  },
  [types.SET_HGDNA_PLATE](state, data) {
    state.plate.data.hgDNAConcentration = data.reduce((acc, x) => {
      x.allRows.map(
        y =>
          (acc[y] = _.times(x.repeat, () => x.concentration.split(',')).reduce((a, x) => {
            a = a.concat(x);
            return a;
          }, [])),
      );
      return acc;
    }, {});
  },
};
const getters = {
  getTemplate(state, getters, rootState) {
    return state.plate.data.templateConcentration;
  },
  gethgDNA(state, getters, rootState) {
    return state.plate.data.hgDNAConcentration;
  },
  getDilution(state, getters, rootState) {
    return state.dilution.data;
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
