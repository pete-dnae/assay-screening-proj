

<template>

<div>
    <div class="row">
        <div class="col-5">
            <div id="editor"></div>
        </div>
        <div class="col -5">
          <div >

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
      </div>
    <div id="result" class="col mt-5 list-group pre-scrollable">
        <div class="list-group-item list-group-item-action" @mouseover="highlightError(err)" v-for="err in invalidTextObjects">{{err.msg}}</div>
    </div>
  </div>
</div>

</template>

<script src="./scriptinput.js"></script>
<style scoped>
 ul {
  margin: 0;
  margin-top: 2px;
  padding: 0;
  width: 300px;
  list-style: none;
  background: #efefef; }
 li {
  padding: 5px 5px;
  cursor: pointer; }
   li:hover {
    background: #ddd; }
   li span {
    font-weight: bold; }
</style>
