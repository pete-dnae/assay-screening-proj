import * as types from './mutation-types';

export const state = {
  template: {
    data: {},
  },
  hgDNA: {
    data: {},
  },
  dilution: {
    data: {},
  },
};

const actions = {};
const mutations = {
  [types.SET_TEMPLATE_RULES](state, data) {
    state.template.data = data;
  },
};
const getters = {};

export default {
  state,
  actions,
  mutations,
  getters,
};
