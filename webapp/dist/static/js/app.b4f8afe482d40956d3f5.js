webpackJsonp([1],{"5W1q":function(t,a){},GJ4g:function(t,a){},IcnI:function(t,a,s){"use strict";(function(t){var e=s("NYxO"),i=s("7+uW"),o=s("LuzH");i.a.use(e.a),a.a=new e.a.Store({strict:!1,modules:{rules:o.a}})}).call(a,s("W2nU"))},LuzH:function(t,a,s){"use strict";var e,i=s("bOdI"),o=s.n(i),n=s("M4fF"),l=s.n(n),r=s("nEJY"),c=(e={},o()(e,"SET_TEMPLATE_RULES",function(t,a){t.template.data=a}),o()(e,"SET_HGDNA_RULES",function(t,a){t.hgDNA.data=a}),o()(e,"SET_TEMPLATE_PLATE",function(t,a){t.plate.data.templateConcentration=a.reduce(function(a,s){return s.allRows.map(function(e){var i=s.concentration.split(","),o=t.colId.length/s.blocks;return i=i.length!==o?i.concat(l.a.times(o-i.length,function(){return""})):i,a[e]=l.a.times(s.blocks,function(){return i}).reduce(function(t,a){return t=t.concat(a)},[]),a[e]}),a},{})}),o()(e,"SET_HGDNA_PLATE",function(t,a){t.plate.data.hgDNAConcentration=a.reduce(function(a,s){return s.allRows.map(function(e){var i=s.concentration.split(","),o=t.colId.length/s.blocks;return i=i.length!==o?i.concat(l.a.times(o-i.length,function(){return""})):i,a[e]=l.a.times(s.blocks,function(){return i}).reduce(function(t,a){return t=t.concat(a)},[]),a[e]}),a},{})}),o()(e,"SET_STRAINS",function(t,a){t.strains.data=a}),o()(e,"SET_ID_PRIMERS",function(t,a){t.idPrimers.data=a}),o()(e,"SET_STRAINS_PLATE",function(t,a){var s=a.data,e=a.blocks,i=a.byBlock,o=a.blockNo,n=t.colId.length/e,l=Object(r.a)(i,o,e,t.colId,n,s);t.plate.data.strains=Object(r.b)(i,e,t.rowId,l)}),o()(e,"SET_ID_PRIMERS_PLATE",function(t,a){var s=a.data,e=a.blocks,i=a.byBlock,o=(a.blockNo,t.colId.length/e),n=Object(r.a)(i,e,t.colId,o,s);t.plate.data.idPrimers=Object(r.b)(i,e,t.rowId,n)}),e);a.a={state:{template:{data:[]},hgDNA:{data:[]},dilution:{data:{}},strains:{data:{}},idPrimers:{data:{}},plate:{data:{templateConcentration:{},hgDNAConcentration:{},strains:{},idPrimers:{}}},rowId:["A","B","C","D","E","F","G","H"],colId:[1,2,3,4,5,6,7,8,9,10,11,12]},actions:{},mutations:c,getters:{getTemplate:function(t,a,s){return t.plate.data.templateConcentration},gethgDNA:function(t,a,s){return t.plate.data.hgDNAConcentration},getDilution:function(t,a,s){return t.dilution.data},getStrains:function(t,a,s){return t.plate.data.strains},getIdPrimers:function(t,a,s){return t.plate.data.idPrimers}}}},M93x:function(t,a,s){"use strict";var e=s("7+uW"),i={render:function(){this.$createElement;this._self._c;return this._m(0)},staticRenderFns:[function(){var t=this.$createElement,a=this._self._c||t;return a("div",{staticClass:"hello"},[a("nav",{staticClass:"navbar navbar-expand-lg navbar-light bg-light"},[a("a",{staticClass:"navbar-brand",attrs:{href:"#"}},[this._v("Assay Experiment Design")]),this._v(" "),a("button",{staticClass:"navbar-toggler",attrs:{type:"button","data-toggle":"collapse","data-target":"#navbarSupportedContent","aria-controls":"navbarSupportedContent","aria-expanded":"false","aria-label":"Toggle navigation"}},[a("span",{staticClass:"navbar-toggler-icon"})]),this._v(" "),a("span",[a("b",[this._v("Experiment")])]),this._v(" "),a("div",{staticClass:"dropdown pl-3"},[a("button",{staticClass:"btn btn-secondary dropdown-toggle",attrs:{type:"button",id:"dropdownMenu2","data-toggle":"dropdown","aria-haspopup":"true","aria-expanded":"false"}},[this._v("\n        A60E010\n      ")]),this._v(" "),a("div",{staticClass:"dropdown-menu",attrs:{"aria-labelledby":"dropdownMenu2"}},[a("button",{staticClass:"dropdown-item",attrs:{type:"button"}},[this._v("A82E131")]),this._v(" "),a("button",{staticClass:"dropdown-item",attrs:{type:"button"}},[this._v("A82E121")]),this._v(" "),a("button",{staticClass:"dropdown-item",attrs:{type:"button"}},[this._v("A82E101")])])])])])}]},o=s("VU/8")({name:"HelloWorld",data:function(){return{msg:"Welcome to Your Vue.js App "}}},i,!1,null,null,null).exports;e.a.component("titlemenu",o);var n={render:function(){var t=this.$createElement,a=this._self._c||t;return a("div",[a("titlemenu"),this._v(" "),a("div",{attrs:{id:"app"}},[a("router-view")],1)],1)},staticRenderFns:[]},l=s("VU/8")({name:"app"},n,!1,function(t){s("Tq6Z")},null,null);a.a=l.exports},NHnr:function(t,a,s){"use strict";Object.defineProperty(a,"__esModule",{value:!0}),function(t,a){var e=s("qb6w"),i=(s.n(e),s("5W1q")),o=(s.n(i),s("UQ8B")),n=(s.n(o),s("GJ4g")),l=(s.n(n),s("K3J8")),r=(s.n(l),s("9JMe")),c=(s.n(r),s("7+uW")),d=s("M93x"),u=s("YaEn"),v=s("IcnI");c.a.config.productionTip=!1,window.$=t,Object(r.sync)(v.a,u.a),new c.a({el:"#app",router:u.a,store:v.a,template:"<App/>",components:{App:d.a}})}.call(a,s("7t+N"),s("7t+N"))},OckA:function(t,a,s){"use strict";(function(t,e){var i=s("mvHQ"),o=s.n(i),n=s("bOdI"),l=s.n(n),r=s("Dd8w"),c=s.n(r),d=s("woOf"),u=s.n(d),v=s("M4fF"),p=s.n(v),h=s("nEJY");a.a={name:"ExpandColumns",props:{type:String,columnBlocks:Number},data:function(){return{msg:"This is ExpandColumns",options:[{text:"A",value:"A"},{text:"B",value:"B"},{text:"C",value:"C"},{text:"D",value:"D"},{text:"E",value:"E"},{text:"F",value:"F"},{text:"G",value:"G"},{text:"H",value:"H"}],rows:[],data:{}}},methods:{handleRowAdd:function(){var a=this.rows.length-1,s=0==this.rows.length?0:this.rows[a]+1;if(0==s||Object(h.c)(this.columnBlocks,this.data[a].concentration))this.rows.push(s),this.data[s]={startAt:"",allRows:"",concentration:"",blocks:this.columnBlocks};else{t("#popup"+this.type).show();new e(document.getElementById((s-1).toString()+this.type),this.$refs.popup,{placement:"top"})}},handleRowDelete:function(a){this.rows=this.rows.filter(function(t){return t!=a}),delete this.data[a],t("#popup"+this.type).hide(),this.changeAllocationRules()},changeAllocationRules:function(){var t=this;this.rows.map(function(a){var s=t.options.map(function(t){return t.value}),e=s.indexOf(t.data[a].startAt),i=t.data[a+1]?s.indexOf(t.data[a+1].startAt):s.length;t.data=u()({},t.data,l()({},a,c()({},t.data[a],{allRows:s.slice(e,i)})))}),p.a.isEmpty(p.a.filter(this.data,function(t){return""!=t.startAt}))||this.$emit("ruleChange",this.type,JSON.parse(o()(p.a.map(this.data,function(t){return t}))))}},mounted:function(){var a=this;t("#popup"+this.type).hide(),t("#popup"+this.type).click(function(){t("#popup"+a.type).hide()})}}}).call(a,s("7t+N"),s("Zgw8").default)},OmrJ:function(t,a,s){(t.exports=s("FZ+f")(void 0)).push([t.i,"#app{font-family:Avenir,Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;text-align:center;color:#2c3e50;margin-top:60px}",""])},SpqO:function(t,a,s){(t.exports=s("FZ+f")(void 0)).push([t.i,".footer[data-v-2fb89cf9]{position:absolute;left:0;bottom:0;width:100%;background-color:#a6a6a6;color:#fff;text-align:center}",""])},Tq6Z:function(t,a,s){var e=s("OmrJ");"string"==typeof e&&(e=[[t.i,e,""]]),e.locals&&(t.exports=e.locals);s("rjj0")("9d452fb8",e,!0)},UQ8B:function(t,a,s){(t.exports=s("FZ+f")(void 0)).push([t.i,".transparent {\n  display: relative;\n  background-color: rgba(0, 0, 0, 0.8);\n  cursor: pointer; }\n",""])},YaEn:function(t,a,s){"use strict";var e=s("7+uW"),i=s("/ocq"),o=s("Dd8w"),n=s.n(o),l=s("NYxO"),r=s("OckA"),c={render:function(){var t=this,a=t.$createElement,s=t._self._c||a;return s("div",[t._l(t.rows,function(a){return s("div",{staticClass:"row"},[t._m(0,!0),t._v(" "),s("div",{staticClass:"col"},[s("select",{directives:[{name:"model",rawName:"v-model",value:t.data[a].startAt,expression:"data[rowId].startAt"}],on:{change:[function(s){var e=Array.prototype.filter.call(s.target.options,function(t){return t.selected}).map(function(t){return"_value"in t?t._value:t.value});t.$set(t.data[a],"startAt",s.target.multiple?e:e[0])},function(a){t.changeAllocationRules()}]}},t._l(t.options,function(a){return s("option",{domProps:{value:a.value}},[t._v("\n          "+t._s(a.text)+"\n        ")])}))]),t._v(" "),s("div",{staticClass:"col"},[s("input",{directives:[{name:"model",rawName:"v-model",value:t.data[a].concentration,expression:"data[rowId].concentration"}],attrs:{id:a+t.type,placeholder:"edit me"},domProps:{value:t.data[a].concentration},on:{keyup:function(a){if(!("button"in a)&&t._k(a.keyCode,"enter",13,a.key))return null;t.changeAllocationRules()},input:function(s){s.target.composing||t.$set(t.data[a],"concentration",s.target.value)}}})]),t._v(" "),s("div",{staticClass:"col"},[s("a",{staticClass:"btn btn-danger",attrs:{"aria-label":"Delete"},on:{click:function(s){t.handleRowDelete(a)}}},[s("i",{staticClass:"fa fa-trash-o",attrs:{"aria-hidden":"true"}})])]),t._v(" "),s("div",{staticClass:"col"},[s("input",{directives:[{name:"model",rawName:"v-model",value:t.data[a].allRows,expression:"data[rowId].allRows"}],attrs:{disabled:""},domProps:{value:t.data[a].allRows},on:{input:function(s){s.target.composing||t.$set(t.data[a],"allRows",s.target.value)}}})])])}),t._v(" "),s("div",{staticClass:"row"},[s("div",{staticClass:"col float-right"},[s("a",{staticClass:"btn btn-info",attrs:{"aria-label":"Add"},on:{click:function(a){t.handleRowAdd()}}},[s("i",{staticClass:"fa fa-plus-square",attrs:{"aria-hidden":"true"}})])])]),t._v(" "),s("div",{ref:"popup",staticClass:"popper",attrs:{id:"popup"+t.type}},[t._v("\n  Check concentration\n  ")])],2)},staticRenderFns:[function(){var t=this.$createElement,a=this._self._c||t;return a("div",{staticClass:"col"},[a("span",{staticStyle:{color:"White"}},[this._v("Start @")])])}]},d=s("VU/8")(r.a,c,!1,null,null,null).exports,u=s("YesG");e.a.component("modal",u.modal);var v={name:"EditableList",props:{type:String,columnBlocks:Number},data:function(){return{msg:"This is EditableList",rows:[],showModal:!1,modalText:"",listItem:{},repeatOption:"",blockNo:""}},methods:{handleListAdd:function(t){if(""!=t){var a=0==this.rows.length?0:this.rows[this.rows.length-1]+1;this.rows.push(a),this.listItem[a]=t;var s="Strain"==this.type?"SET_STRAINS":"SET_ID_PRIMERS";this.$store.commit(s,{blocks:this.columnBlocks,byBlock:"block"==this.repeatOption,blockNo:this.blockNo,data:this.listItem}),this.$store.commit(s+"_PLATE",{blocks:this.columnBlocks,byBlock:"block"==this.repeatOption,blockNo:this.blockNo,data:this.listItem})}else alert("Please enter a valid name")},handleListDelete:function(t){var a=this;this.rows=this.rows.filter(function(a){return a!=t}),this.listItem=_.filter(this.listItem,function(t,s){return-1!=a.rows.indexOf(parseInt(s))});var s="Strain"==this.type?"SET_STRAINS":"SET_ID_PRIMERS";this.$store.commit(s,{blocks:this.columnBlocks,byBlock:"block"==this.repeatOption,blockNo:this.blockNo,data:this.listItem}),this.$store.commit(s+"_PLATE",{blocks:this.columnBlocks,byBlock:"block"==this.repeatOption,blockNo:this.blockNo,data:this.listItem})}}},p={render:function(){var t=this,a=t.$createElement,s=t._self._c||a;return s("div",[s("ul",{staticClass:"list-group m-3"},[t._l(t.rows,function(a){return s("div",{staticClass:"row"},[s("div",{staticClass:"col"},[s("li",{staticClass:"list-group-item",staticStyle:{"background-color":"rgba(0,0,0,0)",color:"white"}},[t._v(t._s(t.listItem[a]))])]),t._v(" "),s("div",{staticClass:"col"},[s("a",{staticClass:"btn btn-info",attrs:{"aria-label":"delete"},on:{click:function(s){t.handleListDelete(a)}}},[s("i",{staticClass:"fa fa-trash-o",attrs:{"aria-hidden":"true"}})])])])}),t._v(" "),s("div",{staticClass:"row"},[s("div",{staticClass:"col float-right"},[s("a",{staticClass:"btn btn-info",attrs:{"aria-label":"Add"},on:{click:function(a){t.showModal=!0}}},[s("i",{staticClass:"fa fa-plus-square",attrs:{"aria-hidden":"true"}})])])])],2),t._v(" "),s("modal",{model:{value:t.showModal,callback:function(a){t.showModal=a},expression:"showModal"}},[s("div",{staticClass:"modal-header",attrs:{slot:"modal-header"},slot:"modal-header"},[s("h4",{staticClass:"modal-title"},[t._v("Strain Name")])]),t._v(" "),s("div",{staticClass:"modal-body",attrs:{slot:"modal-body"},slot:"modal-body"},[s("div",{staticClass:"row"},[s("div",{staticClass:"col mt-3"},[s("div",{staticClass:"row ml-2"},[s("input",{directives:[{name:"model",rawName:"v-model",value:t.modalText,expression:"modalText"}],attrs:{type:"text",placeholder:"Enter Name"},domProps:{value:t.modalText},on:{input:function(a){a.target.composing||(t.modalText=a.target.value)}}})]),t._v(" "),"block"==t.repeatOption?s("div",{staticClass:"row mt-5"},[s("span",[t._v("Specify Block No")]),t._v(" "),t._l(t.columnBlocks,function(a){return s("div",[s("input",{directives:[{name:"model",rawName:"v-model",value:t.blockNo,expression:"blockNo"}],attrs:{type:"radio",id:a},domProps:{value:a,checked:t._q(t.blockNo,a)},on:{change:function(s){t.blockNo=a}}}),t._v(" "),s("label",[t._v(t._s(a))])])})],2):t._e()]),t._v(" "),s("div",{staticClass:"col"},[s("div",{staticClass:"row"},[s("input",{directives:[{name:"model",rawName:"v-model",value:t.repeatOption,expression:"repeatOption"}],attrs:{type:"radio",id:"one",value:"column"},domProps:{checked:t._q(t.repeatOption,"column")},on:{change:function(a){t.repeatOption="column"}}}),t._v(" "),s("img",{attrs:{src:"src\\assets\\bycol.JPG"}})]),t._v(" "),s("br"),t._v(" "),s("br"),t._v(" "),s("div",{staticClass:"row"},[s("input",{directives:[{name:"model",rawName:"v-model",value:t.repeatOption,expression:"repeatOption"}],attrs:{type:"radio",id:"two",value:"block"},domProps:{checked:t._q(t.repeatOption,"block")},on:{change:function(a){t.repeatOption="block"}}}),t._v(" "),s("img",{attrs:{src:"src\\assets\\byblock.JPG"}})])])])]),t._v(" "),s("div",{staticClass:"modal-footer",attrs:{slot:"modal-footer"},slot:"modal-footer"},[s("button",{on:{click:function(a){t.showModal=!1}}},[t._v("Close")]),t._v(" "),s("button",{on:{click:function(a){t.handleListAdd(t.modalText),t.showModal=!1}}},[t._v("Add")])])])],1)},staticRenderFns:[]},h=s("VU/8")(v,p,!1,null,null,null).exports;e.a.component("expandColumns",d),e.a.component("editableList",h);var m={render:function(){var t=this,a=t.$createElement,s=t._self._c||a;return s("ul",{staticClass:"nav navbar-nav mt-3"},[s("li",{staticClass:"dropdown dropdown-lg"},[t._m(0),t._v(" "),s("div",{class:t.currentDisplayClass,style:t.currentDisplayStyle,attrs:{onClick:"event.stopPropagation();"}},[s("div",{staticClass:"row"},[s("div",{staticClass:"input-group col-4 ml-3"},[s("span",{staticClass:"input-group-addon",attrs:{id:"basic-addon1"}},[t._v("Column Block")]),t._v(" "),s("input",{directives:[{name:"model",rawName:"v-model",value:t.columnBlocks,expression:"columnBlocks"}],staticClass:"form-control",attrs:{type:"number",placeholder:"No of repeats","aria-label":"number","aria-describedby":"basic-addon1"},domProps:{value:t.columnBlocks},on:{input:function(a){a.target.composing||(t.columnBlocks=a.target.value)}}})]),t._v(" "),s("div",{staticClass:"col-md-7"}),t._v(" "),s("div",{staticClass:"col"},[s("a",{staticClass:"btn btn-danger",attrs:{"aria-label":"Delete"},on:{click:function(a){t.handleRuleClose()}}},[s("i",{staticClass:"fa fa-window-close",attrs:{"aria-hidden":"true"}})])])]),t._v(" "),s("div",{staticClass:"row mt-3"},[s("div",{staticClass:"col-3 border-right"},[s("h6",{staticClass:"dropdown-header"},[t._v("Repeated Every 4 Columns")]),t._v(" "),t._m(1),t._v(" "),s("div",{staticClass:"row"},[s("div",{staticClass:"col"},[s("editableList",{attrs:{columnBlocks:parseInt(t.columnBlocks),type:"Strain"}})],1)]),t._v(" "),t._m(2),t._v(" "),s("div",{staticClass:"row"},[s("div",{staticClass:"col"},[s("editableList",{attrs:{columnBlocks:parseInt(t.columnBlocks),type:"ID Primers"}})],1)])]),t._v(" "),s("div",{staticClass:"col-5 border-right"},[s("h6",{staticClass:"dropdown-header"},[t._v("Expanded to 4 columns each")]),t._v(" "),s("div",{staticClass:"row"},[t._m(3),t._v(" "),s("expandColumns",{attrs:{columnBlocks:parseInt(t.columnBlocks),type:"template"},on:{ruleChange:t.handleRuleChange}})],1),t._v(" "),s("div",{staticClass:"row mt-3"},[t._m(4),t._v(" "),s("expandColumns",{attrs:{columnBlocks:parseInt(t.columnBlocks),type:"HgDna"},on:{ruleChange:t.handleRuleChange}})],1),t._v(" "),t._m(5)]),t._v(" "),s("div",{staticClass:"col-4"},[s("h6",{staticClass:"dropdown-header"},[t._v("PA Primers")]),t._v(" "),t._m(6),t._v(" "),t._m(7),t._v(" "),t._m(8),t._v(" "),s("div",{staticClass:"row mt-3"},[t._m(9),t._v(" "),s("div",{staticClass:"col mr-2"},[s("editableList")],1)])])]),t._v(" "),t._m(10)])])])},staticRenderFns:[function(){var t=this.$createElement,a=this._self._c||t;return a("a",{staticClass:"dropdown-toggle float-left",attrs:{href:"#","data-toggle":"dropdown"}},[this._v("Rules "),a("b",{staticClass:"caret"})])},function(){var t=this.$createElement,a=this._self._c||t;return a("div",{staticClass:"row"},[a("div",{staticClass:"col"},[a("span",{staticClass:"dropdown-header"},[this._v("Strains")])])])},function(){var t=this.$createElement,a=this._self._c||t;return a("div",{staticClass:"row mt-3"},[a("div",{staticClass:"col"},[a("span",{staticClass:"dropdown-header"},[this._v("ID Primers")])])])},function(){var t=this.$createElement,a=this._self._c||t;return a("div",{staticClass:"col"},[a("span",{staticClass:"dropdown-header"},[this._v("Template Copies")])])},function(){var t=this.$createElement,a=this._self._c||t;return a("div",{staticClass:"col"},[a("span",{staticClass:"dropdown-header"},[this._v("HgDna")])])},function(){var t=this.$createElement,a=this._self._c||t;return a("div",{staticClass:"row mt-3"},[a("div",{staticClass:"col"},[a("span",{staticClass:"dropdown-header"},[this._v("Dilution Factor")])]),this._v(" "),a("div",{staticClass:"col"}),this._v(" "),a("div",{staticClass:"col"},[a("input",{attrs:{placeholder:"values seperated by ','"}})])])},function(){var t=this.$createElement,a=this._self._c||t;return a("div",{staticClass:"row mt-3"},[a("div",{staticClass:"col"},[a("span",{staticClass:"dropdown-header"},[this._v("First Block")])]),this._v(" "),a("div",{staticClass:"col"},[a("select",[a("option",{attrs:{disabled:"",value:""}},[this._v("Please select one")]),this._v(" "),a("option",[this._v("Ec_uidA_6.x_Eco63_Eco60")]),this._v(" "),a("option",[this._v("PoolA")]),this._v(" "),a("option",[this._v("Ko_pehX_1.x_Kox05_Kox02")])])])])},function(){var t=this.$createElement,a=this._self._c||t;return a("div",{staticClass:"row mt-3"},[a("div",{staticClass:"col"},[a("span",{staticClass:"dropdown-header"},[this._v("Second Block")])]),this._v(" "),a("div",{staticClass:"col"},[a("select",[a("option",{attrs:{disabled:"",value:""}},[this._v("Please select one")]),this._v(" "),a("option",[this._v("Ec_uidA_6.x_Eco63_Eco60")]),this._v(" "),a("option",[this._v("PoolA")]),this._v(" "),a("option",[this._v("Ko_pehX_1.x_Kox05_Kox02")])])])])},function(){var t=this.$createElement,a=this._self._c||t;return a("div",{staticClass:"row mt-3"},[a("div",{staticClass:"col"},[a("span",{staticClass:"dropdown-header"},[this._v("Third Block")])]),this._v(" "),a("div",{staticClass:"col"},[a("select",[a("option",{attrs:{disabled:"",value:""}},[this._v("Please select one")]),this._v(" "),a("option",[this._v("Ec_uidA_6.x_Eco63_Eco60")]),this._v(" "),a("option",[this._v("PoolA")]),this._v(" "),a("option",[this._v("Ko_pehX_1.x_Kox05_Kox02")])])])])},function(){var t=this.$createElement,a=this._self._c||t;return a("div",{staticClass:"col"},[a("span",{staticClass:"dropdown-header"},[this._v("Custom")])])},function(){var t=this.$createElement,a=this._self._c||t;return a("div",{staticClass:"row"},[a("div",{staticClass:"input-group col-4 m-3"},[a("span",{staticClass:"input-group-addon",attrs:{id:"basic-addon1"}},[this._v("Suppress Columns")]),this._v(" "),a("input",{staticClass:"form-control",attrs:{type:"number",placeholder:"No of repeats","aria-label":"number","aria-describedby":"basic-addon1"}})])])}]},f=s("VU/8")({name:"rulesDropDown",data:function(){return{msg:"loaded rules drop down",currentDisplayStyle:{display:"relative","background-color":"rgba(0,0,0,0.7)",cursor:"pointer"},currentDisplayClass:["dropdown-menu","dropdown-menu-lg","w-100"],columnBlocks:4}},methods:{handleRuleClose:function(){this.currentDisplayClass.pop()},handleRuleChange:function(t,a){var s="template"==t?"SET_TEMPLATE":"SET_HGDNA";this.$store.commit(s+"_RULES",a),this.$store.commit(s+"_PLATE",a)}}},m,!1,null,null,null).exports,b={render:function(){this.$createElement;this._self._c;return this._m(0)},staticRenderFns:[function(){var t=this.$createElement,a=this._self._c||t;return a("div",{staticClass:"footer"},[a("div",{staticClass:"row"},[a("div",{staticClass:"col"},[a("a",[this._v("PA Master Mix")])]),this._v(" "),a("div",{staticClass:"col"},[a("a",[this._v("ID MAster Mix")])]),this._v(" "),a("div",{staticClass:"col"},[a("a",[this._v("Primers")])])]),this._v(" "),a("div",{staticClass:"row"},[a("div",{staticClass:"col"},[a("a",[this._v("Cycleing Pattern")])]),this._v(" "),a("div",{staticClass:"col"},[a("a",[this._v("Settings")])]),this._v(" "),a("div",{staticClass:"col"},[a("a",[this._v("Strains")])])])])}]},C=s("VU/8")({name:"Footer",data:function(){return{msg:"This is footer"}}},b,!1,function(t){s("mFHI")},"data-v-2fb89cf9",null).exports,g={name:"plateLayout",props:{templateData:Object,hgDNAData:Object,dilutionData:Object,strainData:Object,idPrimerData:Object},data:function(){return{msg:"This is plateLayout",rows:["A","B","C","D","E","F","G","H"],cols:[0,1,2,3,4,5,6,7,8,9,10,11]}}},w={render:function(){var t=this,a=t.$createElement,s=t._self._c||a;return s("div",{staticClass:"mt-3"},t._l(t.rows,function(a){return s("div",{staticClass:"row"},t._l(t.cols,function(e){return s("div",{staticClass:"col border border-primary"},[s("div",{staticClass:"row"},[t._v(t._s(a)+"--"+t._s(e+1))]),t._v(" "),t.templateData[a]&&t.templateData[a][e]?s("div",{staticClass:"row"},[s("div",{staticClass:"col"},[t._v(t._s(t.templateData[a][e])+" Cp")])]):t._e(),t._v(" "),t.hgDNAData[a]&&t.hgDNAData[a][e]?s("div",{staticClass:"row"},[s("div",{staticClass:"col"},[t._v(t._s(t.hgDNAData[a][e])+" hgDNA")])]):t._e(),t._v(" "),t.idPrimerData[a]&&t.idPrimerData[a][e]?s("div",{staticClass:"row"},[s("div",{staticClass:"col",staticStyle:{color:"green"}},[t._v(t._s(t.idPrimerData[a][e])+" ")])]):t._e(),t._v(" "),t.strainData[a]&&t.strainData[a][e]?s("div",{staticClass:"row"},[s("div",{staticClass:"col",staticStyle:{color:"red"}},[t._v(t._s(t.strainData[a][e]))])]):t._e()])}))}))},staticRenderFns:[]},k=s("VU/8")(g,w,!1,null,null,null).exports;s("UQ8B");e.a.component("rulesdropdown",f),e.a.component("customfooter",C),e.a.component("plateLayout",k);var E={name:"HelloWorld",data:function(){return{msg:"Welcome Bitch"}},computed:n()({},Object(l.b)({templateData:"getTemplate",hgDNAData:"gethgDNA",dilutionData:"getDilution",strainData:"getStrains",idPrimerData:"getIdPrimers"}))},D={render:function(){var t=this.$createElement,a=this._self._c||t;return a("div",{staticClass:"container-fluid"},[this._m(0),this._v(" "),a("div",{staticClass:"tab-content",attrs:{id:"myTabContent"}},[a("div",{staticClass:"tab-pane fade show active",attrs:{id:"Plate1",role:"tabpanel","aria-labelledby":"Plate-1"}},[a("rulesdropdown"),this._v(" "),a("plateLayout",{attrs:{templateData:this.templateData,idPrimerData:this.idPrimerData,strainData:this.strainData,hgDNAData:this.hgDNAData}}),this._v(" "),a("customfooter")],1),this._v(" "),a("div",{staticClass:"tab-pane fade",attrs:{id:"Plate2",role:"tabpanel","aria-labelledby":"Plate-2"}},[a("rulesdropdown"),this._v(" "),a("plateLayout",{attrs:{templateData:this.templateData,idPrimerData:this.idPrimerData,strainData:this.strainData,hgDNAData:this.hgDNAData}}),this._v(" "),a("customfooter")],1)])])},staticRenderFns:[function(){var t=this.$createElement,a=this._self._c||t;return a("ul",{staticClass:"nav nav-tabs"},[a("li",{staticClass:"nav-item"},[a("a",{staticClass:"nav-link active",attrs:{id:"Plate-1","data-toggle":"tab",href:"#Plate1"}},[this._v("Plate 1")])]),this._v(" "),a("li",{staticClass:"nav-item"},[a("a",{staticClass:"nav-link",attrs:{id:"Plate-2","data-toggle":"tab",href:"#Plate2"}},[this._v("Plate 2")])]),this._v(" "),a("li",{staticClass:"nav-item"},[a("a",{staticClass:"nav-link",attrs:{"data-toggle":"tab",href:"#"}},[this._v("+")])])])}]},y=s("VU/8")(E,D,!1,null,null,null).exports;e.a.use(i.a);a.a=new i.a({routes:[{path:"/",name:"Home",component:y}]})},mFHI:function(t,a,s){var e=s("SpqO");"string"==typeof e&&(e=[[t.i,e,""]]),e.locals&&(t.exports=e.locals);s("rjj0")("bebe35ac",e,!0)},nEJY:function(t,a,s){"use strict";s.d(a,"c",function(){return l}),s.d(a,"a",function(){return r}),s.d(a,"b",function(){return c});var e=s("gRE1"),i=s.n(e),o=s("M4fF"),n=s.n(o),l=function(t,a){return!n.a.isEmpty(a)&&a.split(",").length<=t},r=function(t,a,s,e,o,l){return t?e.map(function(t,s){return Math.floor(s/o)+1==a?l[0]:""}):i()(l).length!==o?i()(l).concat(n.a.times(o-i()(l).length,function(){return""})):i()(l)},c=function(t,a,s,e){return t?s.reduce(function(t,a){return t[a]=e,t},{}):s.reduce(function(t,s){return t[s]=n.a.times(a,function(){return e}).reduce(function(t,a){return t=t.concat(a)},[]),t},{})}},qb6w:function(t,a){}},["NHnr"]);
//# sourceMappingURL=app.b4f8afe482d40956d3f5.js.map