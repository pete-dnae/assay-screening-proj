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
      content: '<p>example content</p>',
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
    splitLines(text) {},
    onEditorChange(event) {
      const lines = splitLines('\n', event.text).filter(x => x);
      let feedDict = {};
      lines.forEach((x, i) => {
        const { feedback, resultHtml } = validateRule(
          ['Titanium-Taq'],
          ['x'],
          x,
        );
        feedDict[i] = feedback;
        this.resultHtml = resultHtml.join('');
      });
      document.getElementById('result').innerHTML = this.resultHtml;
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
    this.tribute.attach(document.getElementsByClassName('ql-editor'));
  },
};
