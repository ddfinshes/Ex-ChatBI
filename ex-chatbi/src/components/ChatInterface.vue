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
                  <MarkdownRenderer
                    class="message-text"
                    :content="messages.data?.text || ''"
                  />
                </el-tab-pane>
                <el-tab-pane label="chart" name="chart"> Chart </el-tab-pane>
                <el-tab-pane label="code" name="code">
                  <MarkdownRenderer
                    class="sql-code"
                    :content="messages.code || ''"
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
export default {
components: {
    MarkdownRenderer,
  },
  data() {
    return {
      activeName: 'data', // 默认激活的 tab
      query: '', // 输入框的值
      response: '', // 响应数据（如果需要的话）
      messages: {
        code: '',
        data: { text: '', type: 'data', timestamp: '' },
        user: { text: '', type: 'user', timestamp: '' },
      },
    };
  },
  methods: {
    handleClick(tab) {
      console.log('当前 tab:', tab.name); // tab 切换时的处理
    },
    extractSQL(text) {
      const sqlRegex = /```sql[\s\S]*?```/gis; // 提取SQL代码块的正则表达式
      const matches = text.match(sqlRegex);
      return matches
        ? matches
            .map((match) => match.replace(/```sql|```/g, '').trim())
            .join('\n')
        : 'No SQL code found';
    },
    async sendQuery() {
      if (!this.query) return;

      const formattedText = this.query.replace(/\n/g, '<br>'); // 将换行符替换为 <br>
      this.messages.user = {
        text: formattedText,
        type: 'user',
        timestamp: new Date().toLocaleTimeString(),
      };

      const currentQuery = this.query; // 保存当前的 query 值
      this.query = ''; // 清空输入框

      try {
        const res = await axios.post(
          '/api/query',
          { query: currentQuery },
          {
            headers: {
              'Content-Type': 'application/json',
              Accept: 'application/json',
            },
          }
        );

        this.messages.code = res.data.response.code || '';
        this.messages.data = {
          text: res.data.response.data || '',
          type: 'data',
          timestamp: new Date().toLocaleTimeString(),
        };
        console.log(this.messages.data.text);
      } catch (error) {
        console.error('Error fetching response:', error);
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
    console.log('组件已挂载');
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
</style>
