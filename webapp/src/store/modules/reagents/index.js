/* eslint-disable */
import * as api from "@/models/api";
import * as types from "./mutation-types";
import * as ui from "../ui/mutation-types";
import _ from "lodash";

export const state = {
  reagents: {
    data: null,
    isFetching: false,
    fetched: false,
    didInvalidate: false,
    isPosting: false,
    posted: false,
    isDeleting: false,
    deleted: false,
    isPutting:false,
    put:false
  },
  errors:{
    data:null
  },
  units: { data: null, isFetching: false, fetched: false, didInvalidate: false }
};

const actions = {
  fetchReagents({ commit }) {
    commit(types.REQUEST_REAGENTS);
    return new Promise((resolve, reject) => {
      api
        .getReagents()
        .then(res => {
          commit(types.RECEIVED_REAGENTS, res);
          resolve("success");
        })
        .catch(e => {
          reject(e);
          commit(ui.SHOW_BLUR);
          commit(types.REAGENTS_FAILURE);
        });
    });
  },
  addReagent({ commit },data) {
    commit(types.REQUEST_REAGENT_ADD);
    return new Promise((resolve, reject) => {
      api
        .addReagent(data)
        .then(res => {          
          commit(types.REAGENT_ADD_SUCCESS);
          resolve("success");
        },({response:{data}})=>{
          
          commit(types.ADD_ERROR_MESSAGE, data);
        })
        .catch(e => {
          reject(e);
          commit(ui.SHOW_BLUR);
          commit(types.REAGENT_ADD_FAILURE);
        });
    });
  },
  removeReagent({ commit },reagentName) {
    commit(types.REQUEST_REAGENT_REMOVE);
    return new Promise((resolve, reject) => {
      api
        .removeReagent(reagentName)
        .then(
          res => {
            commit(types.REAGENT_REMOVE_SUCCESS);
            resolve("success");
          },
          ({ response: { data } })=>{
            commit(types.ADD_ERROR_MESSAGE, data);
          }
        )
        .catch(e => {
          reject(e);
          commit(ui.SHOW_BLUR);
          commit(types.REAGENT_REMOVE_FAILURE);
        });
    });
  },
  editReagent({ commit },args) {
    commit(types.REQUEST_REAGENT_EDIT);
    return new Promise((resolve, reject) => {
      api
        .editReagent(args)
        .then(
          res => {
            commit(types.REAGENT_EDIT_SUCCESS);
            resolve("success");
          },
          ({ response: { data } })=>{
            commit(types.ADD_ERROR_MESSAGE, data);
          }
        )
        .catch(e => {
          reject(e);
          commit(ui.SHOW_BLUR);
          commit(types.REAGENT_EDIT_FAILURE);
        });
    });
  },
  fetchUnits({ commit }) {
    commit(types.REQUEST_UNITS);
    return new Promise((resolve, reject) => {
      api
        .getUnits()
        .then(res => {
          commit(types.RECEIVED_UNITS, res);
          resolve("success");
        })
        .catch(e => {
          reject(e);
          commit(ui.SHOW_BLUR);
          commit(types.UNITS_FAILURE);
        });
    });
  }
};
const mutations = {
  [types.REQUEST_REAGENTS](state) {
    state.reagents.isFetching = true;
    state.reagents.fetched = false;
    state.reagents.didInvalidate = false;
  },
  [types.RECEIVED_REAGENTS](state, data) {
    state.reagents.data = data;
    state.reagents.isFetching = false;
    state.reagents.fetched = true;
    state.reagents.didInvalidate = false;
  },
  [types.REAGENTS_FAILURE](state) {
    state.reagents.isFetching = false;
    state.reagents.fetched = false;
    state.reagents.didInvalidate = true;
  },
  [types.REQUEST_REAGENT_ADD](state) {
    state.reagents.isPosting = true;
    state.reagents.posted = false;
    state.reagents.didInvalidate = false;
  },
  [types.REAGENT_ADD_SUCCESS](state) {    
    state.reagents.isPosting = false;
    state.reagents.posted = true;
    state.reagents.didInvalidate = false;
  },
  [types.REAGENT_ADD_FAILURE](state) {
    state.reagents.isPosting = false;
    state.reagents.posted = false;
    state.reagents.didInvalidate = true;
  },
  [types.REQUEST_REAGENT_REMOVE](state) {
    state.reagents.isDeleting = true;
    state.reagents.deleted = false;
    state.reagents.didInvalidate = false;
  },
  [types.REAGENT_REMOVE_SUCCESS](state) {    
    state.reagents.isDeleting = false;
    state.reagents.deleted = true;
    state.reagents.didInvalidate = false;
  },
  [types.REAGENT_REMOVE_FAILURE](state) {
    state.reagents.isDeleting = false;
    state.reagents.deleted = false;
    state.reagents.didInvalidate = true;
  },
  [types.REQUEST_REAGENT_EDIT](state) {
    state.reagents.isPutting = true;
    state.reagents.put = false;
    state.reagents.didInvalidate = false;
  },
  [types.REAGENT_EDIT_SUCCESS](state) {    
    state.reagents.isPutting = false;
    state.reagents.put = true;
    state.reagents.didInvalidate = false;
  },
  [types.REAGENT_EDIT_FAILURE](state) {
    state.reagents.isPutting = false;
    state.reagents.put = false;
    state.reagents.didInvalidate = true;
  },
  [types.REQUEST_UNITS](state) {
    state.units.isFetching = true;
    state.units.fetched = false;
    state.units.didInvalidate = false;
  },
  [types.RECEIVED_UNITS](state, data) {
    state.units.data = data;
    state.units.isFetching = false;
    state.units.fetched = true;
    state.units.didInvalidate = false;
  },
  [types.UNITS_FAILURE](state) {
    state.units.isFetching = false;
    state.units.fetched = false;
    state.units.didInvalidate = true;
  },
  [types.ADD_ERROR_MESSAGE](state,data){
    state.errors.data = data
  }
};
const getters = {
  getReagents(state, getters, rootState) {
    return state.reagents.data;
  },
  getUnits(state, getters, rootState) {
    return state.units.data;
  },
  getReagentErrors(state, getters, rootState) {
    return state.errors.data;
  }
};

export default {
  state,
  actions,
  mutations,
  getters
};
