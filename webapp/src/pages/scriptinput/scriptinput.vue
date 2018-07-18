<style scoped src="./scriptEditor.css"></style>
<template>
<div>
    <div  :class="{'container-fluid':true}">
        <!-- toolbar -->
        <toolbar    :error="error"
                    :showSpinner="showSpinner"
                    @switchInfoVisiblity="handleSwitchInfoVisiblity"
                    @formatText="handleFormat"
                    @highlightError="highlightError"
                    >
        </toolbar>     
        <!-- toolbar -->
        <div class="row mt-3 w-100">
            <!-- editor -->
            <div class="col">
            <div id="editor" class="editor ql-editor" @keyup="editorChange"  
            @mouseout="handleMouseOut">
            </div>
            </div>
            <!-- editor -->
            <div class="mw-100 col">
                <!-- hovervisualizer -->
                <div class="d-flex justify-content-start">
                    <ul class="nav nav-pills nav-fill">
                        
                        <li class="nav-item">
                            <a :class="{'nav-link':'true','active':!showPictures}" 
                                href="javascript:;"
                            >Rules Feedback</a>
                        </li>                       
                        
                        <li class="nav-item">
                            <a :class="{'nav-link':'true','active':showPictures}" 
                                href="javascript:;"
                                @click="showPictures=!showPictures">Show Plate Variables
                                </a>
                        </li>
                        
                    </ul>
                    <button class="btn btn-secondary mr-2" @click="showUpload=!showUpload">Upload Files</button>
                    <button class="btn btn-secondary" @click="showDelete=!showDelete">Delete Results</button>
                </div>

                <div v-show="!showPictures">
                    <div  class="row mt-3" v-if="!error">                    
                        <hovervisualizer    :currentPlate="currentPlate" 
                                            :plateBoundaries="plateBoundaries"                                                                   
                                            :highlightedLineNumber="highlightedLineNumber"
                                            :hoverHighlight="hoverHighlight"
                                            :allocationMapping="allocationMapping"                                
                                            @wellHovered="handleWellHover"
                                            @hoverComplete="handleWellHoverComplete"
                                            >
                        </hovervisualizer>                   
                        
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
                <div v-show="showPictures" class="overlay">
                    <!-- experimentImages -->  
                    <div class="overlay-content"> 
                        <pictures  :experimentImages="experimentImages"
                                    @exit="showPictures=!showPictures">
                        </pictures>                      
                    </div>
                    <!-- experimentImages -->
                </div>       
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
        <!-- sampleExperiment -->
        <modal title="Example Script" effect="fade/zoom" large :value="showInfo">
            <textarea v-model="referenceText" class="w-100 editor" readonly></textarea>
            <div slot="modal-footer" class="modal-footer">
                <button type="button" class="btn btn-default" @click="handleSwitchInfoVisiblity()">Exit</button>
            </div>
        </modal>
        <!-- sampleExperiment -->    
        <!--fileUploader-->
        <fileUploader :show="showUpload" :experimentName="experimentId" :plateName="currentPlate" @exit="showUpload=!showUpload"></fileUploader>
        <!--fileUploader-->
        <!--destroyer-->
        <destroyer :show="showDelete" :experimentName="experimentId" :plateName="currentPlate" @exit="showDelete=!showDelete"></destroyer>
        <!--destroyer-->
    </div>
 <div class="overlay" v-if="showBlur">
        <div id="text">Possible Connection Error</div>
</div>

</div>

</template>
<script src="./scriptinput.js"></script>
