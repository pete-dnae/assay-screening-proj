<style>

.dropdown-menu > li > a {
    cursor: pointer;
}

</style>

<template>

<div style="position: relative">    
    <input class="form-control" autocomplete="off" 
            v-model="val" 
            :placeholder="placeholder" 
            :type.once="type" 
            @blur="showDropdown = false" 
            @keydown.down.prevent="down" 
            @keydown.enter="hit" 
            @keydown.esc="reset" 
            @keydown.up.prevent="up" />
    <ul :class="{'dropdown-menu':true,show:showDropdown}" ref="dropdown">
        <div class="list-group">
            <li v-for="(item, i) in items" :class="{'list-group-item':true,active: isActive(i)}" v-bind:key="i">
                <a @mousedown.prevent="hit" @mousemove="setActive(i)">
                    <component :is="templateComp" :item="item"></component>
                </a>
            </li>
        </div>
    </ul>
</div>

</template>

<script src="./Typeahead.js"> </script>
