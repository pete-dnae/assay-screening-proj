<style scoped>
td:hover {
  background-color: #40a9e6e7 !important;
}
</style>
<template>

<div class="w-100">
    <div class="row text-left">
            <label class="mt-2 col"><strong>{{currentPlate}}</strong></label>
            <div class="col">
                <i class="fa fa-lightbulb-o fa-2x btn" aria-hidden="true"></i>
                <label class="text-info">Hover over an &lt;A&gt; or &lt;T&gt; line</label>
            </div>
        </div>
        <div @mouseout="handleHoverLeave">
        <table id="tableGoesHere" class="m-5 h-100" v-if="allocationMapping">
            <tr>
                <td>
                </td>
                <td v-for="col in tableBoundaries[1]" v-bind:key="col">
                    {{col}}
                </td>
            </tr>
            <tr v-for="row in tableBoundaries[0]" v-bind:key="row">   
                <td>
                    {{String.fromCharCode(row+64)}}
                </td>             
                <td v-for="col in tableBoundaries[1]" v-bind:key="col" class="rounded">                                                            
                    <div id="cell" class="bg-secondary border border-secondary  rounded p-3 m-1" @mouseover="handleShowCellContents([row,col])" v-if="isItemInArray(allocationMapping[highlightedLineNumber],[col,row])&&hoverHighlight">
                    </div>
                    <div id="cell" class="bg-light border border-light rounded p-3 m-1" @mouseover="handleShowCellContents([row,col])" v-else>
                    </div>                                      
                </td>
            </tr>
        </table>   
        </div>     
    
</div>

</template>

<script src="./hovervisualizer.js"></script>
