<template>
  <modal title="Well Annotations Pane" effect="fade/zoom" large :value="showAnnotator">    
  <h5 class="text-left">Selection</h5> 
  <loader v-if="isPosting"></loader>
    <div class="row text-left">
        <div class="col" v-if="qpcrSelection">
            <strong class="d-block">qPCR Wells</strong>
            <select v-model="qpcrSelection" class="ml-3 w-50" multiple>
                <option v-for="op in qpcrWells" v-bind:key="op.text" v-bind:value="op.value">
                   {{op.text}}
                </option>
            </select>
        </div>
        <div class="col" v-if="labchipSelection">
            <strong class="d-block">labchip Wells</strong>
            <select v-model="labchipSelection" class="ml-3 w-50" multiple>
                <option v-for="op in labchipWells" v-bind:key="op.text" v-bind:value="op.value">
                    {{op.text}}
                </option>
            </select>
        </div>
    </div>
    <hr/>
    <h5 class="text-left">Feedback</h5>
    <div class="row">
        <div class="col">
            <textarea v-model="comment" placeholder="Provide Comments (within 200 chars)">

            </textarea>
        </div>
        <div class="col">
            <div class="form-group">
                <label>Mark wells as excluded</label>
                <input type="checkbox" v-model="exclude" true-value="True" false-value="False">
            </div>
        </div>
    </div>
            <div slot="modal-footer" class="modal-footer">
                <button type="button" class="btn btn-default" @click="handleSubmit()">Submit</button>
                <button type="button" class="btn btn-default" @click="handleExit()">Exit</button>
            </div>
        </modal>
</template>
<script src='./annotator.js'></script>
