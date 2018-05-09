import _ from 'lodash';

export default {
  name: 'AddReagent',
  props: { categoryOptions: Array },
  data() {
    return {
      msg: 'Welcome',
      name: null,
      category: null,
      metaObject: [
        {
          key: null,
          value: null,
        },
      ],
    };
  },
  methods: {
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
        opaque_payload: opaquePayload,
        name: this.name,
        category: this.category,
      });
    },
  },
};
