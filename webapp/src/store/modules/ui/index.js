/* eslint-disable */
import _ from "lodash";
import * as types from "./mutation-types";
import * as api from "@/models/api";
export const state = {
  toolTipStyle: {
    "max-height": "300px",
    "max-width": "500px",
    "text-align": "center",
    "border-radius": "6px",
    padding: "5px 0" /* Position the tooltip */,
    position: "absolute",
    "z-index": 99999
  },
  suggestions: { showTooltip: false, showList: false },
  showBlur: false,
  showWellContents:false,
  showInfo:false,
  highlightHover:true,
  highlightedLineNumber:null,
  currentPlate:null,
  currentCol:null,
  currentRow:null
};

const actions = {};
const mutations = {
  [types.ADJUST_TOOL_TIP_POSITION](state, args) {
    const { cursorLocation, parentBound } = args;
    const top = `${cursorLocation.top + parentBound.top}px`;
    const left = `${cursorLocation.left + parentBound.left}px`;
    state.toolTipStyle = { ...state.toolTipStyle, top, left };
  },
  [types.SHOW_BLUR](state) {
    state.showBlur = true;
  },
  [types.SHOW_SUGGESTIONS_TOOL_TIP](state, bool) {
    state.suggestions.showTooltip = bool;
  },
  [types.SHOW_SUGGESTIONS_LIST](state, bool) {
    state.suggestions.showList = bool;
  },
  [types.SHOW_WELL_CONTENTS](state, bool) {
    state.showWellContents = bool;
  },
  [types.SHOW_INFO](state) {
    state.showInfo = !state.showInfo;
  },
  [types.HIGHLIGHT_HOVER](state, bool) {
    state.highlightHover = bool;
  },
  [types.SET_CURRENT_ROW](state, number) {
    state.currentRow = number;
  },
  [types.SET_CURRENT_COL](state, number) {
    state.currentCol = number;
  },
  [types.SET_CURRENT_PLATE](state, value) {
    state.currentPlate = value;
  },
  [types.SET_HIGHLIGHTED_LINE_NUMBER](state, number) {
    state.highlightedLineNumber = number;
  }
};
const getters = {
  getToolTipStyle(state, getters, rootState) {
    return state.toolTipStyle;
  },
  getBlurFlag(state, getters, rootState) {
    return state.showBlur;
  },
  getSuggestionToolTip(state, getters, rootState) {
    return state.suggestions.showTooltip;
  },
  getSuggestionList(state, getters, rootState) {
    return state.suggestions.showList;
  },
  getShowWellContetns(state, getters, rootState) {
    return state.showWellContents;
  },
  getShowInfo(state, getters, rootState) {
    return state.showInfo;
  },
  getHighlightHover(state, getters, rootState) {
    return state.highlightHover;
  },
  getCurrentRow(state, getters, rootState) {
    return state.currentRow;
  },
  getCurrentCol(state, getters, rootState) {
    return state.currentCol;
  },
  getCurrentPlate(state, getters, rootState) {
    return state.currentPlate;
  },
  getHighlightedLineNumber(state, getters, rootState) {
    return state.highlightedLineNumber;
  }
};

export default {
  state,
  actions,
  mutations,
  getters
};
