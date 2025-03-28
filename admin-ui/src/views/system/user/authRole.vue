<template>
  <div class="app-container">
    <h4 class="form-header h4">基本信息</h4>
    <el-form :model="form" label-width="80px">
      <el-row>
        <el-col :span="8" :offset="2">
          <el-form-item label="用户昵称" prop="nickName">
            <el-input v-model="form.nickName" disabled />
          </el-form-item>
        </el-col>
        <el-col :span="8" :offset="2">
          <el-form-item label="登录账号" prop="username">
            <el-input v-model="form.username" disabled />
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <h4 class="form-header h4">角色信息</h4>
    <el-table
      v-loading="loading"
      :row-key="getRowKey"
      @row-click="clickRow"
      ref="roleRef"
      @selection-change="handleSelectionChange"
      :data="roles.slice((pageNum - 1) * pageSize, pageNum * pageSize)"
    >
      <el-table-column label="序号" width="55" type="index" align="center">
        <template #default="scope">
          <span>{{ (pageNum - 1) * pageSize + scope.$index + 1 }}</span>
        </template>
      </el-table-column>
      <el-table-column
        type="selection"
        :reserve-selection="true"
        width="55"
      ></el-table-column>
      <el-table-column
        label="角色编号"
        align="center"
        prop="roleId"
        type="index"
        width="120px"
      />
      <el-table-column label="角色名称" align="center" prop="roleName" />
      <el-table-column label="权限字符" align="center" prop="roleKey" />
      <el-table-column label="创建时间" align="center" prop="create_time">
        <template #default="scope">
          <span>{{ parseTime(scope.row.create_time) }}</span>
        </template>
      </el-table-column>

      <el-table-column label="操作" align="center" prop="create_time">
         <template #default="scope">
        <el-tooltip content="删除角色绑定" placement="top">
          <el-button link type="primary" icon="Delete"  @click="handleAuthRole(scope.row)"></el-button>
        </el-tooltip>
      </template>
      </el-table-column>
      
    </el-table>

    <pagination
      v-show="total > 0"
      :total="total"
      v-model:page="pageNum"
      v-model:limit="pageSize"
    />

    <el-form label-width="100px">
      <div style="text-align: center; margin-left: -120px; margin-top: 30px">
        <el-button type="primary" @click="submitForm()">提交</el-button>
        <el-button @click="close()">返回</el-button>
      </div>
    </el-form>
  </div>
</template>

<script setup name="AuthRole">
import { getAuthRole, updateAuthRole } from "@/api/system/user";

const route = useRoute();
const { proxy } = getCurrentInstance();

const loading = ref(true);
const total = ref(0);
const pageNum = ref(1);
const pageSize = ref(10);
const roleIds = ref([]);
const roles = ref([]);
const form = ref({
  nickName: undefined,
  username: undefined,
  userId: undefined,
});

/** 取消人员角色绑定 */
function handleAuthRole(row){
   console.log("🚀 ~ handleAuthRole ~ row:", row)
   
}

/** 单击选中行数据 */
function clickRow(row) {
  proxy.$refs["roleRef"].toggleRowSelection(row);
}
/** 多选框选中数据 */
function handleSelectionChange(selection) {
  roleIds.value = selection.map((item) => item.roleId);
}
/** 保存选中的数据编号 */
function getRowKey(row) {
  return row.roleId;
}
/** 关闭按钮 */
function close() {
  const obj = { path: "/system/user" };
  proxy.$tab.closeOpenPage(obj);
}
/** 提交按钮 */
function submitForm() {
  const userId = form.value.userId;
  const rIds = roleIds.value.join(",");
  updateAuthRole({ userId: userId, roleIds: rIds }).then((response) => {
    proxy.$modal.msgSuccess("授权成功");
    close();
  });
}

(() => {
  const userId = route.params && route.params.userId;
  if (userId) {
    loading.value = true;
    getAuthRole(userId).then((response) => {
      form.value = response.data.user;
      roles.value = response.data.roles;
      total.value = roles.value.length;
      nextTick(() => {
        roles.value.forEach((row) => {
          if (row.flag) {
            proxy.$refs["roleRef"].toggleRowSelection(row);
          }
        });
      });
      loading.value = false;
    });
  }
})();
</script>
