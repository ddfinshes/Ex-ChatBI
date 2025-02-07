<template>
  <div class="common-layout">
    <el-container class="common-container">
      <el-aside id="aside">Aside</el-aside>
      <el-container>
        <el-header id="header">Header</el-header>
        <el-main id="main">
          <div class="message-container">
            <div v-for="(msg, index) in messages" :key="index" :class="msg.type">
              <pre v-if="msg.type === 'ai'" class="sql-code"><code>{{ msg.text }}</code></pre>
              <p v-else class="message-text">{{ msg.text }}</p>
            </div>
          </div>
          <div class="input-container">
            <el-input v-model="query" placeholder="请输入您的问题" @keyup.enter="sendQuery"></el-input>
            <el-button type="primary" @click="sendQuery">提交</el-button>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
export default {
  setup() {
    const query = ref('');
    const response = ref('');
    const messages = ref([]);

    const extractSQL = (text) => {
      const sqlRegex = /```sql[\s\S]*?```/gis; // 提取SQL代码块的正则表达式
      const matches = text.match(sqlRegex);
      return matches ? matches.map(match => match.replace(/```sql|```/g, '').trim()).join('\n') : 'No SQL code found';
    };

    const sendQuery = async () => {
      if (!query.value) return;
      messages.value.push({ text: query.value, type: 'user', timestamp: new Date().toLocaleTimeString() });
      const currentQuery = query.value; // 保存当前的query值
      query.value = ''; // 清空输入框
      try {
        const res = await axios.post('http://127.0.0.1:5000/api/query', { 
          query: currentQuery // 使用保存的query值
        },
        {
          headers: {
            'Content-Type': 'application/json', // 明确指定请求头
            'Accept': 'application/json' 
          }
        });
        messages.value.push({ text: res.data.response, type: 'ai', timestamp: new Date().toLocaleTimeString() });
      } catch (error) {
        console.error('Error fetching response:', error);
      }
    };

    return { query, response, sendQuery, messages, extractSQL };
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
  background-color: #ccc;
  height: 100%;
  width: 30%;
  border: 1px solid #ccc;
  margin: 5px;
}

#header {
  background-color: #ccc;
  height: 20%;
  width: 70%;
  border: 1px solid #ccc;
  margin: 5px;
}

#main {
  background-color: #ccc;
  height: 80%;
  width: 70%;
  border: 1px solid #ccc;
  margin: 5px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.message-container {
  flex: 1;
  overflow-y: auto;
  max-width: 100%;
  margin: 1rem auto;
}

.user 
{
  background-color: #e0f7fa;
  border-radius: 10px;
  padding: 10px; 
  margin-bottom: 1rem;
  text-align: right;
  margin-right: 5px;
} 

.ai {
  background-color: #ccc;
  border-radius: 10px;
  padding: 10px;
  margin-bottom: 1rem;
  text-align: left;
  margin-left: 2px;
}

.timestamp {
  font-size: 0.8rem;
  color: gray;
}

.input-container {
  display: flex;
  align-items: center;
  padding: 10px;
  border-top: 1px solid #ccc;
}

.input-container el-input {
  flex: 1;
  margin-right: 10px;
}
/* .message-text {
  background-color: #bbd2eb;
  border-radius: 10px;
  padding: 10px;
  margin-bottom: 1rem;
  text-align: left;
} */
.sql-code {
  background-color: #f5f5f5;
  border-radius: 5px;
  padding: 10px;
  font-family: monospace;
  white-space: pre-wrap;
}
</style>
