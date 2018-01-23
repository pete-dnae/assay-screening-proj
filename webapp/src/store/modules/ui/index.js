/* eslint-disable */
import _ from 'lodash';
import * as types from './mutation-types';
import * as api from '@/models/api';
export const state = {
  primerKit: {
    id_primers: null,
    pa_primers: null,
  },
  strainKit: {
    strain: null,
  },
};

const actions = {};
const mutations = {
  [types.SET_PRIMER_KIT](state, data) {
    state.primerKit = data;
  },
  [types.SET_STRAIN_KIT](state, data) {
    state.strainKit = data;
  },
};
const getters = {
  getPaPrimers(state, getters, rootState) {
    return state.primerKit.pa_primers;
  },
  getIdPrimers() {
    return state.primerKit.id_primers;
  },
  getStrains() {
    return state.strainKit.strain;
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
