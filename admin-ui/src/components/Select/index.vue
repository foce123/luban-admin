<template>
  <el-select v-model="modelValue" v-bind="$attrs">
    <el-option
      v-for="(val, key) in $attrs.valueEnum"
      :key="key"
      :label="val"
      :value="key"
    />
  </el-select>
</template>

<script>
export default {
  name: 'Select',
  model: {
    prop: 'value',
    event: 'change'
  },
  props: {
    value: {
      type: [String, Number, Object],
      default: undefined
    }
  },
  computed: {
    modelValue: {
      get() {
        return this.value
      },
      set(val) {
        this.$emit('change', val)
      }
    }
  }
}
</script>
