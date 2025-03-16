<template>
  <div class="chat-layout">
    <div class="message-container">
      <div class="messages-wrapper" v-if="messageHistory.length > 0">
        <div v-for="(message, index) in messageHistory" :key="index" :class="[
          'message-wrapper',
          message.type === 'user' ? 'user-message' : 'ai-message',
        ]">
          <div v-if="message.type === 'user'" class="user-content">
            <img class="avatar" src="@/assets/image/human.png" alt="User Avatar" />
            <div class="message-bubble user-bubble">
              <div class="message-text" v-html="message.text"></div>
              <span class="timestamp">{{ message.timestamp }}</span>
            </div>
          </div>
          <AiMessage v-else :message="message" />
        </div>
      </div>
    </div>
    <div class="input-container">
      <el-input 
        type="textarea" 
        v-model="query" 
        placeholder="Please enter your question"
        :autosize="{ minRows: 2, maxRows: 4 }"
        @keydown.enter="handleEnter"
      />
      <el-button type="primary" @click="sendQuery">Send</el-button>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import axios from "axios";
import MarkdownRenderer from "./MarkdownRenderer.vue";
import AiMessage from "./AiMessage.vue"; // 导入新组件
import { useQueryStore } from '@/stores/query';
import { emitter } from '@/assets/ts/eventBus.js';

export default {
  components: {
    MarkdownRenderer,
    AiMessage, // 注册组件
  },
  data() {
    return {
      query: "",
      currentQuery: "",
      messageHistory: [],
      currentMessage: {},
    };
  },
  setup() {
    const queryStore = useQueryStore();
    return { queryStore };
  },
  methods: {
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

      const formattedText = this.query.replace(/\n/g, "<br>");
      this.messageHistory.push({
        type: "user",
        text: formattedText,
        timestamp: new Date().toLocaleTimeString(),
      });
      this.currentQuery = this.query;

      this.queryStore.setCurrentQuery(this.query);
      console.log("Parent sending to Pinia:", this.queryStore.currentQuery);
      this.query = "";

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

        // this.queryStore.setResponse(res.data);

        const newMessage = {
          type: "ai",
          code: {
            text: res.data.response.code || "",
            type: "code",
            timestamp: new Date().toLocaleTimeString(),
          },
          data: res.data.response.data,
          understanding: res.data.response.understanding,
          explanation: res.data.response.explanation,
          vis_data: res.data.response.vis_data,
          vis_tag_name: `chart_${Date.now()}_${this.messageHistory.length}`,
          timestamp: new Date().toLocaleTimeString(),
          top_k_similar: res.data.top_k_similar,
          message_history: res.data.message_history,
        };
        this.currentMessage = newMessage;

        this.messageHistory.push(newMessage);
      } catch (error) {
        console.error("Error fetching response:", error);
      }
    },
    handleEnter(event) {
      if (event.shiftKey) {
        return;
      } else {
        event.preventDefault();
        this.sendQuery();
      }
    },
    handleSubmitQuery(newQuery) {
      this.currentQuery = newQuery;
    },
  },
  mounted() {
    console.log("组件已挂载");
  },
};
</script>

<style scoped>
.chat-layout {
  /* height: 100vh;
  width: 100vh; */
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  background-color: #f0f0f0;
  border: 1px solid #dcdfe6;
}
.message-container {
  flex: 1;
  overflow-y: auto;
  /* padding-left: 10px;
  padding-right: 10px; */
  /* min-height: 90%; */
  /* margin-bottom: 20px; */
}

.messages-wrapper {
  /* max-height: 100%; */
  overflow-y: auto;
  padding-bottom: 20px;
}

.input-container {
  display: flex;
  align-items: center;
  padding-left: 10px;
  padding-right: 10px;
  border-top: 2px solid #a5a5a5;
  margin-bottom: 17px;
  /* margin-top: 1000px; */
  height: 15px;
}

.el-textarea {
  flex: 1;
  margin-right: 10px;
}

.el-button {
  height: 35px;
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
  margin-right: 10px;
  display: flex;
}

.ai-content {
  flex-direction: row;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin: 0 10px;
}

.message-bubble {
  padding: 12px 16px;
  border-radius: 12px;
  position: relative;
}

.user-bubble {
  background-color: #409EFF;
  color: white;
}

.ai-bubble {
  background-color: #f5f5f5;
  color: #333;
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
</style>