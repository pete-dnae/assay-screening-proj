/* eslint-disable */
import _ from "lodash";
import * as types from "./mutation-types";
import * as api from "@/models/api";
import * as ui from "../ui/mutation-types";
import { findSuggestions } from "@/models/editor2.0.js";

export const state = {
  reagentGroupList:{
    data:null,
    isFetching:false,
    fetched:false,
    didInvalidate:false
  }
};

const actions = {
  fetchAvailableReagentGroups({ commit }) {
    commit(types.REQUEST_AVAILABLE_REAGENT_GROUPS);
    return new Promise(function(resolve, reject) {
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
};
const mutations = {
  [types.REQUEST_AVAILABLE_REAGENT_GROUPS](state) {
    state.avaliableSuggestions.isFetching = true;
    state.avaliableSuggestions.fetched = false;
    state.avaliableSuggestions.didInvalidate = false;
  },
  [types.RECEIVED_AVAILABLE_REAGENT_GROUPS](state, data) {
    state.avaliableSuggestions.data = data;
    state.avaliableSuggestions.isFetching = false;
    state.avaliableSuggestions.fetched = true;
    state.avaliableSuggestions.didInvalidate = false;
  },
  [types.AVAILABLE_REAGENT_GROUPS_FAILURE](state) {
    state.avaliableSuggestions.isFetching = false;
    state.avaliableSuggestions.fetched = false;
    state.avaliableSuggestions.didInvalidate = true;
  }
};
const getters = {
  getReagentGroupList(state, getters, rootState) {
    return state.reagentGroupList.data;
  }
};

export default {
  state,
  actions,
  mutations,
  getters
};
