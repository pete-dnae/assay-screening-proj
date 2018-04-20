<template>
<div>
    <HotTable :root="root" :settings="hotSettings"></HotTable>
    <button class="btn btn-info float-left mt-3" @click="getData">Save</button>
    {{data}}
</div>
</template>
<script src="./hottable.js"></script>