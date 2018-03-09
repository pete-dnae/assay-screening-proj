import Quill from 'quill';
import _ from 'lodash';
// require styles
import 'quill/dist/quill.core.css';
import 'quill/dist/quill.snow.css';
import 'quill/dist/quill.bubble.css';

import { formatText } from '@/models/visualizer';
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
      this.$store.commit('LOG_ERROR', null);
      validateText(text);
      this.paintText();
    },
    paintText() {
      const textLength = this.editor.getText().length;
      this.editor.formatText(0, textLength, 'color', 'green');
      if (this.error) {
        this.error.action.forEach((x, i) => {
          this.editor.formatText(
            this.error.startIndex,
            this.error.length,
            'color',
            x.color,
          );
        });
        // this.editor.removeFormat(
        //   this.error.startIndex + this.error.length,
        //   textLength,
        // );
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
    highlightError(err) {
      this.editor.setSelection(err.index, err.length);
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
    handleFormat() {
      this.editor.setText(formatText(this.editor.getText()));
    },
    handleTab(range) {
      this.handleAutoCompleteClick(this.suggestions[this.index]);
      this.index += 1;
      this.index = this.suggestions[this.index] ? this.index : 0;
    },
  },
  mounted() {
    const Delta = Quill.import('delta');
    const Font = Quill.import('formats/font');
    Font.whitelist = ['monospace'];
    Quill.register(Font, true);
    this.editor = new Quill('#editor', this.options);
    // this.editor.on('text-change', (...args) => this.onEditorChange(args));
    // this.editor.clipboard.addMatcher(Node.TEXT_NODE, function(node, delta) {
    //   return new Delta().insert(node.data);
    // });
    this.editor.keyboard.addBinding({ key: 'tab', shiftKey: true }, (range) =>
      this.handleTab(range),
    );
  },
};
