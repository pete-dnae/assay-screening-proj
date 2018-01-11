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
    <div class="fluid-container w-100 ml-3" v-show="'id' in element">
        <h5 class="text-left">Selected Rule</h5>
        <div class="row">
            <div class="col-5 text-left">
                <label>Distribute these</label>
                <select v-model="element['title']">
                    <option v-for="type in types" v-bind:value="type.value">
                        <label>{{type.text}}</label>
                    </option>
                </select>
            </div>
            <div class="col text-left">
                <select v-model="element['type']">
                    <option v-for="option in options" v-bind:value="option.value">
                        <b>{{option.value}}</b>
                        <label>{{option.text}}</label>
                    </option>
                </select>
            </div>
        </div>
        <div class="row ">
            <div class="col-5">
                <div class="row">
                    <draggable :list="element['value']" class="w-100 list-group" @filter="handleDeleteValue" :options="{filter:'.fa-trash-o',chosenClass: 'active'}">

                        <button class="list-group-item list-group-item-action text-left" v-for="element in element['value']" :key="element['value'].id">
                            <div class="row">
                                <i class="fa fa-bars  col-1 grab" aria-hidden="true"></i>
                                <label class="col">{{element['value']}}</label>
                                <i class="fa fa-trash-o col-1" aria-hidden="true"></i>
                            </div>
                        </button>

                    </draggable>
                </div>
                <div class="row mt-3">
                    <div class="col-md-10">
                    </div>
                    <div class="col">
                        <i class="fa fa-plus-square" @click="showModal=true" aria-hidden="true"></i>
                    </div>
                </div>
            </div>
            <div class="col">
                <h6 class="text-left"><b>Over</b></h6>
                <div class="row">
                    <div class="col-2 text-left">
                        <label>Rows</label>
                    </div>
                    <div class="col-1">
                        <input v-model="element['rowRange']" @keyup="validateRowRange">
                    </div>
                </div>
                <div class="row mt-3">
                    <div class="col-2 text-left">
                        <label>Col</label>
                    </div>
                    <div class="col-1">
                        <input v-model="element['colRange']" @keyup="validateColRange">
                    </div>
                </div>
            </div>
            <div class="col">
                <img src="../../assets/table.jpg" id="imgZoom" class="zoomIn" v-on:mousemove="zoomIn" v-on:mouseout="zoomOut"  style="max-width: 100%;height: auto;">
                <label class="blockquote-footer text-left">Hover over thumbnail to zoom</label>
            </div>
        </div>
    </div>
    <modal v-model="showModal">
        <div slot="modal-header" class="modal-header">
            <h4 class="modal-title">Enter new entity</h4>
        </div>
        <div slot="modal-body" class="modal-body">
            <h5>(Will be replaced by live dropdowns)</h5>
            <label>Entity text</label>
            <input v-model="textElem">
        </div>
        <div slot="modal-footer" class="modal-footer">
            <button @click="showModal = false">Close</button>
            <button @click="handleAddValue(textElem);showModal = false">Add</button>
        </div>
    </modal>

</div>

</template>
<script src="./selectedrule"></script>
