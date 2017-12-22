<template>
  <div class="container-fluid">

    <ul class="nav nav-tabs">
      <li class="nav-item">
        <a class="nav-link active" id="Plate-1" data-toggle="tab" href="#Plate1">Plate 1</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" id="Plate-2" data-toggle="tab" href="#Plate2">Plate 2</a>
      </li>
      <li class="nav-item">
        <a class="nav-link"  data-toggle="tab" href="#">+</a>
      </li>

    </ul>
    <div class="tab-content" id="myTabContent">
      <div class="tab-pane fade show active" id="Plate1" role="tabpanel" aria-labelledby="Plate-1"><div class="card">
        <div>
          This is some text within a card body.
        </div>
      </div>
    </div>
    <div class="tab-pane fade" id="Plate2" role="tabpanel" aria-labelledby="Plate-2">...</div>

    </div>
  </div>
</template>

<script src="./home.js"></script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
