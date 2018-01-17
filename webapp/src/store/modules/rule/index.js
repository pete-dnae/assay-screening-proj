/* eslint-disable */
import _ from 'lodash';
import * as types from './mutation-types';
import * as api from '@/models/api'
import experiment from '@/assets/json/response.json';
export const state = {
  currentRule: {
    display_string: null,
    end_column: null,
    end_row_letter: null,
    id: null,
    pattern: null,
    payload_type: null,
    payload_csv: null,
    rank_for_ordering: null,
    start_column: null,
    start_row_letter: null,
    url: null
  }
};

const actions = {

};
const mutations = {
  [types.SET_CURRENT_RULE](state, data) {
    state.currentRule = data;
    state.currentRule.payload_csv = (typeof state.currentRule.payload_csv == 'string') ? state.currentRule.payload_csv.split(',') : state.currentRule.payload_csv;
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
    state.currentRule.payload_csv = data;
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
