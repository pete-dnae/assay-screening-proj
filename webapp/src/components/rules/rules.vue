<template>
  <div>
  <ul class="nav navbar-nav mt-3">
    <li class="dropdown dropdown-lg">
      <a href="#" class="dropdown-toggle float-left" data-toggle="dropdown" >Rules <b class="caret"></b></a>
      <button class="float-left ml-3" @click="showRight = true"> Show Rules on sidebar</button>
      <div v-bind:class="currentDisplayClass"  v-bind:style="currentDisplayStyle" onClick="event.stopPropagation();">
        <div class="row">
          <div class="input-group col-4 ml-3">
            <span class="input-group-addon" id="basic-addon1">Column Block</span>
            <input type="number" class="form-control" v-model="columnBlocks" placeholder="No of repeats" aria-label="number" aria-describedby="basic-addon1">
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
        <div class="col-3 border-right" >
          <h6 class="dropdown-header">Repeated Every 4 Columns</h6>
          <div class="row">
            <div class="col">
              <span class="dropdown-header">Strains</span>
            </div>
          </div>
          <div class="row">
            <div class="col">
              <editableList :columnBlocks="parseInt(columnBlocks)" :type="'Strain'"></editableList>
            </div>
          </div>
          <div class="row mt-3">
            <div class="col">
              <span class="dropdown-header">ID Primers</span>
            </div>
          </div>
          <div class="row">
            <div class="col">
              <editableList :columnBlocks="parseInt(columnBlocks)" :type="'ID Primers'"></editableList>
            </div>
          </div>
        </div>
        <div class="col-5 border-right" >
          <h6 class="dropdown-header">Expanded to 4 columns each</h6>
          <div class="row">
            <div class="col">
              <span class="dropdown-header">Template Copies</span>
            </div>
            <expandColumns :columnBlocks="parseInt(columnBlocks)" :type="'template'" :data="templates" @ruleChange="handleRuleChange"></expandColumns>
          </div>
          <div class="row mt-3">
            <div class="col">
              <span class="dropdown-header">HgDna</span>
            </div>
            <expandColumns :columnBlocks="parseInt(columnBlocks)" :type="'HgDna'" :data="hgDNA" @ruleChange="handleRuleChange"></expandColumns>
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
            <input type="number" class="form-control" v-model="surpressColumns" placeholder="No of repeats" aria-label="number" aria-describedby="basic-addon1">
          </div>
        </div>
      </div>

    </li>

  </ul>


<sidebar :show="showRight" @close='showRight = false' placement="right" header="Rules" width="350">
  <nav>
  <div class="nav nav-tabs" id="nav-tab" role="tablist">
    <a class="nav-item nav-link active" id="nav-home-tab" data-toggle="tab" href="#strain" role="tab" aria-controls="strain" aria-selected="true">Repeat Col</a>
    <a class="nav-item nav-link" id="nav-profile-tab" data-toggle="tab" href="#nav-profile" role="tab" aria-controls="nav-profile" aria-selected="false">Expand Col</a>
    <a class="nav-item nav-link" id="nav-contact-tab" data-toggle="tab" href="#nav-contact" role="tab" aria-controls="nav-contact" aria-selected="false">Primers</a>
  </div>
</nav>
<div class="tab-content" id="nav-tabContent">
  <div class="tab-pane fade show active" id="strain" role="tabpanel" aria-labelledby="nav-home-tab">
    <div class="row mt-3">
      <div class="col">
        <span class="dropdown-header">Strains</span>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <editableList :columnBlocks="parseInt(columnBlocks)" :type="'Strain'"></editableList>
      </div>
    </div>
    <div class="row mt-3">
      <div class="col">
        <span class="dropdown-header">ID Primers</span>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <editableList :columnBlocks="parseInt(columnBlocks)" :type="'ID Primers'"></editableList>
      </div>
    </div>
  </div>
  <div class="tab-pane fade" id="nav-profile" role="tabpanel" aria-labelledby="nav-profile-tab">
    <div class="row">
      <div class="col">
        <span class="dropdown-header">Template Copies</span>
      </div>
      <expandColumns :columnBlocks="parseInt(columnBlocks)" :type="'template'" :data="templates" @ruleChange="handleRuleChange"></expandColumns>
    </div>
    <div class="row mt-3">
      <div class="col">
        <span class="dropdown-header">HgDna</span>
      </div>
      <expandColumns :columnBlocks="parseInt(columnBlocks)" :type="'HgDna'" :data="hgDNA" @ruleChange="handleRuleChange"></expandColumns>
    </div>
  </div>
  <div class="tab-pane fade" id="nav-contact" role="tabpanel" aria-labelledby="nav-contact-tab">...</div>
</div>



</sidebar>
</div>
</template>
<script src="./rules.js"></script>
