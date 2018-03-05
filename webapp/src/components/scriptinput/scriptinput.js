import Quill from 'quill';
import _ from 'lodash';
// require styles
import 'quill/dist/quill.core.css';
import 'quill/dist/quill.snow.css';
import 'quill/dist/quill.bubble.css';

import { mapGetters, mapActions } from 'vuex';
import { validateText, splitLine } from '@/models/editor';
import { getToolTipPosition } from '@/models/tooltip';

export default {
  name: 'ScriptInputComponent',
  data() {
    return {
      msg: 'Welcome',
      suggestions: null,
      tooltiptext: {
        visibility: 'visible',
        'max-height': '300px',
        'max-width': '500px',
        'text-align': 'center',
        'border-radius': '6px',
        padding: '5px 0',

        /* Position the tooltip */
        position: 'absolute',
        'z-index': 99999,
      },
    };
  },
  computed: {
    ...mapGetters({
      options: 'getQuillOptions',
      version: 'getVersion',
      validTextObjects: 'getValidTextObjects',
      invalidTextObjects: 'getInValidTextObjects',
      errorMessages: 'getErrorMessages',
      parsedPlates: 'getparsedPlates',
      reagents: 'getreagents',
      units: 'getunits',
    }),
  },
  watch: {},
  methods: {
    ...mapActions(['setFeedback']),
    onEditorChange([delta, oldDelta, source]) {
      if (source === 'user') {
        const text = this.editor.getText();
        this.alterToolTip(text);
        this.setFeedback(
          validateText(text, {
            version: this.version,
            parsedPlates: this.parsedPlates,
            reagents: this.reagents,
            units: this.units,
          }),
        );
        this.paintText();
      }
    },
    paintText() {
      this.validTextObjects.forEach((range) => {
        this.editor.formatText(
          range.index,
          range.length,
          range.action[0],
          range.action[1],
        );
      });
      this.invalidTextObjects.forEach((range) => {
        this.editor.formatText(
          range.index,
          range.length,
          range.action[0],
          range.action[1],
        );
      });
    },
    alterToolTip(text) {
      const bounds = this.editor.getBounds(this.editor.getSelection().index);
      this.tooltiptext = getToolTipPosition(this.tooltiptext, bounds);
      const strings = splitLine(text);
      strings.pop();
      const currentString = strings.pop();
      this.suggestions = this.reagents.filter(
        (x) => x.indexOf(currentString) > -1,
      );
    },
  },
  mounted() {
    this.editor = new Quill('#editor', this.options);
    this.editor.on('text-change', (...args) => this.onEditorChange(args));
  },
};
