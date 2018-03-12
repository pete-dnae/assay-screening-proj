import Quill from 'quill';
import _ from 'lodash';
// require styles
import 'quill/dist/quill.core.css';
import 'quill/dist/quill.snow.css';
import 'quill/dist/quill.bubble.css';

import { formatText, paintTable } from '@/models/visualizer';
import { mapGetters, mapActions } from 'vuex';
// import { validateText } from '@/models/editor';
import { getToolTipPosition } from '@/models/tooltip';
import { validateText } from '@/models/editor2.0';

export default {
  name: 'ScriptInputComponent',
  data() {
    return {
      msg: 'Welcome',
      showToolTip: false,
      index: 0,
      image: null,
      rowCount: 8,
      colCount: 12,
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
      error: 'getError',
      parsedPlates: 'getparsedPlates',
      reagents: 'getreagents',
      units: 'getunits',
      currentPlate: 'getCurrentPlate',
      suggestions: 'getSuggestions',
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
    EditorChange() {
      const text = this.editor.getText();
      this.alterToolTip(text);
      this.$store.commit('CLEAR_ERROR', null);
      validateText(text);
      this.paintText();
    },
    paintText() {
      const textLength = this.editor.getText().length;
      this.editor.formatText(0, textLength, 'color', 'green');
      this.editor.formatText(0, textLength, 'font', 'monospace');
      if (this.error) {
        this.error.action.forEach((x, i) => {
          this.editor.formatText(
            this.error.startIndex,
            this.error.length,
            'color',
            x.color,
          );
        });
        this.editor.formatText(
          this.error.startIndex + this.error.length,
          textLength,
          'color',
          'black',
        );
      }
    },
    alterToolTip() {
      this.editor.focus();
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
      if (
        this.suggestions &&
        this.suggestions.length < 5 &&
        this.suggestions.length >= 1
      ) {
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

      this.$store.commit('CLEAR_SUGGESTIONS');
    },
    highlightError() {
      this.editor.setSelection(this.error.startIndex, this.error.length);
    },
    hideSuggestion() {
      this.$store.commit('CLEAR_SUGGESTIONS');
    },
    getCurrentStringRange() {
      this.editor.focus();
      const cursorIndex = this.editor.getSelection().index;
      const textTillCursor = this.editor.getText().slice(0, cursorIndex);
      const currentStringStart = textTillCursor.lastIndexOf(' ');
      return { currentStringStart, cursorIndex };
    },
    async handleFormat() {
      const formattedText = formatText(this.editor.getText());
      await this.editor.setText(formattedText);
      this.EditorChange();
    },
    handleTab(range) {
      this.handleAutoCompleteClick(this.suggestions[this.index]);
      this.index += 1;
      this.index = this.suggestions[this.index] ? this.index : 0;
    },
    handleSelection(range, oldRange, source) {
      if (range && range.length > 1) {
        const text = this.editor.getText(range.index, range.length);
        this.image = paintTable(
          window.webkitURL,
          { rows: this.rowCount, cols: this.colCount },
          range.index,
          text,
        );
      }
    },
  },
  mounted() {
    const Delta = Quill.import('delta');
    const Font = Quill.import('formats/font');
    Font.whitelist = ['monospace'];
    Quill.register(Font, true);
    this.editor = new Quill('#editor', this.options);
    this.editor.on('selection-change', (range, oldRange, source) =>
      this.handleSelection(range, oldRange, source),
    );
    this.editor.keyboard.addBinding({ key: 'tab', shiftKey: true }, (range) =>
      this.handleTab(range),
    );
    this.editor.clipboard.addMatcher(Node.TEXT_NODE, function(node, delta) {
      return new Delta().insert(node.data, { font: 'monospace' });
    });
  },
};
