export default class SVGtoPNGDataURL {
  constructor() {
    this.can = document.createElement('canvas'); // Not shown on page
    this.ctx = this.can.getContext('2d');
    this.loader = new Image(); // Not shown on page
  }

  // Generate PNG data URL from SVG and send it to callback function when ready
  go(mySVG, callback) {
    const svgAsXML = new XMLSerializer().serializeToString(mySVG);
    this.loader.width = this.can.width = 2800;
    this.loader.height = this.can.height = 2800;
    const self = this;
    this.loader.onload = function () {
      self.ctx.drawImage(
        self.loader,
        0,
        0,
        self.loader.width,
        self.loader.height,
      );
      callback(self.can.toDataURL('image/png'));
    };
    this.loader.src = `data:image/svg+xml,${encodeURIComponent(svgAsXML)}`;
  }
}
