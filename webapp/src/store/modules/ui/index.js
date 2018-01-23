/* eslint-disable */
import _ from 'lodash';
import * as types from './mutation-types';
import * as api from '@/models/api';
export const state = {
  kit: {},
  currentPayloadOptions: null,
  payloadTypeDropDown: [
    {
      text: 'Strain Count',
      value: 'Strain Count',
    },
    {
      text: 'Strain',
      value: 'Strain',
    },
    {
      text: 'Dilution Factor',
      value: 'Dilution Factor',
    },
    {
      text: 'PA Primers',
      value: 'PA Primers',
    },
    {
      text: 'ID-Primers',
      value: 'ID-Primers',
    },
    {
      text: 'HgDNA',
      value: 'HgDNA',
    },
  ],
  patternDropDown: [
    {
      text: 'AAAA BBBB CCCC',
      value: 'In Blocks',
    },
    {
      text: 'ABCD ABCD ABCD',
      value: 'Consecutive',
    },
  ],
};

const actions = {};
const mutations = {
  [types.SET_PRIMER_KIT](state, data) {
    state.kit['ID-Primers'] = data.id_primers;
    state.kit['PA Primers'] = data.pa_primers;
  },
  [types.SET_STRAIN_KIT](state, data) {
    state.kit.Strain = data.strains;
  },
  [types.SET_PAYLOAD_OPTIONS](state, arg) {
    state.currentPayloadOptions = state.kit[arg].map(x => {
      return { text: x.display_name, value: x.display_name };
    });
  },
};
const getters = {
  getCurrentPayloadOptions(state, getters, rootState) {
    return state.currentPayloadOptions;
  },
  getPatternDropDown() {
    return state.patternDropDown;
  },
  getPayloadTypeDropDown() {
    return state.payloadTypeDropDown;
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
