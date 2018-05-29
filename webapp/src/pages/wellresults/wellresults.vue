<template>
<div >
<wellResultsSummary :options="headers" 
                    :data="resultList" 
                    :selectedRowProps="['experiment_id','qpcr_plate_id','wells']"
                    @tableRowSelected="getSummary"></wellResultsSummary>
</div>
</template>
<script src='./wellresults.js'></script>