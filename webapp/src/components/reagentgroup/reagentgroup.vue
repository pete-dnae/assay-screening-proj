<template>
<div>
  <div class="card">
                <div class="card-body">        
                    <h5 class="card-title">Pools</h5>            
                    <div class="d-flex justify-content-start  bg-dark">
                        <nav class="navbar navbar-dark">
                            <form class="form-inline">
                                <div class="input-group">   
                                    {{reagentGroupList}}     
                                <select v-model="currentReagentGroup" @change="handleReagentGroupSelection">
                                    <option value="null">Please select a pool name</option>
                                    <option v-for="reagentGroup in reagentGroupList" v-bind:key="reagentGroup">{{reagentGroup}}</option>                    
                                </select>
                                </div>
                            </form>
                            <nav class="nav nav-pills flex-column flex-sm-row">
                            <li class="nav-item active">
                                <a class="nav-link" href="#" @click="handleCreateNew">Create New</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="#" @click="show=!show">Save As</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="#" @click="handleReagentGroupDelete">Delete</a>
                            </li>
                            </nav>            
                        
                        </nav>
                    </div> 
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
                        <div id="handsonTable">
                    </div>   
                </div>    
            </div>    
        </div>
            <modal v-model="show" @ok="show=!show">
                <div slot="modal-header" class="modal-header">
                    <h4 class="modal-title">
                        <b>Provide Group Name</b>
                    </h4>
                </div>
                <div class="form-group">
                    <label class="float-left">Group Name :</label><input class="form-control" v-model="groupName"  type="text"/>
                </div>
                <div slot="modal-footer" class="modal-footer">
                    <button type="button" class="btn btn-default" @click="show=!show">Exit</button>
                    <button type="button" class="btn btn-success" @click="saveData();show=!show">Save</button>            
                </div>
            </modal>
    </div>
</template>
<script src='./reagentgroup.js'></script>
