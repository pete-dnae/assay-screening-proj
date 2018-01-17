/* eslint-disable */
import _ from 'lodash';
import * as types from './mutation-types';
import * as api from '@/models/api'
import experiment from '@/assets/json/response.json';
export const state = {
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
  [types.SET_CURRENT_PLATE](state, data) {
    state.currentPlate = data;
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
  getPlateImage() {
    return state.plateImageUrl;
  },
  getPostingStatus() {
    return state.updateRule.isPosting 
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
