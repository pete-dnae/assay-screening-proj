import Quill from 'quill';
// require styles
import 'quill/dist/quill.core.css';
import 'quill/dist/quill.snow.css';
import 'quill/dist/quill.bubble.css';
import { mapGetters, mapActions } from 'vuex';
import {
  checkVersion,
  validatePlate,
  validateRule,
  validateComment,
} from '@/models/editor';

export default {
  name: 'ScriptInputComponent',
  data() {
    return {
      msg: 'Welcome',
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
        let startIndex = 0;
        let feedBackCollector = [];
        text.split('\n').forEach((line, i) => {
          const lineNum = i + 1;
          switch (true) {
            case lineNum === 1:
              feedBackCollector.push(
                checkVersion(line, this.version, startIndex),
              );
              break;
            case line.startsWith('P'):
              feedBackCollector.push(
                validatePlate(line, this.parsedPlates, startIndex),
              );
              break;
            case line.startsWith('A') || line.startsWith('T'):
              feedBackCollector.push(
                validateRule(
                  line,
                  this.reagents,
                  this.units,
                  this.parsedPlates,
                  startIndex,
                ),
              );
              break;
            case line.startsWith('#'):
              feedBackCollector.push(validateComment(line, startIndex));
              break;
            default:
          }

          this.setFeedback(feedBackCollector);
          startIndex += line.length + 1;
        });

        this.validTextObjects.forEach(range => {
          this.editor.formatText(range.index, range.length, 'color', 'green');
        });
        this.invalidTextObjects.forEach(range => {
          this.editor.formatText(range.index, range.length, 'color', 'red');
        });
      }
    },
  },
  mounted() {
    this.editor = new Quill('#editor', this.options);
    this.editor.on('text-change', (...args) => this.onEditorChange(args));
  },
};
