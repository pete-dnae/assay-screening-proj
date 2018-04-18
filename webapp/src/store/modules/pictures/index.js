/* eslint-disable */
import _ from "lodash";
import * as types from "./mutation-types";
import * as api from "@/models/api";
import * as ui from "../ui/mutation-types";
import { findSuggestions } from "@/models/editor2.0.js";

export const state = {
  experimentImages:{
    data:null,
    didInvalidate:false,
    fetched:false,
    isFetching:false
  }
};

const actions = {
  fetchExperimentImages({commit},experimentId){
    commit(types.REQUEST_EXPERIMENT_IMAGES);
    api
      .getExperimentImages(experimentId)
      .then(res => {
        commit(types.RECEIVED_EXPERIMENT_IMAGES, res.experimentImages.results);
      })
      .catch(e => {
        commit(types.EXPERIMENT_IMAGES_FAILURE);                
      });
  }
};
const mutations = {
  [types.REQUEST_EXPERIMENT_IMAGES](state) {
    state.experimentImages.isFetching = true;
    state.experimentImages.fetched = false;
    state.experimentImages.didInvalidate = false;
  },
  [types.RECEIVED_EXPERIMENT_IMAGES](state, data) {
    state.experimentImages.data = data;
    state.experimentImages.isFetching = false;
    state.experimentImages.fetched = true;
    state.experimentImages.didInvalidate = false;
  },
  [types.EXPERIMENT_IMAGES_FAILURE](state) {
    state.experimentImages.isFetching = false;
    state.experimentImages.fetched = false;
    state.experimentImages.didInvalidate = true;
  }, 
};
const getters = {
  getExperimentImages(state, getters, rootState) {
    return state.experimentImages.data;
  }
};

export default {
  state,
  actions,
  mutations,
  getters
};
