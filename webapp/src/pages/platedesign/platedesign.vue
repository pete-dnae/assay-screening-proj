<style scoped>

#overlay {
    border: 1px solid black;
    width: 650px;
    height: 450px;
    display: inline-block;
    /* background-image: url('../../assets/table.jpg'); */
    background-repeat: no-repeat;
}

</style>

<template>

<div class="fluid-container bg-light">
  <div class="row">
    <div class="col text-left mt-3 ml-4">
      <label><b>Designer</b></label>
      <label>{{designerName}}</label>
      <i class="fa fa-user-o" aria-hidden="true"></i>
    </div>
    <div class="col text-left mt-3">
      <label><b>Experiment</b></label>
      <label>{{experimentName}}</label>
      <i class="fa fa-flask" aria-hidden="true"></i>
    </div>
    <div class="col-7">
    </div>
  </div>
    <div class="row mt-3">
        <div class="col">
            <allocationrules @selectedRule="handleSelectedRule" ></allocationrules>
            <selectedrule :element="selectedrule" :allocationResults="allocationResults"></selectedrule>
        </div>
        <div class="col">
            <div id="overlay" v-on:mousemove="zoomIn"></div>
        </div>
    </div>
</div>

</template>
<script src="./platedesign"></script>
