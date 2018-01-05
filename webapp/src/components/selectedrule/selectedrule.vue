<template>
  <div class="fluid-container w-100 ml-3">
    <h5 class="text-left">Selected Rule</h5>
    <div class="row">
      <div class="col">
        <label>Distribute these</label>
        <input v-model="element['title']" disabled>
      </div>
      <div class="col" id="bong">
        <select v-model="element['type']">
          <option v-for="option in options" v-bind:value="option.value">
            <b>{{option.value}}</b> <label>{{option.text}}</label>
          </option>
        </select>
      </div>
    </div>
    <div class="row ">
      <draggable class="col" :list="element['value']">
        <div class="list-group-item text-left" v-for="element in element['value']" :key="element['value'].id">
          <div class="row">
                <i class="fa fa-bars col-1" aria-hidden="true"></i>
                <label class="col" >{{element['value']}}</label>
                <i class="fa fa-minus-square col-1 float-right" aria-hidden="true"></i>
          </div>
        </div>
      </draggable>
      <div class="col">
        <h6 class="text-left"><b>Over</b></h6>
        <div class="row">
          <div class="col-2 text-left">
            <label>Rows</label>
          </div>
          <div class="col-2">
            <input v-model="element['rowRange']">
          </div>
        </div>
        <div class="row">
          <div class="col-2 text-left">
            <label>Columns</label>
          </div>
          <div class="col-2">
            <input v-model="element['colRange']">
          </div>


        </div>
      </div>
      <div class="col">
        <img src="../../assets/table.jpg"
          v-on:mousemove="zoomIn" v-on:mouseout="zoomOut"
         id="imgZoom" width="300px" height="200px">
        <label class="blockquote-footer text-left">Hover over thumbnai to zoom</label>
      </div>
    </div>
  </div>
</template>
<script src="./selectedRule"></script>
