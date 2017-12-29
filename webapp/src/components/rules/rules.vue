<template>
  <ul class="nav navbar-nav mt-3">
    <li class="dropdown dropdown-lg">
      <a href="#" class="dropdown-toggle float-left" data-toggle="dropdown">Rules <b class="caret"></b></a>
      <div v-bind:class="currentDisplayClass"  v-bind:style="currentDisplayStyle" onClick="event.stopPropagation();">

        <div class="row">
          <div class="input-group col-4 ml-3">
            <span class="input-group-addon" id="basic-addon1">Column Block</span>
            <input type="number" class="form-control" v-model="columnRepeats" placeholder="No of repeats" aria-label="number" aria-describedby="basic-addon1">
          </div>
          <div class="col-md-7">
          </div>
          <div class="col">
            <a class="btn btn-danger"  aria-label="Delete" @click="handleRuleClose()">
              <i class="fa fa-window-close" aria-hidden="true"></i>
            </a>
          </div>
        </div>
        <div class="row mt-3">
        <div class="col-2 border-right" >
          <h6 class="dropdown-header">Repeated Every 4 Columns</h6>
          <div class="row">
            <div class="col">
              <span class="dropdown-header">Strains</span>
            </div>
          </div>
          <div class="row">
            <div class="col">
              <editableList></editableList>
            </div>
          </div>
          <div class="row mt-3">
            <div class="col">
              <span class="dropdown-header">ID Primers</span>
            </div>
          </div>
          <div class="row">
            <div class="col">
              <editableList></editableList>
            </div>
          </div>
        </div>
        <div class="col-4 border-right" >
          <h6 class="dropdown-header">Expanded to 4 columns each</h6>
          <div class="row">
            <div class="col">
              <span class="dropdown-header">Template Copies</span>
            </div>
            <expandColumns :columnRepeats="parseInt(columnRepeats)" :type="'template'" @ruleChange="handleRuleChange"></expandColumns>
          </div>
          <div class="row mt-3">
            <div class="col">
              <span class="dropdown-header">HgDna</span>
            </div>
            <expandColumns :columnRepeats="parseInt(columnRepeats)" :type="'HgDna'" @ruleChange="handleRuleChange"></expandColumns>
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
              <editableList></editableList>
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
      </div>

    </li>
  </ul>
</template>
<script src="./rules.js"></script>
