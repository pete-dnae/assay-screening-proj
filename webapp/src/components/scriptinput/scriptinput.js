import _ from 'lodash';
import horsey from 'horsey';
export default {
  name: 'ScriptInputComponent',
  data() {
    return {
      msg: 'Welcome',
      text: '',
    };
  },
  props: {
    options: Array,
  },
  watch: {},
  methods: {},
  mounted() {
    horsey(document.querySelector('textarea'), {
      source: [
        {
          list: [
            { value: '@Titanium-Taq', text: 'Titanium-Taq' },
            { value: '@(Eco)-ATCC-BAA-2355', text: '(Eco)-ATCC-BAA-2355' },
            { value: '@HgDna', text: 'HgDna' },
            {
              value: '@Ec_uidA_6.x_Eco63_Eco60',
              text: 'Ec_uidA_6.x_Eco63_Eco60',
            },
          ],
        },
      ],
      getText: 'text',
      getValue: 'value',
      anchor: '@',
      highlightCompleteWords: true,
      highlighter: true,
    });
  },
};
