<template>
  <el-form ref="form" v-bind="$attrs" :model="formData" >
    <el-form-item
      v-for="item in items"
      :key="item.dataIndex"
      v-bind="item"
      :label="getItemLabel(item)"
      :prop="item.dataIndex"
    >
      <component
        :is="item.component"
        v-model="formData[item.dataIndex]"
        v-bind="item"
      />
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  name: "Form",
  props: {
    items: {
      type: Array,
      default: () => [],
    },
  },

  data() {
    return {
      formData: {},
    };
  },

  created() {
    this.sortByFieldWith(this.items, "searchIndex");
  },
  watch: {
    items: {
      handler(newItems) {
        this.setFormFields(newItems);
      },
      immediate: true,
    },
  },
  methods: {
    // 排序和重命名
    sortByFieldWith(arr, field) {
      if (arr.length == 0) {
        return arr;
      }
      return arr.sort((a, b) => {
        const aValue = a[field] !== undefined ? a[field] : Infinity;
        const bValue = b[field] !== undefined ? b[field] : Infinity;
        if (aValue === Infinity && bValue === Infinity) {
          return 0;
        } else if (aValue === Infinity) {
          return 1;
        } else if (bValue === Infinity) {
          return -1;
        } else {
          return aValue - bValue;
        }
      });
    },

    setFormFields(items) {
      const data = {};
      for (const item of items) {
        if (item.dataIndex) {
          data[item.dataIndex] = item.value;
        }
      }
      this.formData = data;
    },
    getFormFields() {
      var data = { ...this.formData };
      for (const item of this.items) {
        if (item.valueTransform && data[item.dataIndex]) {
          const newField = item.valueTransform(data[item.dataIndex]);
          delete data[item.dataIndex];
          data = { ...data, ...newField };
        }
      }
      return data;
    },
    getItemLabel(item) {
      if (item.hideItemLabel) {
        return undefined;
      }
      if (item.searchLabel != undefined) {
        return `${item.searchLabel}：`;
      }

      const colon = item.colon === undefined ? true : item.colon;
      if (colon) {
        return `${item.label}：`;
      }

      return item.label;
    },
    resetFields() {
      this.$refs.form.resetFields();
    },
    validate(callback) {
      this.$refs.form.validate(callback);
    },
  },
};
</script>
