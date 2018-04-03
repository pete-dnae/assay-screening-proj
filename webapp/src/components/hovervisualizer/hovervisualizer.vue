<style scoped>
td:hover {
  background-color: #40a9e6e7 !important;
}
</style>
<template>

<div class="w-100" @mouseout="handleHoverLeave">
    <div class="row text-left">
            <label class="mt-2 col"><strong>{{currentPlate}}</strong></label>
            <div class="col">
                <i class="fa fa-lightbulb-o fa-2x btn" aria-hidden="true"></i>
                <tooltip effect="scale" placement="bottom" content="Hover over the rules on your editor to highlight the area of impact for each rule">
                    <label class="text-info">Hover over an &lt;A&gt; or &lt;T&gt; line</label>
                </tooltip>    
            </div>
        </div>
        <div id="monitorMouseLeave">
        <table id="tableGoesHere" class="m-5 h-100" v-if="allocationMapping">
            <tr>
                <td>
                </td>
                <td v-for="col in tableColCount" v-bind:key="col">
                    {{col}}
                </td>
            </tr>
            <tr v-for="row in tableRowCount" v-bind:key="row">   
                <td>
                    {{String.fromCharCode(row+64)}}
                </td>             
                <td v-for="col in tableColCount" v-bind:key="col" class="rounded">                                                            
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
