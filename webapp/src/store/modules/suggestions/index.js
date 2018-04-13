/* eslint-disable */
import _ from "lodash";
import * as types from "./mutation-types";
import * as api from "@/models/api";
import * as ui from "../ui/mutation-types";
import { findSuggestions } from "@/models/editor2.0.js";

export const state = {
  shortlistedSuggestions: [],
  avaliableSuggestions: {
    data: null,
    isFetching: false,
    fetched: false,
    didInvalidate: false
  }
};

const actions = {
  fetchAvailableSuggestions({ commit }) {
    commit(types.REQUEST_AVAILABLE_SUGGESTIONS);
    return new Promise(function(resolve, reject) {
      api
        .getAvailableSuggestions()
        .then(res => {
          commit(types.RECEIVED_AVAILABLE_SUGGESTIONS, res);
          resolve("success");
        })
        .catch(e => {
          reject(e);
          commit(ui.SHOW_BLUR);
          commit(types.AVAILABLE_SUGGESTIONS_FAILURE);
        });
    });
  },
  setSuggestions({ commit }, fields) {
    if (fields[1] && fields[0][0] === "A") {
      let suggestions = findSuggestions(
        fields[1][0],
        state.avaliableSuggestions.data["reagents_and_groups"]
      );
      let suggestionsLength = suggestions ? suggestions.length : 0
      commit(types.SAVE_SUGGESTIONS, suggestions);
      commit(ui.SHOW_SUGGESTIONS_LIST, suggestionsLength >= 5);
      commit(ui.SHOW_SUGGESTIONS_TOOL_TIP, suggestionsLength < 5);
    }
    if (fields[5] && (fields[0][0] === "A" || fields[0][0] === "T")) {
      let suggestions = findSuggestions(
        fields[5][0],
        state.avaliableSuggestions.data["units"]
      );
      let suggestionsLength = suggestions ? suggestions.length : 0;
      commit(types.SAVE_SUGGESTIONS, suggestions);
      commit(ui.SHOW_SUGGESTIONS_LIST, suggestionsLength >= 5);
      commit(ui.SHOW_SUGGESTIONS_TOOL_TIP, suggestionsLength < 5);
    }
  }
};
const mutations = {
  [types.REQUEST_AVAILABLE_SUGGESTIONS](state) {
    state.avaliableSuggestions.isFetching = true;
    state.avaliableSuggestions.fetched = false;
    state.avaliableSuggestions.didInvalidate = false;
  },
  [types.RECEIVED_AVAILABLE_SUGGESTIONS](state, data) {
    state.avaliableSuggestions.data = data;
    state.avaliableSuggestions.isFetching = false;
    state.avaliableSuggestions.fetched = true;
    state.avaliableSuggestions.didInvalidate = false;
  },
  [types.AVAILABLE_SUGGESTIONS_FAILURE](state) {
    state.avaliableSuggestions.isFetching = false;
    state.avaliableSuggestions.fetched = false;
    state.avaliableSuggestions.didInvalidate = true;
  },
  [types.SAVE_SUGGESTIONS](state, data) {
    state.shortlistedSuggestions = data;
  }
};
const getters = {
  getSuggestions(state, getters, rootState) {
    return state.shortlistedSuggestions;
  }
};

export default {
  state,
  actions,
  mutations,
  getters
};
