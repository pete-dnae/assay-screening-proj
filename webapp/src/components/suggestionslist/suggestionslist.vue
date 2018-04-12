<template>
<div class="m-2 text-left ">
    <h5 class="mt-3 w-100"><strong>Suggestions :</strong></h5>
    <h5><strong>Currently retreiving 5+ suggestions</strong></h5>
    <div class="list-group w-100 pre-scrollable">
        <button class="list-group-item list-group-item-action" v-for="text in suggestions" 
        v-bind:key="text.url" @click.left="handleAutoCompleteClick(text);" @click.middle="hideSuggestion()">
            <div v-if="text['name']">{{text['name']}}</div>
            <div v-else>{{text['abbrev']}}</div>
        </button>
    </div>
</div>  
</template>
<script src="./suggestionslist.js"></script>