<template>
  <div class="select-container">
    <el-table
      :data="select_data"
      style="width: 100%"
      :row-class-name="tableRowClassName"
    >
      <el-table-column
        prop="column_name"
        label="Column Name"
        width="120"
      />
      <el-table-column
        prop="column_processing"
        label="Column Processing"
        width="180"
      />
      <el-table-column prop="explain" label="NL Explain" />
    </el-table>
  </div>
</template>
<script>
export default {
  name: "SelectCard",
  props: {
    select_data: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      
    };
  },
  methods: {
    tableRowClassName({ row, rowIndex }) {
      if (rowIndex === 0) {
        return "warning-row"; // 第二行添加 'warning-row' 类
      } else if (rowIndex === 3) {
        return "success-row"; // 第四行添加 'success-row' 类
      }
      return ""; // 其他行不添加类名
    },
  },
};
</script>
<style scoped>
.warning-row {
  background-color: #eee5d8; /* 浅黄色背景 */
}

.success-row {
  background-color: #f0f9eb; /* 浅绿色背景 */
}
</style>
