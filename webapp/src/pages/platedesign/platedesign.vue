<template>
  <div class="fluid-container bg-light ">
    <div class="row">
      <div class="col">
        <allocationrules @selectedRule="handleSelectedRule"></allocationrules>
        <selectedrule :element="selectedrule"></selectedrule>
      </div>
      <div class="col">
          <div id="overlay" v-on:mousemove="zoomIn(event)"></div>
      </div>
    </div>
  </div>
</template>
<script src="./platedesign"></script>
<style scoped>
#overlay{
  border:1px solid black;
  width:650px;
  height:450px;
  display:inline-block;
  background-image:url('../../assets/table.jpg');
  background-repeat:no-repeat;
}
</style>
