<template>
<div class="container-fluid mt-2">
    <div class="row">
        <div class="col-6">
            <reagentGroup></reagentGroup>
        </div>
        <div class="col-6 h-100">
            <div class="card">
                <div class="card-body">
                    <div class="card-title">
                        <h5>Reagents <small class="fa fa-plus btn btn-primary" aria-hidden="true" @click="showAddForm=!showAddForm"></small></h5>
                        
                    </div>                                    
                        <hr/>
                        <alert :value="showErrors" placement="top" type="danger" width="400px" @close="showErrors=!showErrors" dismissable>
                            <span class="icon-info-circled alert-icon-float-left"></span>
                            <ul style="padding:0;list-style-type: none">
                                <li v-for="(message,value) in errors" v-bind:key="value">
                                   {{message}}    
                                </li>
                              </ul>  
                        </alert>    
                        <div class="m-3">            
                            <div v-if="reagents">
                                <div class="row text-left">
                                    <div class="col-4">
                                        <label>Search</label>
                                        <input v-model="searchText"/>
                                    </div>
                                    <div class="col-4">
                                        <select v-model="searchField" class="btn btn-primary" >
                                            <option value="null">Please select a Search Criteria</option>
                                            <option v-for="(key,value) in tableHeaders" v-bind:key="key" :value="value">{{key}}</option>                    
                                        </select>
                                    </div>
                                    <div class="col-4">
                                        
                                    </div>
                                </div>
                                <div class="pre-scrollable">
                                    <table class="text-left table table-striped">
                                        <th v-for="key in Object.keys(reagents[0])" v-bind:key="key">
                                            {{tableHeaders[key]}}                                                                                        
                                        </th>
                                        <tr v-for="reagent in filteredReagents" v-bind:key="reagent.name">
                                            <td v-for="(property,index) in reagent" v-bind:key="index">                                                
                                                <ul v-if="index==='opaque_json_payload'" style="padding:0;list-style-type: none">                                                    
                                                    <li v-for="item in  stringToList(property)" v-bind:key="item.key">
                                                        {{item.key}} {{item.value}}
                                                        
                                                    </li>
                                                </ul>
                                                <label v-else>{{property}}</label>
                                            </td>     
                                            <td>
                                                <i class="fa fa-trash-o btn btn-primary" aria-hidden="true" @click="handleReagentDelete(reagent)"></i>
                                            </td> 
                                            <td>
                                                <i class="fa fa-pencil btn btn-primary" aria-hidden="true" @click="prepReagentEdit(reagent)"></i>
                                            </td>                                 
                                        </tr>
                                        <tr v-if="filteredReagents.length==0"><td></td><td>No Results to show</td></tr>                 
                                    </table>
                                </div>
                            </div>
                            <div v-else>
                                No Reagents to Display
                            </div>
                        </div> 
                </div>
            </div>
        </div>
    </div>
    
    <div class="mt-3">        
        
        
    </div>
<modal v-model="showEditForm" large>
    <div slot="modal-header" class="modal-header">
        <h4 class="modal-title">
            Edit Reagent
        </h4>
    </div>
    <div class="row">        
        <reagentEditForm    :categoryOptions="reagentCategories" 
                            :currentReagent="selectedReagentData.name"
                            :currentCategory="selectedReagentData.category"
                            :opaquePayload="selectedReagentData.opaque_json_payload"
                            @reagentEdited="handleReagentEdit"
                            ></reagentEditForm>
    </div>
    <div slot="modal-footer" class="modal-footer">
        
  </div>
</modal>
<modal v-model="showAddForm" large>
    <div slot="modal-header" class="modal-header">
        <h4 class="modal-title">
            Add Reagent
        </h4>
    </div>
    <div>        
        <reagentCreateForm :categoryOptions="reagentCategories" 
        @reagentSubmit="handleReagentAdd"></reagentCreateForm>
    </div>
    <div slot="modal-footer" class="modal-footer">        
  </div>
</modal>
</div>
</template>
<script src="./reagentshome.js"></script>