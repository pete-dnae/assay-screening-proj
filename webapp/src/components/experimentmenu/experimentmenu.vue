<template>

<div class="container-fluid">
    <div class="jumbotron">
        <div class="form-group row">
            <label  class="col-form-label">Experiment</label>
            <div class="col-2">
              <select v-model="selected" class="btn btn-secondary dropdown-toggle">
                <option disabled value="">Please select one</option>
                <option>A</option>
                <option>B</option>
                <option>C</option>
              </select>
            </div>
            <div class="col-1 text-left">
              <a>copy</a>
            </div>
            <div class="col text-right">
              <a>Manage database</a>
            </div>
        </div>
        <div class="form-group row">
            <label  class="col-form-label">Designed by</label>
            <div class="col-2">
              <label class="col-form-label">PH</label>
            </div>
        </div>
        <div class="row d-flex justify-content-center">
          <ul class="nav nav-pills nav-fill">
            <li class="nav-item">
              <a class="nav-link active" href="#">Plates</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Primer Kit</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Strain Kit</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Robot</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Results</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Operator Notes</a>
            </li>
          </ul>
        </div>
    </div>
</div>

</template>

<script src="./experimentmenu.js"></script>
