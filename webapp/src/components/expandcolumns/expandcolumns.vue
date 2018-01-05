<template>
  <div>
    <div class="row" v-for="rowId in rows" >
    <div class="row ml-1 mr-2">
      <div class="col">
        <span>Start @</span>
      </div>
      <div class="col">
        <select v-model="data[rowId].startAt" @change="changeAllocationRules()">
          <option v-for="option in options" v-bind:value="option.value">
            {{ option.text }}
          </option>
        </select>
      </div>
      <div class="col-3">
        <input style="width:75px" :id="rowId+type" v-model="data[rowId].concentration" @keyup.enter="changeAllocationRules()" >
      </div>

      <div class="col">
        <a class="btn btn-danger"  aria-label="Delete" @click="handleRowDelete(rowId)">
          <i class="fa fa-trash-o" aria-hidden="true"></i>
        </a>
      </div>
      <div class="col">
      <a class="btn btn-info"  aria-label="table" @click="showModal = true;currentRowId=rowId">
        <i class="fa fa-table" aria-hidden="true"></i>
      </a>
    </div>
    </div>
    <hr/>
  </div>
<div class="row ml-2 mt-3 mr-2">
      <a class="btn btn-info w-100"  aria-label="Add" @click="handleRowAdd()">
        <i class="fa fa-plus-square" aria-hidden="true"></i>
      </a>
  </div>
  <div class="row mt-3">
    <div class="col">
      Rows
    </div>
    <div class="col">
      Concentration
    </div>
  </div>
  <div class="mt-3 row" v-for="rowId in rows">
    <div class="col"  >
      <label>{{data[rowId].allRows[0]}}--{{data[rowId].allRows[data[rowId].allRows.length-1]}}</label>
    </div>
    <div class="col"  >
      <label>{{data[rowId].concentration}}</label>
    </div>
  </div>
  <hr/>
    <modal v-model="showModal">
      <div slot="modal-header" class="modal-header">
        <h4 class="modal-title">Mention Block Number</h4>
      </div>
      <div slot="modal-body" class="modal-body">
        <div class="row">
          <div v-for="n in columnBlocks" v-if="showModal" class="col">
            <input type="radio" :id="n" :value="n" v-model="data[currentRowId].blockNo" @click="showModal = false">
            <label>{{n}}</label>
          </div>
        </div>
      </div>
    </modal>
  </div>
</template>
<script src="./expandcolumns.js"></script>
