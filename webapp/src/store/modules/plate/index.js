/* eslint-disable */
import _ from 'lodash';
import * as types from './mutation-types';
import * as api from '@/models/api';
import experiment from '@/assets/json/response.json';
export const state = {
  currentPlate: {
    data: {
      allocation_instructions: {
        rule_list: {
          rules: null,
          url: null,
        },
        allocation_results: null,
      },
    },
    isFetching: false,
    fetched: false,
    didInvalidate: false,
  },
  updateRule: {
    isPosting: false,
    posted: false,
    didInvalidate: false,
  },
  plateImageUrl: '',
};

const actions = {
  fetchPlate({ commit }, args) {
    commit(types.REQUEST_PLATE);
    return new Promise(function(resolve, reject) {
      api
        .getPlate(args)
        .then(data => {
          commit(types.RECEIVED_PLATE, data);
          resolve(data);
        })
        .catch(e => {
          commit(types.PLATE_FAILURE);
          reject(data);
        });
    });
  },
  updateAllocationRules({ commit }, args) {
    commit(types.REQUEST_UPDATE_RULE_ORDER);
    const { data, url } = args;
    return new Promise(function(resolve, reject) {
      api
        .updateAllocationRules(url, data)
        .then(({ data }) => {
          commit(types.UPDATE_RULE_ORDER_SUCESS, data);
          resolve(data);
        })
        .catch(e => {
          commit(types.UPDATE_RULE_ORDER_FAILURE);
          reject(data);
        });
    });
  },
  addAllocationRule({ commit }, args) {
    commit(types.REQUEST_ADD_RULE);
    const { data, url } = args;
    return new Promise(function(resolve, reject) {
      api
        .addAllocationRule(url, data)
        .then(({ data }) => {
          commit(types.ADD_RULE_SUCESS, data);
          resolve(data);
        })
        .catch(e => {
          commit(types.ADD_RULE_FAILURE);
          reject(data);
        });
    });
  },
};
const mutations = {
  [types.SET_CURRENT_PLATE](state, data) {
    state.currentPlate.data = data;
    state.currentPlate.data.allocation_instructions.rule_list.rules = state.currentPlate.data.allocation_instructions.rule_list.rules.map(
      (x, i) => {
        return { ...x, id: i + 1 };
      },
    );
  },
  [types.SET_PLATE_IMAGE_URL](state, url) {
    state.plateImageUrl = url;
  },
  [types.REQUEST_UPDATE_RULE_ORDER](state) {
    state.updateRule.isPosting = true;
    state.updateRule.posted = false;
    state.updateRule.didInvalidate = false;
  },
  [types.UPDATE_RULE_ORDER_SUCESS](state) {
    state.updateRule.isPosting = false;
    state.updateRule.posted = true;
    state.updateRule.didInvalidate = false;
  },
  [types.UPDATE_RULE_ORDER_FAILURE](state) {
    state.updateRule.isPosting = false;
    state.updateRule.posted = false;
    state.updateRule.didInvalidate = true;
  },
  [types.REQUEST_ADD_RULE](state) {
    state.updateRule.isPosting = true;
    state.updateRule.posted = false;
    state.updateRule.didInvalidate = false;
  },
  [types.ADD_RULE_SUCESS](state) {
    state.updateRule.isPosting = false;
    state.updateRule.posted = true;
    state.updateRule.didInvalidate = false;
  },
  [types.ADD_RULE_FAILURE](state) {
    state.updateRule.isPosting = false;
    state.updateRule.posted = false;
    state.updateRule.didInvalidate = true;
  },
  [types.REQUEST_PLATE](state, plateId) {
    state.currentPlate.isFetching = true;
    state.currentPlate.fetched = false;
    state.currentPlate.didInvalidate = false;
  },
  [types.RECEIVED_PLATE](state, data) {
    state.currentPlate.data = data;
    state.currentPlate.isFetching = false;
    state.currentPlate.fetched = true;
    state.currentPlate.didInvalidate = false;
  },
  [types.PLATE_FAILURE](state, plateId) {
    state.currentPlate.isFetching = false;
    state.currentPlate.fetched = false;
    state.currentPlate.didInvalidate = true;
  },
};
const getters = {
  getPlateInfo(state, getters, rootState) {
    return state.currentPlate.data;
  },
  getAllocationRules(state, getters, rootState) {
    return state.currentPlate.data.allocation_instructions.rule_list.rules;
  },
  getAllocationResults(state, getters, rootState) {
    return state.currentPlate.data.allocation_instructions.allocation_results;
  },
  getPlateImage() {
    return state.plateImageUrl;
  },
  getPostingStatus() {
    return state.updateRule.isPosting;
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
