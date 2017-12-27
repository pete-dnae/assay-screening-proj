<template>
  <div class="mt-3">
    <div v-for="row in rows" class="row">
      <div v-for="col in cols"  class="col border border-primary">
        {{row}}--{{col}}
      </div>
    </div>
  </div>
</template>
<script src="./plate.js"></script>
