<style scoped>

.overlay {
    border: 1px solid black;
    width: 70%;
    height: 100%;
    display: inline-block;

    background-repeat: no-repeat;
}

</style>

<template>

<div class="fluid-container">
  <div class="row m-5">
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
    <div class="row m-5">
        <div class="col">
            <allocationrules @selectedRule="handleSelectedRule" @ruleDeleted="handleRuleDelete"  @error="handleErrors" ></allocationrules>
            <transition name="custom-classes-transition" enter-active-class="animated fadeInLeft" leave-active-class="animated zoomOut">
            <selectedrule
            v-if="show"
            :image="plateImage"
            :allocationResults="allocationResults"
            @error="handleErrors"
            @ruleChanged="handleRuleChange"
            ></selectedrule>
          </transition>
        </div>
        <div class="col">
          <div v-if="showAlert" class="alert alert-danger alert-dismissable" @click="showAlert=!showAlert">
            <a href="#" class="close" data-dismiss="alert" aria-label="close" >&times;</a>
            <strong>Error!</strong> {{alert}}.
          </div>
            <spinner :value="spin"></spinner>
            <div class="row overlay" id="overlay" v-on:mousemove="zoomIn" @click="handleDoubleClick"></div>
        </div>
    </div>
</div>

</template>
<script src="./platedesign"></script>
