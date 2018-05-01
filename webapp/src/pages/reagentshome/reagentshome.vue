<template>
<div class="container-fluid mt-2">
    <div class="d-flex justify-content-start  bg-dark">
        <nav class="navbar navbar-dark">
            <form class="form-inline">
                <div class="input-group">   
                    {{reagentGroupList}}     
                <select v-model="currentReagentGroup" @change="handleReagentGroupSelection">
                    <option value="null">Please select one</option>
                    <option v-for="reagentGroup in reagentGroupList" v-bind:key="reagentGroup">{{reagentGroup}}</option>                    
                </select>
                </div>
            </form>
            
            <nav class="nav nav-pills flex-column flex-sm-row">
            <li class="nav-item active">
                <a class="nav-link" href="#">Create</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#" @click="show=!show">Save-As</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#">Delete</a>
            </li>
            </nav>            
        
        </nav>
    </div>
    <div class="mt-3">        
        
        <div class="w-50 mt-3">            
            <div id="handsonTable"></div>       
        </div>
    </div>
    <modal v-model="show" @ok="show=!show">
        <div slot="modal-header" class="modal-header">
            <h4 class="modal-title">
                <b>Provide Group Name</b>
            </h4>
        </div>
        <div class="form-group">
            <label class="float-left">Group Name :</label><input class="form-control" v-model="groupName"  type="text"/>
        </div>
        <div slot="modal-footer" class="modal-footer">
            <button type="button" class="btn btn-default" @click="show=!show">Exit</button>
            <button type="button" class="btn btn-success" @click="getData();show=!show">Custom Save</button>            
        </div>
    </modal>
</div>
</template>
<script src="./reagentshome.js"></script>