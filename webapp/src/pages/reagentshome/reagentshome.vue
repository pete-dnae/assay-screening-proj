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
                                <table class="text-left table table-striped pre-scrollable">
                                    <th v-for="key in Object.keys(reagents[0])" v-bind:key="key">
                                        {{key}}
                                    </th>
                                    <tr v-for="reagent in filteredReagents" v-bind:key="reagent.name">
                                        <td v-for="property in reagent" v-bind:key="property">
                                            {{property}}
                                        </td>     
                                        <td>
                                            <i class="fa fa-trash-o btn" aria-hidden="true" @click="handleReagentDelete(reagent)"></i>
                                        </td> 
                                        <td>
                                            <i class="fa fa-pencil btn" aria-hidden="true" @click="handleReagentEdit(reagent)"></i>
                                        </td>                                 
                                    </tr>
                                    <tr>
                                        <td>
                                            <input/>
                                        </td>
                                        <td>
                                            <input/>
                                        </td>
                                        <td>                                            
                                        </td>
                                        <td>
                                            <i class="fa fa-plus btn" aria-hidden="true"></i>
                                        </td>
                                    </tr>
                                </table>
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
<modal v-model="showEditForm" @ok="showEditForm = false">
    <div slot="modal-header" class="modal-header">
        <h4 class="modal-title">
            Edit Reagent
        </h4>
    </div>
    <div class="row">        
        <div class="col form-group text-left" v-for="(value,key) in selectedReagentData" v-bind:key="key">
            <label>{{key}}</label>
            <input type="text" v-model="selectedReagentData[key]">
        </div>    
    </div>
</modal>
</div>
</template>
<script src="./reagentshome.js"></script>