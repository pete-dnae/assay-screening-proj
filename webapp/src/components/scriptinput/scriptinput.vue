<style scoped>

ul {
    margin: 0;
    margin-top: 2px;
    padding: 0;
    width: 300px;
    list-style: none;
    background: #efefef;
}

li {
    padding: 5px 5px;
    cursor: pointer;
}

li:hover {
    background: #ddd;
}

li span {
    font-weight: bold;
}


#editor {
    font-family: "MONOSPACE";
    font-size: 18px;
    height: 1000px;
}

@keyframes spinner {
    to {
        transform: rotate(360deg);
    }
}

.spinner:before {
    content: '';
    box-sizing: border-box;
    position: relative;
    top: 50%;
    left: 50%;
    width: 20px;
    height: 20px;
    /* margin-top: -10px;
  margin-left: -10px; */
    border-radius: 50%;
    border: 1px solid #f6f;
    border-top-color: #0e0;
    border-right-color: #0dd;
    border-bottom-color: #f90;
    animation: spinner .6s linear infinite;
}

</style>

<template>

<div class="container-fluid w-75">
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
          <label>{{error.message}}</label>
        </div>
    </div>
    <div class="row">
        <div id="editorwindow" class="col-5 h-100">

            <div id="editor" class="" @keyup="editorChange" @mouseover="handleMouseOver"></div>
        </div>
        <div class="col-5">
            <div class="row mt-3" v-if="">
              <hovervisualizer :currentPlate="currentPlate"
                               :tableBoundaries="tableBoundaries"
                               :highlightedLineNumber="highlightedLineNumber"
              :allocationMapping="allocationMapping"
              :allocationData="allocationData">
            </hovervisualizer>
            </div>
            <div class="row text-left " v-show="showSuggestionList">
                <h5 class="mt-3 w-100"><strong>Suggestions :</strong></h5>
                <h5><strong>Currently retreiving 5+ suggestions</strong></h5>
                <div class="list-group w-100 pre-scrollable">
                    <button class="list-group-item list-group-item-action" v-for="text in suggestions" @click.left="handleAutoCompleteClick(text);" @click.middle="hideSuggestion()">
                        {{text}}
                    </button>
                </div>
            </div>
        </div>
        <span v-bind:style="tooltiptext" v-show="showSuggestionToolTip">
    <ul >
    <li v-for = "text in suggestions" @click.left="handleAutoCompleteClick(text);"
    @click.middle="hideSuggestion()">
      {{text}}
    </li>
    </ul>
    </span>
    </div>
    <modal v-model="show" id="modal" @ok="handleReagentAdd" @keyup="handleReagentAdd">
        Do you want to save "{{newReagent}}" to the database
    </modal>
</div>

</template>
<script src="./scriptinput.js"></script>
