import Quill from 'quill';
// require styles
import 'quill/dist/quill.core.css';
import 'quill/dist/quill.snow.css';
import { modal, tooltip } from 'vue-strap';
import { formatText } from '@/models/visualizer';
import hovervisualizer from '@/components/hovervisualizer/hovervisualizer.vue';
import { mapGetters, mapActions } from 'vuex';
import wellcontents from '@/components/wellcontents/wellcontents.vue';
import toolbar from '@/components/editortoolbar/editortoolbar.vue';
import errorPane from '@/components/scripterrorpane/scripterrorpane';
import suggestionsList from '@/components/suggestionslist/suggestionslist.vue';
import suggestionToolTip from '@/components/suggestionstooltip/suggestionstooltip.vue';
import pictures from '@/components/pictures/pictures.vue';
import { hesitationTimer, getCurrentLineFields } from '@/models/editor2.0';
import fileUploader from '@/components/fileupload/fileupload.vue';

export default {
  name: 'ScriptInputComponent',
  components: {
    modal,
    hovervisualizer,
    wellcontents,
    tooltip,
    toolbar,
    errorPane,
    suggestionsList,
    suggestionToolTip,
    pictures,
    fileUploader,
  },
  data() {
    return { msg: 'Welcome', suggestionIndex: 0, editor: null, showPictures: false, showUpload: false };
  },
  computed: {
    ...mapGetters({
      options: 'getQuillOptions',
      error: 'getError',
      showBlur: 'getBlurFlag',
      plateBoundaries: 'getPlateBoundaries',
      experimentImages: 'getExperimentImages',
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
      'fetchAvailableSuggestions',
      'setSuggestions',
    ]),
    handleSwitchInfoVisiblity() {
      this.$store.commit('SHOW_INFO');
    },
    editorChange(event) {
      // Fires on every keypress , Does nothing when it comes to arrow keys
      // Triggers the below actions
      // Remove current color formatting,update tooltip position ,
      // set suggestions and set off the hesitation timer
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
        this.setSuggestions(fields);
        this.alterToolTip(cursorIndex);

        hesitationTimer.cancel();

        hesitationTimer(this.editor.getText(), this.paintText);
      }
    },
    paintText() {
      // Differentiates error-prone line and unprocessed text in editor
      // from  valid script
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
      // switch off highlighting when out of editor DIV
      if (event.fromElement.nodeName === 'DIV' && !this.error) {
        this.$store.commit('HIGHLIGHT_HOVER', false);
        this.removeEditorColorFormatting();
      }
    },
    alterToolTip(cursorIndex) {
      // calculate tool tip position and send to store
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
      // remove current color formatting
      const text = this.editor.getText();
      this.editor.formatText(0, text.length, 'bg', false);
      this.editor.formatText(0, text.length, 'color', false);
    },
    handleAutoCompleteClick(text) {
      // Insert suggestion text at cursor index and trigger hide suggestion
      const { currentStringStart, cursorIndex } = this.getCurrentStringRange();
      this.editor.insertText(cursorIndex, ` ${text}`, {
        color: 'black',
      });
      this.editor.deleteText(
        currentStringStart,
        cursorIndex - currentStringStart,
      );
      hesitationTimer(this.editor.getText(), this.paintText);
      this.hideSuggestion();
    },
    highlightError(index) {
      // move cursor to error index
      this.editor.setSelection(index, 0);
    },
    handleWellHover([row, col]) {
      // on well hover emit save current row col to store
      this.$store.commit('SET_CURRENT_ROW', row);
      this.$store.commit('SET_CURRENT_COL', col);
      this.$store.commit('SHOW_WELL_CONTENTS', true);
    },
    handleWellHoverComplete() {
      // record well hover complete in store
      this.$store.commit('SHOW_WELL_CONTENTS', false);
    },
    hideSuggestion() {
      // set suggestion visiblity to false
      this.$store.commit('SHOW_SUGGESTIONS_TOOL_TIP', false);
      this.$store.commit('SHOW_SUGGESTIONS_LIST', false);
    },
    getCurrentStringRange() {
      // return current string start along with cursor index
      this.editor.focus();
      const cursorIndex = this.editor.getSelection().index;
      const textTillCursor = this.editor.getText().slice(0, cursorIndex);
      const currentStringStart = textTillCursor.lastIndexOf(' ');
      return { currentStringStart, cursorIndex };
    },
    handleFormat() {
      // format text
      const formattedText = formatText(this.editor.getText());
      this.editor.setText(formattedText);
      this.editor.formatText(0, formattedText.length, 'font', 'monospace');
    },
    handleTab() {
      // generate autocomplete click with suggestion at suggestion index
      // move suggestion index by 1
      this.handleAutoCompleteClick(this.suggestions[this.suggestionIndex]);
      this.suggestionIndex += 1;
      this.suggestionIndex = this.suggestions[this.suggestionIndex]
        ? this.suggestionIndex
        : 0;
      this.$store.commit('SHOW_SUGGESTIONS_TOOL_TIP', false);
    },
    handleLineHover(range) {
      // find , store and highlight line number corresponding to click
      // enable hover highlighting
      // store current plate
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
      // set up quill custom formatting and eventlistners
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

    this.fetchAvailableSuggestions();
    this.fetchExperiment({
      experimentName: 'Reference Experiment',
      referenceExperimentFlag: true,
    });
    this.fetchExperiment({ experimentName: 'Reference Experiment' });
  },
};
