<template>
<div>
    <div class="row mt-3 text-left">
        <div class="col-4">
            <select v-model="selected" class="float-left ml-3 btn btn-primary">
                <option disabled value="null">Please select one</option>
                <option v-for="(value,key) in experimentImages"  v-bind:key="key">{{key}}</option>
            </select>
        </div>
        <div class="col-4" v-show="selected">
            <i class="fa fa-lightbulb-o fa-2x btn" aria-hidden="true"></i>       
            <label class="text-info">Right click to save image</label>
        </div>
    </div>
<img :src="image" class="mt-3" style='height: 100%; width: 100%; object-fit: contain'/>
</div>
</template>
<script src="./pictures.js"></script>