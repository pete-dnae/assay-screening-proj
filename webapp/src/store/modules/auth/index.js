/* eslint-disable */
import * as types from "./mutation-types";
import * as api from "@/models/api";
import * as ui from "../ui/mutation-types";
import { inspect } from "util";
import jwt_decode from "jwt-decode";
import router from "@/router";
import { stat } from "fs";

export const state = {
  jwt: {
    data: localStorage.getItem("t"),
    isRequesting: false,
    isUpdated: false,
    didInvalidate: false
  },
  error: null,
  user: null
};

const actions = {
  obtainToken({ commit }, args) {
    return new Promise((resolve, reject) => {
      commit(types.REQUEST_TOKEN);
      commit(types.CLEAR_ERROR);
      api
        .getToken(args)
        .then(
          response => {
            commit(types.UPDATE_TOKEN, response.data.token);
            resolve("success");
          },
          ({ response }) => {
            commit(types.ADD_ERROR, response.data);
            reject(response.data);
          }
        )
        .catch(e => {
          commit(types.REQUEST_TOKEN_FAILURE);
          reject("fail");
        });
    });
  },
  refreshToken({ commit }) {
    const payload = {
      token: state.jwt.data
    };
    commit(types.REQUEST_TOKEN);
    api
      .refreshToken(payload)
      .then(response => {
        commit(types.UPDATE_TOKEN, response.data.token);
      })
      .catch(e => {
        commit(types.REQUEST_TOKEN_FAILURE);
      });
  },
  inspectToken({ dispatch, commit }) {
    return new Promise((resolve, reject) => {
      const token = state.jwt.data;

      if (token) {
        const decoded = jwt_decode(token);
        const exp = decoded.exp;
        const orig_iat = decoded.orig_iat;
        commit(types.SET_USER, decoded.username);        
        if (
          exp - Date.now() / 1000 < 1800 &&
          Date.now() / 1000 - orig_iat < 628200
        ) {
          dispatch("refreshToken");
        } 
        if (
          Date.now() / 1000 - orig_iat > 628200 ||
          exp - Date.now() / 1000 < 0
        ) {
          reject("err");

          router.push("/login");
        }
        resolve("continue");
      } else {
        // PROMPT USER LOGIN
        reject("err");

        router.push("/login");
      }
    });
  }
};
const mutations = {
  [types.UPDATE_TOKEN](state, newToken) {
    localStorage.setItem("t", newToken);
    state.jwt.data = newToken;
    state.jwt.isRequesting = false;
    state.jwt.isUpdated = true;
    state.jwt.didInvalidate = false;
  },
  [types.REQUEST_TOKEN_FAILURE](state) {
    state.jwt.isRequesting = false;
    state.jwt.isUpdated = false;
    state.jwt.didInvalidate = true;
  },
  [types.REQUEST_TOKEN](state) {
    state.jwt.isRequesting = true;
    state.jwt.isUpdated = false;
    state.jwt.didInvalidate = false;
  },
  [types.CLEAR_ERROR](state) {
    state.error = null;
  },
  [types.ADD_ERROR](state, err) {
    state.error = err;
  },
  [types.REMOVE_TOKEN](state) {
    localStorage.removeItem("t");
    state.jwt.data = null;
  },
  [types.SET_USER](state, name) {
    state.user = name;
  },
  [types.LOG_OUT](state) {
    state.jwt.data = null;
    localStorage.removeItem("t");
    state.user = null;
    router.push("/results");
  }
};
const getters = {
  getLoginError(state, getters, rootState) {
    return state.error;
  },
  getUserName(state, getters, rootState) {
    return state.user;
  }
};

export default {
  state,
  actions,
  mutations,
  getters
};
