<template>

<div class="container-fluid">
    <div class="navbar navbar-dark bg-dark">
      <a class="navbar-brand text-white">Assay Screening</a>      
        <div class="form-inline my-2 my-lg-0">                   
            <tooltip effect="scale" placement="left" content="Search your experiment here">            
              <typeahead class="form-control mr-sm-2" 
              :data="data" placeholder="Experiment Name"
              :on-hit="loadExperimentFromName"
              :value="currentExperiment"></typeahead>
            </tooltip>
            <div class="btn  my-2 my-sm-0">  
              <tooltip effect="scale" placement="right" content="To save your current script under different experiment name">            
              <p><a href="#" class="text-primary" @click="showModal=!showModal">Save As</a></p>
              </tooltip>
            </div>
        </div>
        <div class="d-flex flex-row-reverse">
          <ul class="nav nav-pills nav-fill">
            <tooltip effect="scale" placement="bottom" content="Create and edit experiments">
            <li class="nav-item">
              <a :class="{'nav-link':true,active:checkActive('experimenthome')}" @click="redirect('/experiment')" href="javascript:">Experiment</a>
            </li>
            </tooltip>
            <tooltip effect="scale" placement="bottom" content="Edit database entities here">
            <li class="nav-item">
              <a :class="{'nav-link':true,active:checkActive('reagentHome')}"  @click="redirect('/maintenance')"  href="javascript:">Maintenance</a>
            </li>
            </tooltip> 
            <li class="nav-item">
              <a :class="{'nav-link':true,active:checkActive('resultsHome')}" @click="redirect('/results')"  href="javascript:">Experiment Results</a>
            </li>     
          </ul>
        </div>
    </div>
    <div class="row mt-3" v-show="user">
      <div class="col-md-8">
      </div>
      <div class="col text-right">   
        
          <i class="fa fa-user-circle-o fa-2x mr-2" aria-hidden="true"></i>
        
        <label class="text-primary mr-2">{{user}}</label>
        
          <i class="fa fa-sign-out fa-2x" aria-hidden="true" @click="handleLogOut"></i>
        
      </div>
      </div>
    <modal effect="fade/zoom" :value="showModal">
      <div class="form-group mx-sm-3 mb-2 ">
        <label class="text-primary float-left">Experiment Name :</label>
        <input type="text" :class="{'form-control':true,'is-invalid':invalidExpName||experimentNameTaken}" v-model="experiment"/>
        <label class="text-primary text-left mt-3 d-block">Experiment Type :</label>        
        <select class="btn btn-primary" v-model="experimentType">
          <option>nested</option>
          <option>vanilla</option>
        </select>
         <div :class="{'invalid-feedback':invalidExpName||experimentNameTaken,'float-left':true}">
            <label v-if="experimentNameTaken">Experiment name already taken</label>
            <label v-if="invalidExpName">Experiment name should contain characters within 'a-z','A-Z','0-9','_',' '</label>
          </div>
      </div>
    <div slot="modal-footer" class="modal-footer">
      <button type="button" class="btn btn-default" @click="showModal = !showModal">Exit</button>
      <button type="button" class="btn btn-success" @click="handleSave(experiment,experimentType)" :disabled="invalidExpName||experimentNameTaken"> Save</button>    
    </div>
    </modal>
</div>

</template>

<script src="./experimentmenu.js"></script>
