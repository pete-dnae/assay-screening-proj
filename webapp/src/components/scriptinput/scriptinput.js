import Quill from 'quill';
// require styles
import 'quill/dist/quill.core.css';
import 'quill/dist/quill.snow.css';
import 'quill/dist/quill.bubble.css';
import { modal } from 'vue-strap';
import { formatText, paintTable } from '@/models/visualizer';
import { mapGetters, mapActions } from 'vuex';

// import { validateText } from '@/models/editor';
import { getToolTipPosition } from '@/models/tooltip';
import {
  hesitationTimer,
  startEndOfLine,
  getChildIndex,
  getCurrentLineFields,
} from '@/models/editor2.0';

export default {
  name: 'ScriptInputComponent',
  components: {
    modal,
  },
  data() {
    return {
      msg: 'Welcome',
      show: false,
      showToolTip: false,
      index: 0,
      newReagent: null,
      image: null,
      rowCount: 8,
      colCount: 12,
      showSuggestionList: false,
      showSuggestionToolTip: false,
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
      reagents: 'getReagents',
      units: 'getUnits',
      currentPlate: 'getCurrentPlate',
      suggestions: 'getSuggestions',
      showSpinner: 'getRuleIsScriptSaving',
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
    ...mapActions(['saveToDb']),
    editorChange() {
      const cursorIndex = this.editor.getSelection().index;
      const fields = getCurrentLineFields(this.editor.getText(), cursorIndex);
      if (fields[1] && fields[0][0] === 'A') {
        if (this.reagents.indexOf(fields[1][0]) === -1) {
          const suggestions = this.reagents.filter(
            (x) => x.indexOf(fields[1][0]) !== -1,
          );
          this.$store.commit('SET_SUGGESTIONS', suggestions);
          this.alterToolTip(cursorIndex);
          this.showSuggestionList = suggestions.length > 5;
          this.showSuggestionToolTip = suggestions.length < 5;
        }
      }
      hesitationTimer.cancel();
      hesitationTimer(
        this.editor.getText(),
        this.$route.params.ruleScript,
        this.paintText,
      );
    },
    paintText() {
      const text = this.editor.getText();
      const textLength = text.length;
      this.editor.formatText(0, textLength, 'color', 'green');
      this.editor.formatText(0, textLength, 'font', 'monospace');
      if (this.error) {
        const lineEnd = text
          .substr(this.error.where_in_script, textLength)
          .indexOf('\n');
        this.editor.formatText(
          this.error.where_in_script,
          lineEnd,
          'color',
          'black',
        );
        this.editor.formatText(
          lineEnd + this.error.where_in_script,
          textLength,
          'color',
          '#A9A9A9',
        );
      }
    },
    alterToolTip(cursorIndex) {
      const cursorLocation = this.editor.getBounds(cursorIndex);
      const parentBound = document
        .getElementsByClassName('ql-editor')[0]
        .getBoundingClientRect();
      this.tooltiptext = getToolTipPosition(
        this.tooltiptext,
        cursorLocation,
        parentBound,
      );
    },
    handleExcludeReagent() {
      const { currentStringStart, cursorIndex } = this.getCurrentStringRange();
      this.newReagent = this.editor
        .getText()
        .substr(currentStringStart, cursorIndex)
        .replace('!', '');
      this.show = true;
      document.getElementById('modal').focus();
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
    },
    handleMouseOver(event) {
      const fromElement = event.fromElement;
      if (fromElement.tagName === 'SPAN') {
        const text = this.editor.getText();
        const elem = fromElement.parentElement;
        const lineNumber = getChildIndex(elem);
        const [start, end] = startEndOfLine(lineNumber, text);
        this.editor.formatText(0, text.length, 'text-shadow', false);
        this.editor.formatText(
          start,
          end - start,
          'text-shadow',
          '2px 2px 4px #000000',
        );
      }

      // console.log(event.fromElement);
    },
    highlightError(index) {
      this.editor.setSelection(index, 0);
    },
    hideSuggestion() {
      this.showSuggestionList = false;
      this.showSuggestionToolTip = false;
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
    handleTab() {
      this.handleAutoCompleteClick(this.suggestions[this.index]);
      this.index += 1;
      this.index = this.suggestions[this.index] ? this.index : 0;
      this.showSuggestionToolTip = false;
    },
    handleReagentAdd() {
      this.$store.commit('ADD_REAGENT', this.newReagent);
      this.show = false;
    },
    handleSelection(range) {
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
    const Parchment = Quill.import('parchment');
    const LineStyle = new Parchment.Attributor.Style(
      'textShadow',
      'text-shadow',
      {
        scope: Parchment.Scope.INLINE,
      },
    );
    Quill.register(LineStyle, true);
    Font.whitelist = ['monospace'];
    Quill.register(Font, true);
    this.editor = new Quill('#editor', this.options);
    this.editor.on('selection-change', (range, oldRange, source) =>
      this.handleSelection(range, oldRange, source),
    );
    this.editor.keyboard.addBinding({ key: 'tab', shiftKey: true }, (range) =>
      this.handleTab(range),
    );
    this.editor.keyboard.addBinding({ key: '1', shiftKey: true }, (range) =>
      this.handleExcludeReagent(range),
    );
    this.editor.clipboard.addMatcher(Node.TEXT_NODE, (node) =>
      new Delta().insert(node.data, { font: 'monospace' }),
    );

    this.editor.focus();
  },
};
