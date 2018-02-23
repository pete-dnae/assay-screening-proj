import _ from 'lodash';
import horsey from 'horsey';
// require styles
import 'quill/dist/quill.core.css';
import 'quill/dist/quill.snow.css';
import 'quill/dist/quill.bubble.css';
import 'tributejs/dist/tribute.css';
import { splitLines, validateRule } from '@/models/editor';
import Tribute from 'tributejs';

import { quillEditor } from 'vue-quill-editor';

export default {
  name: 'ScriptInputComponent',
  components: {
    quillEditor,
  },
  data() {
    return {
      msg: 'Welcome',
      text: '',
      resultHtml: '',
      content: '',
      units: ['mM', 'mg/ml', 'mM each', 'copies/ul', 'uM', 'ng/ul', 'x'],
      editorOption: {
        /* quill options */
      },
    };
  },
  props: {
    options: Array,
  },
  watch: {},
  methods: {
    onEditorChange({ editor, html, text }) {
      if (!this.content.includes('bla')) {
        this.resultHtml = new Set();
        const lines = splitLines('\n', text).filter(x => x);
        lines.forEach((x, i) => {
          const resultHtml = validateRule(
            i,
            ['Titanium-Taq', 'HgDna'],
            this.units,
            x,
          );
          this.resultHtml = new Set([...this.resultHtml, ...resultHtml]);
        });
        document.getElementById('result').innerHTML = Array.from(
          this.resultHtml,
        ).join('');
      }

      this.content = `${text} bla`;
    },
  },
  mounted() {
    this.tribute = new Tribute({
      values: [
        { key: 'Titanium-Taq', value: 'Titanium-Taq' },
        { key: 'MgCl2', value: 'MgCl2' },
      ],
      lookup: 'key',
    });
    debugger;
    this.tribute.attach(document.getElementsByClassName('ql-editor'));
  },
};
