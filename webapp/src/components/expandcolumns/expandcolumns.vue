<template>
  <div>
    <div class="row">
      <div class="col">
        <span>Start @</span>
      </div>
      <div class="col">
        <select v-model="selected">
          <option v-for="option in options" v-bind:value="option.value">
            {{ option.text }}
          </option>
        </select>
      </div>
      <div class="col">
        <input v-model="message" placeholder="edit me">
      </div>
      <div class="col">
        <a class="btn btn-danger"  aria-label="Delete">
          <i class="fa fa-trash-o" aria-hidden="true"></i>
        </a>
      </div>
      <div class="col">
        <input v-model="message"  disabled>
      </div>
    </div>
    <div class="row">
      <div class="col float-right">
      <a class="btn btn-info"  aria-label="Delete">
        <i class="fa fa-plus-square" aria-hidden="true"></i>
      </a>
    </div>
  </div>
  </div>
</template>
<script src="./expandcolumns.js"></script>
