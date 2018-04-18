<style scoped>
td:hover {
  background-color: #40a9e6e7 !important;
}
</style>
<template>

<div class="ml-5 border border-light rounded w-100" @mouseout="handleHoverLeave">
    <div class="bg-light">
        <div class="row text-left full-width">
                <div class="col-3">
                    <label class="m-3"><strong>{{currentPlate}}</strong></label>
                </div>
                <div class="col-9">
                    <div class="row">
                        <div class="col-1">
                            <i class="fa fa-lightbulb-o fa-2x btn" aria-hidden="true"></i>
                        </div>
                        <div class="col-11">
                            <tooltip effect="scale" placement="bottom" content="Click on a rule from your editor to highlight the area of impact for each rule">
                                <label class="text-info">Click on a &lt;A&gt; or &lt;T&gt; line</label>
                            </tooltip>    
                        </div>
                    </div>
                </div>
            </div>
            <div id="monitorMouseLeave" width="500px">            
            <table id="tableGoesHere" class="m-5 h-100" v-if="allocationMapping&&plateBoundaries[currentPlate]">
                <tr>
                    <td>
                    </td>
                    <td v-for="col in plateBoundaries[currentPlate].colCount" v-bind:key="col">
                        {{col}}
                    </td>
                </tr>
                <tr v-for="row in plateBoundaries[currentPlate].rowCount" v-bind:key="row">   
                    <td>
                        {{String.fromCharCode(row+64)}}
                    </td>             
                    <td v-for="col in plateBoundaries[currentPlate].colCount" v-bind:key="col" class="rounded">                                                            
                        <div  
                            class="bg-secondary border border-secondary  rounded p-3 m-1" 
                            @mouseover="handleShowCellContents([row,col])" 
                            v-if="isItemInArray(allocationMapping[highlightedLineNumber],[col,row])&&hoverHighlight">
                        </div>
                        <div  
                            class="bg-white border border-light rounded p-3 m-1" 
                            @mouseover="handleShowCellContents([row,col])" v-else>
                        </div>                                      
                    </td>
                </tr>
            </table>   
            </div> 
        </div>
        <div class="row w-100 mt-3">
            <div class="col-md-6">
                
            </div>
            <div class="col">
                <i class="fa fa-lightbulb-o fa-2x" aria-hidden="true"></i>
                <label class="text-info">Hover over a well</label>
            </div>                
        </div>    
    
</div>

</template>

<script src="./hovervisualizer.js"></script>
