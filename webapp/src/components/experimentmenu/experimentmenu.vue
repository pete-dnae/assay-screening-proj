<template>

<div class="container-fluid w-75 text-white">
    <div class="navbar navbar-dark bg-dark">
      <a class="navbar-brand">Assay Screening</a>
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
            <tooltip effect="scale" placement="bottom" content="Not sure what to say">
            <li class="nav-item">
              <a class="nav-link active" href="#/">Experiment</a>
            </li>
            </tooltip>
            <tooltip effect="scale" placement="bottom" content="Coming soon">
            <li class="nav-item">
              <a class="nav-link" href="#/pools">Pools</a>
            </li>
            </tooltip>
            <tooltip effect="scale" placement="bottom" content="Coming soon">
            <li class="nav-item">
              <a class="nav-link" href="#/reagents">Reagents</a>
            </li>
            </tooltip>
       
          </ul>
        </div>
    </div>
    <modal effect="fade/zoom" :value="showModal">
      <div class="form-group mx-sm-3 mb-2 ">
        <label class="text-primary float-left">Experiment Name :</label>
        <input type="text" :class="{'form-control':true,'is-invalid':invalidExpName}" v-model="experiment"/>
         <div :class="{'invalid-feedback':invalidExpName,'float-left':true}">
            Experiment name already taken
          </div>
      </div>
    <div slot="modal-footer" class="modal-footer">
      <button type="button" class="btn btn-default" @click="showModal = !showModal">Exit</button>
      <button type="button" class="btn btn-success" @click="handleSave(experiment)" :disabled="invalidExpName"> Save</button>    
    </div>
    </modal>
</div>

</template>

<script src="./experimentmenu.js"></script>
