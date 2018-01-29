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
      text: 'ID Primers',
      value: 'ID Primers',
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
  rowsDropDown: [
    {
      text: 'A',
      value: 'A',
    },
    {
      text: 'B',
      value: 'B',
    },
    {
      text: 'C',
      value: 'C',
    },
    {
      text: 'D',
      value: 'D',
    },
    {
      text: 'E',
      value: 'E',
    },
    {
      text: 'F',
      value: 'F',
    },
    {
      text: 'G',
      value: 'G',
    },
    {
      text: 'H',
      value: 'H',
    },
    {
      text: 'I',
      value: 'I',
    },
    {
      text: 'J',
      value: 'J',
    },
    {
      text: 'K',
      value: 'K',
    },
  ],
  colsDropDown: [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    1,
    18,
    19,
    20,
  ],
};

const actions = {};
const mutations = {
  [types.SET_PRIMER_KIT](state, data) {
    state.kit['ID Primers'] = data.id_primers;
    state.kit['PA Primers'] = data.pa_primers;
  },
  [types.SET_STRAIN_KIT](state, data) {
    state.kit.Strain = data.strains;
  },
  [types.SET_PAYLOAD_OPTIONS](state, arg) {
    let kitProxy = new Proxy(state.kit, {
      get(Obj, prop) {
        return prop in Obj
          ? Obj[prop].map(x => {
              return { text: x.display_name, value: x.display_name };
            })
          : `userText`;
      },
    });

    state.currentPayloadOptions = kitProxy[arg];
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
  getRowsDropDown() {
    return state.rowsDropDown;
  },
  getColsDropDown() {
    return state.colsDropDown;
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
