<template>

<div class="container-fluid w-75 text-white">
    <div class="navbar navbar-dark bg-dark">
        <div class="form-inline my-2 my-lg-0">            
            <tooltip effect="scale" placement="left" content="Search your experiment here">            
              <typeahead class="form-control mr-sm-2" 
              :data="data" placeholder="Experiment Name"
              :value="currentExperiment"></typeahead>
            </tooltip>
            <div class="btn  my-2 my-sm-0">  
              <tooltip effect="scale" placement="right" content="To save your current script under different experimt name">            
              <p><a href="#" class="text-primary">Save As</a></p>
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
</div>

</template>

<script src="./experimentmenu.js"></script>
