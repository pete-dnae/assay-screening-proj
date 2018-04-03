/* eslint-disable */
import _ from "lodash";
import * as types from "./mutation-types";
import * as api from "@/models/api";
import experiment from "@/assets/json/response.json";
import * as ui from "../ui/mutation-types";
import { getMaxRowCol } from "@/models/editor2.0";
import { formatText } from "@/models/visualizer.js";

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
  experimentList: {
    data: null,
    isRequesting: false,
    received: false,
    didInvalidate: false
  },
  suggestions: [],
  savedScript: null,
  ruleScript: {
    referenceExperiment: {
      data: {
        interpretationResults: { lnums: null, parseError: null, table: null },
        text: null
      },
      maxCol: null,
      maxRow: null
    },
    currentExperiment: {
      data: {
        interpretationResults: { lnums: null, parseError: null, table: null },
        text: null
      },
      maxCol: null,
      maxRow: null
    },
    isPosting: false,
    isRequesting: false,
    received: false,
    posted: false,
    didInvalidate: false
  },
  experiment: {
    referenceExperiment: {
      data: null
    },
    currentExperiment: {
      data: null,
      name: null
    },
    isRequesting: false,
    received: false,
    didInvalidate: false
  },
  quillOptions: { debug: "warn", modules: { toolbar: false }, theme: "snow" }
};
const actions = {
  saveToDb({ commit }, { ruleScriptNo, text }) {
    commit(types.REQUEST_PUT_RULE_SCRIPT);
    commit(types.SAVE_SCRIPT, text);
    return new Promise(function(resolve, reject) {
      api
        .putRuleSCript({ ruleScriptNo, text })
        .then(({ data }) => {
          commit(types.PUT_RULE_SCRIPT_SUCCESS);
          commit(types.LOAD_API_RESPONSE, data);
          commit(types.SET_MAX_ROW_COL, "currentExperiment");
          resolve("success");
        })
        .catch(e => {
          commit(types.PUT_RULE_SCRIPT_FAILURE);
          commit(ui.SHOW_BLUR);
          reject(e);
        });
    });
  },
  saveExperimentAs({ commit }, experimentName) {
    commit(types.REQUEST_POST_RULE_SCRIPT);
    
    return new Promise(function(resolve, reject) {
      api
        .postRuleScript({text:state.savedScript})
        .then(({data}) => {          
          commit(types.POST_RULE_SCRIPT_SUCCESS);
          commit(types.REQUEST_POST_NEW_EXPERIMENT);
              
          api
            .postNewExperiment(              
              {
                experiment_name: experimentName,
                rules_script: data.url
              }
            )
            .then(({data}) => {
              resolve(data);
              commit(types.POST_NEW_EXPERIMENT_SUCCESS);
            })
            .catch(e => {
              commit(types.POST_NEW_EXPERIMENT_FAILURE);
              commit(ui.SHOW_BLUR);
              reject(e);
            });
        })
        .catch(e => {
          commit(types.POST_RULE_SCRIPT_FAILURE);
          commit(ui.SHOW_BLUR);
          reject(e);
        });
    });
  },
  fetchExperimentList({ commit }) {
    commit(types.REQUEST_EXPERIMENT_LIST);
    return new Promise(function(resolve, reject) {
      api
        .getExperimentList()
        .then(res => {
          commit(types.EXPERIMENT_LIST_SUCCESS, res);
          resolve("success");
        })
        .catch(e => {
          reject(e);
          commit(ui.SHOW_BLUR);
          commit(types.EXPERIMENT_LIST_FAILURE);
        });
    });
  },
  fetchExperiment({ commit }, { exptNo, referenceExperimentFlag = false }) {
    commit(types.REQUEST_EXPERIMENT);
    return new Promise(function(resolve, reject) {
      api
        .getExperiment(exptNo)
        .then(res => {
          commit(types.EXPERIMENT_SUCCESS, res);
          api
            .getRuleScript(res.rules_script)
            .then(res => {
              commit(types.RULE_SCRIPT_SUCCESS);
              if (referenceExperimentFlag) {
                commit(types.LOAD_API_RESPONSE_REF_EXP, res);
                commit(types.SET_MAX_ROW_COL, "referenceExperiment");
              } else {
                commit(types.LOAD_API_RESPONSE, res);
                commit(types.SAVE_SCRIPT, res.text);
                commit(types.SET_MAX_ROW_COL, "currentExperiment");
              }
              resolve("success");
            })
            .catch(e => {
              commit(types.RULE_SCRIPT_FAILURE);
              commit(ui.SHOW_BLUR);
              reject(e);
            });
        })
        .catch(e => {
          commit(types.EXPERIMENT_FAILURE);
          commit(ui.SHOW_BLUR);
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
          resolve("success");
        })
        .catch(e => {
          reject(e);
          commit(ui.SHOW_BLUR);
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
          commit(ui.SHOW_BLUR);
          commit(types.REQUEST_UNITS_FAILURE);
        });
    });
  }
};
const mutations = {
  [types.REQUEST_PUT_RULE_SCRIPT](state) {
    state.ruleScript.isPosting = true;
    state.ruleScript.posted = false;
    state.ruleScript.didInvalidate = false;
  },
  [types.PUT_RULE_SCRIPT_SUCCESS](state) {
    state.ruleScript.isPosting = false;
    state.ruleScript.posted = true;
    state.ruleScript.didInvalidate = false;
  },
  [types.LOAD_API_RESPONSE](state, response) {
    state.ruleScript.currentExperiment.data = response;
  },
  [types.LOAD_API_RESPONSE_REF_EXP](state, response) {
    state.ruleScript.referenceExperiment.data = response;
  },
  [types.SET_MAX_ROW_COL](state, currentOrReferenceFlag) {
    const lnums =
      state.ruleScript[currentOrReferenceFlag].data.interpretationResults.lnums;
    [
      state.ruleScript[currentOrReferenceFlag].maxRow,
      state.ruleScript[currentOrReferenceFlag].maxCol
    ] = lnums ? getMaxRowCol(lnums) : [0, 0];
  },
  [types.PUT_RULE_SCRIPT_FAILURE](state) {
    state.ruleScript.isPosting = false;
    state.ruleScript.posted = false;
    state.ruleScript.didInvalidate = true;
  },
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
    state.experiment.currentExperiment.name = response.experiment_name;
    state.experiment.currentExperiment.data = response;
    state.experiment.isRequesting = false;
    state.experiment.received = true;
    state.experiment.didInvalidate = false;
  },
  [types.EXPERIMENT_FAILURE](state) {
    state.experiment.isRequesting = false;
    state.experiment.received = false;
    state.experiment.didInvalidate = true;
  },
  [types.REQUEST_POST_NEW_EXPERIMENT](state) {
    state.experiment.isRequesting = true;
    state.experiment.received = false;
    state.experiment.didInvalidate = false;
  },
  [types.POST_NEW_EXPERIMENT_SUCCESS](state, response) {
    state.experiment.isRequesting = false;
    state.experiment.received = true;
    state.experiment.didInvalidate = false;
  },
  [types.POST_NEW_EXPERIMENT_FAILURE](state) {
    state.experiment.isRequesting = false;
    state.experiment.received = false;
    state.experiment.didInvalidate = true;
  },
  [types.REQUEST_EXPERIMENT_LIST](state) {
    state.experimentList.isRequesting = true;
    state.experimentList.received = false;
    state.experimentList.didInvalidate = false;
  },
  [types.EXPERIMENT_LIST_SUCCESS](state, response) {
    state.experimentList.data = response;
    state.experimentList.isRequesting = false;
    state.experimentList.received = true;
    state.experimentList.didInvalidate = false;
  },
  [types.EXPERIMENT_LIST_FAILURE](state) {
    state.experimentList.isRequesting = false;
    state.experimentList.received = false;
    state.experimentList.didInvalidate = true;
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
    state.savedScript = scriptText;
  },
  [types.SET_SUGGESTIONS](state, value) {
    state.suggestions = value;
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
    return state.ruleScript.currentExperiment.data.interpretationResults
      .parseError;
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
  getTableRowCount(state, getters, rootState) {
    return state.ruleScript.currentExperiment.maxRow;
  },
  getTableColCount(state, getters, rootState) {
    return state.ruleScript.currentExperiment.maxCol;
  },
  getAllocationMap(state, getters, rootState) {
    return state.ruleScript.currentExperiment.data.interpretationResults.lnums;
  },
  getRuleScript(state, getters, rootState) {
    return state.ruleScript.currentExperiment.data.text;
  },
  getAllocationData(state, getters, rootState) {
    return state.ruleScript.currentExperiment.data.interpretationResults.table;
  },
  getExperimentList(state, getters, rootState) {
    return state.experimentList.data;
  },
  getCurrentExperiment(state, getters, rootState) {
    return state.experiment.currentExperiment.name;
  },
  getReferenceExperiment(state, getters, rootState) {
    return state.ruleScript.referenceExperiment.data.text;
  }
};

export default {
  state,
  actions,
  mutations,
  getters
};
