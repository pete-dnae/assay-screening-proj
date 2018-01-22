/* eslint-disable */
import _ from 'lodash';
import * as types from './mutation-types';
import * as api from '@/models/api';
export const state = {
  primerKit: {},
  strainKit: {},
};

const actions = {};
const mutations = {
  [types.SET_PRIMER_KIT](state, data) {
    state.primerKit = data;
  },
  [types.SET_PRIMER_KIT](state, data) {
    state.strainKit = data;
  },
};
const getters = {
  getDesignerName(state, getters, rootState) {
    return state.currentExperiment.data.designer_name;
  },
  getExperimentName() {
    return state.currentExperiment.data.experiment_name;
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
