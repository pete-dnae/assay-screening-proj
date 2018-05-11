<template>
<div>
  <div class="card">
                <div class="card-body">        
                    <h5 class="card-title">Reagent Groups</h5>            
                    <div class="d-flex justify-content-start  bg-dark">
                        <div class="form-inline my-2 my-lg-0">                   
                            <typeahead 
                                :data="reagentGroupList" placeholder="Reagent Group Name"
                                :on-hit="handleReagentGroupSelection"
                                :value="currentText"></typeahead>
                        </div>                        
                        <nav class="navbar navbar-dark">         
                            
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
                         
                    
                    <div class="row">                            
                        <div class="col text-left">
                            <i class="fa fa-lightbulb-o" aria-hidden="true"></i>
                            <small>
                                Treat the below table as a spreadsheet . Right click for options
                            </small>
                        </div>
                    </div>          
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
            <alert :value="showErrors" placement="top" type="danger" width="400px" @close="showErrors=!showErrors" dismissable>
                            <span class="icon-info-circled alert-icon-float-left"></span>
                         {{errors}}
            </alert>     
    </div>
</template>
<script src='./reagentgroup.js'></script>
