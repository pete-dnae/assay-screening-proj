<template>
  <div class="mt-3">
    <div v-for="row in rows" class="row">
      <div v-for="col in cols"  class="col border border-primary">
        <div class="row">{{row}}--{{col +1}}</div>
        <div class="row" v-if="templateData[row] && templateData[row][col]">

          <span>{{templateData[row][col]}} Cp</span>

        </div>
        <div class="row" v-if="hgDNAData[row] && hgDNAData[row][col]">

          <span>{{hgDNAData[row][col]}} hgDNA</span>
          </div>
        </div>
      </div>
    </div>

  </div>

</template>
<script src="./plate.js"></script>
