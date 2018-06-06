<template>
    <div class="container-fluid">   
        <nav class="nav nav-pills nav-justified mt-3">
            <a :class="{'nav-link':true,active:showSummary}" href="javascript:;" @click="showSummary=!showSummary">Summary Table</a>
            <a :class="{'nav-link':true,active:!showSummary}" href="javascript:;" @click="showSummary=!showSummary">Master Table</a>            
        </nav>
        <div class="container-fluid" v-show="showSummary">
            
                <calcTable class="mt-3" :options="summaryHeaders" 
                                    :data="resultSummary" 
                                    ></calcTable> 
            
        </div>
            <div class="row" v-show="!showSummary">
                <div class="col-8">
            
                        <calcTable class="mt-3" :options="masterHeaders" 
                                    :data="resultMaster" 
                                    :columnsToColor="columnsToColor"
                                    :selectedRowProps="['qPCR Well','LC Well']"
                                    @multipleSelection="handleWellSelection">
                        </calcTable>
            
                </div>
                <div class="col-4">
                    <div id="ampGraph"></div>
                    <div id="meltGraph"></div>
                    <div id="labChipGraph"></div>
                    <div id="copyCountGraph"></div>
                </div>
                             
                
            </div>
            </div>
</template>
<script src='./wellsummary.js'></script>
<style scoped>
.movable {
    position: absolute;
    z-index: 9;
    background-color: #f1f1f1;
    border: 1px solid #d3d3d3;
    text-align: center;
}

#mydivheader {
    padding: 10px;
    cursor: move;
    z-index: 10;
    background-color: #2196F3;
    color: #fff;
}

</style>
