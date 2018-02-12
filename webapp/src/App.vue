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

        <router-view/>
    </div>
</div>

</template>

<script>
import Vue from 'vue';
import Menu from '@/components/menu/menu.vue';

Vue.component('titlemenu', Menu);

export default {
  name: 'app',
};
</script>
