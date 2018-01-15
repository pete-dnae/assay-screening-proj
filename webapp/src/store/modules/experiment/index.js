/* eslint-disable */
import _ from 'lodash';
import * as types from './mutation-types';
import experiment from '@/assets/json/response.json';
export const state = {
  experiment,
  plateImageUrl: '',
};

const actions = {};
const mutations = {
  [types.SET_RULE_ID](state, plateId) {
    state.experiment.plates[plateId].allocation_instructions.allocation_rules = _.map(
      state.experiment.plates[plateId].allocation_instructions.allocation_rules,
      (x, i) => (x = { ...x, id: i }),
    );
  },
  [types.SET_PLATE_IMAGE_URL](state, url) {
    state.plateImageUrl = url;
  },
  [types.SET_RULE_ORDER_CHANGE](state, args) {
    const { data, plateId } = args;
    state.experiment.plates[plateId].allocation_instructions.allocation_rules = _.map(
      data,
      (x, i) => (x = { ...x, id: i }),
    );
  },
};
const getters = {
  getPlateInfo(state, getters, rootState) {
    return state.experiment.plates[rootState.route.params.plateId];
  },
  getAllocationRules(state, getters, rootState) {
    return state.experiment.plates[rootState.route.params.plateId].allocation_instructions
      .allocation_rules;
  },
  getAllocationResults(state, getters, rootState) {
    return state.experiment.plates[rootState.route.params.plateId].allocation_instructions
      .allocation_results;
  },
  getDesignerName(state, getters, rootState) {
    return state.experiment.designer_name;
  },
  getExperimentName() {
    return state.experiment.experiment_name;
  },
  getPlateImage() {
    return state.plateImageUrl;
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
