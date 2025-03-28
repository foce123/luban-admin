<template>
  <div class="table-wrapper">
    <div v-if="showSearch" class="search-wrapper">
      <Form ref="searchForm" :items="searchItems" inline />
      <div
        class="operation-wrapper"
        :style="{ 'justify-content': searchJustify }"
      >
        <slot name="search-operation">
          <el-button type="primary" @click="handleQueryData">查询</el-button>
          <el-button @click="resetSearchParams">重置</el-button>
        </slot>
      </div>
    </div>
    <div><slot name="extra" /></div>
    <el-table v-bind="$attrs" @selection-change="handleSelectTable">
      <el-table-column v-if="selectable" type="selection" width="55" />
      <el-table-column
        v-for="column in tableColumns"
        :key="column.dataIndex"
        v-bind="column"
      >
        <template #default="scope">
          <slot :name="column.dataIndex" :data="scope">
            <span>{{
              formateValue(scope?.row[column.dataIndex], column)
            }}</span>
          </slot>
        </template>
      </el-table-column>
    </el-table>
    <div v-if="pagination" class="pagination-wrapper">
      <el-pagination
        v-bind="pagination"
        :current-page.sync="page"
        :page-size.sync="size"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script>
import Form from "../form";

export default {
  name: "Table",
  components: {
    Form,
  },
  props: {
    showSearch: {
      type: Boolean,
      default: false,
    },
    searchJustify: {
      type: String,
      default: undefined,
    },
    columns: {
      type: Array,
      // eslint-disable-next-line vue/require-valid-default-prop
      default: [],
    },
    showIndex: {
      type: Boolean,
      default: false,
    },
    pagination: {
      type: Object,
      default: undefined,
    },

    selectable: {
      type: Boolean,
      default: false,
    },
    fetchData: {
      type: Function,
      default: undefined,
    },

    fetchSelect: {
      type: Function,
      default: undefined,
    },

    defaultPage: {
      type: Number,
      default: 1,
    },
    defaultSize: {
      type: Number,
      default: 10,
    },
    total: {
      type: Number,
      default: 0,
    },
  },
  data() {
    return {
      searchItems: [],
      tableColumns: [],
      page: 1,
      size: 10,
      selectItem: [],
    };
  },
  created() {
    const searchItems = [];
    const tableColumns = [];
    for (const column of this.columns) {
      if (!column.hideInSearch) {
        searchItems.push(column);
      }
      if (!column.hideInTable) {
        tableColumns.push(column);
      }
    }
    this.searchItems = searchItems;
    this.tableColumns = tableColumns;
  },
  mounted() {
    this.handleQueryData();
  },
  methods: {
    handleSizeChange(size) {
      this.page = 1;
      this.size = size;
      this.dispatchQueryData();
    },
    handlePageChange(page) {
      this.page = page;
      this.dispatchQueryData();
    },
    formateValue(value, column) {
      if (column.valueEnum) {
        return column.valueEnum[value] || value || "-";
      }
      return value || "-";
    },
    initPageInfo() {
      if (!this.pagination) return;

      this.page = this.defaultPage;
      this.size = this.defaultSize;
    },
    handleQueryData() {
      this.initPageInfo();
      this.dispatchQueryData();
    },
    resetSearchParams() {
      this.initPageInfo();
      this.$refs.searchForm.resetFields();
      this.dispatchQueryData();
    },
    dispatchQueryData() {
      if (!this.fetchData) return;
      var params = { page: this.page, size: this.size };
      if (this.showSearch) {
        const formFields = this.$refs.searchForm.getFormFields();
        params = { ...params, ...formFields };
      }
      this.fetchData(params);
    },
    handleSelectTable(rows) {
      if (!this.fetchSelect) return;
      this.fetchSelect(rows);
    },
  },
};
</script>

<style scoped>
.search-wrapper {
  display: flex;
  flex-direction: row;
}
.operation-wrapper {
  display: flex;
  flex-direction: row;
  align-items: baseline;
  padding: 0px 30px;
}
.pagination-wrapper {
  display: flex;
  flex-direction: row-reverse;
  margin-top: 20px;
  align-items: center;
}
</style>
