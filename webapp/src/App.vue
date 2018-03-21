<style>

#app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
}

</style>

<template>

<div>
    <!-- <titlemenu></titlemenu> -->
    <div id="app">
      <experimentmenu></experimentmenu>
        <router-view/>
    </div>
</div>

</template>

<script>
import experimentmenu from '@/components/experimentmenu/experimentmenu.vue';
import Vue from 'vue';


export default {
  name: 'app',
  components:{experimentmenu}
};
</script>
