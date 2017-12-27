<template>
  <ul class="nav navbar-nav mt-3">
    <li class="dropdown dropdown-lg">
      <a href="#" class="dropdown-toggle float-left" data-toggle="dropdown">Rules <b class="caret"></b></a>
      <ul class="dropdown-menu dropdown-menu-lg w-100">
        <div class="row">
          <div class="input-group col-4 ml-3">
            <span class="input-group-addon" id="basic-addon1">Column Block</span>
            <input type="number" class="form-control" placeholder="No of repeats" aria-label="number" aria-describedby="basic-addon1">
          </div>
        </div>
        <div class="row mt-3">
        <div class="col-4 border-right" >
          <h6 class="dropdown-header">Repeated Every 4 Columns</h6>
          <div class="row">
            <div class="col">
              <span class="dropdown-header">Strains</span>
            </div>
            <div class="col">
              <ul class="list-group">
                <li class="list-group-item">Eco</li>
                <li class="list-group-item">Efs VanB</li>
                <li class="list-group-item">Efs VanB</li>
                <li class="list-group-item">Kox</li>
              </ul>
            </div>
          </div>
          <div class="row mt-3">
            <div class="col">
              <span class="dropdown-header">ID Primers</span>
            </div>
            <div class="col">
              <ul class="list-group">
                <li class="list-group-item">Ec_uidA_6.x_Eco63_Eco60</li>
                <li class="list-group-item">Efs_cpn60_1.x_Efs04_Efs01</li>
                <li class="list-group-item">Efs_vanB_1.x_van10_van06</li>
                <li class="list-group-item">Ko_pehX_1.x_Kox05_Kox02</li>
              </ul>
            </div>
          </div>
        </div>
        <div class="col-4 border-right" >
          <h6 class="dropdown-header">Expanded to 4 columns each</h6>
          <div class="row">
            <div class="col">
              <span class="dropdown-header">Template Copies</span>
            </div>
            <div class="col">
              <select  multiple>
                <option disabled value="">Please select one</option>
                <option>A</option>
                <option>B</option>
                <option>C</option>
                <option>D</option>
                <option>E</option>
                <option>F</option>
              </select>
            </div>
            <div class="col">
              <input placeholder="column numbers">
            </div>
          </div>
          <div class="row mt-3">
            <div class="col">
              <span class="dropdown-header">HgDna</span>
            </div>
            <div class="col">
              <select  multiple>
                <option disabled value="">Please select one</option>
                <option>A</option>
                <option>B</option>
                <option>C</option>
                <option>D</option>
                <option>E</option>
                <option>F</option>
              </select>
            </div>
            <div class="col">
              <input  placeholder="column numbers">
            </div>
          </div>
          <div class="row mt-3">
            <div class="col">
              <span class="dropdown-header">Dilution Factor</span>
            </div>
            <div class="col">

            </div>
            <div class="col">
              <input  placeholder="values seperated by ','">
            </div>
          </div>

        </div>
        <div class="col-4" >
          <h6 class="dropdown-header">PA Primers</h6>
          <div class="row mt-3">
            <div class="col">
              <span class="dropdown-header">First Block</span>
            </div>
            <div class="col">
              <select >
                <option disabled value="">Please select one</option>
                <option>Ec_uidA_6.x_Eco63_Eco60</option>
                <option>PoolA</option>
                <option>Ko_pehX_1.x_Kox05_Kox02</option>
              </select>
            </div>
          </div>
          <div class="row mt-3">
            <div class="col">
              <span class="dropdown-header">Second Block</span>
            </div>
            <div class="col">
              <select >
                <option disabled value="">Please select one</option>
                <option>Ec_uidA_6.x_Eco63_Eco60</option>
                <option>PoolA</option>
                <option>Ko_pehX_1.x_Kox05_Kox02</option>
              </select>
            </div>
          </div>
          <div class="row mt-3">
            <div class="col">
              <span class="dropdown-header">Third Block</span>
            </div>
            <div class="col">
              <select >
                <option disabled value="">Please select one</option>
                <option>Ec_uidA_6.x_Eco63_Eco60</option>
                <option>PoolA</option>
                <option>Ko_pehX_1.x_Kox05_Kox02</option>
              </select>
            </div>
          </div>
          <div class="row mt-3">
            <div class="col">
              <span class="dropdown-header">Custom</span>
            </div>
            <div class="col mr-2">
              <ul class="list-group">
                <li class="list-group-item">Ec_uidA_6.x_Eco63_Eco60</li>
                <li class="list-group-item">Efs_cpn60_1.x_Efs04_Efs01</li>
                <li class="list-group-item">Efs_vanB_1.x_van10_van06</li>
                <li class="list-group-item">Ko_pehX_1.x_Kox05_Kox02</li>
              </ul>
            </div>
          </div>
        </div>
        </div>
        <div class="row">
          <div class="input-group col-4 m-3">
            <span class="input-group-addon" id="basic-addon1">Suppress Columns</span>
            <input type="number" class="form-control" placeholder="No of repeats" aria-label="number" aria-describedby="basic-addon1">
          </div>
        </div>
      </ul>

    </li>
  </ul>
</template>
<script src="./rules.js"></script>
