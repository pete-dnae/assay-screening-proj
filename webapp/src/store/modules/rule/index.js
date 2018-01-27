/* eslint-disable */
import _ from 'lodash';
import * as types from './mutation-types';
import * as api from '@/models/api';
import experiment from '@/assets/json/response.json';
export const state = {
  currentRule: {
    display_string: null,
    end_column: null,
    end_row_letter: null,
    id: null,
    pattern: null,
    payload_type: null,
    payload_csv: [],
    rank_for_ordering: null,
    start_column: null,
    start_row_letter: null,
    url: null,
  },
  updateRule: {
    isPosting: false,
    posted: false,
    didInvalidate: false,
  },
};

const actions = {
  updateRule({ commit }, url) {
    commit(types.REQUEST_UPDATE_RULE);
    const data = {
      ...state.currentRule,
      payload_csv: state.currentRule.payload_csv.toString(),
    };
    return new Promise(function(resolve, reject) {
      api
        .updateRule(url, data)
        .then(
          ({ data }) => {
            commit(types.UPDATE_RULE_SUCESS, data);
            resolve(data);
          },
          ({ response }) => {
            reject(response.data);
          },
        )
        .catch(e => {
          commit(types.UPDATE_RULE_FAILURE);
          reject(e);
        });
    });
  },
};
const mutations = {
  [types.SET_CURRENT_RULE](state, data) {
    state.currentRule = data;
    state.currentRule.payload_csv =
      typeof state.currentRule.payload_csv == 'string'
        ? state.currentRule.payload_csv.split(',')
        : state.currentRule.payload_csv;
  },
  [types.SET_ROW_START](state, data) {
    state.currentRule.start_row_letter = data;
  },
  [types.SET_ROW_END](state, data) {
    state.currentRule.end_row_letter = data;
  },
  [types.SET_COL_START](state, data) {
    state.currentRule.start_column = data;
  },
  [types.SET_COL_END](state, data) {
    state.currentRule.end_column = data;
  },
  [types.SET_DIST_PATTERN](state, data) {
    state.currentRule.pattern = data;
  },
  [types.SET_PAYLOAD_TYPE](state, data) {
    state.currentRule.payload_type = data;
  },
  [types.SET_PAYLOAD](state, data) {
    state.currentRule.payload_csv = state.currentRule.payload_csv
      .filter(x => x)
      .concat(data);
  },
  [types.DELETE_PAYLOAD](state, data) {
    state.currentRule.payload_csv = [''];
  },
  [types.REORDER_PAYLOAD](state, data) {
    state.currentRule.payload_csv = data.filter(x => x);
  },
  [types.UPDATE_PAYLOAD](state, data) {
    state.currentRule.payload_csv = data;
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
  getRowStart(state, getters, rootState) {
    return state.currentRule.start_row_letter;
  },
  getRowEnd(state, getters, rootState) {
    return state.currentRule.end_row_letter;
  },
  getColStart(state, getters, rootState) {
    return state.currentRule.start_column;
  },
  getColEnd(state, getters, rootState) {
    return state.currentRule.end_column;
  },
  getDistPattern(state, getters, rootState) {
    return state.currentRule.pattern;
  },
  getPayloadType(state, getters, rootState) {
    return state.currentRule.payload_type;
  },
  getPayload(state, getters, rootState) {
    return state.currentRule.payload_csv;
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
