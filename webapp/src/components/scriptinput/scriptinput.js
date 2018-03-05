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
      showToolTip: false,
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
      const cursorIndex = this.editor.getSelection().index;
      const cursorLocation = this.editor.getBounds(cursorIndex);
      const parentBound = document
        .getElementsByClassName('ql-editor')[0]
        .getBoundingClientRect();
      this.tooltiptext = getToolTipPosition(
        this.tooltiptext,
        cursorLocation,
        parentBound,
      );
      const textTillCursor = text.slice(0, cursorIndex);
      const currentStringStart = textTillCursor.lastIndexOf(' ');
      const currentString = text.slice(currentStringStart, cursorIndex);

      this.suggestions = this.reagents.filter(
        (x) => x.indexOf(currentString.trim()) > -1,
      );
      if (this.suggestions.length < 5 && this.suggestions.length > 1) {
        this.showToolTip = true;
      } else {
        this.showToolTip = false;
      }
    },
    handleAutoCompleteClick(text) {
      this.editor.focus();
      this.editor.insertText(this.editor.getSelection().index, text, {
        color: 'black',
      });
      this.showToolTip = false;
    },
    highlightError(err) {
      this.editor.setSelection(err.index, err.length);
    },
  },
  mounted() {
    this.editor = new Quill('#editor', this.options);
    this.editor.on('text-change', (...args) => this.onEditorChange(args));
  },
};
