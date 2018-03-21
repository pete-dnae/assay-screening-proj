<template>

<div class="container-fluid w-75 text-white">
    <div class="jumbotron bg-dark">
        <div class="form-group row">
            <label  class="col-form-label">Experiment</label>
            <div class="col-2">
              <typeahead :data="USstate" placeholder="Experiment Name"></typeahead>
            </div>
            <div class="col-1 text-left">
              <a>copy</a>
            </div>
        </div>
        <div class="form-group row">
            <label  class="col-form-label">Designed by</label>
            <div class="col-2">
              <label class="col-form-label">PH</label>
            </div>
        </div>
        <div class="d-flex flex-row-reverse">
          <ul class="nav nav-pills nav-fill">
            <li class="nav-item">
              <a class="nav-link active" href="#">Experiment</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Reagents</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Plates</a>
            </li>
          </ul>
        </div>
    </div>
</div>

</template>

<script src="./experimentmenu.js"></script>
