<template>
<div>
<wellResultsSummary :options="headers" 
                    :data="resultList" 
                    :selectedRowProps="['experiment_id','qpcr_plate_id','wells']"
                    >
                    <template slot ='redirect' slot-scope="slotProps">
                        <a :href="'#/summary/'+slotProps.row.experiment_id+'/'+slotProps.row.qpcr_plate_id+'/'+slotProps.row.wells">
                            <button>Open Summary</button>
                        </a>
                    </template>
</wellResultsSummary>
</div>
</template>
<script src='./wellresults.js'></script>