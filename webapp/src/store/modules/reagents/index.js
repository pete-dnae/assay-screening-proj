/* eslint-disable */
import * as api from "@/models/api";
import * as types from "./mutation-types";
import * as ui from "../ui/mutation-types";
import _ from "lodash";

export const state = {
  reagentGroupList: {
    data: null,
    isFetching: false,
    fetched: false,
    didInvalidate: false
  },
  currentGroupReagents: {
    data: null,
    isFetching: false,
    fetched: false,
    didInvalidate: false,
    isPosting:false,
    posted:false,    
    isDeleting:false,
    deleted:false,    
  },
  reagents: {
    data: null,    
    isFetching: false,
    fetched: false,
    didInvalidate: false
  },
  units: {
    data: null,
    isFetching: false,
    fetched: false,
    didInvalidate: false
  },
};

const actions = {
  fetchAvailableReagentGroups({ commit }) {
    commit(types.REQUEST_AVAILABLE_REAGENT_GROUPS);
    return new Promise((resolve, reject) => {
      api
        .getAvailableReagentGroups()
        .then(res => {
          commit(types.RECEIVED_AVAILABLE_REAGENT_GROUPS, res);
          resolve("success");
        })
        .catch(e => {
          reject(e);
          commit(ui.SHOW_BLUR);
          commit(types.AVAILABLE_REAGENT_GROUPS_FAILURE);
        });
    });
  },
  fetchSelectedReagentGroup({ commit }, { reagentGroupName }) {
    commit(types.REQUEST_SELECTED_REAGENT_GROUPS);
    return new Promise((resolve, reject) => {
      api
        .getSelectedReagentGroup(reagentGroupName)
        .then(res => {
          commit(types.RECEIVED_SELECTED_REAGENT_GROUPS, res);
          resolve("success");
        })
        .catch(e => {
          reject(e);
          commit(ui.SHOW_BLUR);
          commit(types.SELECTED_REAGENT_GROUPS_FAILURE);
        });
    });
  },
  fetchReagents({ commit }) {
    commit(types.REQUEST_REAGENTS);
    return new Promise((resolve, reject) => {
      api
        .getReagents()
        .then(res => {
          commit(types.RECEIVED_REAGENTS, res);
          resolve("success");
        })
        .catch(e => {
          reject(e);
          commit(ui.SHOW_BLUR);
          commit(types.REAGENTS_FAILURE);
        });
    });
  },
  fetchUnits({ commit }) {
    commit(types.REQUEST_UNITS);
    return new Promise((resolve, reject) => {
      api
        .getUnits()
        .then(res => {
          commit(types.RECEIVED_UNITS, res);
          resolve("success");
        })
        .catch(e => {
          reject(e);
          commit(ui.SHOW_BLUR);
          commit(types.UNITS_FAILURE);
        });
    });
  },
  saveReagents({ commit }, reagents) {
    commit(types.REQUEST_SAVE_REAGENT_GROUP);
    return new Promise((resolve, reject) => {
      api
        .postReagentGroup(reagents)
        .then(res => {
          commit(types.SAVE_REAGENT_GROUP_SUCCESS, res);
          resolve("success");
        })
        .catch(e => {
          reject(e);
          commit(ui.SHOW_BLUR);
          commit(types.SAVE_REAGENT_GROUP_FAILURE);
        });
    });
  },
  deleteReagentGroup({ commit }, reagentGroupName) {
    commit(types.REQUEST_DELETE_REAGENT_GROUP);    
    return new Promise((resolve, reject) => {
      api
        .deleteReagentGroup(reagentGroupName)
        .then(res => {
          commit(types.DELETE_REAGENT_GROUP_SUCCESS, res);
          resolve("success");
        })
        .catch(e => {
          reject(e);
          commit(ui.SHOW_BLUR);
          commit(types.DELETE_REAGENT_GROUP_FAILURE);
        });
    });
  }
};
const mutations = {
  [types.REQUEST_AVAILABLE_REAGENT_GROUPS](state) {
    state.reagentGroupList.isFetching = true;
    state.reagentGroupList.fetched = false;
    state.reagentGroupList.didInvalidate = false;
  },
  [types.RECEIVED_AVAILABLE_REAGENT_GROUPS](state, data) {
    state.reagentGroupList.data = data;
    state.reagentGroupList.isFetching = false;
    state.reagentGroupList.fetched = true;
    state.reagentGroupList.didInvalidate = false;
  },
  [types.AVAILABLE_REAGENT_GROUPS_FAILURE](state) {
    state.reagentGroupList.isFetching = false;
    state.reagentGroupList.fetched = false;
    state.reagentGroupList.didInvalidate = true;
  },
  [types.REQUEST_SELECTED_REAGENT_GROUPS](state) {
    state.currentGroupReagents.isFetching = true;
    state.currentGroupReagents.fetched = false;
    state.currentGroupReagents.didInvalidate = false;
  },
  [types.RECEIVED_SELECTED_REAGENT_GROUPS](state, data) {
    state.currentGroupReagents.data = data;
    state.currentGroupReagents.isFetching = false;
    state.currentGroupReagents.fetched = true;
    state.currentGroupReagents.didInvalidate = false;
  },
  [types.SELECTED_REAGENT_GROUPS_FAILURE](state) {
    state.currentGroupReagents.isFetching = false;
    state.currentGroupReagents.fetched = false;
    state.currentGroupReagents.didInvalidate = true;
  },
  [types.REQUEST_REAGENTS](state) {
    state.reagents.isFetching = true;
    state.reagents.fetched = false;
    state.reagents.didInvalidate = false;
  },
  [types.RECEIVED_REAGENTS](state, data) {
    state.reagents.data = data;
    state.reagents.isFetching = false;
    state.reagents.fetched = true;
    state.reagents.didInvalidate = false;
  },
  [types.REAGENTS_FAILURE](state) {
    state.reagents.isFetching = false;
    state.reagents.fetched = false;
    state.reagents.didInvalidate = true;
  },
  [types.REQUEST_UNITS](state) {
    state.units.isFetching = true;
    state.units.fetched = false;
    state.units.didInvalidate = false;
  },
  [types.RECEIVED_UNITS](state, data) {
    state.units.data = data;
    state.units.isFetching = false;
    state.units.fetched = true;
    state.units.didInvalidate = false;
  },
  [types.UNITS_FAILURE](state) {
    state.units.isFetching = false;
    state.units.fetched = false;
    state.units.didInvalidate = true;
  },
  [types.REQUEST_SAVE_REAGENT_GROUP](state, data) {
    state.currentGroupReagents.isPosting = true;
    state.currentGroupReagents.posted = false;
    state.currentGroupReagents.didInvalidate = false;
  },
  [types.SAVE_REAGENT_GROUP_SUCCESS](state, data) {
    state.currentGroupReagents.isPosting = false;
    state.currentGroupReagents.posted = true;
    state.currentGroupReagents.didInvalidate = false;
  },
  [types.SAVE_REAGENT_GROUP_FAILURE](state, data) {
    state.currentGroupReagents.isPosting = false;
    state.currentGroupReagents.posted = false;
    state.currentGroupReagents.didInvalidate = true;
  },
  [types.REQUEST_DELETE_REAGENT_GROUP](state, data) {
    state.currentGroupReagents.isDeleting = true;
    state.currentGroupReagents.eleted = false;
    state.currentGroupReagents.didInvalidate = false;
  },
  [types.DELETE_REAGENT_GROUP_SUCCESS](state, data) {
    state.currentGroupReagents.isDeleting = false;
    state.currentGroupReagents.eleted = true;
    state.currentGroupReagents.didInvalidate = false;
  },
  [types.DELETE_REAGENT_GROUP_FAILURE](state, data) {
    state.currentGroupReagents.isDeleting = false;
    state.currentGroupReagents.eleted = false;
    state.currentGroupReagents.didInvalidate = true;
  }
};
const getters = {
  getReagentGroupList(state, getters, rootState) {
    return state.reagentGroupList.data;
  },
  getCurrentGroupReagents(state, getters, rootState) {
    return state.currentGroupReagents.data;
  },
  getReagents(state, getters, rootState) {
    return state.reagents.data;
  },
  getUnits(state, getters, rootState) {
    return state.units.data;
  }
};

export default {
  state,
  actions,
  mutations,
  getters
};
