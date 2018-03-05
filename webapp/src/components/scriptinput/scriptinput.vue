

<template>

<div>
    <div class="col" id="editor">

    </div>
    <span v-bind:style="tooltiptext" v-show="showToolTip">
    <ul>
    <li v-for = "text in suggestions" @click="handleAutoCompleteClick(text);">
      {{text}}
    </li>
  </ul>
  </span>
    <div id="result" class="col list-group pre-scrollable">
        <div class="list-group-item list-group-item-action" @mouseover="highlightError(err)"
        v-for="err in invalidTextObjects">{{err.msg}}</div>
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
