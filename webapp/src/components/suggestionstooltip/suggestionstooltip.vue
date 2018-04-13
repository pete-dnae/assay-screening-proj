<style scoped>
ul {
  margin: 0;
  margin-top: 2px;
  padding: 0;
  width: 300px;
  list-style: none;
  background: #efefef;
}

li {
  padding: 5px 5px;
  cursor: pointer;
}

li:hover {
  background: #ddd;
}

li span {
  font-weight: bold;
}
</style>
 <template>
 <span v-bind:style="toolTipPosition">            
    <ul >
        <li v-for = "text in suggestions" v-bind:key="text.url" @click.left="handleAutoCompleteClick(text);"
        @click.right="hideSuggestion()">
            <div>{{text}}</div>            
        </li>
    </ul>
</span>
</template>
<script src="./suggestionstooltip.js"></script>