<template>
<div>
    <modal title="Delete Results" effect="fade/zoom" large :value="show">    
            <div class="row text-left">
                <div class="col">                    
                    <input type="text" class="d-block" placeholder="No Plate Name Chosen" v-model="plateName" disabled/>
                    <small id="info">To choose a plate click on a plate from rule script</small>
                </div>                
            </div>
            <div class="row mt-3 text-left">
                <div class="col">
                    <button class="btn btn-danger" @click="handleLabchipDelete">Delete Labchip Data</button>
                </div>
                <div class="col">
                    <button class="btn btn-danger" @click="handleQpcrDelete">Delete Qpcr Data</button>
                </div>             
            </div>
            
            <p id="info"></p>
            <div class="text-left">
                    <textarea rows="4" cols="90" v-model="DeleteFeedBack"></textarea>
            </div>
            <div slot="modal-footer" class="modal-footer">
                
                <button type="button" class="btn btn-default" @click="handleExit">Exit</button>
            </div>
        </modal>
</div>
</template>
<script src='./destroyer.js'></script>
