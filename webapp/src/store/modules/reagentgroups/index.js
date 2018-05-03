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
  errors:{
    data:null
  }
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
  saveReagents({ commit }, reagents) {
    commit(types.REQUEST_SAVE_REAGENT_GROUP);
    return new Promise((resolve, reject) => {
      api
        .postReagentGroup(reagents)
        .then(res => {
            commit(types.SAVE_REAGENT_GROUP_SUCCESS, res);
            resolve("success");
          }, ({ response: { data } }) => {
            commit(types.ADD_ERROR_MESSAGE_REAGENT_GROUP, data);
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
          }, ({ response: { data } }) => {
            commit(types.ADD_ERROR_MESSAGE_REAGENT_GROUP, data);
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
  },
  [types.ADD_ERROR_MESSAGE_REAGENT_GROUP](state, data) {
    state.errors.data = data;
  }
};
const getters = {
  getReagentGroupList(state, getters, rootState) {
    return state.reagentGroupList.data;
  },
  getCurrentGroupReagents(state, getters, rootState) {
    return state.currentGroupReagents.data;
  },
  getReagentGroupsErrors(state, getters, rootState) {
    return state.errors.data;
  }
};

export default {
  state,
  actions,
  mutations,
  getters
};
