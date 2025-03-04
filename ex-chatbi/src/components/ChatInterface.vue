<template>
  <div class="common-layout">
    <el-container class="common-container">
      <el-container>
        <el-main id="main">
          <!-- 只有当有消息时才显示 message-container -->
          <div class="message-container" v-if="messageHistory.length > 0">
            <!-- 遍历历史消息 -->
            <div
              v-for="(message, index) in messageHistory"
              :key="index"
              :class="[
                'message-wrapper',
                message.type === 'user' ? 'user-message' : 'ai-message',
              ]"
            >
              <!-- 用户消息 -->
              <div v-if="message.type === 'user'" class="user-content">
                <img
                  class="avatar"
                  src="@/assets/image/human.png"
                  alt="User Avatar"
                />
                <div class="message-bubble user-bubble">
                  <div class="message-text" v-html="message.text"></div>
                  <span class="timestamp">{{ message.timestamp }}</span>
                </div>
                
              </div>

              <!-- AI 响应 -->
              <div v-else class="ai-content">
                <img
                  class="avatar"
                  src="@/assets/image/robot.png"
                  alt="AI Avatar"
                />
                <div class="message-bubble ai-bubble">
                  <el-tabs
                    v-model="activeName"
                    type="card"
                    class="demo-tabs"
                    @tab-click="handleClick"
                  >
                    <el-tab-pane label="data" name="data">
                      <table v-if="message.data" class="result-table">
                        <thead>
                          <tr>
                            <th
                              v-for="(column, idx) in message.data.column"
                              :key="idx"
                            >
                              {{ column }}
                            </th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr
                            v-for="(row, rowIdx) in message.data.data"
                            :key="rowIdx"
                          >
                            <td v-for="(cell, cellIdx) in row" :key="cellIdx">
                              {{ cell }}
                            </td>
                          </tr>
                        </tbody>
                      </table>
                      <p v-else class="no-data">no data</p>
                    </el-tab-pane>
                    <el-tab-pane label="chart" name="chart">
                      <div id="chart-container">
                        <div
                          :id="message.vis_tag_name"
                          style="width: 600px; height: 400px"
                        ></div>
                      </div>
                    </el-tab-pane>
                    <el-tab-pane label="code" name="code">
                      <MarkdownRenderer
                        class="sql-code"
                        :content="message.code?.text || ''"
                      />
                    </el-tab-pane>
                  </el-tabs>
                  <span class="timestamp">{{ message.timestamp }}</span>
                </div>
              </div>
            </div>
          </div>
          <div class="input-container">
            <el-input
              type="textarea"
              v-model="query"
              placeholder="Please enter your question"
              @keydown.enter="handleEnter"
            ></el-input>
            <el-button type="primary" @click="sendQuery">Send</el-button>
            <SelectPanel ref="selectPanelKey"/>
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
import SelectPanel from './SelectPanel.vue'
import { useQueryStore } from '@/stores/query';
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
      currentQuery: "",
      messageHistory: [], // 存储所有对话历史
    };
  },
  setup() {
    const queryStore = useQueryStore();
    return { queryStore };
  },
  methods: {
    handleClick(tab) {
      console.log(tab);
      const tab_name = tab.props.name;
      if (tab_name === "chart") {
        // 找到当前激活的消息（假设是最后一条 AI 消息）
      
        const lastAiMessage = this.messageHistory
          .slice()
          .reverse()
          .find((msg) => msg.type === "ai");
        console.log("lastAiMessage: ", lastAiMessage)
        if (lastAiMessage && lastAiMessage.vis_data) {
          nextTick(() => {
            console.log("lastAiMessage.vis_data", lastAiMessage.vis_data)
            chart(lastAiMessage.vis_tag_name, lastAiMessage.vis_data);
          });
        }
      }
    },
    extractSQL(text) {
      const sqlRegex = /```sql[\s\S]*?```/gis;
      const matches = text.match(sqlRegex);
      return matches
        ? matches
            .map((match) => match.replace(/```sql|```/g, "").trim())
            .join("\n")
        : "No SQL code found";
    },
    async sendQuery() {
      if (!this.query) return;

      // 将用户输入添加到历史记录
      const formattedText = this.query.replace(/\n/g, "<br>");
      this.messageHistory.push({
        type: "user",
        text: formattedText,
        timestamp: new Date().toLocaleTimeString(),
      });
      console.log(this.messageHistory)
      this.currentQuery = this.query;

      this.queryStore.setCurrentQuery(this.query);
      console.log('Parent sending to Pinia:', this.queryStore.currentQuery);
      this.query = ""; // 清空输入框

      try {
        const res = await axios.post(
          "/api/query",
          { query: this.currentQuery },
          {
            headers: {
              "Content-Type": "application/json",
              Accept: "application/json",
            },
          }
        );

        this.queryStore.setResponse(res.data);
        console.log('Parent stored response in Pinia:', res.data);

        // 将 LLM 响应添加到历史记录
        this.messageHistory.push({
          type: "ai",
          code: {
            text: res.data.response.code || "",
            type: "code",
            timestamp: new Date().toLocaleTimeString(),
          },
          data: res.data.response.data,
          vis_data: res.data.response.vis_data,
          vis_tag_name: `chart_${Date.now()}_${this.messageHistory.length}`,
          //{ 
            // vis_tag:
            //   res.data.response.vis_data.vis_tag ||
            //   `chart_${Date.now()}_${this.messageHistory.length}`,
          //},
          timestamp: new Date().toLocaleTimeString(),
        });


        // 处理图表
        console.log(res.data.response.vis_data);
        // const vis_id = "vis_tag_"+String(this.messageHistory.length-1)
        // chart(res.data.response.vis_data, vis_id);
      } catch (error) {
        console.error("Error fetching response:", error);
      }
    },
    handleEnter(event) {
      if (event.shiftKey) {
        return; // Shift + Enter 不触发
      } else {
        event.preventDefault(); // 阻止默认换行
        this.sendQuery();
      }
    },

    handleSubmitQuery(newQuery) {
      this.currentQuery = newQuery
      // this.query = newQuery
    }
  },
  mounted() {
    console.log("组件已挂载");
    nextTick(() => {
      console.log("DOM 已更新");
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

#main {
  background-color: #ffffff;
  height: 100%;
  width: 70%;
  border: 1px solid #afafaf;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

/* .message-container {
  flex: 1;
  overflow-y: auto;
  max-width: 100%;
} */

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

.user-content, .ai-content {
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

.result-table {
  width: 100%;
  border-collapse: collapse;
}

.no-data {
  padding: 10px;
  color: #666;
}
</style>