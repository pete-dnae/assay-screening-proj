<template>
  <div class="hello">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="#">Assay Experiment Design</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <span ><b>Experiment</b></span>
      <div class="dropdown pl-3">
        <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenu2" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          {{currentExpt}}
        </button>

      <div class="dropdown-menu" style="width:400px;height:100px" onClick="event.stopPropagation();" aria-labelledby="dropdownMenu2">
        <ExptLoad @experimentChange="handleExptChange"></ExptLoad>
      </div>
    </div>

    </nav>
  </div>
</template>

<script src="./menu.js"></script>
