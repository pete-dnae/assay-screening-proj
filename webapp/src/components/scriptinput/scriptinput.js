import Quill from 'quill';
// require styles
import 'quill/dist/quill.core.css';
import 'quill/dist/quill.snow.css';
import 'quill/dist/quill.bubble.css';

import { mapGetters, mapActions } from 'vuex';
import { validateText } from '@/models/editor';

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
        this.setFeedback(
          validateText(text, {
            version: this.version,
            parsedPlates: this.parsedPlates,
            reagents: this.reagents,
            units: this.units,
          }),
        );
        this.validTextObjects.forEach(range => {
          this.editor.formatText(
            range.index,
            range.length,
            range.action[0],
            range.action[1],
          );
        });
        this.invalidTextObjects.forEach(range => {
          this.editor.formatText(
            range.index,
            range.length,
            range.action[0],
            range.action[1],
          );
        });
      }
    },
  },
  mounted() {
    this.editor = new Quill('#editor', this.options);
    this.editor.on('text-change', (...args) => this.onEditorChange(args));
  },
};
