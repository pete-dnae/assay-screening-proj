import Quill from 'quill';
// require styles
import 'quill/dist/quill.core.css';
import 'quill/dist/quill.snow.css';
import 'quill/dist/quill.bubble.css';
import _ from 'lodash';
import { modal, tooltip } from 'vue-strap';
import { formatText, isItemInArray } from '@/models/visualizer';
import hovervisualizer from '@/components/hovervisualizer/hovervisualizer.vue';
import { mapGetters, mapActions } from 'vuex';
import wellcontents from '@/components/wellcontents/wellcontents.vue';

// import { validateText } from '@/models/editor';

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
    hovervisualizer,
    wellcontents,
    tooltip,
  },
  data() {
    return {
      msg: 'Welcome',
      show: false,
      showToolTip: false,
      suggestionIndex: 0,
      currentPlate: null,
      highlightedLineNumber: null,
      showSuggestionList: false,
      showSuggestionToolTip: false,
      currentRow: null,
      currentCol: null,
      showWellContents: false,
      hoverHighlight: true,
      showInfo: false,
    };
  },
  computed: {
    ...mapGetters({
      options: 'getQuillOptions',
      error: 'getError',
      reagents: 'getReagents',
      units: 'getUnits',
      showBlur: 'getBlurFlag',
      tableBoundaries: 'getTableBoundaries',
      allocationMapping: 'getAllocationMap',
      suggestions: 'getSuggestions',
      showSpinner: 'getRuleIsScriptSaving',
      ruleScript: 'getRuleScript',
      allocationData: 'getAllocationData',
      tooltiptext: 'getToolTipStyle',
      referenceText: 'getReferenceExperiment',
    }),
  },
  watch: {
    showToolTip() {
      if (this.showToolTip === false) {
        this.suggestionIndex = 0;
      }
    },
  },
  methods: {
    ...mapActions([
      'saveToDb',
      'fetchExperiment',
      'fetchReagentList',
      'fetchUnitList',
    ]),
    isItemInArray,
    editorChange() {
      const cursorIndex = this.editor.getSelection().index;
      const fields = getCurrentLineFields(this.editor.getText(), cursorIndex);
      if (fields[1] && fields[0][0] === 'A') {
        if (!_.find(this.reagents, reagent => reagent.name === fields[1][0])) {
          const suggestions = this.reagents.filter(
            x => x.name.indexOf(fields[1][0]) !== -1,
          );
          this.$store.commit('SET_SUGGESTIONS', suggestions);
          this.alterToolTip(cursorIndex);
          this.showSuggestionList = suggestions.length > 5;
          this.showSuggestionToolTip = suggestions.length < 5;
        }
      }
      if (fields[5] && (fields[0][0] === 'A' || fields[0][0] === 'T')) {
        if (!_.find(this.units, unit => unit.abbrev === fields[5][0])) {
          const suggestions = this.units.filter(
            unit => unit.abbrev.indexOf(fields[5][0]) !== -1,
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
        this.$route.params.exptNo,
        this.paintText,
      );
    },
    paintText() {
      const text = this.editor.getText();
      const textLength = text.length;
      this.editor.formatText(0, textLength, 'font', 'monospace');
      if (this.error) {
        this.editor.formatText(
          this.error.where_in_script,
          textLength,
          'color',
          '#A9A9A9',
        );
      }
    },
    handleMouseOut(event) {
      if (event.fromElement.nodeName === 'DIV') {
        this.hoverHighlight = false;
        const text = this.editor.getText();
        this.editor.formatText(0, text.length, 'bg', false);
        this.editor.formatText(0, text.length, 'color', false);
      }
    },
    alterToolTip(cursorIndex) {
      const cursorLocation = this.editor.getBounds(cursorIndex);
      const parentBound = document
        .getElementsByClassName('ql-editor')[0]
        .getBoundingClientRect();
      this.$store.commit('ADJUST_TOOL_TIP_POSITION', {
        cursorLocation,
        parentBound,
      });
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
      this.editor.insertText(
        cursorIndex,
        ` ${text.name ? text.name : text.abbrev}`,
        {
          color: 'black',
        },
      );
      this.editor.deleteText(
        currentStringStart,
        cursorIndex - currentStringStart,
      );
      hesitationTimer(
        this.editor.getText(),
        this.$route.params.exptNo,
        this.paintText,
      );
      this.hideSuggestion();
    },
    handleMouseOver(event) {
      const fromElement = event.fromElement;
      if (fromElement && fromElement.tagName === 'SPAN') {
        const text = this.editor.getText();
        const elem = fromElement.parentElement;
        const { lineNumber, plateName } = getChildIndex(elem);
        const [start, end] = startEndOfLine(lineNumber, text);
        this.currentPlate = plateName;
        this.highlightedLineNumber = lineNumber + 1;
        this.editor.formatText(0, text.length, 'bg', false);
        this.editor.formatText(0, text.length, 'color', false);
        this.editor.formatText(start, end - start, 'bg', 'primary');
        this.editor.formatText(start, end - start, 'color', 'white');
        this.hoverHighlight = true;
      }
    },
    highlightError(index) {
      this.editor.setSelection(index, 0);
    },
    handleWellHover([row, col]) {
      [this.currentRow, this.currentCol] = [row, col];
      this.showWellContents = true;
    },
    handleWellHoverComplete() {
      this.showWellContents = false;
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
    handleFormat() {
      const formattedText = formatText(this.editor.getText());
      this.editor.setText(formattedText);
      this.editor.formatText(0, formattedText.length, 'font', 'monospace');
    },
    handleTab() {
      this.handleAutoCompleteClick(this.suggestions[this.suggestionIndex]);
      this.suggestionIndex += 1;
      this.suggestionIndex = this.suggestions[this.suggestionIndex]
        ? this.suggestionIndex
        : 0;
      this.showSuggestionToolTip = false;
    },
    handleReagentAdd() {
      this.$store.commit('ADD_REAGENT', this.newReagent);
      this.show = false;
    },
  },
  mounted() {
    const Delta = Quill.import('delta');

    const Parchment = Quill.import('parchment');
    const LineStyle = new Parchment.Attributor.Style(
      'textShadow',
      'text-shadow',
      {
        scope: Parchment.Scope.INLINE,
      },
    );
    const background = new Parchment.Attributor.Class('bg', 'bg', {
      scope: Parchment.Scope.INLINE,
      whitelist: ['primary', 'secondary', 'success'],
    });

    Quill.register(background, true);
    Quill.register(LineStyle, true);
    // Quill.register(text, true);
    this.editor = new Quill('#editor', this.options);
    this.editor.keyboard.addBinding({ key: 'tab', shiftKey: true }, range =>
      this.handleTab(range),
    );
    this.editor.keyboard.addBinding({ key: '1', shiftKey: true }, range =>
      this.handleExcludeReagent(range),
    );
    this.editor.keyboard.addBinding({ key: 'F', ctrlKey: true }, () =>
      this.handleFormat(),
    );
    this.editor.clipboard.addMatcher(Node.TEXT_NODE, node =>
      new Delta().insert(node.data, { font: 'monospace' }),
    );
    this.fetchReagentList();
    this.fetchUnitList();
    this.fetchExperiment({ exptNo: 1, referenceExperimentFlag: true });
    this.fetchExperiment({ exptNo: this.$route.params.exptNo }).then(() => {
      this.editor.setText(formatText(this.referenceText));
      this.editor.formatText(0, this.ruleScript.length, 'font', 'monospace');
    });

    this.editor.focus();
  },
};
