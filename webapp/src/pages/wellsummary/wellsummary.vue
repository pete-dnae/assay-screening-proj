<template>
    <div class="container-fluid">   
            <calcTable class="mt-3" :options="summaryHeaders" 
                                  :data="resultSummary" 
                                ></calcTable> 
        <calcTable class="mt-3" :options="masterHeaders" 
                                  :data="resultMaster" 
                                  :columnsToColor="columnsToColor"
                                  :selectedRowProps="['qPCR Well','LC Well']"
                                  @multipleSelection="handleWellSelection">

        </calcTable>
    
        <div class="row">
            <div class="col">
                <div id="ampGraph"></div>
            </div>
            <div class="col">
                <div id="meltGraph"></div>
            </div>
        </div>
        <div class="row">
            <div class="col">
                <div id="copyCountGraph"></div>
            </div>
            <div class="col">
                <div id="labChipGraph"></div>
            </div>
        </div>
            
            
            
            
        
    </div>
</template>
<script src='./wellsummary.js'></script>