/* eslint-disable */
import _ from 'lodash';
import * as types from './mutation-types';
import * as api from '@/models/api';
import experiment from '@/assets/json/response.json';

import { getMaxRowCol } from '@/models/editor2.0';

export const state = {
  reagents: [
    'DNA-free-Water',
    'Titanium-PCR-Buffer',
    'KCl',
    'MgCl2',
    'BSA',
    'dNTPs',
    'Titanium-Taq',
    '(Eco)-ATCC-BAA-2355',
    '(Efs-vanB)-ATCC-700802',
    '(Kox)-ATCC-15764',
    'Ec_uidA_6.x_Eco63_Eco60',
    'Efs_cpn60_1.x_Efs04_Efs01',
    'Efs_vanB_1.x_van10_van06',
    'Efm_vanA_1.x_van05_van01',
    'Ko_pehX_1.x_Kox05_Kox02',
    'Kp_khe_2.x_Kpn13_Kpn01',
    'Pm_zapA_1.x_Pmi01_Pmi05',
    'Spo_gp_1.x_Spo09_Spo13',
    'HgDna',
    'Triton',
    'SYBRgreen',
    'KOH',
    'Ec_uidA_x.2_Eco64_Eco66',
    'Efs_cpn60_x.1_Efs03_Efs02',
    'Efs_vanB_x.3_van30_van33',
    'Efm_vanA_x.1_van04_van02',
    'Ko_pehX_x.1_Kox04_Kox03',
    'Kp_khe_x.1_Kpn03_Kpn02',
    'Pm_zapA_x.1_Pmi02_Pmi03',
    'Spo_gp_x.1_Spo03_Spo05',
  ],
  units: ['mM', 'mg/ml', 'mMeach', 'copies', 'uM', 'ng', 'x', 'dil', '%'],
  maxRow: null,
  maxCol: null,
  suggestions: [],
  savedScript: null,
  ruleScript: {
    data: {
      interpretationResults: { lnums: null, parseError: null, table: null },
      text: null,
    },
    isPosting: false,
    isRequesting: false,
    received: false,
    posted: false,
    didInvalidate: false,
  },
  experiment: {
    data: null,
    isRequesting: false,
    received: false,
    didInvalidate: false,
  },
  quillOptions: {
    debug: 'warn',
    modules: {
      toolbar: false,
    },
    theme: 'snow',
  },
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
          resolve('success');
        })
        .catch((e) => {
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
        .then((res) => {
          commit(types.EXPERIMENT_SUCCESS, res);
          api
            .getRuleScript(res.rules_script)
            .then((res) => {
              commit(types.RULE_SCRIPT_SUCCESS);
              commit(types.LOAD_API_RESPONSE, res);

              resolve('success');
            })
            .catch((e) => {
              commit(types.RULE_SCRIPT_FAILURE);
              reject(e);
            });
        })
        .catch((e) => {
          commit(types.EXPERIMENT_FAILURE);
          reject(e);
        });
    });
  },
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
      text,
    } = response;

    [state.maxRow, state.maxCol] = lnums ? getMaxRowCol(lnums) : [0, 0];
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
  },
};
const getters = {
  getQuillOptions(state, getters, rootState) {
    return state.quillOptions;
  },
  getError(state, getters, rootState) {
    return state.ruleScript.data.interpretationResults.parseError;
  },
  getReagents(state, getters, rootState) {
    return state.reagents;
  },
  getUnits(state, getters, rootState) {
    return state.units;
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
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
