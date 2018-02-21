<template>
  <div>
  <!-- <textarea class="panel panel-default text-justify" style="width:500px;height:400px">

  </textarea> -->
  <quill-editor :content="content"
                :options="editorOption"
                @change="onEditorChange($event)">
  </quill-editor>
  <div id="result">
  </div>
</div>
</template>
<script src="./scriptinput.js"></script>
