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
            <button class="float-right btn btn-primary" @click="handleClose()">close</button>
        </div>
    </div>   
    
    <div id='csvTable' class="mt-3"></div>
</div>
</template>
<script src="./pictures.js"></script>