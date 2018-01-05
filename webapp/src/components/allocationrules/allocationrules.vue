<template>
  <div class="fluid-container w-100 ml-3">
      <div class="row ml-3">
        <b>Allocation Rules</b>
      </div>
      <div class="row ml-3">
        <draggable :list="items" class="pre-scrollable w-75" @choose="handleSelect">
          <div class="list-group-item text-left" v-for="element in items" :key="element.id">
            <div class="row">
                  <i class="fa fa-bars col-1" aria-hidden="true"></i>
                  <label class="col" >{{element.title}} - <i v-for="val in element.value">{{val.value}},</i>
                    {{element.type}},{{element.rowRange}},{{element.colRange}}</label>
                  <i class="fa fa-minus-square col-1 float-right" aria-hidden="true"></i>
            </div>
          </div>
        </draggable>
      </div>
      <div class="row ml-3">
        <label class="blockquote-footer">Later rules override earlier rules</label>
      </div>
      <div class="row">
        <div class="col-md-5">
        </div>
        <div class="col">
            <a class="btn btn-info">
              <i class="fa fa-plus-square float-right" aria-hidden="true"></i>
            </a>
        </div>
      </div>
  </div>
</template>
<script src="./allocationrules"></script>
