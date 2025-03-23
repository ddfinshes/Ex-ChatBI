<template>
  <div class="ai-content">
    <img class="avatar" src="@/assets/image/robot.png" alt="AI Avatar" />
    <div class="message-bubble ai-bubble">
      <div class="explanation-section">
        <MarkdownRenderer class="explanation-text" :content="message.understanding" />
      </div>

      
      <!-- Data Card -->
      <div class="card-section">
        <div class="card-title">Data</div>
        <div class="card-content" @click="handleOutsideClick">
          <table v-if="message.data" class="result-table">
            <thead>
              <tr>
                <th v-for="(column, idx) in message.data.column" :key="idx"
                  :class="{ 'highlighted': highlighted.type === 'header' && highlighted.columnIndex === idx }"
                  @click="handleHeaderClick(column, idx)">
                  {{ column }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, rowIdx) in message.data.data" :key="rowIdx">
                <td v-for="(cell, cellIdx) in row" :key="cellIdx"
                  :class="{ 'highlighted': highlighted.type === 'cell' && highlighted.rowIndex === rowIdx && highlighted.columnIndex === cellIdx }"
                  @click="handleCellClick(cell, rowIdx, message.data.column[cellIdx])">
                  {{ cell }}
                </td>
              </tr>
            </tbody>
          </table>
          <p v-else class="no-data">no data</p>
        </div>
      </div>

      <!-- Chart Card -->
      <div class="card-section">
        <div class="card-title">Chart</div>
        <div class="card-content">
          <div id="chart-container">
            <div :id="message.vis_tag_name" style="width: 600px; height: 400px"></div>
          </div>
        </div>
      </div>

      <!-- Code Card -->
      <div class="card-section">
        <div class="card-title">Code</div>
        <div class="card-content">
          <MarkdownRenderer class="sql-code" :content="message.code?.text || ''" />
        </div>
      </div>

      <div class="explanation-section">
        <MarkdownRenderer class="explanation-text" :content="message.explanation" />
      </div>


      <div class="bottom-section">
        <span class="timestamp">{{ message.timestamp }}</span>
        <button class="icon-button" @click="handleIconClick">
          <img class="userIconClass" src="@/assets/image/detail.png" />
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { chart } from "@/assets/ts/chart.ts";
import MarkdownRenderer from "./MarkdownRenderer.vue";
import axios from "axios";
import { useQueryStore } from '@/stores/query';
export default {
  name: "AiMessage",

  components: {
    MarkdownRenderer,
  },
  data() {
    return {
      clickdata: {},
      isMounted: false,
      timeoutId: null,
      highlighted: {
        type: null, // 'header' 或 'cell'
        rowIndex: null,
        columnIndex: null,
      },
    }
  },
  setup() {
    const queryStore = useQueryStore();

    return { queryStore };
  },
  props: {
    message: {
      type: Object,
      required: true,
    },
  },
  mounted() {
    const chartElement = document.getElementById(this.message.vis_tag_name);
    if (chartElement) {
      console.log(`渲染图表: ${this.message.vis_tag_name}`);
      chart(this.message.vis_tag_name, this.message.vis_data);
    } else {
      console.error(`未找到图表元素: ${this.message.vis_tag_name}`);
    }
  },
  beforeUnmount() {
    if (this.timeoutId) {
      clearTimeout(this.timeoutId); // 卸载时清除定时器
    }
  },
  methods: {
    handleHeaderClick(column, columnIndex) {
      this.clickdata = {
        columnName: column,
        columnIndex: columnIndex
      }
      this.highlighted = {
        type: 'header',
        rowIndex: null,
        columnIndex: columnIndex,
      };
      console.log('highlighted 点击了表头:', this.highlighted);
      console.log('---点击了表头:', this.clickdata)
      this.relatSQL()

    },
    // handleRowClick(row, rowIndex) {
    //   this.clickdata = {
    //     rowData: row,
    //     rowIndex: rowIndex
    //   }
    //   this.relatSQL()
    //   console.log('点击了行:', 
    //     this.clickdata
    //   );
    // },
    handleCellClick(cellValue, rowIndex, columnName) {
      this.clickdata = {
        value: cellValue,
        rowIndex: rowIndex,
        columnName: columnName
      }
      this.highlighted = {
        type: 'cell',
        rowIndex: rowIndex,
        columnIndex: this.message.data.column.indexOf(columnName),
      };
      console.log('highlighted 点击了单元格:', this.highlighted);
      this.relatSQL()

    },
    handleOutsideClick(event) {
      // 如果点击不在表格内，则取消高亮
      if (!event.target.closest('.result-table')) {
        this.highlighted = {
          type: null,
          rowIndex: null,
          columnIndex: null,
        };
      }
    },
    async relatSQL() {
      if (!this.clickdata) return;
      try {
        const payload = {
          sql_query: this.message.code,
          query_out: this.message.data,
          click_info: this.clickdata
        };
        // this.queryStore.setSubSQLJson(payload);
        console.log('Request payload:', payload);
        const res = await axios.post(
          "/api/relatsql",
          payload
        );
        // 点击单元格后的sql2json
        const subsqljson = res.data;
        console.log('subsql2json: ', subsqljson)
        this.queryStore.setSubSQLJson(subsqljson);
      } catch (error) {
        console.error("Error fetching response:", error);
      }
    },
    async handleIconClick() {
      this.queryStore.setIsDataReady(!this.queryStore.isDataReady);
      if (this.queryStore.isDataReady) {
        this.timeoutId = setTimeout(() => {
          this.queryStore.setResponse(this.message);
          this.timeoutId = null;
        }, 1000);
      }


    },
  }
};
</script>

<style>
.common-layout {
  height: 100vh;
  width: 100vh;
  display: flex;
  flex-direction: column;
}

.common-container {
  height: 100%;
  width: 100%;
  background-color: #f0f0f0;
  display: flex;
}

#main {
  background-color: #ffffff;
  height: 100%;
  width: 70%;
  border: 1px solid #afafaf;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.user {
  border-bottom: 3px solid #a5a5a5;
  padding: 10px;
  margin-bottom: 1rem;
  text-align: left;
  position: relative;
}

.ai {
  border-bottom: 3px solid #a5a5a5;
  padding: 10px;
  margin-bottom: 1rem;
  text-align: left;
}

.timestamp {
  font-size: 0.8rem;
  color: gray;
  display: block;
  margin-top: 5px;
}

.input-container {
  display: flex;
  align-items: center;
  padding: 10px;
  border-top: 2px solid #a5a5a5;
}

.result-table {
  width: 100%;
  border-collapse: collapse;
}

.result-table th,
.result-table td {
  border: 1px solid #dcdcdc;
  padding: 8px;
  text-align: left;
}

.result-table th {
  background-color: #f5f5f5;
  font-weight: bold;
}

.result-table tbody tr:hover {
  background-color: #fafafa;
}

.highlighted {
  background-color: #f8f29d !important;
  /* 高亮颜色，可以自定义 */
}

.sql-code {
  background-color: #dadada;
  border-radius: 5px;
  padding: 10px;
  font-family: monospace;
  white-space: pre-wrap;
}

.message-text {
  white-space: pre-line;
}

/* --- */
.message-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  height: 1000px;
}

.message-wrapper {
  display: flex;
  margin-bottom: 20px;
  align-items: flex-start;
}

.user-message {
  justify-content: flex-end;
}

.ai-message {
  justify-content: flex-start;
}

.user-content,
.ai-content {
  display: flex;
  align-items: flex-start;
  max-width: 70%;
}

.user-content {
  flex-direction: row-reverse;
}

.ai-content {
  flex-direction: row;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin: 0 10px;
  object-fit: cover;
}

.message-bubble {
  padding: 12px 16px;
  border-radius: 12px;
  position: relative;
}

.user-bubble {
  background-color: #409EFF;
  color: white;
  margin-left: 10px;
}

.ai-bubble {
  background-color: #f5f5f5;
  color: #333;
  margin-right: 10px;
}

.timestamp {
  font-size: 12px;
  margin-top: 4px;
  display: block;
}

.user-bubble .timestamp {
  color: rgba(255, 255, 255, 0.7);
  text-align: right;
}

.ai-bubble .timestamp {
  color: #666;
  text-align: left;
}

.demo-tabs {
  width: 100%;
}


.no-data {
  color: #909399;
  text-align: center;
  padding: 20px;
}

.card-section {
  margin-bottom: 20px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background-color: #fff;
}

.card-title {
  padding: 10px 15px;
  border-bottom: 1px solid #dcdfe6;
  background-color: #f5f7fa;
  color: #303133;
  font-weight: bold;
}

.card-content {
  padding: 15px;
}

#chart-container {
  margin: 0 auto;
}

.bottom-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.icon-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
}

.icon-button i {
  font-size: 16px;
  color: #007bff;
}

.userIconClass {
  width: 30px;
  height: 30px;
}
</style>