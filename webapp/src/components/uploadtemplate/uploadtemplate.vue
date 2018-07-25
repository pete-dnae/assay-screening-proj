<template>
<div>
    <modal title="File Upload" effect="fade/zoom" large :value="show">
    <loader v-if="isPosting"></loader>
            <form>
                <div class="row">
                    <div class="col">
                         <div class="form-group text-left">
                            <label>Select PA Mastermix</label>
                                <select class="form-control" v-model="paMastermix">
                                    <option v-for="pool in availablePools" v-bind:key="pool">{{pool}}</option>                 
                                </select>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-group text-left">
                            <label>Select ID Mastermix</label>
                            <select class="form-control" v-model="idMastermix">
                                <option v-for="pool in availablePools" v-bind:key="pool">{{pool}}</option>                 
                            </select>
                        </div>
                    </div>
                </div>
                 <div class="row">
                    <div class="col">
                         <div class="form-group text-left">
                            <label>PA Primer Conc and Unit</label>
                            <div class="row">
                                <div class="col">
                                    <input type="text" v-model="paConc" placeholder="Concentration"/>
                                </div>
                                <div class="col mt-2">
                                    <input type="text" v-model="paUnit" placeholder="Unit"/>
                                </div>                               
                            </div>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-group text-left">
                            <label>ID Primer Conc and Unit</label>
                             <div class="row">
                                <div class="col">
                                    <input type="text" v-model="idConc" placeholder="Concentration"/>
                                </div>
                                <div class="col mt-2">
                                    <input type="text" v-model="idUnit" placeholder="Unit"/>
                                </div>                               
                            </div>                           
                        </div>
                    </div>
                </div>
                 <div class="row">
                    <div class="col-6">
                         <div class="form-group text-left">
                            <label class="d-block">Dilution</label>
                                <input type="text" placeholder="dilution" v-model="dilution">
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="form-group text-left">
                            <label class="d-block">Excel File</label>
                                <input type="file" placeholder="dilution" id='templateFile'>
                        </div>
                    </div>
                </div>
               
            </form>
            <div class="row mt-3 text-left">
                <div class="col">
                    <button @click="handleTemplateUpload">Upload Template File</button>
                </div>                    
            </div>
            
            <p id="info"></p>
            <div class="text-left">
                    <textarea rows="4" cols="90" v-model="uploadFeedBack" disabled></textarea>
            </div>
            <div slot="modal-footer" class="modal-footer">
                
                <button type="button" class="btn btn-default" @click="handleExit">Exit</button>
            </div>
        </modal>
</div>
</template>
<script src="./uploadtemplate.js"></script>