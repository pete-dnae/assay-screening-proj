import Vue from 'vue';
import draggable from 'vuedraggable';

export default {
  name: 'AllocationRules',
  components: {
    draggable,
  },
  data() {
    return {
      msg: 'Welcome',
      items: [
        {
          id: 0,
          title: 'Template Copies',
          type: 'In Blocks',
          value: [{ value: 0, id: 0 }, { value: 0, id: 1 }, { value: 0, id: 2 }],
          rowRange: 'A-B',
          colRange: '1-12',
        },
        {
          id: 1,
          title: 'Template Copies',
          type: 'In Blocks',
          value: [{ value: 5, id: 0 }, { value: 5, id: 1 }, { value: 50, id: 2 }],
          rowRange: 'C-D',
          colRange: '1-12',
        },
        {
          id: 2,
          title: 'ID Primers',
          type: 'Consecutively',
          value: [
            { value: 'Ec_uidA_6.x_Eco63_Eco60', id: 0 },
            { value: 'Efs_cpn60_1.x_Efs04_Efs01', id: 1 },
          ],
          rowRange: 'A-H',
          colRange: '5-12',
        },
      ],
    };
  },
  methods: {
    handleSelect(evt) {
      this.$emit('selectedRule', this.items[evt.oldIndex]);
    },
  },
};
