<template>
  <div>
    <input type="text" class="w-100" v-model="val">
    <div class="list-group" v-if="showDropdown">
      <a v-for="(item, i) in result"
      class="list-group-item list-group-item-action"
      @click="handleSelection(item[prop])">
        {{item[prop]}}
      </a>
    </div>
    <div class="row mt-2">
      <div class="col">
        <button class="btn btn-info" @click="handleCopyExperiment">Copy and Load</button>
      </div>
      <div class="col">
        <button class="btn btn-info" @click="handleBack">Back</button>
      </div>
    </div>
  </div>
</template>
<script src="./typeahead.js"></script>
