import _ from 'lodash';

export default {
  name: 'EditReagent',
  props: {
    categoryOptions: Array,
    currentReagent: String,
    currentCategory: String,
    opaquePayload: String,
  },
  data() {
    return {
      msg: 'Welcome',
      category: null,
      metaObject: [{},
      ],
    };
  },
  watch: {
    opaquePayload() {
      const opaquePayloadObj = JSON.parse(this.opaquePayload);
      const opaquePayloadList = _.map(opaquePayloadObj, (value, key) => ({
        key,
        value,
      }));
      this.metaObject = opaquePayloadList;
    },
    currentCategory() {
      this.category = this.currentCategory;
    },
  },
  methods: {
    handleRemoveProperty(value) {
      this.metaObject.splice(value, 1);
      if (_.isEmpty(this.metaObject)) {
        this.metaObject = [{}];
      }
    },
    handleAddProperty() {
      if (!_.isEmpty(this.metaObject)) {
        this.metaObject.push({ key: null, value: null });
      } else {
        this.metaObject = [{},
        ];
      }
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
      this.$emit('reagentEdited', {
        opaque_payload: opaquePayload,
        category: this.category,
        name: this.currentReagent,
      });
    },
  },
};
