<template>
  <div>
    <div class="row" v-for="rowId in rows">

      <div class="col">
        <span style="color:White">Start @</span>
      </div>
      <div class="col">
        <select v-model="selected[rowId]" @change="handleDropDownChange()">
          <option v-for="option in options" v-bind:value="option.value">
            {{ option.text }}
          </option>
        </select>
      </div>
      <div class="col">
        <input v-model="concentration[rowId]" placeholder="edit me">
      </div>
      <div class="col">
        <a class="btn btn-danger"  aria-label="Delete" @click="handleRowDelete(rowId)">
          <i class="fa fa-trash-o" aria-hidden="true"></i>
        </a>
      </div>
      <div class="col">
        <input v-model="rowRepeat[rowId]"  disabled>
      </div>
    </div>
    <div class="row">
      <div class="col float-right">
      <a class="btn btn-info"  aria-label="Add" @click="handleRowAdd()">
        <i class="fa fa-plus-square" aria-hidden="true"></i>
      </a>
    </div>
  </div>
  </div>
</template>
<script src="./expandcolumns.js"></script>
