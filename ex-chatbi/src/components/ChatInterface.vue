<template>
  <div class="common-layout">
    <el-container class="common-container">
      <el-container>
        <el-main id="main">
          <div class="message-container">
            <!-- <div
              v-for="(msg, index) in messages"
              :key="index"
              :class="msg.type"
            >
            <el-tabs
              v-model="activeName"
              type="card"
              class="demo-tabs"
              @tab-click="handleClick"
            >
              <el-tab-pane label="chart" name="chart">
                Chart
                
                </el-tab-pane>
              <el-tab-pane label="data" name="second">
                <MarkdownRenderer
                v-if="msg.type === 'data'" 
                class="message-text"
                :content="msg.text"
              />
                
              </el-tab-pane>
              <el-tab-pane label="code" name="third">
                <MarkdownRenderer
                v-if="msg.type === 'code'"
                class="sql-code"
                :content="msg.text"
              />
              </el-tab-pane>
            </el-tabs>
            </div> -->
            <div>
              <el-tabs
                v-model="activeName"
                type="card"
                class="demo-tabs"
                @tab-click="handleClick"
              >
                <el-tab-pane label="data" name="data">
                  <!-- 动态生成表格 -->
                  <table v-if="messages.data" class="result-table">
                    <!-- 表头 -->
                    <thead>
                      <tr>
                        <th
                          v-for="(column, index) in messages.data.column"
                          :key="index"
                        >
                          {{ column }}
                        </th>
                      </tr>
                    </thead>
                    <!-- 表格内容 -->
                    <tbody>
                      <tr
                        v-for="(row, rowIndex) in messages.data.data"
                        :key="rowIndex"
                      >
                        <td v-for="(cell, cellIndex) in row" :key="cellIndex">
                          {{ cell }}
                        </td>
                      </tr>
                    </tbody>
                  </table>

                  <!-- 如果没有数据，显示提示信息 -->
                  <p v-else class="no-data">no data</p>
                </el-tab-pane>
                <el-tab-pane label="chart" name="chart">
                  <!-- 柱状图、折线图和饼图 -->
                  <div id="vis_tag">
                    <div
                      :id="messages.vis_data.vis_tag"
                      style="width: 600px; height: 400px"
                    ></div>
                  </div>
                </el-tab-pane>
                <el-tab-pane label="code" name="code">
                  <MarkdownRenderer
                    class="sql-code"
                    :content="messages.code?.text || ''"
                  />
                </el-tab-pane>
              </el-tabs>
            </div>
          </div>
          <div class="input-container">
            <el-input
              type="textarea"
              v-model="query"
              placeholder="Please enter your question"
              @keydown.enter="handleEnter"
            ></el-input>
            <el-button type="primary" @click="sendQuery">sent</el-button>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { ref } from "vue";
import axios from "axios";
import MarkdownRenderer from "./MarkdownRenderer.vue";
import { useTabs } from "@/assets/ts/useTabs.ts";
import { chart } from "@/assets/ts/chart.ts";
import { nextTick } from "vue";
export default {
  components: {
    MarkdownRenderer,
  },
  data() {
    return {
      activeName: "data", // 默认激活的 tab
      query: "", // 输入框的值
      response: "", // 响应数据（如果需要的话）
      messages: {
        code: "",
        data: {},
        user: { text: "", type: "user", timestamp: "" },
        vis_data: {},
      },
    };
  },
  methods: {
    handleClick(tab) {
      console.log("当前 tab:", tab.name); // tab 切换时的处理
    },
    extractSQL(text) {
      const sqlRegex = /```sql[\s\S]*?```/gis; // 提取SQL代码块的正则表达式
      const matches = text.match(sqlRegex);
      return matches
        ? matches
            .map((match) => match.replace(/```sql|```/g, "").trim())
            .join("\n")
        : "No SQL code found";
    },

    async sendQuery() {
      if (!this.query) return;

      const formattedText = this.query.replace(/\n/g, "<br>"); // 将换行符替换为 <br>
      this.messages.user = {
        text: formattedText,
        type: "user",
        timestamp: new Date().toLocaleTimeString(),
      };

      const currentQuery = this.query; // 保存当前的 query 值
      this.query = ""; // 清空输入框

      try {
        const res = await axios.post(
          "/api/query",
          { query: currentQuery },
          {
            headers: {
              "Content-Type": "application/json",
              Accept: "application/json",
            },
          }
        );

        this.messages.code = {
          text: res.data.response.code || "",
          type: "code",
          timestamp: new Date().toLocaleTimeString(),
        };
        this.messages.data = res.data.response.data; //字典类型
        this.messages.vis_data = res.data.response.vis_data;
        // 处理chart
        chart(res.data.response.vis_data);
      } catch (error) {
        console.error("Error fetching response:", error);
      }
    },
    handleEnter(event) {
      if (event.shiftKey) {
        return; // 按 Shift + Enter 不触发发送
      } else {
        event.preventDefault(); // 阻止默认的 Enter 换行
        this.sendQuery(); // 调用发送方法
      }
    },
  },
  mounted() {
    // 如果需要初始化数据，可以在这里添加逻辑
    console.log("组件已挂载");
    nextTick(() => {
      console.log("组件已挂载");

    });
  },
};
</script>

<style>
.common-layout {
  height: 100vh;
  width: 1300px;
  display: flex;
  flex-direction: column;
}

.common-container {
  height: 100%;
  width: 100%;
  background-color: #f0f0f0;
  display: flex;
}

#aside {
  background-color: #ffffff;
  height: 100%;
  width: 30%;
  border: 1px solid #afafaf;
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

.message-text {
  white-space: pre-line; /* 保留换行符 */
  font-family: inherit; /* 继承默认字体 */
  line-height: 1.6; /* 设置行高 */
}

.message-container {
  flex: 1;
  overflow-y: auto;
  max-width: 100%;
}

.user {
  border-bottom: 3px solid #a5a5a5;
  border-radius: 0;
  padding: 10px;
  margin-bottom: 1rem;
  margin-right: 1px;
  text-align: left;
  position: relative; /* 确保图标可以相对于对话框定位 */
}

.user::after {
  content: "user"; /* 伪元素内容 */
  display: inline-block;
  width: 20px; /* 图标的宽度 */
  height: 20px; /* 图标的高度 */
  background-size: cover; /* 确保图标覆盖整个区域 */
  position: absolute; /* 绝对定位 */
  top: -10px; /* 距离顶部的距离 */
  left: 10px; /* 距离右侧的距离 */
}

.ai {
  border-bottom: 3px solid #a5a5a5;
  border-radius: 0;
  padding: 10px;
  margin-bottom: 1rem;
  margin-left: 2px;
  text-align: left;
}

.ai::after {
  content: "ai"; /* 伪元素内容 */
  display: inline-block;
  width: 20px; /* 图标的宽度 */
  height: 20px; /* 图标的高度 */
  background-size: cover; /* 确保图标覆盖整个区域 */
  position: absolute; /* 绝对定位 */
  top: -10px; /* 距离顶部的距离 */
  left: 10px; /* 距离右侧的距离 */
}

.timestamp {
  font-size: 0.8rem;
  color: gray;
}

.input-container {
  display: flex;
  align-items: center;
  padding: 10px;
  border-top: 2px solid #a5a5a5;
}

.input-container el-input {
  flex: 1;
  margin-right: 10px;
}

/*.input-container el-button{
  
}*/
/* .message-text {
  background-color: #bbd2eb;
  border-radius: 10px;
  padding: 10px;
  margin-bottom: 1rem;
  text-align: left;
} */
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

/* 为表格添加样式 */
.result-table {
  width: 100%; /* 确保表格占满容器宽度 */
  border-collapse: collapse; /* 合并边框，避免双重边框 */
}

/* 为表头和单元格添加边框 */
.result-table th,
.result-table td {
  border: 1px solid #dcdcdc; /* 设置边框颜色和样式 */
  padding: 8px; /* 添加内边距，使内容不紧贴边框 */
  text-align: left; /* 设置文本对齐方式 */
}

/* 为表头添加背景色*/
.result-table th {
  background-color: #f5f5f5; /* 表头背景色 */
  font-weight: bold; /* 加粗表头文字 */
}

/* 为表格行添加悬停效果*/
.result-table tbody tr:hover {
  background-color: #fafafa; /* 鼠标悬停时的背景色 */
}
</style>
