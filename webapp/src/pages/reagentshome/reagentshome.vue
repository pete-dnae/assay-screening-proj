<template>
<div class="container-fluid mt-2">
    <div class="row">
        <div class="col-6">
            <reagentGroup></reagentGroup>
        </div>
        <div class="col-6 h-100">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Reagents</h5>     
                        <div class="d-flex justify-content-start  bg-dark">
                            <nav class="navbar navbar-dark">                              
                                <nav class="nav nav-pills flex-column flex-sm-row">
                                <li class="nav-item active">
                                    <a class="nav-link" href="#" @click="showReagents=!showReagents">Add New</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" href="#" @click="showReagents=!showReagents">Edit Existing</a>
                                </li>                                
                                </nav>            
                            
                            </nav>
                        </div> 
                        <div class="m-3">            
                            <form v-if="!showReagents">
                                <div class="form-group">
                                    <div class="form-row">
                                        <div class="form-group col-md-6">
                                            <label class="float-left">Reagent Name</label>
                                            <input  class="form-control" 
                                            placeholder="Titanium Taq">
                                        </div>
                                        <div class="form-group col-md-6">
                                            <label class="float-left">Reagent Category</label>
                                            <input  class="form-control" placeholder="Buffer">
                                        </div>
                                    </div>
                                </div>
                            </form>
                            <div v-else-if="reagents[0]">
                                <div class="row">
                                    <div class="col-5">
                                        <label>Search</label>
                                        <input v-model="searchText"/>
                                    </div>
                                    <div class="col-3">
                                        <select v-model="searchField" >
                                            <option value="null">Please select a Search Criteria</option>
                                            <option v-for="key in Object.keys(reagents[0])" v-bind:key="key">{{key}}</option>                    
                                        </select>
                                    </div>
                                    <div class="col-4">
                                        
                                    </div>
                                </div>
                                <table class="text-left table table-striped">
                                    <th v-for="key in Object.keys(reagents[0])" v-bind:key="key">
                                        {{key}}
                                    </th>
                                    <tr v-for="reagent in filteredReagents" v-bind:key="reagent.name">
                                        <td v-for="property in reagent" v-bind:key="property">
                                            {{property}}
                                        </td>                                        
                                    </tr>
                                </table>
                            </div>
                            <div v-else>
                                No Reagents to Display
                            </div>
                        </div> 
                </div>
            </div>
        </div>
    </div>
    
    <div class="mt-3">        
        
        
    </div>

</div>
</template>
<script src="./reagentshome.js"></script>