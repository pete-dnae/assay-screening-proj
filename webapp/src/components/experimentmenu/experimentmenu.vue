<template>

<div class="container-fluid w-75 text-white">
    <div class="navbar navbar-dark bg-dark">
        <div class="form-inline my-2 my-lg-0">            
            
              <typeahead class="form-control mr-sm-2" 
              :data="data" placeholder="Experiment Name"
              :value="currentExperiment"></typeahead>
            
            <div class="btn  my-2 my-sm-0">              
              <p><a href="#" class="text-primary">Save As</a></p>
            </div>
        </div>
        <div class="d-flex flex-row-reverse">
          <ul class="nav nav-pills nav-fill">
            <li class="nav-item">
              <a class="nav-link active" href="#/">Experiment</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#/reagents">Reagents</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#/pools">Pools</a>
            </li>
          </ul>
        </div>
    </div>
</div>

</template>

<script src="./experimentmenu.js"></script>
