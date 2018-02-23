<template>
  <div>
  <quill-editor :content="content"
                :options="editorOption"
                @change="onEditorChange($event)">
  </quill-editor>
  <div id="result" class="container-fluid pre-scrollable">
  </div>
  <button @click="showHelp">help</button>
</div>
</template>
<script src="./scriptinput.js"></script>
