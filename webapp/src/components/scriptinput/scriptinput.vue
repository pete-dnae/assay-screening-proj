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
#editor{
  font-family: "MONOSPACE";
  font-size: 18px;
  height: 1200px;
}

</style>

<template>

<div>
    <div class="row">
        <div class="col-5">
            <div id="editor"></div>

        </div>
        <div class="col-5">
            <h5 class="mt-3 text-left"><strong>Some Examples of rules</strong></h5>
            <div class="row ml-3 jumbotron jumbotron-fluid">
                <div class="container text-left" style="font-family:monospace;">
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
            </div>
            <h5 class="mt-3 text-left"><strong>Feedbacks :</strong></h5>
            <div class="row ml-3 mt-3 h-50 border border-warning">
                <div id="result" class="list-group w-100 pre-scrollable">
                    <div class="list-group-item list-group-item-action" @mouseover="highlightError(err)" v-for="err in invalidTextObjects">{{err.msg}}</div>
                </div>
            </div>
        </div>

        <span v-bind:style="tooltiptext" v-show="showToolTip">
    <ul>
    <li v-for = "text in suggestions" @click.left="handleAutoCompleteClick(text);"
    @click.middle="hideSuggestion()">
      {{text}}
    </li>
    </ul>
    </span>
    </div>
    <div class="row mt-5">
        <div class="col-md-5">
            <button @click="handleFormat()">Format</button>
        </div>

    </div>
</div>

</template>

<script src="./scriptinput.js"></script>
