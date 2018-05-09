<template>
<form>
    <div class="row ml-2 d-flex justify-content-start text-left">
        <div class="form-group">
            <label class="d-block">Reagent Name</label>
            <input  class="form-control" placeholder="Name" v-model="name">            
        </div>
        <div class="form-group ml-2">
            <label class="d-block">Reagent Category</label>
            <select v-model="category" class="btn btn-primary">
                <option value=null>Please select a category</option>
                <option v-for="option in categoryOptions" v-bind:key="option.name">
                    {{ option.name }}
                </option>
            </select>
        </div>
    </div>
    <hr/>
    <div class="text-left">
        <h5>Add meta data</h5>
    </div>    
    <div class="row ml-2 text-left" v-for="(property,index) in metaObject" v-bind:key="index">
        <div class="form-group">
            <input  class="form-control" placeholder="key" v-model="property['key']">            
        </div>
        <div class="form-group ml-2">
            <input class="form-control" placeholder="value" v-model="property['value']">
        </div>
        <div class="ml-2">
            <button class="btn btn-primary" @click="handleRemoveProperty(index)">Remove row</button>
        </div>
    </div>
    
    <button class="btn btn-primary" @click="handleAddProperty">Add row</button>
    
    <button type="submit" class="btn btn-primary" @click="handleSubmit">Submit</button>
</form>
</template>
<script src='./addreagent.js'></script>