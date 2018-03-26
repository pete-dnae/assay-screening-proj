/* eslint-disable */
import _ from "lodash";
import * as types from "./mutation-types";
import * as api from "@/models/api";
import experiment from "@/assets/json/response.json";

import { getMaxRowCol } from "@/models/editor2.0";

export const state = {
  reagents: {
    data: null,
    isRequesting: false,
    received: false,
    didInvalidate: false
  },
  units: {
    data: null,
    isRequesting: false,
    received: false,
    didInvalidate: false
  },
  maxRow: null,
  maxCol: null,
  suggestions: [],
  savedScript: null,
  ruleScript: {
    data: {
      interpretationResults: { lnums: null, parseError: null, table: null },
      text: null
    },
    isPosting: false,
    isRequesting: false,
    received: false,
    posted: false,
    didInvalidate: false
  },
  experiment: {
    data: null,
    isRequesting: false,
    received: false,
    didInvalidate: false
  },
  quillOptions: { debug: "warn", modules: { toolbar: false }, theme: "snow" }
};
const actions = {
  saveToDb({ commit }, { ruleScriptNo, text }) {
    commit(types.REQUEST_POST_RULE_SCRIPT);
    commit(types.SAVE_SCRIPT, text);
    return new Promise(function(resolve, reject) {
      api
        .postRuleSCript({ ruleScriptNo, text })
        .then(({ data }) => {
          commit(types.POST_RULE_SCRIPT_SUCCESS);
          commit(types.LOAD_API_RESPONSE, data);
          resolve("success");
        })
        .catch(e => {
          commit(types.POST_RULE_SCRIPT_FAILURE);
          reject(e);
        });
    });
  },
  fetchExperiment({ commit }, expNo) {
    commit(types.REQUEST_EXPERIMENT);
    return new Promise(function(resolve, reject) {
      api
        .getExperiment(expNo)
        .then(res => {
          commit(types.EXPERIMENT_SUCCESS, res);
          api
            .getRuleScript(res.rules_script)
            .then(res => {
              commit(types.RULE_SCRIPT_SUCCESS);
              commit(types.LOAD_API_RESPONSE, res);

              resolve("success");
            })
            .catch(e => {
              commit(types.RULE_SCRIPT_FAILURE);
              reject(e);
            });
        })
        .catch(e => {
          commit(types.EXPERIMENT_FAILURE);
          reject(e);
        });
    });
  },
  fetchReagentList({ commit }) {
    commit(types.REQUEST_REAGENTS);
    return new Promise(function(resolve, reject) {
      api
        .getReagents()
        .then(res => {
          commit(types.REAGENTS_RECEIVED, res);
          resolve('success')
        })
        .catch(e => {
          reject(e);
          commit(types.REQUEST_REAGENTS_FAILURE);
        });
    });
  },
  fetchUnitList({ commit }) {
    commit(types.REQUEST_UNITS);
    return new Promise(function(resolve, reject) {
      api
        .getUnits()
        .then(res => {
          commit(types.UNITS_RECEIVED, res);
          resolve("success");
        })
        .catch(e => {
          reject(e);
          commit(types.REQUEST_UNITS_FAILURE);
        });
    });
  }
};
const mutations = {
  [types.REQUEST_POST_RULE_SCRIPT](state) {
    state.ruleScript.isPosting = true;
    state.ruleScript.posted = false;
    state.ruleScript.didInvalidate = false;
  },
  [types.POST_RULE_SCRIPT_SUCCESS](state) {
    state.ruleScript.isPosting = false;
    state.ruleScript.posted = true;
    state.ruleScript.didInvalidate = false;
  },
  [types.LOAD_API_RESPONSE](state, response) {
    state.ruleScript.data = response;
    const {
      interpretationResults: { lnums, parseError, table },
      text
    } = response;

    [state.maxRow, state.maxCol] = lnums ? getMaxRowCol(lnums) : [0, 0];
  },
  [types.POST_RULE_SCRIPT_FAILURE](state) {
    state.ruleScript.isPosting = false;
    state.ruleScript.posted = false;
    state.ruleScript.didInvalidate = true;
  },
  [types.REQUEST_REAGENTS](state) {
    state.reagents.isPosting = true;
    state.reagents.posted = false;
    state.reagents.didInvalidate = false;
  },
  [types.REAGENTS_RECEIVED](state, data) {
    state.reagents.data = data;
    state.reagents.isPosting = false;
    state.reagents.posted = true;
    state.reagents.didInvalidate = false;
  },
  [types.REQUEST_REAGENTS_FAILURE](state) {
    state.reagents.isPosting = false;
    state.reagents.posted = false;
    state.reagents.didInvalidate = true;
  },
  [types.REQUEST_UNITS](state) {
    state.units.isPosting = true;
    state.units.posted = false;
    state.units.didInvalidate = false;
  },
  [types.UNITS_RECEIVED](state, data) {
    state.units.data = data;
    state.units.isPosting = false;
    state.units.posted = true;
    state.units.didInvalidate = false;
  },
  [types.REQUEST_UNITS_FAILURE](state) {
    state.units.isPosting = false;
    state.units.posted = false;
    state.units.didInvalidate = true;
  },
  [types.REQUEST_EXPERIMENT](state) {
    state.experiment.isRequesting = true;
    state.experiment.received = false;
    state.experiment.didInvalidate = false;
  },
  [types.EXPERIMENT_SUCCESS](state, response) {
    state.experiment.data = response;
    state.experiment.isRequesting = false;
    state.experiment.received = true;
    state.experiment.didInvalidate = false;
  },
  [types.EXPERIMENT_FAILURE](state) {
    state.experiment.isRequesting = false;
    state.experiment.received = false;
    state.experiment.didInvalidate = true;
  },
  [types.REQUEST_RULE_SCRIPT](state) {
    state.ruleScript.isRequesting = true;
    state.ruleScript.received = false;
    state.ruleScript.didInvalidate = false;
  },
  [types.RULE_SCRIPT_SUCCESS](state) {
    state.ruleScript.isRequesting = false;
    state.ruleScript.received = true;
    state.ruleScript.didInvalidate = false;
  },
  [types.RULE_SCRIPT_FAILURE](state) {
    state.ruleScript.isRequesting = false;
    state.ruleScript.received = false;
    state.ruleScript.didInvalidate = true;
  },
  [types.SAVE_SCRIPT](state, scriptText) {
    state.validScript = scriptText;
  },
  [types.SET_SUGGESTIONS](state, value) {
    state.suggestions = value;
  },
  [types.SET_VALID_SCRIPT](state, data) {
    state.savedScript = data;
  },
  [types.ADD_REAGENT](state, value) {
    state.reagents.push(value);
  }
};
const getters = {
  getQuillOptions(state, getters, rootState) {
    return state.quillOptions;
  },
  getError(state, getters, rootState) {
    return state.ruleScript.data.interpretationResults.parseError;
  },
  getReagents(state, getters, rootState) {
    return state.reagents.data;
  },
  getUnits(state, getters, rootState) {
    return state.units.data;
  },
  getSuggestions(state, getters, rootState) {
    return state.suggestions;
  },
  getRuleIsScriptSaving(state, getters, rootState) {
    return state.ruleScript.isPosting;
  },
  getTableBoundaries(state, getters, rootState) {
    return [state.maxRow, state.maxCol];
  },
  getAllocationMap(state, getters, rootState) {
    return state.ruleScript.data.interpretationResults.lnums;
  },
  getRuleScript(state, getters, rootState) {
    return state.ruleScript.data.text;
  },
  getAllocationData(state, getters, rootState) {
    return state.ruleScript.data.interpretationResults.table;
  }
};

export default {
  state,
  actions,
  mutations,
  getters
};
