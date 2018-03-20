/* eslint-disable */
import _ from 'lodash';
import * as types from './mutation-types';
import * as api from '@/models/api';
import experiment from '@/assets/json/response.json';
import { makeFeedback } from '@/models/editor';

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
  currentPlate: null,
  parsedPlates: [],
  info: null,
  version: 1,
  validScript: null,
  allocation: null,
  error: null,
  versionStatisfied: false,
  suggestions: [],
  savedScript: null,
  ruleScript: {
    data: [],
    isPosting: false,
    posted: false,
    didInvalidate: false,
  },
  quillOptions: {
    debug: 'warn',
    modules: {
      toolbar: '#toolbar',
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
        .then((res) => {
          commit(types.POST_RULE_SCRIPT_SUCCESS, res);
          resolve('success');
        })
        .catch((e) => {
          commit(types.POST_RULE_SCRIPT_FAILURE);
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
  [types.POST_RULE_SCRIPT_SUCCESS](state, response) {
    const { interpretation_results, text } = response.data;
    const { allocation, parse_error } = interpretation_results;

    state.error = parse_error;
    state.allocation = allocation;
    state.ruleScript.isPosting = false;
    state.ruleScript.posted = true;
    state.ruleScript.didInvalidate = false;
  },
  [types.POST_RULE_SCRIPT_FAILURE](state) {
    state.ruleScript.isPosting = false;
    state.ruleScript.posted = false;
    state.ruleScript.didInvalidate = true;
  },
  [types.SET_CURRENT_PLATE_FROM_SCRIPT](state, value) {
    state.currentPlate = value;
  },
  [types.SAVE_SCRIPT](state, scriptText) {
    state.validScript = scriptText;
  },

  [types.LOG_ERROR](state, data) {
    state.error = data;
  },
  [types.CLEAR_ERROR](state) {
    state.error = null;
  },
  [types.SET_PARSED_PLATE](state, value) {
    state.parsedPlates.push(value);
  },
  [types.SET_SUGGESTIONS](state, value) {
    state.suggestions = value;
  },
  [types.CLEAR_SUGGESTIONS](state) {
    state.suggestions = [];
  },
  [types.CLEAR_PARSED_PLATE](state) {
    state.parsedPlates = [];
  },
  [types.SET_VALID_SCRIPT](state, data) {
    state.savedScript = data;
  },
  [types.SET_VERSION_VERIFIED](state, value) {
    state.versionStatisfied = value;
  },
  [types.ADD_REAGENT](state, value) {
    state.reagents.push(value);
  },
};
const getters = {
  getVersionVerified(state, getters, rootState) {
    return state.versionStatisfied;
  },
  getQuillOptions(state, getters, rootState) {
    return state.quillOptions;
  },
  getVersion(state, getters, rootState) {
    return state.version;
  },
  getError(state, getters, rootState) {
    return state.error;
  },
  getParsedPlates(state, getters, rootState) {
    return state.parsedPlates;
  },
  getReagents(state, getters, rootState) {
    return state.reagents;
  },
  getUnits(state, getters, rootState) {
    return state.units;
  },
  getCurrentPlate(state, getters, rootState) {
    return state.currentPlate;
  },
  getSuggestions(state, getters, rootState) {
    return state.suggestions;
  },
  getRuleIsScriptSaving(state, getters, rootState) {
    return state.ruleScript.isPosting;
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
