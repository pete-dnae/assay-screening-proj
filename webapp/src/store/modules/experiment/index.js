/* eslint-disable */
import _ from 'lodash';
import * as types from './mutation-types';
import * as api from '@/models/api'
import experiment from '@/assets/json/response.json';
export const state = {
  experiment: {
    data: {
      designer_name: '',
      experiment_name: ''
    },
    isFetching: false,
    fetched: false,
    didInvalidate: false,
  },
  currentPlate: {
    allocation_instructions: {
      rule_list: {
        rules: null,
        url: null
      },
      allocation_results: null
    }
  },
  updateRule:{
    isPosting: false,
    posted: false,
    didInvalidate: false,
  },
  plateImageUrl: '',
};

const actions = {
  fetchExperiment({
    commit
  }, args) {
    commit(types.REQUEST_EXPERIMENT);
    return new Promise(function(resolve, reject) {
      api
        .getExperiment(args)
        .then(data => {
          commit(types.RECEIVED_EXPERIMENT, data);
          resolve(data);
        })
        .catch(e => {
          commit(types.EXPERIMENT_FAILURE);
          reject(data);
        });
    });
  },
  updateAllocationRules({
    commit
  }, args) {
    commit(types.REQUEST_UPDATE_RULE);
    const{data,url}=args;
    return new Promise(function(resolve, reject) {
      api
        .updateAllocationRules(url,data)
        .then(({data}) => {
          commit(types.UPDATE_RULE_SUCESS, data);
          resolve(data);
        })
        .catch(e => {
          commit(types.UPDATE_RULE_FAILURE);
          reject(data);
        });
    });
  }
};
const mutations = {
  [types.REQUEST_EXPERIMENT](state, plateId) {
    state.experiment.isFetching = true;
    state.experiment.fetched = false;
    state.experiment.didInvalidate = false;
  },
  [types.SET_CURRENT_PLATE](state, data) {
    state.currentPlate = data;
  },
  [types.RECEIVED_EXPERIMENT](state, data) {
    state.experiment.data = data;
    state.experiment.isFetching = false;
    state.experiment.fetched = true;
    state.experiment.didInvalidate = false;
  },
  [types.EXPERIMENT_FAILURE](state, plateId) {
    state.experiment.isFetching = false;
    state.experiment.fetched = false;
    state.experiment.didInvalidate = true;
  },
  [types.SET_PLATE_IMAGE_URL](state, url) {
    state.plateImageUrl = url;
  },
  [types.REQUEST_UPDATE_RULE](state) {
    state.updateRule.isPosting = true;
    state.updateRule.posted = false;
    state.updateRule.didInvalidate = false;
  },
  [types.UPDATE_RULE_SUCESS](state) {
    state.updateRule.isPosting = false;
    state.updateRule.posted = true;
    state.updateRule.didInvalidate = false;
  },
  [types.UPDATE_RULE_FAILURE](state) {
    state.updateRule.isPosting = false;
    state.updateRule.posted = false;
    state.updateRule.didInvalidate = true;
  },

};
const getters = {
  getPlateInfo(state, getters, rootState) {
    return state.currentPlate;
  },
  getAllocationRules(state, getters, rootState) {
    return state.currentPlate.allocation_instructions
      .rule_list.rules;
  },
  getAllocationResults(state, getters, rootState) {
    return state.currentPlate.allocation_instructions
      .allocation_results;
  },
  getDesignerName(state, getters, rootState) {
    return state.experiment.data.designer_name;
  },
  getExperimentName() {
    return state.experiment.data.experiment_name;
  },
  getPlateImage() {
    return state.plateImageUrl;
  },
  getPostingStatus() {
    return state.updateRule.isPosting ||
    state.experiment.isFetching;
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
