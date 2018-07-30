
<template>
    <div class="fluid-container">
        <table class="table table-striped table-hover" id="table" style="font-size: .45vw;" onselectstart="return false;">
            <thead>
                <th>Selected</th>
                <th v-for="(value,key) in options" v-bind:key="key" @click="handleSortBy(key)">{{value.title}}</th>
            </thead>
            <thead v-if="!searchByColumns">
                    <th>
                    </th>
                    <th v-for="(value,key) in options" v-bind:key="key" >
                        <input v-model="search[key]" style="max-width:100%;width:100%"/>                        
                    </th> 
            </thead>
            <tbody class="text-left">                
                <tr v-for ="(row,id) in filteredRows"  v-bind:key="id" @click="handleTableRowClick(id)">
                    <td>
                        <i class="fa fa-check" aria-hidden="true" v-if="checkRowSelected(id)"></i>
                    </td>    
                    <td v-for="(value,key) in options" :class="determineClass(row,value)" v-bind:key="key" >                               
                        <div v-if="value.array">                 
                            <ul style="padding:0;list-style-type: none">
                                <li v-for="value in row[key]" v-bind:key="value" v-if ="value">
                                    <i v-if="options[key].round">{{handleRoundOff(value)}}</i>
                                    <label v-else>{{value}}</label>
                                </li>
                            </ul>
                        </div>
                        <div v-else>
                            <i v-if="options[key].round">{{handleRoundOff(row[key])}}</i>
                            <label v-else-if="columnsToColor.includes(key)" 
                            :class="{'text-success':row[key],'text-danger':!row[key]}">{{row[key]}}</label>
                            <label v-else>{{row[key]}}</label>
                        </div>
                    </td>
                    <td>
                        <slot v-bind:row="row" name='redirect'>                    
                            
                        </slot>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
<script src='./table.js'></script>
<style scoped>
.table td{
    padding: .2em !important;
}
.overflow-wrap {
  overflow-wrap: break-word !important;  
}

</style>