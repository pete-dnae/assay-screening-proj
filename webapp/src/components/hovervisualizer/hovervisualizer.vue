

<template>

<div class="w-100">
    <div class="col  text-left">
        <h5 class="text-left"><strong>Plate Visualization</strong></h5>
        <strong class="d-block">User Selection</strong>
        <div class="row">
            <label class="mt-2 col">Plate Name :{{currentPlate}}</label>
            <div class="col">
                <i class="fa fa-lightbulb-o fa-2x btn" aria-hidden="true"></i>
                <label>Hover over a line</label>
            </div>
        </div>
        <table id="tableGoesHere" style="max-width:100%;height:auto" v-if="allocationMapping">
            <tr v-for="row in tableBoundaries[0]" v-bind:key="row">
                <td v-for="col in tableBoundaries[1]" v-bind:key="col">
                    <div class="bg-secondary border border-secondary  rounded p-3 ml-1" @mouseover="handleShowCellContents([row,col])" v-if="isItemInArray(allocationMapping[highlightedLineNumber],[col,row])">

                    </div>
                    <div class="bg-light border border-light rounded p-3 ml-1" @mouseover="handleShowCellContents([row,col])" v-else>

                    </div>
                </td>
            </tr>
        </table>
        <wellcontents class="mt-3" v-if="allocationData" :currentRow="currentRow" :currentCol="currentCol" :allocationData="allocationData[currentPlate]"></wellcontents>
    </div>
</div>

</template>

<script src="./hovervisualizer.js"></script>
