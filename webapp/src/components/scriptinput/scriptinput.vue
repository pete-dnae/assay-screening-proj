<template>
  <div >
  <div class="col" id="editor">
  </div>
  <div  id="result" class="col container-fluid pre-scrollable">
    <div v-for="err in errorMessages">{{err}}</div>
  </div>

</div>
</template>
<script src="./scriptinput.js"></script>
