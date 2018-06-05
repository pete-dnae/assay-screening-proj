/* eslint-disable */
import _ from "lodash";
import * as types from "./mutation-types";
import * as ui from "../ui/mutation-types";
import * as api from "@/models/api";
export const state = {
  resultList: {
    data: null,
    received: false,
    isReceiving: false,
    didInvalidate: false
  },
  resultSummary: {
    data: {
      summary_table: null,
      amp_graph:null,
      melt_grapp:null,
      copy_cnt_graph:null,
      labchip_peaks:null,
      master_table: null
    },
    received: false,
    isReceiving: false,
    didInvalidate: false
  }
};

const actions = {
  fetchWellResultSummary({ commit }) {
    commit(types.REQUEST_WELL_RESULTS_LIST);
    return new Promise((resolve, reject) => {
      api
        .getWellResultSummary()
        .then(res => {
          commit(types.RECEIVED_WELL_RESULTS_LIST, res);
          resolve("success");
        })
        .catch(e => {
          reject(e);
          commit(ui.SHOW_BLUR);
          commit(types.WELL_RESULTS_LIST_FAILURE);
        });
    });
  },
  fetchWellSummary({ commit }, args) {
    commit(types.REQUEST_WELL_SUMMARY);
    return new Promise((resolve, reject) => {
      api
        .getWellSummary(args)
        .then(res => {
          commit(types.RECEIVED_WELL_SUMMARY, res);
          resolve("success");
        })
        .catch(e => {
          reject(e);
          commit(ui.SHOW_BLUR);
          commit(types.WELL_SUMMARY_FAILURE);
        });
    });
  }
};
const mutations = {
  [types.REQUEST_WELL_RESULTS_LIST](state) {
    state.resultList.isReceiving = true;
    state.resultList.received = false;
    state.resultList.didInvalidate = false;
  },
  [types.RECEIVED_WELL_RESULTS_LIST](state, data) {
    state.resultList.data = data;
    state.resultList.isReceiving = false;
    state.resultList.received = true;
    state.resultList.didInvalidate = false;
  },
  [types.WELL_RESULTS_LIST_FAILURE](state) {
    state.resultList.isReceiving = false;
    state.resultList.received = false;
    state.resultList.didInvalidate = true;
  },
  [types.REQUEST_WELL_SUMMARY](state) {
    state.resultSummary.isReceiving = true;
    state.resultSummary.received = false;
    state.resultSummary.didInvalidate = false;
  },
  [types.RECEIVED_WELL_SUMMARY](state, data) {
    state.resultSummary.data = data;
    state.resultSummary.isReceiving = false;
    state.resultSummary.received = true;
    state.resultSummary.didInvalidate = false;
  },
  [types.WELL_SUMMARY_FAILURE](state) {
    state.resultSummary.isReceiving = false;
    state.resultSummary.received = false;
    state.resultSummary.didInvalidate = true;
  }
};
const getters = {
  getResultList(state, getters, rootState) {
    return state.resultList.data;
  },
  getResultMaster(state, getters, rootState) {
    return state.resultSummary.data.master_table;
  },
  getResultSummary(state, getters, rootState) {
    return state.resultSummary.data.summary_table;
  },
  getAmpGraphData(state, getters, rootState) {
    return state.resultSummary.data.amp_graph;
  },
  getMeltGraphData(state, getters, rootState) {
    return state.resultSummary.data.melt_graph;
  },
  getCopyCountGraphData(state, getters, rootState) {
    return state.resultSummary.data.copy_cnt_graph;
  },
  getLabchiPGraphData(state, getters, rootState) {
    return state.resultSummary.data.labchip_peaks;
  }
};

export default {
  state,
  actions,
  mutations,
  getters
};
