<style scoped src="./scriptEditor.css"></style>
<template>
<div>
<div  :class="{'container-fluid':true,'w-75':true}">
    <div class="row text-left" style="height:50px">
      <div class="col-1">
          <tooltip effect="scale" placement="bottom" content="Click me to show example script">
          <i class="btn fa fa-info-circle" @click="showInfo=!showInfo" aria-hidden="true"></i>            
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
    <div class="row">
        <div id="editorwindow" class="col-5 h-100" @mouseout="handleMouseOut">
            <div id="editor" class="border editor" @keyup="editorChange"
                                      @mouseover="handleMouseOver"></div>
        </div>
        <div class="col-5">
            <div class="row mt-3">
              <hovervisualizer :currentPlate="currentPlate"
                               :tableBoundaries="tableBoundaries"
                               :highlightedLineNumber="highlightedLineNumber"
                               :hoverHighlight="hoverHighlight"
                                :allocationMapping="allocationMapping"                                
                                @wellHovered="handleWellHover"
                                @hoverComplete="handleWellHoverComplete">
            </hovervisualizer>
            </div> 
            <div class="row mt-3" v-if="showWellContents&&!error">
                <wellcontents   :currentRow="currentRow" 
                                :currentCol="currentCol" 
                                :allocationData="allocationData[currentPlate]">
                </wellcontents> 
            </div>
            
            <div class="row justify-content-center" v-if="error">
              <i class="fa fa-frown-o fa-5x" aria-hidden="true"></i>
            </div>          
            <div class="row text-left " v-show="showSuggestionList">
                <h5 class="mt-3 w-100"><strong>Suggestions :</strong></h5>
                <h5><strong>Currently retreiving 5+ suggestions</strong></h5>
                <div class="list-group w-100 pre-scrollable">
                    <button class="list-group-item list-group-item-action" v-for="text in suggestions" v-bind:key="text.url" @click.left="handleAutoCompleteClick(text);" @click.middle="hideSuggestion()">
                        <div v-if="text['name']">{{text['name']}}</div>
                        <div v-else>{{text['abbrev']}}</div>
                    </button>
                </div>
            </div>
            
            
        </div>
        <span v-bind:style="tooltiptext" v-if="showSuggestionToolTip">
            
    <ul >
    <li v-for = "text in suggestions" v-bind:key="text.url" @click.left="handleAutoCompleteClick(text);"
    @click.middle="hideSuggestion()">
      <div v-if="text['name']">{{text['name']}}</div>
                        <div v-else>{{text['abbrev']}}</div>
    </li>
    </ul>
    </span>
    </div>  
    <modal title="Example Script" effect="fade/zoom" large :value="showInfo">
        <textarea v-model="referenceText" class="w-100 editor" readonly></textarea>
        <div slot="modal-footer" class="modal-footer">
            <button type="button" class="btn btn-default" @click="showInfo = !showInfo">Exit</button>
        </div>
    </modal>
   
</div>
 <div id="overlay" v-if="showBlur">
        <div id="text">Possible Connection Error</div>
</div>
</div>
</template>
<script src="./scriptinput.js"></script>