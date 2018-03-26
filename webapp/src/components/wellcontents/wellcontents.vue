

<template>

<div class="w-100" v-if="allocationData">
    <div class="row">
        <h5 class="col"><strong>Contents of {{String.fromCharCode(currentRow+64)}}{{currentCol}}</strong></h5>
        <div class="col">
            <i class="fa fa-lightbulb-o fa-2x btn" aria-hidden="true"></i>
            <label class="text-info">Hover over a well</label>
        </div>
    </div>
    <div class="mt-4">        
      <transition-group name="zoomIn" enter-active-class="animated zoomIn"
      leave-active-class="animated zoomOut" tag="p">
      
        <li class="row" v-for="elem in allocationData[currentCol][currentRow]" v-bind:key="elem[0]">
            <label class="col-3" v-for="entity in elem" v-bind:key="entity">{{entity}}</label>
        </li>
      </transition-group>




    </div>
</div>

</template>

<script src="./wellcontents.js"></script>
