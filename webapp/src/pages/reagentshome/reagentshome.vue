<template>
<div class="container-fluid mt-2">
    <div class="row">
        <div class="col-6">
            <reagentGroup></reagentGroup>
        </div>
        <div class="col-6 h-100">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Reagents</h5>        
                        <hr/>
                        <alert :value="showErrors" placement="top" duration="3000" type="danger" width="400px" dismissable>
                            <span class="icon-info-circled alert-icon-float-left"></span>
                            <ul>
                                <li v-for="(message,value) in errors" v-bind:key="value">
                                   {{value}} {{message}}    
                                </li>
                              </ul>  
                        </alert>    
                        <div class="m-3">            
                            <div v-if="reagents">
                                <div class="row text-left">
                                    <div class="col-5">
                                        <label>Search</label>
                                        <input v-model="searchText"/>
                                    </div>
                                    <div class="col-3">
                                        <select v-model="searchField" >
                                            <option value="null">Please select a Search Criteria</option>
                                            <option v-for="key in Object.keys(reagents[0])" v-bind:key="key">{{key}}</option>                    
                                        </select>
                                    </div>
                                    <div class="col-4">
                                        
                                    </div>
                                </div>
                                <div class="pre-scrollable">
                                    <table class="text-left table table-striped">
                                        <th v-for="key in Object.keys(reagents[0])" v-bind:key="key">
                                            {{key}}
                                        </th>
                                        <tr v-for="reagent in filteredReagents" v-bind:key="reagent.name">
                                            <td v-for="property in reagent" v-bind:key="property">
                                                {{property}}
                                            </td>     
                                            <td>
                                                <i class="fa fa-trash-o btn btn-primary" aria-hidden="true" @click="handleReagentDelete(reagent)"></i>
                                            </td> 
                                            <td>
                                                <i class="fa fa-pencil btn btn-primary" aria-hidden="true" @click="prepReagentEdit(reagent)"></i>
                                            </td>                                 
                                        </tr>
                                        <tr v-if="filteredReagents.length==0"><td></td><td>No Results to show</td></tr>
                                        <tr>
                                            <td v-for="key in Object.keys(reagents[0])" v-bind:key="key">
                                                <select v-if="key==='category'" v-model="addReagentData[key]">
                                                    <option value="null">Please select a category</option>
                                                    <option v-for="category in reagentCategories" v-bind:key="category.name">{{category.name}}</option>
                                                </select>
                                                <input v-model="addReagentData[key]" placeholder="Reagent Name" v-else/>
                                            </td>                                      
                                            <td>                                            
                                            </td>
                                            <td>                                            
                                                <i :class="{'fa':true, 'fa-plus':true,'btn':true,'btn-primary':!reagentAddEmpty,'btn-secondary':reagentAddEmpty}" 
                                                aria-hidden="true" @click="handleReagentAdd"></i>
                                            </td>
                                        </tr>
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
<modal v-model="showEditForm">
    <div slot="modal-header" class="modal-header">
        <h4 class="modal-title">
            Edit Reagent
        </h4>
    </div>
    <div class="row">        
        <div class="col form-group text-left" v-for="(value,key) in selectedReagentData" v-bind:key="key">
            <label>{{key}}</label>            
             <select v-if="key==='category'" v-model="selectedReagentData[key]">
                <option value="null">Please select a category</option>
                <option v-for="category in reagentCategories" v-bind:key="category.name">{{category.name}}</option>
            </select>
            <input type="text" v-model="selectedReagentData[key]" :disabled="key==='name'" v-else>
        </div>    
    </div>
    <div slot="modal-footer" class="modal-footer">
        <button type="button" class="btn btn-default" @click="showEditForm = false">Cancel</button>
        <button type="button" class="btn btn-success" @click="handleReagentEdit();showEditForm = false">Save</button>        
  </div>
</modal>
</div>
</template>
<script src="./reagentshome.js"></script>