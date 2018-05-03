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
                                    <a class="nav-link" href="#" >Add New</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" href="#">Edit Existing</a>
                                </li>                                
                                </nav>            
                            
                            </nav>
                        </div> 
                        <div class="m-3">            
                            <form>
                                <div class="form-group">
                                    <div class="form-row">
                                        <div class="form-group col-md-6">
                                            <label class="float-left">Reagent Name</label>
                                            <input  class="form-control" placeholder="Titanium Taq">
                                        </div>
                                        <div class="form-group col-md-6">
                                            <label class="float-left">Reagent Category</label>
                                            <input  class="form-control" placeholder="Buffer">
                                        </div>
                                    </div>
                                </div>
                            </form>
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