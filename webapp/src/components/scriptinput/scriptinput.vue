<template>
  <div >
  <div class="col" id="editor">

  </div>
  <div v-bind:style="tooltiptext">
    <ul>
    <li v-for = "text in suggestions" >
      {{text}}
    </li>
  </ul>
  </div>
  <div  id="result" class="col container-fluid pre-scrollable">
    <div v-for="err in errorMessages">{{err}}</div>
  </div>

</div>
</template>
<script src="./scriptinput.js"></script>
<style scoped>
 ul {
  margin: 0;
  margin-top: 2px;
  padding: 0;
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
