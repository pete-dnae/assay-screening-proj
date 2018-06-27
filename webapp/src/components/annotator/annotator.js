import { dropdown, modal } from 'vue-strap';
import * as api from '@/models/api';
import loader from '@/components/loader';
import _ from 'lodash';

export default {
  name: 'annotator',
  components: {
    dropdown,
    modal,
    loader,
  },
  data() {
    return {
      qpcrWells: null,
      labchipWells: null,
      qpcrSelection: [],
      labchipSelection: [],
      exclude: 'False',
      comment: null,
      isPosting: false,
      posted: false,
      didInvalidate: false,
    };
  },
  props: {
    currentSelection: Array,
    showAnnotator: Boolean,
  },
  watch: {
    currentSelection() {
      this.qpcrWells = _.uniqBy(this.currentSelection.map(selection => ({
        text: selection['qPCR Well'],
        value: selection['qPCR Well Id'],
      })), 'value');
      this.labchipWells = _.uniqBy(this.currentSelection.map(
          selection => ({
            text: selection['LC Well'],
            value: selection['Labchip Well Id'],
          }),
        ), 'value');
      //   this.qpcrSelection = this.qpcrWells.map(x => x.value);
      //   this.labchipSelection = this.labchipWells.map(x => x.value);
    },
  },
  methods: {
    handleExit() {
      this.$emit('exit');
    },
    annotationsFail() {
      this.isPosting = false;
      this.posted = false;
      this.didInvalidate = true;
    },
    annotationsSuccess() {
      this.isPosting = false;
      this.posted = true;
      this.didInvalidate = false;
      this.$emit('annotated');
    },
    handleSubmit() {
      this.isPosting = true;
      this.posted = false;
      this.didInvalidate = false;
      if (this.qpcrSelection.length !== 0) {
        api
          .annotateQPCRWells({
            exclude_well: this.exclude,
            comment: this.comment,
            qpcr_well_ids: JSON.stringify(this.qpcrSelection),
          })
          .then(() => this.annotationsSuccess(), () => this.annotationsFail());
      }
      if (this.labchipSelection.length !== 0) {
        let selection = [];
        this.labchipSelection.forEach((element) => {
          selection = selection.concat(element);
        });
        api
          .annotateLabchipWells({
            exclude_well: this.exclude,
            comment: this.comment,
            labchip_well_ids: JSON.stringify(selection),
          })
          .then(() => this.annotationsSuccess(), () => this.annotationsFail());
      }
    },
  },
};
