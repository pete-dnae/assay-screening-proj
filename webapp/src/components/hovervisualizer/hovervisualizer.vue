<style scoped>
td:hover {
  background-color: #40a9e6e7 !important;
}
</style>


<template>

<div class="w-100">
    <div class="col  text-left">
        <div class="row">
            <label class="mt-2 col"><strong>{{currentPlate}}</strong></label>
            <div class="col">
                <i class="fa fa-lightbulb-o fa-2x btn" aria-hidden="true"></i>
                <label class="text-info">Hover over an &ltA&gt or &ltT&gt line</label>
            </div>
        </div>
        <table id="tableGoesHere" style="max-width:100%;height:auto" v-if="allocationMapping">
            <tr v-for="row in tableBoundaries[0]" v-bind:key="row">                
                <td v-for="col in tableBoundaries[1]" v-bind:key="col" class="rounded">
                    <div  v-if="row===1&&col!=1">
                        {{col-1}}
                    </div>       
                    <div  v-if="col===1&&row!=1">
                        {{String.fromCharCode(row+63)}}
                    </div>                                    
                    <div id="cell" class="bg-secondary border border-secondary  rounded p-3 m-1" @mouseover="handleShowCellContents([row-1,col-1])" v-if="isItemInArray(allocationMapping[highlightedLineNumber],[col-1,row-1])">

                    </div>
                    <div id="cell" class="bg-light border border-light rounded p-3 m-1" @mouseover="handleShowCellContents([row-1,col-1])" v-if="!isItemInArray(allocationMapping[highlightedLineNumber],[col-1,row-1])&&row!=1&&col!=1">

                    </div>                  
                    
                </td>
            </tr>
        </table>
        <wellcontents class="mt-3" v-if="currentRow&&currentCol" 
                                :currentRow="currentRow" 
                                :currentCol="currentCol" 
                                :allocationData="allocationData[currentPlate]">
                                </wellcontents>
    </div>
</div>

</template>

<script src="./hovervisualizer.js"></script>
