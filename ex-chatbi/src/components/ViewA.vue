<!-- QueryDisplay.vue -->
<template>
    <el-row type="flex" justify="space-between" style="padding: 10px">
      <!-- User Input Card -->
      <el-col :span="6">
        <!-- <el-card shadow="hover" style="width: 180px; margin-right: 10px">
          <div slot="header">User Input</div>
          <div style="text-align: left">{{ currentQuery }}</div>
        </el-card> -->

        <el-card ref="userInputCard"
          shadow="hover" 
          style="width: 160px; margin-right: 10px; padding: 0; border: none;"
          body-style="padding: 0;"
        >
          <div slot="header" style="background-color: #909aa3; color: white; padding: 10px; border-radius: 4px 4px 0 0; text-transform: uppercase; text-align: center;">
            User Input
          </div>
          <div style="background-color: #ffffff; color: #303133; padding: 10px; text-align: left; border-radius: 0 0 4px 4px; min-height: 40px;">
            {{ currentQuery }}
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="4">
      <div
        class="arrow-connector"
        style="
          position: absolute;
          left: 180px;
          top: 50%;
          transform: translateY(-50%);
          display: flex;
          align-items: center;
          width: 60px;
          justify-content: space-between;
        "
      >
        <!-- 左箭头 -->
        <div
          style="
            width: 0;
            height: 0;
            border-top: 5px solid transparent;
            border-bottom: 5px solid transparent;
            border-right: 8px solid #409EFF;
          "
        ></div>
        
        <!-- 中间圆点 -->
        <div
          style="
            width: 15px;
            height: 15px;
            background-color: #3da59b;
            border-radius: 50%;
          "
        ></div>
        
        <!-- 右箭头 -->
        <div
          style="
            width: 0;
            height: 0;
            border-top: 5px solid transparent;
            border-bottom: 5px solid transparent;
            border-left: 8px solid #409EFF;
          "
        ></div>
      </div>
      </el-col>

      <!-- Model Understanding Card -->
      <el-col :span="8">
        <el-card ref="modelUnderstandingCard"
          shadow="hover" 
          style="width: 230px; margin-right: 10px; padding: 0; border: none;"
          body-style="padding: 0;"
        >
          <div slot="header" style="background-color: #909aa3; color: white; padding: 10px; border-radius: 4px 4px 0 0; text-transform: uppercase; text-align: center;">
            Model Understanding
          </div>
          <div
            style="background-color: #ffffff; color: #303133; padding: 10px; text-align: left; border-radius: 0 0 4px 4px; min-height: 40px;"
          >
            <p v-html="highlightText(modelResponse, searchtext)"></p>
          </div>
        </el-card>
      </el-col>
  
      <!-- Previous Questions with Similarity -->
      <el-col :span="6">
        <div style="position: relative">
          <div
            v-for="(item, index) in topKSimilar"
            :key="'arrow-' + index"
            class="branch-arrow"
            :style="{
              top: index * 60 + 60 + 'px',
              width: '20px',
              height: `${Math.max(2, item.similarity * 10)}px`,
              backgroundColor: '#000',
            }"
          >
            <div
              style="
                position: absolute;
                top: -5px;
                right: -8px;
                width: 0;
                height: 0;
                border-top: 5px solid transparent;
                border-bottom: 5px solid transparent;
                border-left: 8px solid #000;
              "
            ></div>
          </div>
  
          <el-card
            v-for="(item, index) in topKSimilar"
            :key="index"
            shadow="hover"
            :style="{
              width: '150px',
              marginTop: index === 0 ? '20px' : '10px',
            }"
          >
            <div slot="header">{{ item.query }}</div>
            <div>Similarity: {{ item.similarity.toFixed(2) }}</div>
          </el-card>
        </div>
      </el-col>
    </el-row>
  </template>
  
  <script>
  import { useQueryStore } from '@/stores/query'; // 假设这是你的 Pinia store 路径
  
  export default {
    name: 'QueryDisplay',
    props: {
      drawer: Boolean,
      direction: String,
      saveLog: Function,
    },
    setup() {
      const queryStore = useQueryStore();
      return { queryStore };
    },
    computed: {
      currentQuery() {
        return this.queryStore.currentQuery;
      },
      response() {
        return this.queryStore.response;
      }
    },
    data() {
      return {
        query: '',
        messageHistory: [],
        modelResponse: '',
        topKSimilar: [],
        highlight: [],
        searchtext:[],
      };
    },
    watch: {
      currentQuery(newVal) {
        console.log('监听到新查询:', newVal);
        if (newVal) {
          // this.sendQuery(); // 如果需要发送查询，可以在这里实现或通过 emit 通知父组件
        }
      },
      response(newVal) {
        console.log('监听到新响应:', newVal);
        if (newVal) {
          this.modelResponse = newVal.response.understanding;
          this.topKSimilar = newVal.top_k_similar || [];
          this.messageHistory = newVal.message_history || [];
          this.highlight = newVal.response.pair_relevance;
          this.searchtext = newVal.response.highlight_words;
        }
      }
    },
    methods: {
      // 如果需要发送查询，可以取消注释并实现
      // async sendQuery() {
      //   const res = await someApiCall(this.currentQuery);
      //   this.modelResponse = res.data.response.code || JSON.stringify(res.data.response.data);
      //   this.topKSimilar = res.data.top_k_similar || [];
      // }
      // 获取元素底部中心坐标
      highlightText(text, searchTextArray) {
      if (!searchTextArray || searchTextArray.length === 0) return text;

      // 遍历数组中的每个关键词
      searchTextArray.forEach(searchText => {
        const regex = new RegExp(`(${searchText})`, 'gi');
        text = text.replace(regex, '<span class="highlight">$1</span>');
      });

      return text;
    },

    getCardPositions() {
      return {
        userInput: this.calcPosition(this.$refs.userInputCard.$el),
        model: this.calcPosition(this.$refs.modelUnderstandingCard.$el)
      }
    },
    
    calcPosition(el) {
      if (!el) return null
      const rect = el.getBoundingClientRect()
      return {
        x: rect.left + rect.width / 2,
        y: rect.bottom
      }
    }
    }
  };
  </script>
  
  <style>
  .branch-arrow {
    position: absolute;
    left: -20px;
    width: 20px;
    height: 2px;
    background-color: #000;
  }

  .highlight {


  background-color: yellow;


}
  </style>
