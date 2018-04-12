

<template>

<div class="w-100 ml-5 border border-light rounded bg-light" v-if="allocationData">
    <div class="row">
        <label class="col text-left "><strong>Contents of </strong><strong>{{String.fromCharCode(currentRow+64)}}{{currentCol}} </strong></label>
        <div class="col">            
        </div>
    </div>
    
    <div class="mt-4" v-if="allocationData[currentCol]&&allocationData[currentCol][currentRow]">        
      <transition-group name="zoomIn" enter-active-class="animated zoomIn"
      leave-active-class="animated zoomOut">
      
        <li class="row" v-for="elem in allocationData[currentCol][currentRow]" v-bind:key="elem[0]">
            <label class="col-5 text-left" >{{elem[0]}}</label>
            <label class="col-2" >{{elem[1]}}</label>
            <label class="col-2" >{{elem[2]}}</label>
        </li>
      </transition-group>




    </div>
    <div class="mt-4" v-else>
        <label class="text-primary"><strong>Well Empty</strong></label>
    </div>
</div>

</template>

<script src="./wellcontents.js"></script>
