<template>
<div>
    <modal title="File Upload" effect="fade/zoom" large :value="show">
    <loader v-if="isPosting"></loader>
            <div class="row text-left">
                <div class="col">                    
                    <input type="text" class="d-block" placeholder="No Plate Name Chosen" v-model="plateName" disabled/>
                    <small id="info">To choose a plate click on a plate from rule script</small>
                </div>
                <div class="col">
                    <input type="file" class="d-block" id="fileLoad" @change="getFileInfo"/>
                    <small id="info"></small>
                </div>
                
            </div>
            <div class="row mt-3 text-left">
                <div class="col">
                    <button @click="handleLabchipUpload" :disabled="disableUpload">Upload Labchip Data</button>
                </div>
                <div class="col">
                    <button @click="handleQpcrUpload" :disabled="disableUpload">Upload Qpcr Data</button>
                </div>             
            </div>
            <p id="info"></p>
            <div class="text-left">
                    <textarea rows="4" cols="90" v-model="uploadFeedBack"></textarea>
            </div>
            <div slot="modal-footer" class="modal-footer">
                
                <button type="button" class="btn btn-default" @click="handleExit">Exit</button>
            </div>
        </modal>
</div>
</template>
<script src="./fileupload.js"></script>