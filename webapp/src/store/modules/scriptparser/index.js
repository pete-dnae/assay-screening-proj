/* eslint-disable */
import _ from 'lodash';
import * as types from './mutation-types';
import * as api from '@/models/api';
import experiment from '@/assets/json/response.json';
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
  ],
  units: ['mM', 'mg/ml', 'mMeach', 'copies', 'uM', 'ng', 'x', 'dil'],
  currentPlate: null,
  parsedPlates: [],
  version: 0.1,
  validTextObjects: [],
  invalidTextObjects: [],
  errorMessages: [],
  savedScript: null,
  quillOptions: {
    debug: 'warn',
    modules: {
      toolbar: [
        [{ header: [1, 2, false] }],
        ['bold', 'italic', 'underline'],
        ['image', 'code-block'],
      ],
    },

    theme: 'snow',
  },
};

const actions = {
  setFeedback({ commit }, data) {
    const pos = data.filter((x) => x.pass);
    const neg = data.filter((x) => !x.pass);
    commit(types.SET_VALID_OBJECTS, pos);
    commit(types.SET_INVALID_OBJECTS, neg);
  },
};
const mutations = {
  [types.SET_CURRENT_PLATE](state, value) {
    state.currentPlate = value;
  },
  [types.SET_VALID_OBJECTS](state, data) {
    state.validTextObjects = data;
  },
  [types.SET_INVALID_OBJECTS](state, data) {
    state.invalidTextObjects = data;
  },
  [types.SET_PARSED_PLATE](state, value) {
    state.parsedPlates.push(value);
  },
};
const getters = {
  getQuillOptions(state, getters, rootState) {
    return state.quillOptions;
  },
  getVersion(state, getters, rootState) {
    return state.version;
  },
  getValidTextObjects(state, getters, rootState) {
    return state.validTextObjects;
  },
  getInValidTextObjects(state, getters, rootState) {
    return state.invalidTextObjects;
  },
  getErrorMessages(state, getters, rootState) {
    return state.errorMessages;
  },
  getparsedPlates(state, getters, rootState) {
    return state.parsedPlates;
  },
  getreagents(state, getters, rootState) {
    return state.reagents;
  },
  getunits(state, getters, rootState) {
    return state.units;
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
