<template>
    <div class="container-fluid">   
            <div class="row">
                <table class="table m-3 text-left w-50">
                    <tr>
                        <td>
                            <label>Experiment</label> 
                        </td>
                        <td>
                            <label>{{experimentId}}</label>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label>Plate</label> 
                        </td>
                        <td>
                            <label>{{plateId}}</label>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label>Wells</label> 
                        </td>
                        <td>
                            <label>{{wells}}</label>
                        </td>
                    </tr>
                </table>
                
            </div>
            <div class="row">
                <div class="col">
                    <h4 class="text-left">Summary Table</h4>
                    <calcTable class="mt-3" :options="summaryHeaders" 
                                    :data="resultSummary" 
                                    ></calcTable> 
                </div>
            </div>
            <div class="row" >
                <div class="col-8">                   
                    <h4 class="text-left">Master Table</h4>
                        <calcTable class="mt-3" :options="masterHeaders" 
                                    :data="resultMaster" 
                                    :columnsToColor="columnsToColor"
                                    :selectedRowProps="['qPCR Well','LC Well']"
                                    @multipleSelection="handleWellSelection">
                        </calcTable>
            
                </div>
                <div class="col-4">
                    <h4 class="text-left">Graphs</h4>
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
