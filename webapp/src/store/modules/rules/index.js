/* eslint-disable */
import _ from 'lodash';
import * as types from './mutation-types';
import { getRepeatedDataByColumn, getitemsByColDict } from '@/models/rules';
export const state = {
  template: {
    data: [],
  },
  hgDNA: {
    data: [],
  },
  dilution: {
    data: {},
  },
  strains: {
    data: {},
  },
  idPrimers: {
    data: {},
  },
  plate: {
    data: { templateConcentration: {}, hgDNAConcentration: {}, strains: {}, idPrimers: {} },
  },
  rowId: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
  colId: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
};

const actions = {};
const mutations = {
  [types.SET_TEMPLATE_RULES](state, data) {
    state.template.data = data;
  },
  [types.SET_HGDNA_RULES](state, data) {
    state.hgDNA.data = data;
  },
  [types.SET_TEMPLATE_PLATE](state, data) {
    state.plate.data.templateConcentration = data.reduce((acc, x) => {
      x.allRows.map(y => {
        let concList = x.concentration.split(',');
        let repeats = state.colId.length / x.blocks;

        concList =
          concList.length !== repeats
            ? concList.concat(_.times(repeats - concList.length, () => ''))
            : concList;

        acc[y] = _.times(x.blocks, () => concList).reduce((a, el) => {
          a = a.concat(el);
          return a;
        }, []);
        return acc[y];
      });
      return acc;
    }, {});
  },
  [types.SET_HGDNA_PLATE](state, data) {
    state.plate.data.hgDNAConcentration = data.reduce((acc, x) => {
      x.allRows.map(y => {
        let concList = x.concentration.split(',');
        let repeats = state.colId.length / x.blocks;
        concList =
          concList.length !== repeats
            ? concList.concat(_.times(repeats - concList.length, () => ''))
            : concList;

        acc[y] = _.times(x.blocks, () => concList).reduce((a, el) => {
          a = a.concat(el);
          return a;
        }, []);
        return acc[y];
      });
      return acc;
    }, {});
  },
  [types.SET_STRAINS](state, data) {
    state.strains.data = data;
  },
  [types.SET_ID_PRIMERS](state, data) {
    state.idPrimers.data = data;
  },
  [types.SET_STRAINS_PLATE](state, args) {
    const { blocks, data } = args;
    const repeats = state.colId.length / blocks;
    const dataByBlock = _.filter(data, 'byBlock');
    const dataByColumn = _.filter(data, x => !x.byBlock);
    const repeatedDataByColumn = getRepeatedDataByColumn(
      repeats,
      blocks,
      _.map(dataByColumn, 'Strain'),
    );
    let itemsByColDict = getitemsByColDict(repeats, state.colId, repeatedDataByColumn, dataByBlock);

    const plateDisplayByBlock = state.rowId.reduce((acc, x) => {
      acc[x] = state.colId.map(colNum => (colNum in itemsByColDict ? itemsByColDict[colNum] : ''));
      return acc;
    }, {});
    state.plate.data.strains = plateDisplayByBlock;
  },
  [types.SET_ID_PRIMERS_PLATE](state, args) {
    const { blocks, data } = args;
    const repeats = state.colId.length / blocks;
    const dataByBlock = _.filter(data, 'byBlock');
    const dataByColumn = _.filter(data, x => !x.byBlock);
    const repeatedDataByColumn = getRepeatedDataByColumn(
      repeats,
      blocks,
      _.map(dataByColumn, 'ID Primers'),
    );
    let itemsByColDict = getitemsByColDict(repeats, state.colId, repeatedDataByColumn, dataByBlock);

    const plateDisplayByBlock = state.rowId.reduce((acc, x) => {
      acc[x] = state.colId.map(colNum => (colNum in itemsByColDict ? itemsByColDict[colNum] : ''));
      return acc;
    }, {});
    state.plate.data.idPrimers = plateDisplayByBlock;
  },
};
const getters = {
  getTemplate(state, getters, rootState) {
    return state.plate.data.templateConcentration;
  },
  gethgDNA(state, getters, rootState) {
    return state.plate.data.hgDNAConcentration;
  },
  getDilution(state, getters, rootState) {
    return state.dilution.data;
  },
  getStrains(state, getters, rootState) {
    return state.plate.data.strains;
  },
  getIdPrimers(state, getters, rootState) {
    return state.plate.data.idPrimers;
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
