<template>
  <div class="container">
  <div slot="modal-header" class="modal-header">
    <h4 class="modal-title">
      <i>Load Experiment</i>
    </h4>
  </div>
  <div slot="modal-body" class="modal-body">
    <div class="row">
      <div class="col">
        <button type="button" class="btn btn-primary btn-lg">Create new experiment</button>
      </div>
      <div class="col">
          <button v-if="!showTypehead" type="button" class="btn btn-primary btn-lg" @click="showTypehead=!showTypehead">Copy existing experiment</button>
          <typeahead @typeaheadBack="handleTypeheadBack" v-if="showTypehead" :options="expts"  :prop="'experiment_name'"></typeahead>
      </div>
    </div>
  </div>
  </div>
</template>
<script src="./experimentloader.js"></script>
