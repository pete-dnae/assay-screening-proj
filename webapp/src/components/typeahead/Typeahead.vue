<style>

.dropdown-menu > li > a {
    cursor: pointer;
}

</style>

<template>

<div style="position: relative">    
    <button type="button" class="btn btn-secondary" disabled><i class="fa fa-flask" aria-hidden="true"></i></button>
    <input class="form-control" autocomplete="off" 
            v-model="val" 
            :placeholder="placeholder" 
            :type.once="type" 
            @blur="showDropdown = false" 
            @keydown.down.prevent="down" 
            @keydown.enter="hit" 
            @keydown.esc="reset" 
            @keydown.up.prevent="up" />
    <span class="input-group-prepend"><i class="fa fa-search btn btn-secondary" aria-hidden="true"></i></span>

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
