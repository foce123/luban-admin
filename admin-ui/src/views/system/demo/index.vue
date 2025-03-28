<template>
  <div class="app-container">
    <CommonTable
      ref="table"
      v-loading="loading"
      :data="dataList"
      :total="total"
      :columns="columns"
      :pagination="pagination"
      :fetch-data="fetchData"
      search-justify="space-between"
      show-search
      selectable
    >
      <template #extra="ctx">
        <el-button
          type="primary"
          link
          size="small"
          @click="handleEdit(ctx.data)"
        >
          查看
        </el-button>
      </template>
      <template #operation="ctx">
        <el-button
          type="primary"
          link
          size="small"
          @click="handleEdit(ctx.data.row)"
        >
          查看
        </el-button>
      </template>
      <template #userId="ctx">
        <span>{{ ctx.data.row.userId }}</span>
      </template>
    </CommonTable>
  </div>
</template>

<script setup>
import { DATA_TAG_TYPE } from "@/utils/enum";
const total = ref(100);
const loading = ref(false);
const queryParams = ref({});

const pagination = ref({
  small: true,
  background: true,
  layout: "total, prev, pager, next, sizes, jumper",
});
const dataList = ref([{ userId: "12313" }, { userId: "12313" }]);
const columns = ref([
  {
    label: "书写者ID",
    dataIndex: "userId",
    hideInSearch: true,
  },
  {
    label: "书写者姓名",
    dataIndex: "name",
    component: "el-input",
    clearable: true,
    placeholder: "请输入",
    hideInSearch: false,
  },
  {
    label: "笔迹ID",
    dataIndex: "hwid",
    component: "el-input",
    clearable: true,
    placeholder: "请输入",
    hideInSearch: false,
  },
  {
    label: "业务系统",
    dataIndex: "appName",
    component: "common-select",
    placeholder: "请选择",
    clearable: true,
    valueEnum: DATA_TAG_TYPE,
  },

  {
    label: "识别时间",
    dataIndex: "timeStamp",
    component: "el-date-picker",
    type: "daterange",
    startPlaceholder: "开始时间",
    endPlaceholder: "结束时间",
    separator: "至",
    valueFormat: "YYYY-MM-DD",
    clearable: true,
    valueTransform: (field) => {
      return {
        startTime: field[0],
        endTime: field[1],
      };
    },
  },

  {
    label: "识别结果",
    dataIndex: "dataStatus",
    hideInSearch: true,
  },

  {
    label: "错误类型",
    dataIndex: "validMsg",
    hideInSearch: true,
  },
  {
    label: "操作",
    dataIndex: "operation",
    hideInSearch: true,
    fixed: "right",
    width: "200",
  },
]);

const fetchData = (params) => {
  queryParams.value = params;
  console.log("🚀 ~ fetchData ~ queryParams:", queryParams);
};

const handleEdit = (data) => {
  console.log("🚀 ~ data:", data);
  return {};
};
</script>

<style scoped lang="scss">
.home {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  font-size: 120px;
  font-weight: 700;
  padding-top: 300px;
}
</style>
