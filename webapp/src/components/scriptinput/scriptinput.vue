<style scoped src="./scriptEditor.css"></style>
<template>
<div  :class="{blurComponent:showBlur,'container-fluid':true,'w-75':true}">
    <div class="row text-left" style="height:50px">
      <div class="col-1">
          <i class="btn fa fa-info-circle" aria-hidden="true"></i>
          <label>info</label>
      </div>
        <div class="col-1">
            <i @click="handleFormat()" class="btn fa fa-align-justify"></i>
            <label>Format</label>
        </div>
        <div class="col-2">
            <i class="btn fa fa-hand-o-down" aria-hidden="true"></i>
            <label>Type your rules here</label>
        </div>

        <div class="col-1">
            <span v-show="showSpinner" class="spinner "> <i class="fa fa-floppy-o">saving</i></span>
        </div>
        <div id="result" class="col" v-if="error" @mouseover="highlightError(error.where_in_script)">
          <i class="fa fa-frown-o fa-2x" aria-hidden="true"></i>
          <label class="text-danger">{{error.message}}</label>
        </div>
    </div>
    <div class="row">
        <div id="editorwindow" class="col-5 h-100">

            <div id="editor" class="" @keyup="editorChange" @mouseover="handleMouseOver"></div>
        </div>
        <div class="col-5">
            <div class="row mt-3" v-if="error===null">
              <hovervisualizer :currentPlate="currentPlate"
                               :tableBoundaries="tableBoundaries"
                               :highlightedLineNumber="highlightedLineNumber"
              :allocationMapping="allocationMapping"
              :allocationData="allocationData">
            </hovervisualizer>
            </div>
            <div class="row justify-content-center mt-5" v-else>
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
        <span v-bind:style="tooltiptext" v-show="showSuggestionToolTip">
    <ul >
    <li v-for = "text in suggestions" v-bind:key="text.url" @click.left="handleAutoCompleteClick(text);"
    @click.middle="hideSuggestion()">
      <div v-if="text['name']">{{text['name']}}</div>
                        <div v-else>{{text['abbrev']}}</div>
    </li>
    </ul>
    </span>
    </div>
    <!-- <modal v-model="show" id="modal" @ok="handleReagentAdd" @keyup="handleReagentAdd">
        Do you want to save "{{newReagent}}" to the database
    </modal> -->
</div>

</template>
<script src="./scriptinput.js"></script>
