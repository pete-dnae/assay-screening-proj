<style scoped>

.grab {
    cursor: grab;
}

.zoomIn {
    cursor: zoom-in;
}

.overflow {
    width: 200px;
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;
}

</style>

<template>

<div>
    <div class="fluid-container w-100 ml-3">
        <h5 class="text-left">Selected Rule</h5>
        <div class="row">
            <div class="col-5 text-left">
                <div class="form-group row">
                    <label class="col col-form-label">Distribute these</label>
                    <select v-model="payloadType">
                        <option v-for="type in types" v-bind:value="type.value">
                            <label>{{type.text}}</label>
                        </option>
                    </select>
                </div>
            </div>
            <div class="col text-left">
                <select v-model="distPattern" class="btn btn-info dropdown-toggle">
                    <option v-for="option in options" v-bind:value="option.value">
                        <b>{{option.value}}</b>
                        <label>{{option.text}}</label>
                    </option>
                </select>
            </div>
        </div>
        <div class="row mt-4">
            <div class="col-5">
                <div class="row">
                    <transition name="custom-classes-transition" enter-active-class="animated fadeInLeft" leave-active-class="animated bounceOutRight">
                        <draggable v-model="payload" v-show="show" class="w-100 list-group" @filter="handleDeleteValue" :options="{filter:'.fa-trash-o',chosenClass: 'active'}">

                            <button class="list-group-item list-group-item-action text-left" v-for="element in payload" :key="element.id">
                                <div class="row">
                                    <i class="fa fa-bars  col-1 grab" aria-hidden="true"></i>
                                    <label class="col">{{element}}</label>
                                    <i class="fa fa-trash-o btn btn-warning" aria-hidden="true"></i>                                    
                                </div>
                            </button>

                        </draggable>

                    </transition>
                    <transition name="custom-classes-transition" enter-active-class="animated fadeInLeft" leave-active-class="animated zoomOut">
                      <select v-if="!show && currentOptions!='userText'" class="pre-scrollable h-50 w-100 list-group" v-model="payload" multiple>
                        <option v-for="options in currentOptions" class="list-group-item list-group-item-action text-left">
                          <div class="row">
                              <label class="col">{{options.text}}</label>
                          </div>
                        </option>
                      </select>
                      <div v-if="!show && currentOptions=='userText'" class="pre-scrollable h-50 w-100 list-group">
                          <div v-for="option in textBoxNo"  class="list-group-item list-group-item-action text-left">
                              <input class="row" type="number" v-model="userText[option]">
                          </div>
                      </div>
                    </transition>
                </div>
                <div class="row mt-3">
                    <div class="col-md-9">
                    </div>
                    <div class="col">
                      <div class="row">
                        <i class="fa fa-long-arrow-left" v-if="!show" @click="show = !show;selectMode=!selectMode"aria-hidden="true"></i>
                        <i class="fa fa-floppy-o ml-3" v-if="!show && currentOptions=='userText'" @click="show = !show;handleUserInput(userText)" aria-hidden="true"></i>
                        <i class="fa fa-plus ml-3" v-if="!show && currentOptions=='userText'" @click="textBoxNo+=1" aria-hidden="true"></i>
                        <i class="fa fa-minus ml-3" v-if="!show && currentOptions=='userText'" @click="handleTextBoxDel()" aria-hidden="true"></i>
                        <i class="fa fa-plus-square" v-if="show"  @click="show = !show;selectMode=!selectMode" aria-hidden="true"></i>
                      </div>
                    </div>
                </div>
            </div>
            <div class="col">
                <h6 class="text-left"><b>Over</b></h6>
                <div class="row mt-4">
                    <div class="col-2 text-left">
                        <label>Rows</label>
                    </div>
                    <div class="col-2">
                        <input style="width:50px" v-model="rowStart" @keyup="validateRowRange">
                    </div>
                    <div class="col-2 text-right">
                        <label>to</label>
                    </div>
                    <div class="col-1 ">
                        <input style="width:50px" v-model="rowEnd" @keyup="validateRowRange">
                    </div>
                </div>
                <div class="row mt-3">
                    <div class="col-2 text-left">
                        <label>Col</label>
                    </div>
                    <div class="col-2">
                        <input style="width:50px" v-model="colStart" @keyup="validateColRange">
                    </div>
                    <div class="col-2 text-right">
                        <label>to</label>
                    </div>
                    <div class="col-1">
                        <input style="width:50px" v-model="colEnd" @keyup="validateRowRange">
                    </div>
                </div>
            </div>
            <div class="col">
                <img :src="image" id="imgZoom" class="zoomIn" v-on:mousemove="zoomIn" style="max-width: 100%;height: auto;">
                <label class="blockquote-footer text-left">Hover over thumbnail to zoom</label>
            </div>
        </div>
    </div>

</div>

</template>

<script src="./selectedrule"></script>
