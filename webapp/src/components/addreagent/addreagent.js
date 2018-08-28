import _ from 'lodash';
import * as api from '@/models/api';
import loader from '@/components/loader';

export default {
  name: 'AddReagent',
  props: { categoryOptions: Array },
  components: {
    loader,
  },
  data() {
    return {
      msg: 'Welcome',
      name: null,
      category: null,
      isPosting: null,
      posted: null,
      didInvalidate: null,
      uploadFeedback: null,
      metaObject: [
        {
          key: null,
          value: null,
        },
      ],
    };
  },
  methods: {
    handleSuccess() {
      this.uploadFeedBack = 'Upload sucessful';
      this.isPosting = false;
      this.posted = true;
      this.didInvalidate = false;
    },
    handleFailure(response) {
      debugger;
      this.uploadFeedBack = `Failure : ${response.data}`;
      this.isPosting = false;
      this.posted = false;
      this.didInvalidate = true;
    },
    handleRemoveProperty(value) {
      this.metaObject.splice(value, 1);
      if (_.isEmpty(this.metaObject)) {
        this.metaObject = [{ key: null, value: null }];
      }
    },
    handleAddProperty() {
      if (!_.isEmpty(this.metaObject)) {
        this.metaObject.push({ key: null, value: null });
      } else {
        this.metaObject = [
          {
            key: null,
            value: null,
          },
        ];
      }
    },
    handleFileUpload() {
      this.uploadFeedBack = null;
      const formData = new FormData();
      const file = document.getElementById('bulkLoad');
      formData.append('file', file.files[0]);
      this.isPosting = true;
      this.posted = false;
      this.didInvalidate = false;
      api
        .postBulkReagents(formData)
        .then(
          ({ data }) => this.handleSuccess(data),
          ({ response }) => this.handleFailure(response),
        )
        .catch((e) => {
          this.uploadFeedBack = `Failure ${e.toString()}`;
        });
    },
    handleSubmit() {
      let opaquePayload = _.reduce(
        this.metaObject,
        (acc, property) => {
          acc[property.key] = property.value;
          return acc;
        },
        {},
      );
      opaquePayload = JSON.stringify(opaquePayload);
      this.$emit('reagentSubmit', {
        opaque_json_payload: opaquePayload,
        name: this.name,
        category: this.category,
      });
    },
  },
};
