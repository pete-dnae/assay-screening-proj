<template>
<div>
<select v-model="selected">
  <option v-for="(value,key) in experimentImages"  v-bind:key="key">{{key}}</option>
</select>
<img :src="image" style='height: 100%; width: 100%; object-fit: contain'/>
</div>
</template>
<script src="./pictures.js"></script>