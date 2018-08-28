<template>
<form>
    <loader v-if="isPosting"></loader>
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
    <hr/>
    <h5 class="text-left">Bulk Upload</h5>
    <div class="row">
        <div class="col">
            <input type="file" id='bulkLoad'/>
        </div>
        <div class="col">
            <button class="btn btn-primary" @click="handleFileUpload">Upload reagents in file</button>
        </div>
    </div>
    <div class="row">
        <div class="col-12 text-left">
            <label>Upload Response</label>
            <textarea v-model="uploadFeedBack" class="w-100" disabled></textarea>
        </div>
    </div>
</form>
</template>
<script src='./addreagent.js'></script>