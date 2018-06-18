/* eslint-disable */
import * as types from "./mutation-types";
import * as api from "@/models/api";
import * as ui from "../ui/mutation-types";
import { inspect } from "util";
import jwt_decode from "jwt-decode";
import router from "@/router";

export const state = {
  jwt: {
    data: localStorage.getItem("t"),
    isRequesting: false,
    isUpdated: false,
    didInvalidate: false
  },
  error: null
};

const actions = {
  obtainToken({ commit }, args) {
    return new Promise((resolve, reject) => {
      commit(types.REQUEST_TOKEN);
      api
        .getToken(args)
        .then(response => {
          commit(types.UPDATE_TOKEN, response.data.token);
          resolve("success");
        })
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
  inspectToken({ dispatch }) {
    return new Promise((resolve, reject) => {
      const token = state.jwt.data;
      if (token) {
        const decoded = jwt_decode(token);
        const exp = decoded.exp;
        const orig_iat = decoded.orig_iat;
        if (
          exp - Date.now() / 1000 < 1800 &&
          Date.now() / 1000 - orig_iat < 628200
        ) {
          dispatch("refreshToken");
        } else if (exp - Date.now() / 1000 < 1800) {
          // DO NOTHING, DO NOT REFRESH
        }
        if (Date.now() / 1000 - orig_iat > 628200) {
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

  [types.REMOVE_TOKEN](state) {
    localStorage.removeItem("t");
    state.jwt.data = null;
  }
};
const getters = {
  getLoginError(state, getters, rootState) {
    return state.error;
  }
};

export default {
  state,
  actions,
  mutations,
  getters
};
