<template>
<div>
    <ul class="list-group m-3">
      <div class="row" v-for="rowId in rows">
        <div class="col">
        <li class="list-item" style="background-color: rgba(0,0,0,0);">{{listItem[rowId][type]}}</li>
        </div>
        <div class="col">
          <a class="btn btn-danger"  aria-label="delete"  @click="handleListDelete(rowId)">
            <i class="fa fa-trash-o" aria-hidden="true"></i>
          </a>
        </div>
      </div>

        <a class="btn btn-info float-right mt-3"  aria-label="Add" @click="showModal=true">
          <i class="fa fa-plus-square" aria-hidden="true"></i>
        </a>

    </ul>
    <modal v-model="showModal">
      <div slot="modal-header" class="modal-header">
        <h4 class="modal-title">{{type}} Name</h4>
      </div>
      <div slot="modal-body" class="modal-body">
        <div class="row">
            <div class="col mt-3">
              <div class="row ml-2">
              <input type="text" placeholder="Enter Name" v-model="modalText">
              </input>
            </div>
              <div class="row mt-5" v-if="repeatOption=='block'">
                <span>Specify Block No</span>
                <div v-for="n in columnBlocks">
                  <input type="radio" :id="n" :value="n" v-model="blockNo">
                  <label>{{n}}</label>
                </div>
              </div>
            </div>
            <div class="col">
              <div class="row">
              <input type="radio" id="one" value="column" v-model="repeatOption">
                <img src="src\assets\bycol.JPG">
              </div>
              <br>
              <br>
              <div class="row">
              <input type="radio" id="two" value="block" v-model="repeatOption">
                <img src="src\assets\byblock.JPG">
            </div>

        </div>
      </div>
      </div>
      <div slot="modal-footer" class="modal-footer">
        <button @click="showModal = false">Close</button>
        <button @click="handleListAdd(modalText);showModal = false">Add</button>
      </div>
    </modal>
</div>
</template>
<script src="./editablelist.js"></script>
