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
    height: 1200px;
}

</style>

<template>

<div>
    <div class="row">
        <div id="editorwindow" class="col-5">
          <div class="quill-wrapper">
            <div id="toolbar" class="toolbar ql-toolbar ql-snow">
                <span class="ql-formats">
                  <button @click="handleFormat()" class="fa fa-align-justify"></button>
                  <label>Format</label>
                </span>

            </div>
          </div>
            <div id="editor" @keyup="EditorChange"></div>

        </div>
        <div class="col-5">
            <div class="row mt-3">
                <div class="container col text-left" style="font-family:monospace;">
                    <h5 class="text-left"><strong>Some Examples of rules</strong></h5>
                    <h6><strong>Version rule </strong></h6>
                    <div class="ml-3">
                        <span class="d-block">V 1</span>
                    </div>
                    <h6 class="mt-3"><strong>Plate rule </strong></h6>
                    <div class="ml-3">
                        <span class="d-block">P 1</span>
                    </div>
                    <h6 class="mt-3"><strong>A rule </strong></h6>
                    <div class="ml-3">
                        <span class="d-block">A  (Eco)-ATCC-BAA-2355       1,5,9  A-B 0     copies</span>
                        <span class="d-block">A  (Eco)-ATCC-BAA-2355       10-12  G-H 5000  copies</span>
                        <span class="d-block">A  (Eco)-ATCC-BAA-2355           9  G-H 5000  copies</span>
                    </div>
                    <h6 class="mt-3"><strong>T rule </strong></h6>
                    <div class="ml-3">
                        <span class="d-block">T  P1       1,8   A-B 0   dil</span>
                        <span class="d-block">T  P1       4-12  G-H 50  dil</span>
                        <span class="d-block">T  P1          9  G-H 50  dil</span>
                    </div>
                    <h6 class="mt-3"><strong>Comment rule </strong></h6>
                    <div class="ml-3">
                        <span class="d-block"># Hey there am a comment </span>
                    </div>
                </div>
                <div class="col  text-left">
                    <h5 class="text-left"><strong>Plate Visualization</strong></h5>
                    <small class="form-text text-muted">Change defaults if its a bigger plate</small>
                    <div class="row">
                        <div class="col form-group">
                            <label>Row Count</label>
                            <input type="number" class="form-control" v-model="rowCount" placeholder="Enter Row count">
                        </div>
                        <div class="col form-group">
                            <label>Column Count</label>
                            <input type="number" class="form-control" v-model="colCount" placeholder="Enter Col count">
                        </div>
                    </div>
                    <strong>User Selection</strong>
                    <img :src="image" id="imgZoom" class="mt-3" style="max-width: 100%;height: auto;">
                </div>
            </div>
            <h5 class="mt-3 text-left"><strong>Feedbacks :</strong></h5>
            <div class="row ml-3 mt-3  border border-warning">

                <div id="result" class="list-group w-100" v-if="error" @mouseover="highlightError()">
                    {{error.err}}
                </div>

            </div>
            <div class="row text-left " v-show="suggestions.length >5">
                <h5 class="mt-3 w-100"><strong>Suggestions :</strong></h5>
                <h5><strong>Currently retreiving 5+ suggestions</strong></h5>
                <div class="list-group w-100 pre-scrollable">
                    <button class="list-group-item list-group-item-action" v-for="text in suggestions" @click.left="handleAutoCompleteClick(text);" @click.middle="hideSuggestion()">
                        {{text}}
                    </button>
                </div>
            </div>
        </div>
        <span v-bind:style="tooltiptext" v-show="suggestions.length <5 && suggestions.length >1">
    <ul>
    <li v-for = "text in suggestions" @click.left="handleAutoCompleteClick(text);"
    @click.middle="hideSuggestion()">
      {{text}}
    </li>
    </ul>
    </span>
    </div>
    </div>

</template>

<script src="./scriptinput.js"></script>
