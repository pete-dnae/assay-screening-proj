import { dropdown } from 'vue-strap';
import SVGtoPNGDataURL from '@/models/SVGtoPNG';
import { makeSVG } from '@/models/visualizer';

export default {
  name: 'pictures',
  components: {
    dropdown,
  },
  data() {
    return {
      image: null,
      selected: null,
    };
  },
  props: {
    experimentImages: Object,
  },
  watch: {
    selected() { this.generateImage(); },
    experimentImages() { this.generateImage(); },
  },
  methods: {
    generateImage() {
      const html = this.experimentImages[this.selected];
      const template = document.createElement('div');
      template.innerHTML = makeSVG(html);
      const converter = new SVGtoPNGDataURL();
      converter.go(template.firstElementChild, (dataURL) => {
        this.image = dataURL;
      });
    },
  },
};
