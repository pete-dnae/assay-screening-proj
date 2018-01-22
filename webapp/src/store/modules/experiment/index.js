/* eslint-disable */
import _ from 'lodash';
import * as types from './mutation-types';
import * as api from '@/models/api';
import experiment from '@/assets/json/response.json';
export const state = {
  currentExperiment: {
    data: {
      designer_name: '',
      experiment_name: '',
    },
    isFetching: false,
    fetched: false,
    didInvalidate: false,
  },
};

const actions = {
  fetchExperiment({ commit }, args) {
    commit(types.REQUEST_EXPERIMENT);
    return new Promise(function(resolve, reject) {
      api
        .getExperiment(args)
        .then(data => {
          commit(types.RECEIVED_EXPERIMENT, data);
          resolve(data);
        })
        .catch(e => {
          commit(types.EXPERIMENT_FAILURE);
          reject(data);
        });
    });
  },
};
const mutations = {
  [types.REQUEST_EXPERIMENT](state, plateId) {
    state.currentExperiment.isFetching = true;
    state.currentExperiment.fetched = false;
    state.currentExperiment.didInvalidate = false;
  },
  [types.RECEIVED_EXPERIMENT](state, data) {
    state.currentExperiment.data = data;
    state.currentExperiment.isFetching = false;
    state.currentExperiment.fetched = true;
    state.currentExperiment.didInvalidate = false;
  },
  [types.EXPERIMENT_FAILURE](state, plateId) {
    state.currentExperiment.isFetching = false;
    state.currentExperiment.fetched = false;
    state.currentExperiment.didInvalidate = true;
  },
};
const getters = {
  getDesignerName(state, getters, rootState) {
    return state.currentExperiment.data.designer_name;
  },
  getExperimentName() {
    return state.currentExperiment.data.experiment_name;
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
