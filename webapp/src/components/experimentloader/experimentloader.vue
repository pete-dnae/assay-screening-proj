<template>
  <div class="container">
    <div class="row">
      <div class="col">
        <h5>Title</h5>
      </div>
      <div class="col">
        <input type="text">
      </div>
      <div class="col">
        <i class="fa fa-search" aria-hidden="true"></i>
      </div>
    </div>
    <div class="row mt-3">

        <select class="w-100" v-model="currentExpt" stacked>
          <option>A81_E004</option>
          <option>A81_E005</option>
          <option>A81_E008</option>
        </select>
        <br>
        <span>Selected Expt: {{ currentExpt }}</span>

    </div>
  </div>
</template>
<script src="./experimentloader.js"></script>
