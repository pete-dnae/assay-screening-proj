<style scoped>

.grab {
    cursor: grab;
}
.overflow {
  width: 200px;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
}


</style>

<template>

<div class="fluid-container w-100 ml-3">
    <div class="row ml-3">
        <b>Allocation Rules</b>
    </div>
    <div class="row ml-3">

        <spinner class="pre-scrollable w-100 m-4"  :value="spin" size="xl"  text="I will close in 2 secs"></spinner>

        <draggable v-model="rules" class="pre-scrollable w-100" @choose="handleSelect" @filter="handleDelete" :options="{filter:'.fa-trash-o',chosenClass:'active'}">

            <button class="list-group-item list-group-item-action text-left" v-for="element in rules" :key="element.id">
                <div class="row">
                    <i class="fa fa-bars col-1  grab" aria-hidden="true"></i>
                    <label class="col overflow" ><b >{{element.id}}  </b>{{element.display_string}}</label>
                    <i class="fa fa-trash-o col-1 float-right" aria-hidden="true"></i>
                </div>
            </button>

        </draggable>
    </div>
    <div class="row ml-3">
        <label class="blockquote-footer">Later rules override earlier rules</label>
    </div>
    <div class="row">
        <div class="col-md-5">
        </div>
        <div class="col text-right">

            <i class="fa fa-plus-square fa-2x" @click="handleAddRule" aria-hidden="true"></i>

        </div>
    </div>
</div>

</template>
<script src="./allocationrules"></script>
