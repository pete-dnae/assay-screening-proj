<template>
<div class="row text-left toolbar ql-toolbar ql-snow border border-secondary rounded" style="height:50px">
            <div class="col-1">
                <tooltip effect="scale" placement="bottom" content="Click me to show example script">
                <i class="btn fa fa-info-circle" @click="handleSwitchInfoVisiblity()" aria-hidden="true"></i>            
                </tooltip>
            </div>
            <div class="col-2">            
                <label>Type your rules here</label>
                <i class="btn fa fa-hand-o-down" aria-hidden="true" ></i>
            </div>
            <div class="col-1">
                <tooltip effect="scale" placement="bottom" content="Click me to format text or Press ctrl+F ">
                <i @click="handleFormat()" class="btn fa fa-align-right"></i>    
                </tooltip>        
            </div>    
            <div class="col-1">
                <span v-show="showSpinner"> <i class="fa fa-floppy-o">saving</i></span>
            </div>
            <div id="result" class="col" v-if="error" @mouseover="highlightError(error.where_in_script)">
                <i class="fa fa-frown-o fa-2x" aria-hidden="true"></i>
                <label class="text-danger">{{error.message}}</label>
            </div>
</div>
</template>
<script src="./editortoolbar.js"></script>
