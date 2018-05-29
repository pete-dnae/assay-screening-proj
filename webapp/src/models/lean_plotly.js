const Plotly = require('plotly.js/lib/core');
const scatter = require('plotly.js/lib/scatter');
const histogram = require('plotly.js/lib/histogram');
// Load only the required components from Plotly to avoid issues with glslify
Plotly.register([
  scatter,
  histogram,
]);

module.exports = Plotly;

