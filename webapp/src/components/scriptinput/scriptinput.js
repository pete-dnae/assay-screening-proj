import Quill from 'quill';
import _ from 'lodash';
// require styles
import 'quill/dist/quill.core.css';
import 'quill/dist/quill.snow.css';
import 'quill/dist/quill.bubble.css';

import { formatText } from '@/models/visualizer';
import { mapGetters, mapActions } from 'vuex';
import { validateText } from '@/models/editor';
import { getToolTipPosition } from '@/models/tooltip';

export default {
  name: 'ScriptInputComponent',
  data() {
    return {
      msg: 'Welcome',
      suggestions: null,
      showToolTip: false,
      index: 0,
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
      currentPlate: 'getCurrentPlate',
    }),
  },
  watch: {
    showToolTip() {
      if (this.showToolTip === false) {
        this.index = 0;
      }
    },
  },
  methods: {
    ...mapActions(['setFeedback', 'setRuleStart', 'setCurrentElement']),
    onEditorChange([delta, oldDelta, source]) {
      if (source === 'user') {
        const text = this.editor.getText();
        this.alterToolTip(text);
        this.setFeedback(
          validateText(
            text,
            {
              version: this.version,
              parsedPlates: this.parsedPlates,
              reagents: this.reagents,
              units: this.units,
              currentPlate: this.currentPlate,
            },
            this,
          ),
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
      const { currentStringStart, cursorIndex } = this.getCurrentStringRange();
      const cursorLocation = this.editor.getBounds(cursorIndex);
      const parentBound = document
        .getElementsByClassName('ql-editor')[0]
        .getBoundingClientRect();
      this.tooltiptext = getToolTipPosition(
        this.tooltiptext,
        cursorLocation,
        parentBound,
      );

      const currentString = text.slice(currentStringStart, cursorIndex);

      this.suggestions = this.reagents.filter(
        (x) => x.indexOf(currentString.trim()) > -1,
      );
      if (this.suggestions.length < 5 && this.suggestions.length >= 1) {
        this.showToolTip = true;
      } else {
        this.showToolTip = false;
      }
    },
    handleAutoCompleteClick(text) {
      const { currentStringStart, cursorIndex } = this.getCurrentStringRange();
      this.editor.insertText(cursorIndex, ` ${text}`, {
        color: 'black',
      });
      this.editor.deleteText(
        currentStringStart,
        cursorIndex - currentStringStart,
      );

      this.showToolTip = false;
    },
    highlightError(err) {
      this.editor.setSelection(err.index, err.length);
    },
    hideSuggestion() {
      this.showToolTip = false;
    },
    getCurrentStringRange() {
      this.editor.focus();
      const cursorIndex = this.editor.getSelection().index;
      const textTillCursor = this.editor.getText().slice(0, cursorIndex);
      const currentStringStart = textTillCursor.lastIndexOf(' ');
      return { currentStringStart, cursorIndex };
    },
    handleFormat() {
      this.editor.setText(formatText(this.editor.getText()));
    },
    handleTab(range) {
      console.log(this.suggestions);
      this.handleAutoCompleteClick(this.suggestions[this.index]);
      this.index += 1;
    },
  },
  mounted() {
    const Delta = Quill.import('delta');
    const Font = Quill.import('formats/font');
    Font.whitelist = ['monospace'];
    Quill.register(Font, true);
    this.editor = new Quill('#editor', this.options);
    this.editor.on('text-change', (...args) => this.onEditorChange(args));
    this.editor.clipboard.addMatcher(Node.TEXT_NODE, function(node, delta) {
      return new Delta().insert(node.data);
    });
    this.editor.keyboard.addBinding({ key: 'tab', shiftKey: true }, (range) =>
      this.handleTab(range),
    );
  },
};
