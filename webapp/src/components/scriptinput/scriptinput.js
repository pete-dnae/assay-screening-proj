import Quill from 'quill';
// require styles
import 'quill/dist/quill.core.css';
import 'quill/dist/quill.snow.css';
import _ from 'lodash';
import { modal, tooltip } from 'vue-strap';
import { formatText } from '@/models/visualizer';
import hovervisualizer from '@/components/hovervisualizer/hovervisualizer.vue';
import { mapGetters, mapActions } from 'vuex';
import wellcontents from '@/components/wellcontents/wellcontents.vue';
// import { validateText } from '@/models/editor';

import {
  hesitationTimer,
  getCurrentLineFields,
  findSuggestions,
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
      suggestionIndex: 0,
      editor: null,
    };
  },
  computed: {
    ...mapGetters({
      options: 'getQuillOptions',
      error: 'getError',
      reagents: 'getReagents',
      units: 'getUnits',
      showBlur: 'getBlurFlag',
      tableRowCount: 'getTableRowCount',
      tableColCount: 'getTableColCount',
      allocationMapping: 'getAllocationMap',
      suggestions: 'getSuggestions',
      showSpinner: 'getRuleIsScriptSaving',
      ruleScript: 'getRuleScript',
      allocationData: 'getAllocationData',
      tooltiptext: 'getToolTipStyle',
      referenceText: 'getReferenceExperiment',
      experimentId: 'getExperimentId',
      showSuggestionList: 'getSuggestionList',
      showSuggestionToolTip: 'getSuggestionToolTip',
      hoverHighlight: 'getHighlightHover',
      showWellContents: 'getShowWellContetns',
      currentRow: 'getCurrentRow',
      currentCol: 'getCurrentCol',
      highlightedLineNumber: 'getHighlightedLineNumber',
      currentPlate: 'getCurrentPlate',
      showInfo: 'getShowInfo',
    }),
  },
  watch: {
    ruleScript() {
      this.editor.setText(formatText(this.ruleScript));
      this.paintText();
    },
  },
  methods: {
    ...mapActions([
      'saveToDb',
      'fetchExperiment',
      'fetchReagentList',
      'fetchUnitList',
    ]),
    handleSwitchInfoVisiblity() {
      this.$store.commit('SHOW_INFO');
    },
    editorChange(event) {
      if (
        !['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(event.key)
      ) {
        this.removeEditorColorFormatting();
        const cursorIndex = this.editor.getSelection().index;
        this.alterToolTip(cursorIndex);
        const { fields } = getCurrentLineFields(
          this.editor.getText(),
          cursorIndex,
        );

        if (fields[1] && fields[0][0] === 'A') {
          this.$store.commit(
            'SET_SUGGESTIONS',
            findSuggestions(fields[1][0], 'name', this.reagents),
          );
        }
        if (fields[5] && (fields[0][0] === 'A' || fields[0][0] === 'T')) {
          this.$store.commit(
            'SET_SUGGESTIONS',
            findSuggestions(fields[5][0], 'abbrev', this.units),
          );
        }
        this.alterToolTip(cursorIndex);
        this.$store.commit(
          'SHOW_SUGGESTIONS_LIST',
          this.suggestions.length > 5,
        );

        this.$store.commit(
          'SHOW_SUGGESTIONS_TOOL_TIP',
          this.suggestions.length < 5,
        );
        hesitationTimer.cancel();

        hesitationTimer(this.editor.getText(), this.paintText);
      }
    },
    paintText() {
      const text = this.editor.getText();
      const textLength = text.length;
      this.removeEditorColorFormatting();
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
      if (event.fromElement.nodeName === 'DIV' && !this.error) {
        this.$store.commit('HIGHLIGHT_HOVER', false);
        this.removeEditorColorFormatting();
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
    removeEditorColorFormatting() {
      const text = this.editor.getText();
      this.editor.formatText(0, text.length, 'bg', false);
      this.editor.formatText(0, text.length, 'color', false);
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
      hesitationTimer(this.editor.getText(), this.paintText);
      this.hideSuggestion();
    },
    highlightError(index) {
      this.editor.setSelection(index, 0);
    },
    handleWellHover([row, col]) {
      this.$store.commit('SET_CURRENT_ROW', row);
      this.$store.commit('SET_CURRENT_COL', col);
      this.$store.commit('SHOW_WELL_CONTENTS', true);
    },
    handleWellHoverComplete() {
      this.$store.commit('SHOW_WELL_CONTENTS', false);
    },
    hideSuggestion() {
      this.$store.commit('SHOW_SUGGESTIONS_TOOL_TIP', false);
      this.$store.commit('SHOW_SUGGESTIONS_LIST', false);
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
      this.$store.commit('SHOW_SUGGESTIONS_TOOL_TIP', false);
    },
    handleLineHover(range) {
      if (range) {
        const text = this.editor.getText();
        const {
          currentLineStart,
          currentLineLength,
          lineNumber,
          plateName,
        } = getCurrentLineFields(text, range.index);
        this.removeEditorColorFormatting();
        this.editor.formatText(
          currentLineStart,
          currentLineLength,
          'bg',
          'primary',
        );
        this.editor.formatText(
          currentLineStart,
          currentLineLength,
          'color',
          'white',
        );
        this.$store.commit('SET_CURRENT_PLATE', plateName);
        this.$store.commit('SET_HIGHLIGHTED_LINE_NUMBER', lineNumber);
        this.$store.commit('HIGHLIGHT_HOVER', true);
      }
    },
    setupQuill() {
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
      this.editor = new Quill('#editor', this.options);
      this.editor.keyboard.addBinding({ key: 'tab', shiftKey: true }, range =>
        this.handleTab(range),
      );
      this.editor.keyboard.addBinding({ key: 'F', ctrlKey: true }, () =>
        this.handleFormat(),
      );
      this.editor.clipboard.addMatcher(Node.TEXT_NODE, node =>
        new Delta().insert(node.data, { font: 'monospace' }),
      );
      this.editor.on('selection-change', (range) => {
        this.handleLineHover(range);
      });
      this.editor.focus();
    },
  },
  mounted() {
    // Quill Initialization
    this.setupQuill();
    // Data Retreival
    this.fetchReagentList();
    this.fetchUnitList();
    this.fetchExperiment({ exptNo: 1, referenceExperimentFlag: true });
    this.fetchExperiment({ exptNo: 1 });

    document.addEventListener(
      'contextmenu',
      (e) => {
        e.preventDefault();
      },
      false,
    );
  },
};
