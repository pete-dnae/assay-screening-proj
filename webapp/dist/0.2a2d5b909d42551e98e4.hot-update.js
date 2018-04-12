webpackHotUpdate(0,{

/***/ "./node_modules/vue-loader/lib/template-compiler/index.js?{\"id\":\"data-v-6375eea2\",\"hasScoped\":true,\"transformToRequire\":{\"video\":[\"src\",\"poster\"],\"source\":\"src\",\"img\":\"src\",\"image\":\"xlink:href\"},\"buble\":{\"transforms\":{}}}!./node_modules/vue-loader/lib/selector.js?type=template&index=0&bustCache!./src/components/scriptinput/scriptinput.vue":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
var render = function() {
  var _vm = this
  var _h = _vm.$createElement
  var _c = _vm._self._c || _h
  return _c("div", [
    _c(
      "div",
      { class: { "container-fluid": true } },
      [
        _c("toolbar", {
          attrs: { error: _vm.error, showSpinner: _vm.showSpinner },
          on: {
            switchInfoVisiblity: _vm.handleSwitchInfoVisiblity,
            formatText: _vm.handleFormat,
            highlightError: _vm.highlightError
          }
        }),
        _vm._v(" "),
        _c(
          "div",
          { staticClass: "row mt-3 w-100" },
          [
            _c("div", {
              staticClass: "editor ql-editor",
              attrs: { id: "editor" },
              on: { keyup: _vm.editorChange, mouseout: _vm.handleMouseOut }
            }),
            _vm._v(" "),
            _c(
              "div",
              { staticClass: "mw-100" },
              [
                !_vm.error
                  ? _c(
                      "div",
                      { staticClass: "row mt-3 w-50" },
                      [
                        _c("hovervisualizer", {
                          attrs: {
                            currentPlate: _vm.currentPlate,
                            tableRowCount: _vm.tableRowCount,
                            tableColCount: _vm.tableColCount,
                            highlightedLineNumber: _vm.highlightedLineNumber,
                            hoverHighlight: _vm.hoverHighlight,
                            allocationMapping: _vm.allocationMapping
                          },
                          on: {
                            wellHovered: _vm.handleWellHover,
                            hoverComplete: _vm.handleWellHoverComplete
                          }
                        }),
                        _vm._v(" "),
                        _vm._m(0)
                      ],
                      1
                    )
                  : _vm._e(),
                _vm._v(" "),
                _vm.showWellContents && !_vm.error
                  ? _c(
                      "div",
                      { staticClass: "row mt-3" },
                      [
                        _c("wellcontents", {
                          attrs: {
                            currentRow: _vm.currentRow,
                            currentCol: _vm.currentCol,
                            allocationData: _vm.allocationData[_vm.currentPlate]
                          }
                        })
                      ],
                      1
                    )
                  : _vm._e(),
                _vm._v(" "),
                _vm.error ? _c("errorPane") : _vm._e(),
                _vm._v(" "),
                _c("suggestionsList", {
                  directives: [
                    {
                      name: "show",
                      rawName: "v-show",
                      value: _vm.showSuggestionList,
                      expression: "showSuggestionList"
                    }
                  ],
                  attrs: { suggestions: _vm.suggestions },
                  on: {
                    autoComplete: _vm.handleAutoCompleteClick,
                    hideSuggestion: _vm.hideSuggestion
                  }
                })
              ],
              1
            ),
            _vm._v(" "),
            _vm.showSuggestionToolTip
              ? _c("suggestionToolTip", {
                  attrs: {
                    suggestions: _vm.suggestions,
                    toolTipPosition: _vm.tooltiptext
                  },
                  on: {
                    autoComplete: _vm.handleAutoCompleteClick,
                    hideSuggestion: _vm.hideSuggestion
                  }
                })
              : _vm._e()
          ],
          1
        ),
        _vm._v(" "),
        _c(
          "modal",
          {
            attrs: {
              title: "Example Script",
              effect: "fade/zoom",
              large: "",
              value: _vm.showInfo
            }
          },
          [
            _c("textarea", {
              directives: [
                {
                  name: "model",
                  rawName: "v-model",
                  value: _vm.referenceText,
                  expression: "referenceText"
                }
              ],
              staticClass: "w-100 editor",
              attrs: { readonly: "" },
              domProps: { value: _vm.referenceText },
              on: {
                input: function($event) {
                  if ($event.target.composing) {
                    return
                  }
                  _vm.referenceText = $event.target.value
                }
              }
            }),
            _vm._v(" "),
            _c(
              "div",
              {
                staticClass: "modal-footer",
                attrs: { slot: "modal-footer" },
                slot: "modal-footer"
              },
              [
                _c(
                  "button",
                  {
                    staticClass: "btn btn-default",
                    attrs: { type: "button" },
                    on: {
                      click: function($event) {
                        _vm.handleSwitchInfoVisiblity()
                      }
                    }
                  },
                  [_vm._v("Exit")]
                )
              ]
            )
          ]
        )
      ],
      1
    ),
    _vm._v(" "),
    _vm.showBlur
      ? _c("div", { attrs: { id: "overlay" } }, [
          _c("div", { attrs: { id: "text" } }, [
            _vm._v("Possible Connection Error")
          ])
        ])
      : _vm._e()
  ])
}
var staticRenderFns = [
  function() {
    var _vm = this
    var _h = _vm.$createElement
    var _c = _vm._self._c || _h
    return _c("div", { staticClass: "row w-100 mt-3" }, [
      _c("div", { staticClass: "col-md-6" }),
      _vm._v(" "),
      _c("div", { staticClass: "col" }, [
        _c("i", {
          staticClass: "fa fa-lightbulb-o fa-2x",
          attrs: { "aria-hidden": "true" }
        }),
        _vm._v(" "),
        _c("label", { staticClass: "text-info" }, [_vm._v("Hover over a well")])
      ])
    ])
  }
]
render._withStripped = true
var esExports = { render: render, staticRenderFns: staticRenderFns }
/* harmony default export */ __webpack_exports__["a"] = (esExports);
if (true) {
  module.hot.accept()
  if (module.hot.data) {
    __webpack_require__("./node_modules/vue-hot-reload-api/dist/index.js")      .rerender("data-v-6375eea2", esExports)
  }
}

/***/ })

})
//# sourceMappingURL=0.2a2d5b909d42551e98e4.hot-update.js.map