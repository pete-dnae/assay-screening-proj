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
    padding: "5px 0",
    /* Position the tooltip */
    position: "absolute",
    "z-index": 99999
  },
  showBlur:false
};

const actions = {};
const mutations = {
[types.ADJUST_TOOL_TIP_POSITION](state,args){
  
  const { cursorLocation, parentBound } = args;  
  const top = `${cursorLocation.top + parentBound.top}px`;
  const left = `${cursorLocation.left + parentBound.left}px`;
  state.toolTipStyle = { ...state.toolTipStyle, top, left };

},
[types.SHOW_BLUR](state){
  state.showBlur = true
}
};
const getters = {
  getToolTipStyle(state, getters, rootState) {
    return state.toolTipStyle;
  },
  getBlurFlag(state, getters, rootState) {
    return state.showBlur;
  }
};

export default {
  state,
  actions,
  mutations,
  getters
};
