<template>
<div>
    <ul class="list-group m-3">
      <div class="row" v-for="rowId in rows">
        <div class="col">
        <li class="list-group-item" style="background-color: rgba(0,0,0,0);color:white">{{listItem[rowId]}}</li>
        </div>
        <div class="col">
          <a class="btn btn-info"  aria-label="delete"  @click="handleListDelete(rowId)">
            <i class="fa fa-trash-o" aria-hidden="true"></i>
          </a>
        </div>
      </div>
      <div class="row">
        <div class="col float-right">
        <a class="btn btn-info"  aria-label="Add" @click="showModal=true">
          <i class="fa fa-plus-square" aria-hidden="true"></i>
        </a>
        </div>
      </div>

    </ul>
    <modal v-model="showModal">
      <div slot="modal-header" class="modal-header">
        <h4 class="modal-title">Strain Name</h4>
      </div>
      <div slot="modal-body" class="modal-body"><input type="text" v-model="modalText"></input></div>
      <div slot="modal-footer" class="modal-footer">
        <button @click="showModal = false">Close</button>
        <button @click="handleListAdd(modalText);showModal = false">Add</button>
      </div>
    </modal>
</div>
</template>
<script src="./editablelist.js"></script>
