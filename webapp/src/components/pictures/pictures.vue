<template>
<div>
    <h2 class="text-white">Plate Variables View</h2>    
    <div class="row mt-3 text-left">
        <div class="col-4">
            <select v-model="selected" class="float-left ml-3 btn btn-primary">
                <option disabled value="null">Please select one</option>
                <option v-for="(value,key) in experimentImages"  v-bind:key="key">{{key}}</option>
            </select>
        </div> 
        <div class="col">
            <button class="float-right btn btn-primary ml-3" @click="handleClose()">close</button>
            <button class="float-right btn btn-primary ml-3" @click="coloring =!coloring">
                <label v-if="coloring">Remove Coloring</label>
                <label v-else>Add Coloring</label>                
            </button>            
        </div>
    </div>   
    
    <div id='csvTable' class="mt-3" style="overflow-x:scroll"></div>
</div>
</template>
<script src="./pictures.js"></script>