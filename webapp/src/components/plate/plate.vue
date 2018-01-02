<template>
  <div class="mt-3">
    <div v-for="row in rows" class="row">
      <div v-for="col in cols"  class="col border border-primary">
        <div class="row">{{row}}--{{col +1}}</div>
        <div class="row" v-if="templateData[row] && templateData[row][col]">

          <div class="col">{{templateData[row][col]}} Cp</div>

        </div>
        <div class="row" v-if="hgDNAData[row] && hgDNAData[row][col]">

          <div class="col">{{hgDNAData[row][col]}} hgDNA</div>
          </div>
          <div class="row" v-if="idPrimerData[row] && idPrimerData[row][col]">

            <div class="col" style="color:green">{{idPrimerData[row][col]}} </div>
            </div>
            <div class="row" v-if="strainData[row] && strainData[row][col]">

              <div class="col" style="color:red">{{strainData[row][col]}}</div>
            </div>
        </div>
      </div>

    </div>



</template>
<script src="./plate.js"></script>
