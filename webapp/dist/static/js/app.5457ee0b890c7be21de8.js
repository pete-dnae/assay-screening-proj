webpackJsonp([1],{"5W1q":function(t,s){},NHnr:function(t,s,a){"use strict";Object.defineProperty(s,"__esModule",{value:!0});a("qb6w"),a("5W1q"),a("UQ8B"),a("K3J8");var e=a("7t+N"),i=a.n(e),l=a("7+uW"),o={render:function(){this.$createElement;this._self._c;return this._m(0)},staticRenderFns:[function(){var t=this,s=t.$createElement,a=t._self._c||s;return a("div",{staticClass:"hello"},[a("nav",{staticClass:"navbar navbar-expand-lg navbar-light bg-light"},[a("a",{staticClass:"navbar-brand",attrs:{href:"#"}},[t._v("Assay Experiment Design")]),t._v(" "),a("button",{staticClass:"navbar-toggler",attrs:{type:"button","data-toggle":"collapse","data-target":"#navbarSupportedContent","aria-controls":"navbarSupportedContent","aria-expanded":"false","aria-label":"Toggle navigation"}},[a("span",{staticClass:"navbar-toggler-icon"})]),t._v(" "),a("span",[a("b",[t._v("Experiment")])]),t._v(" "),a("div",{staticClass:"dropdown pl-3"},[a("button",{staticClass:"btn btn-secondary dropdown-toggle",attrs:{type:"button",id:"dropdownMenu2","data-toggle":"dropdown","aria-haspopup":"true","aria-expanded":"false"}},[t._v("\n        A60E010\n      ")]),t._v(" "),a("div",{staticClass:"dropdown-menu",attrs:{"aria-labelledby":"dropdownMenu2"}},[a("button",{staticClass:"dropdown-item",attrs:{type:"button"}},[t._v("A82E131")]),t._v(" "),a("button",{staticClass:"dropdown-item",attrs:{type:"button"}},[t._v("A82E121")]),t._v(" "),a("button",{staticClass:"dropdown-item",attrs:{type:"button"}},[t._v("A82E101")])])])])])}]},n=a("VU/8")({name:"HelloWorld",data:function(){return{msg:"Welcome to Your Vue.js App "}}},o,!1,null,null,null).exports;l.a.component("titlemenu",n);var r={render:function(){var t=this.$createElement,s=this._self._c||t;return s("div",[s("titlemenu"),this._v(" "),s("div",{attrs:{id:"app"}},[s("router-view")],1)],1)},staticRenderFns:[]},c=a("VU/8")({name:"app"},r,!1,function(t){a("Tq6Z")},null,null).exports,v=a("/ocq"),d={render:function(){var t=this,s=t.$createElement,a=t._self._c||s;return a("div",[a("div",{staticClass:"row"},[t._m(0),t._v(" "),a("div",{staticClass:"col"},[a("select",{directives:[{name:"model",rawName:"v-model",value:t.selected,expression:"selected"}],on:{change:function(s){var a=Array.prototype.filter.call(s.target.options,function(t){return t.selected}).map(function(t){return"_value"in t?t._value:t.value});t.selected=s.target.multiple?a:a[0]}}},t._l(t.options,function(s){return a("option",{domProps:{value:s.value}},[t._v("\n          "+t._s(s.text)+"\n        ")])}))]),t._v(" "),a("div",{staticClass:"col"},[a("input",{directives:[{name:"model",rawName:"v-model",value:t.message,expression:"message"}],attrs:{placeholder:"edit me"},domProps:{value:t.message},on:{input:function(s){s.target.composing||(t.message=s.target.value)}}})]),t._v(" "),t._m(1),t._v(" "),a("div",{staticClass:"col"},[a("input",{directives:[{name:"model",rawName:"v-model",value:t.message,expression:"message"}],attrs:{disabled:""},domProps:{value:t.message},on:{input:function(s){s.target.composing||(t.message=s.target.value)}}})])]),t._v(" "),t._m(2)])},staticRenderFns:[function(){var t=this.$createElement,s=this._self._c||t;return s("div",{staticClass:"col"},[s("span",[this._v("Start @")])])},function(){var t=this.$createElement,s=this._self._c||t;return s("div",{staticClass:"col"},[s("a",{staticClass:"btn btn-danger",attrs:{"aria-label":"Delete"}},[s("i",{staticClass:"fa fa-trash-o",attrs:{"aria-hidden":"true"}})])])},function(){var t=this.$createElement,s=this._self._c||t;return s("div",{staticClass:"row"},[s("div",{staticClass:"col float-right"},[s("a",{staticClass:"btn btn-info",attrs:{"aria-label":"Delete"}},[s("i",{staticClass:"fa fa-plus-square",attrs:{"aria-hidden":"true"}})])])])}]},_=a("VU/8")({name:"ExpandColumns",data:function(){return{msg:"This is ExpandColumns",options:[{text:"A",value:"A"},{text:"B",value:"B"},{text:"C",value:"C"},{text:"D",value:"D"},{text:"E",value:"E"},{text:"F",value:"F"},{text:"G",value:"D"},{text:"H",value:"H"}]}}},d,!1,null,null,null).exports;l.a.component("expandColumns",_);var u={render:function(){var t=this,s=t.$createElement,a=t._self._c||s;return a("ul",{staticClass:"nav navbar-nav mt-3"},[a("li",{staticClass:"dropdown dropdown-lg"},[t._m(0),t._v(" "),a("div",{class:t.currentDisplayClass,style:t.currentDisplayStyle,attrs:{onClick:"event.stopPropagation();"}},[a("div",{staticClass:"row"},[t._m(1),t._v(" "),a("div",{staticClass:"col-md-7"}),t._v(" "),a("div",{staticClass:"col"},[a("a",{staticClass:"btn btn-danger",attrs:{"aria-label":"Delete"},on:{click:function(s){t.handleRuleClose()}}},[a("i",{staticClass:"fa fa-window-close",attrs:{"aria-hidden":"true"}})])])]),t._v(" "),a("div",{staticClass:"row mt-3"},[t._m(2),t._v(" "),a("div",{staticClass:"col-4 border-right"},[a("h6",{staticClass:"dropdown-header"},[t._v("Expanded to 4 columns each")]),t._v(" "),a("div",{staticClass:"row"},[t._m(3),t._v(" "),a("expandColumns")],1),t._v(" "),a("div",{staticClass:"row mt-3"},[t._m(4),t._v(" "),a("expandColumns")],1),t._v(" "),t._m(5)]),t._v(" "),t._m(6)]),t._v(" "),t._m(7)])])])},staticRenderFns:[function(){var t=this.$createElement,s=this._self._c||t;return s("a",{staticClass:"dropdown-toggle float-left",attrs:{href:"#","data-toggle":"dropdown"}},[this._v("Rules "),s("b",{staticClass:"caret"})])},function(){var t=this.$createElement,s=this._self._c||t;return s("div",{staticClass:"input-group col-4 ml-3"},[s("span",{staticClass:"input-group-addon",attrs:{id:"basic-addon1"}},[this._v("Column Block")]),this._v(" "),s("input",{staticClass:"form-control",attrs:{type:"number",placeholder:"No of repeats","aria-label":"number","aria-describedby":"basic-addon1"}})])},function(){var t=this.$createElement,s=this._self._c||t;return s("div",{staticClass:"col-4 border-right"},[s("h6",{staticClass:"dropdown-header"},[this._v("Repeated Every 4 Columns")]),this._v(" "),s("div",{staticClass:"row"},[s("div",{staticClass:"col"},[s("span",{staticClass:"dropdown-header"},[this._v("Strains")])]),this._v(" "),s("div",{staticClass:"col"},[s("ul",{staticClass:"list-group"},[s("li",{staticClass:"list-group-item"},[this._v("Eco")]),this._v(" "),s("li",{staticClass:"list-group-item"},[this._v("Efs VanB")]),this._v(" "),s("li",{staticClass:"list-group-item"},[this._v("Efs VanB")]),this._v(" "),s("li",{staticClass:"list-group-item"},[this._v("Kox")])])])]),this._v(" "),s("div",{staticClass:"row mt-3"},[s("div",{staticClass:"col"},[s("span",{staticClass:"dropdown-header"},[this._v("ID Primers")])]),this._v(" "),s("div",{staticClass:"col"},[s("ul",{staticClass:"list-group"},[s("li",{staticClass:"list-group-item"},[this._v("Ec_uidA_6.x_Eco63_Eco60")]),this._v(" "),s("li",{staticClass:"list-group-item"},[this._v("Efs_cpn60_1.x_Efs04_Efs01")]),this._v(" "),s("li",{staticClass:"list-group-item"},[this._v("Efs_vanB_1.x_van10_van06")]),this._v(" "),s("li",{staticClass:"list-group-item"},[this._v("Ko_pehX_1.x_Kox05_Kox02")])])])])])},function(){var t=this.$createElement,s=this._self._c||t;return s("div",{staticClass:"col"},[s("span",{staticClass:"dropdown-header"},[this._v("Template Copies")])])},function(){var t=this.$createElement,s=this._self._c||t;return s("div",{staticClass:"col"},[s("span",{staticClass:"dropdown-header"},[this._v("HgDna")])])},function(){var t=this.$createElement,s=this._self._c||t;return s("div",{staticClass:"row mt-3"},[s("div",{staticClass:"col"},[s("span",{staticClass:"dropdown-header"},[this._v("Dilution Factor")])]),this._v(" "),s("div",{staticClass:"col"}),this._v(" "),s("div",{staticClass:"col"},[s("input",{attrs:{placeholder:"values seperated by ','"}})])])},function(){var t=this.$createElement,s=this._self._c||t;return s("div",{staticClass:"col-4"},[s("h6",{staticClass:"dropdown-header"},[this._v("PA Primers")]),this._v(" "),s("div",{staticClass:"row mt-3"},[s("div",{staticClass:"col"},[s("span",{staticClass:"dropdown-header"},[this._v("First Block")])]),this._v(" "),s("div",{staticClass:"col"},[s("select",[s("option",{attrs:{disabled:"",value:""}},[this._v("Please select one")]),this._v(" "),s("option",[this._v("Ec_uidA_6.x_Eco63_Eco60")]),this._v(" "),s("option",[this._v("PoolA")]),this._v(" "),s("option",[this._v("Ko_pehX_1.x_Kox05_Kox02")])])])]),this._v(" "),s("div",{staticClass:"row mt-3"},[s("div",{staticClass:"col"},[s("span",{staticClass:"dropdown-header"},[this._v("Second Block")])]),this._v(" "),s("div",{staticClass:"col"},[s("select",[s("option",{attrs:{disabled:"",value:""}},[this._v("Please select one")]),this._v(" "),s("option",[this._v("Ec_uidA_6.x_Eco63_Eco60")]),this._v(" "),s("option",[this._v("PoolA")]),this._v(" "),s("option",[this._v("Ko_pehX_1.x_Kox05_Kox02")])])])]),this._v(" "),s("div",{staticClass:"row mt-3"},[s("div",{staticClass:"col"},[s("span",{staticClass:"dropdown-header"},[this._v("Third Block")])]),this._v(" "),s("div",{staticClass:"col"},[s("select",[s("option",{attrs:{disabled:"",value:""}},[this._v("Please select one")]),this._v(" "),s("option",[this._v("Ec_uidA_6.x_Eco63_Eco60")]),this._v(" "),s("option",[this._v("PoolA")]),this._v(" "),s("option",[this._v("Ko_pehX_1.x_Kox05_Kox02")])])])]),this._v(" "),s("div",{staticClass:"row mt-3"},[s("div",{staticClass:"col"},[s("span",{staticClass:"dropdown-header"},[this._v("Custom")])]),this._v(" "),s("div",{staticClass:"col mr-2"},[s("ul",{staticClass:"list-group"},[s("li",{staticClass:"list-group-item"},[this._v("Ec_uidA_6.x_Eco63_Eco60")]),this._v(" "),s("li",{staticClass:"list-group-item"},[this._v("Efs_cpn60_1.x_Efs04_Efs01")]),this._v(" "),s("li",{staticClass:"list-group-item"},[this._v("Efs_vanB_1.x_van10_van06")]),this._v(" "),s("li",{staticClass:"list-group-item"},[this._v("Ko_pehX_1.x_Kox05_Kox02")])])])])])},function(){var t=this.$createElement,s=this._self._c||t;return s("div",{staticClass:"row"},[s("div",{staticClass:"input-group col-4 m-3"},[s("span",{staticClass:"input-group-addon",attrs:{id:"basic-addon1"}},[this._v("Suppress Columns")]),this._v(" "),s("input",{staticClass:"form-control",attrs:{type:"number",placeholder:"No of repeats","aria-label":"number","aria-describedby":"basic-addon1"}})])])}]},p=a("VU/8")({name:"rulesDropDown",data:function(){return{msg:"loaded rules drop down",currentDisplayStyle:{display:"relative","background-color":"rgba(0,0,0,0.7)",cursor:"pointer"},currentDisplayClass:["dropdown-menu","dropdown-menu-lg","w-100"]}},methods:{handleRuleClose:function(){this.currentDisplayClass.pop()}}},u,!1,null,null,null).exports,h={render:function(){this.$createElement;this._self._c;return this._m(0)},staticRenderFns:[function(){var t=this.$createElement,s=this._self._c||t;return s("div",{staticClass:"footer"},[s("div",{staticClass:"row"},[s("div",{staticClass:"col"},[s("a",[this._v("PA Master Mix")])]),this._v(" "),s("div",{staticClass:"col"},[s("a",[this._v("ID MAster Mix")])]),this._v(" "),s("div",{staticClass:"col"},[s("a",[this._v("Primers")])])]),this._v(" "),s("div",{staticClass:"row"},[s("div",{staticClass:"col"},[s("a",[this._v("Cycleing Pattern")])]),this._v(" "),s("div",{staticClass:"col"},[s("a",[this._v("Settings")])]),this._v(" "),s("div",{staticClass:"col"},[s("a",[this._v("Strains")])])])])}]},m=a("VU/8")({name:"Footer",data:function(){return{msg:"This is footer"}}},h,!1,function(t){a("oDHt")},"data-v-70383784",null).exports,C={render:function(){var t=this,s=t.$createElement,a=t._self._c||s;return a("div",{staticClass:"mt-3"},t._l(t.rows,function(s){return a("div",{staticClass:"row"},t._l(t.cols,function(e){return a("div",{staticClass:"col border border-primary"},[t._v("\n      "+t._s(s)+"--"+t._s(e)+"\n    ")])}))}))},staticRenderFns:[]},f=a("VU/8")({name:"plateLayout",data:function(){return{msg:"This is plateLayout",rows:["A","B","C","D","E","F","G","H"],cols:[0,1,2,3,4,5,6,7,8,9,10,11,12]}}},C,!1,null,null,null).exports;l.a.component("rulesdropdown",p),l.a.component("customfooter",m),l.a.component("plateLayout",f);var g={render:function(){var t=this.$createElement,s=this._self._c||t;return s("div",{staticClass:"container-fluid"},[this._m(0),this._v(" "),s("div",{staticClass:"tab-content",attrs:{id:"myTabContent"}},[s("div",{staticClass:"tab-pane fade show active",attrs:{id:"Plate1",role:"tabpanel","aria-labelledby":"Plate-1"}},[s("rulesdropdown"),this._v(" "),s("plateLayout"),this._v(" "),s("customfooter")],1),this._v(" "),s("div",{staticClass:"tab-pane fade",attrs:{id:"Plate2",role:"tabpanel","aria-labelledby":"Plate-2"}},[s("rulesdropdown"),this._v(" "),s("plateLayout"),this._v(" "),s("customfooter")],1)])])},staticRenderFns:[function(){var t=this.$createElement,s=this._self._c||t;return s("ul",{staticClass:"nav nav-tabs"},[s("li",{staticClass:"nav-item"},[s("a",{staticClass:"nav-link active",attrs:{id:"Plate-1","data-toggle":"tab",href:"#Plate1"}},[this._v("Plate 1")])]),this._v(" "),s("li",{staticClass:"nav-item"},[s("a",{staticClass:"nav-link",attrs:{id:"Plate-2","data-toggle":"tab",href:"#Plate2"}},[this._v("Plate 2")])]),this._v(" "),s("li",{staticClass:"nav-item"},[s("a",{staticClass:"nav-link",attrs:{"data-toggle":"tab",href:"#"}},[this._v("+")])])])}]},b=a("VU/8")({name:"HelloWorld",data:function(){return{msg:"Welcome Bitch"}}},g,!1,null,null,null).exports;l.a.use(v.a);var w=new v.a({routes:[{path:"/",name:"Home",component:b}]});l.a.config.productionTip=!1,window.$=i.a,window.jQuery=i.a,new l.a({el:"#app",router:w,template:"<App/>",components:{App:c}})},OmrJ:function(t,s,a){(t.exports=a("FZ+f")(void 0)).push([t.i,"#app{font-family:Avenir,Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;text-align:center;color:#2c3e50;margin-top:60px}",""])},Tq6Z:function(t,s,a){var e=a("OmrJ");"string"==typeof e&&(e=[[t.i,e,""]]),e.locals&&(t.exports=e.locals);a("rjj0")("9d452fb8",e,!0)},UQ8B:function(t,s,a){(t.exports=a("FZ+f")(void 0)).push([t.i,".transparent {\n  display: relative;\n  background-color: rgba(0, 0, 0, 0.8);\n  cursor: pointer; }\n",""])},a2Gr:function(t,s,a){(t.exports=a("FZ+f")(void 0)).push([t.i,".footer[data-v-70383784]{position:fixed;left:0;bottom:0;width:100%;background-color:#a6a6a6;color:#fff;text-align:center}",""])},oDHt:function(t,s,a){var e=a("a2Gr");"string"==typeof e&&(e=[[t.i,e,""]]),e.locals&&(t.exports=e.locals);a("rjj0")("73a0aba1",e,!0)},qb6w:function(t,s){}},["NHnr"]);
//# sourceMappingURL=app.5457ee0b890c7be21de8.js.map