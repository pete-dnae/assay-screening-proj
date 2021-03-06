/* eslint-disable */
import _ from "lodash";
import * as types from "./mutation-types";
import * as api from "@/models/api";
import experiment from "@/assets/json/response.json";
import * as ui from "../ui/mutation-types";
import { getMaxRowCol, getMaxRowColPlate } from "@/models/editor2.0";
import { formatText, getReagentAllocationDict } from "@/models/visualizer.js";

export const state = {
  experimentList: {
    data: null,
    isRequesting: false,
    received: false,
    didInvalidate: false
  },
  savedScript: null,
  ruleScript: {
    referenceExperiment: {
      data: {
        interpretationResults: { lnums: null, parseError: null, table: null },
        text: null
      },
      maxCol: null,
      maxRow: null,
      plateBoundaries: null
    },
    currentExperiment: {
      data: {
        interpretationResults: { lnums: null, parseError: null, table: null },
        text: null
      },
      maxCol: null,
      maxRow: null,
      plateBoundaries: null
    },
    isPosting: false,
    isRequesting: false,
    received: false,
    posted: false,
    didInvalidate: false
  },
  experiment: {
    referenceExperiment: { data: null },
    currentExperiment: { data: { id: null }, name: null },
    isRequesting: false,
    received: false,
    didInvalidate: false
  },
  quillOptions: { debug: "warn", modules: { toolbar: false }, theme: "snow" }
};
const actions = {
  saveToDb({ commit, dispatch }, { text }) {
    commit(types.REQUEST_PUT_RULE_SCRIPT);
    commit(types.SAVE_SCRIPT, text);
    return new Promise(function(resolve, reject) {
      api
        .putRuleSCript({
          ruleScriptUrl: state.experiment.currentExperiment.data.rules_script,
          text
        })
        .then(({ data }) => {
          commit(types.PUT_RULE_SCRIPT_SUCCESS);
          delete data.text;
          commit(types.LOAD_API_RESPONSE, data);
          if (
            state.ruleScript.currentExperiment.data.interpretationResults
              .parseError === null
          )
            dispatch(
              "fetchExperimentImages",
              state.experiment.currentExperiment.data.experiment_name
            );
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
  saveExperimentAs({ commit }, args) {
    commit(types.REQUEST_POST_RULE_SCRIPT);

    return new Promise(function(resolve, reject) {
      api
        .postRuleScript({ text: state.savedScript })
        .then(({ data }) => {
          commit(types.POST_RULE_SCRIPT_SUCCESS);
          commit(types.REQUEST_POST_NEW_EXPERIMENT);
          debugger;
          api
            .postNewExperiment({
              ...args,
              rules_script: data.url
            })
            .then(({ data }) => {
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
  fetchExperiment(
    { commit, dispatch },
    { experimentName, referenceExperimentFlag = false }
  ) {
    commit(types.REQUEST_EXPERIMENT);
    return new Promise(function(resolve, reject) {
      api
        .getExperiment(experimentName)
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
                if (
                  state.ruleScript.currentExperiment.data.interpretationResults
                    .parseError === null
                )
                  dispatch(
                    "fetchExperimentImages",
                    state.experiment.currentExperiment.data.experiment_name
                  );
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
    state.ruleScript.currentExperiment.data = Object.assign(
      state.ruleScript.currentExperiment.data,
      response
    );
  },
  [types.LOAD_API_RESPONSE_REF_EXP](state, response) {
    state.ruleScript.referenceExperiment.data = response;
  },
  [types.SET_MAX_ROW_COL](state, currentOrReferenceFlag) {
    state.ruleScript[
      currentOrReferenceFlag
    ].plateBoundaries = getMaxRowColPlate(
      state.ruleScript[currentOrReferenceFlag].data.interpretationResults.table
    );
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
  getRuleIsScriptSaving(state, getters, rootState) {
    return state.ruleScript.isPosting;
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
  },
  getExperimentId(state, getters, rootState) {
    return state.experiment.currentExperiment.name;
  },
  getPlateBoundaries(state, getters, rootState) {
    return state.ruleScript.currentExperiment.plateBoundaries;
  }
};

export default {
  state,
  actions,
  mutations,
  getters
};
