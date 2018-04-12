<style scoped src="./scriptEditor.css"></style>
<template>
<div>
    <div  :class="{'container-fluid':true,'w-75':true}">
        <!-- toolbar -->
        <toolbar    :error="error"
                    :showSpinner="showSpinner"
                    @switchInfoVisiblity="handleSwitchInfoVisiblity"
                    @formatText="handleFormat"
                    @highlightError="highlightError"
                    >
        </toolbar>     
        <!-- toolbar -->
        <div class="row mt-3">
            <!-- editor -->
            <div id="editor" class="editor ql-editor" @keyup="editorChange"  
            @mouseout="handleMouseOut">
            </div>
            <!-- editor -->
            <div class="mw-100">
                <!-- hovervisualizer -->
                <div class="row mt-3" v-if="!error">                    
                    <hovervisualizer    :currentPlate="currentPlate"                               
                                        :tableRowCount="tableRowCount"
                                        :tableColCount="tableColCount"
                                        :highlightedLineNumber="highlightedLineNumber"
                                        :hoverHighlight="hoverHighlight"
                                        :allocationMapping="allocationMapping"                                
                                        @wellHovered="handleWellHover"
                                        @hoverComplete="handleWellHoverComplete">
                    </hovervisualizer>                    
                    <div class="row w-100 mt-3">
                        <div class="col-md-6">
                            
                        </div>
                        <div class="col">
                            <i class="fa fa-lightbulb-o fa-2x" aria-hidden="true"></i>
                            <label class="text-info">Hover over a well</label>
                        </div>                
                    </div>
                </div> 
                <!-- hovervisualizer -->
                <!-- wellcontents -->
                <div class="row mt-3" v-if="showWellContents&&!error">
                    
                    <wellcontents   :currentRow="currentRow" 
                                    :currentCol="currentCol" 
                                    :allocationData="allocationData[currentPlate]">
                    </wellcontents> 
                    
                </div>
                <!-- wellcontents -->
                <!-- error pane -->
                <errorPane v-if="error"></errorPane>     
                <!-- error pane -->   
                <!-- suggestionslist -->             
                <suggestionsList    v-show="showSuggestionList"
                                    :suggestions="suggestions"
                                    @autoComplete="handleAutoCompleteClick"
                                    @hideSuggestion="hideSuggestion"
                                    >
                </suggestionsList>   
                <!-- suggestionslist -->              
            </div>
        <!-- suggestionToolTip -->        
            <suggestionToolTip  v-if="showSuggestionToolTip"
                                :suggestions="suggestions"
                                :toolTipPosition="tooltiptext" 
                                @autoComplete="handleAutoCompleteClick"
                                @hideSuggestion="hideSuggestion"
                               ></suggestionToolTip>
        <!-- suggestionToolTip -->
        </div>  
        <!-- saveAsPane -->
        <modal title="Example Script" effect="fade/zoom" large :value="showInfo">
            <textarea v-model="referenceText" class="w-100 editor" readonly></textarea>
            <div slot="modal-footer" class="modal-footer">
                <button type="button" class="btn btn-default" @click="handleSwitchInfoVisiblity()">Exit</button>
            </div>
        </modal>
        <!-- saveAsPane -->    
    </div>
 <div id="overlay" v-if="showBlur">
        <div id="text">Possible Connection Error</div>
</div>
</div>

</template>
<script src="./scriptinput.js"></script>
