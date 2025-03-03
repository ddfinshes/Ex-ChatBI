<template>
    <el-aside id="selectPanelContainer" width="605px">
        <button
        @click="drawer = true"
        type="button"
        class="btn btn-link"
        style="border-top: 10px; margin-bottom: 15px; border-left: 5px solid white; padding-left: 26px;"
      >
        <img
          style="width: 48px; height: 48px"
          src="@/assets/image/database.png"
          alt="..."
          :fit="`fill`"
        />
      </button>
      <button
        @click="drawer = true"
        type="button"
        class="btn btn-link"
        style="margin-bottom: 15px; border-left: 5px solid none; padding-left: 26px;"
      >
        <img
          style="width: 48px; height: 48px"
          src="@/assets/image/chat_history.png"
          alt="..."
          :fit="`fill`"
        />
      </button>
      <button
        @click="saveLog"
        type="button"
        class="btn btn-link"
        style="margin-bottom: 15px; border-left: 5px solid none; padding-left: 26px;"
      >
        <img
          style="width: 48px; height: 48px"
          src="@/assets/image/save.png"
          alt="..."
          :fit="`fill`"
        />
      </button>

      <el-row type="flex" justify="space-between" style="padding: 10px;">
        <!-- User Input Card -->
        <el-col :span="8">
          <el-card shadow="hover" style="width: 180px; margin-right: 10px;">
            <div slot="header">User Input</div>
            <!-- <div style="text-align: left;">{{ query }}</div> -->
            <div style="text-align: left;">{{ currentQuery }}</div>
          </el-card>
        </el-col>
        
        <div
            class="arrow-connector"
            style="position: absolute; left: 180px; top: 50%; transform: translateY(-50%) rotate(0deg); width: 20px; height: 2px; background-color: #000;"
        >
            <!-- Arrowhead -->
            <div style="position: absolute; top: -5px; right: -8px; width: 0; height: 0; border-top: 5px solid transparent; border-bottom: 5px solid transparent; border-left: 8px solid #000;"></div>
        </div>

        <!-- Model Understanding Card -->
        <el-col :span="10">
          <el-card shadow="hover" style="width: 220px; margin-right: 10px;">
            <div slot="header">Model Understanding</div>
            <div style="text-align: left;">{{ modelResponse }}</div>
          </el-card>        
        </el-col>  
  
        <!-- Previous Questions with Similarity -->
        <el-col :span="6">
          <div style="position: relative;">
            <!-- Connecting Arrow -->
            <div
              v-for="(item, index) in topKSimilar"
              :key="'arrow-' + index"
              class="branch-arrow"
              :style="{
                top: (index * 60 + 60) + 'px',
                width: '20px',
                height: `${Math.max(2, item.similarity * 10)}px`, // 粗细根据相似度
                backgroundColor: '#000'
              }"
            >
              <div style="position: absolute; top: -5px; right: -8px; width: 0; height: 0; border-top: 5px solid transparent; border-bottom: 5px solid transparent; border-left: 8px solid #000;"></div>
            </div>

            <!-- Dynamically Render Cards -->
            <el-card
              v-for="(item, index) in topKSimilar"
              :key="index"
              shadow="hover"
              :style="{ width: '150px', marginTop: index === 0 ? '20px' : '10px' }"
            >
              <div slot="header">{{ item.query }}</div>
              <div>Similarity: {{ item.similarity.toFixed(2) }}</div>
            </el-card>
          </div>
        </el-col>
      </el-row>
  
      
      <!-- <el-drawer :visible.sync="drawer" :direction="direction">
        <SelectBar />
      </el-drawer> -->
    </el-aside>
  </template>
  
  <script>
  import { ref } from "vue";
  import axios from "axios";
  import { useQueryStore } from '@/stores/query';
  import { nextTick } from "vue";

  export default {
    name: 'SelectPanel',
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
        return this.queryStore.response; // 从 Pinia 获取 response
      }
    },
    data() {
      return {
        query: '',
        messageHistory: [],
        modelResponse: '',
        topKSimilar: []
      };
    },
    watch: {
      currentQuery(newVal) {
        console.log('监听到新查询:', newVal);
        if (newVal) {
          // this.sendQuery();
        }
      },
      response(newVal) {
        console.log('监听到新响应:', newVal);
        if (newVal) {
          // 根据 response 更新本地数据
          this.modelResponse = newVal.response.code || JSON.stringify(newVal.response.data);
          this.topKSimilar = newVal.top_k_similar || [];
          this.messageHistory.push({
            type: 'ai',
            code: {
              text: newVal.response.code || '',
              type: 'code',
              timestamp: new Date().toLocaleTimeString(),
            },
            data: newVal.response.data,
            vis_data: {
              ...newVal.response.vis_data,
              vis_tag:
                newVal.response.vis_data.vis_tag ||
                `chart_${Date.now()}_${this.messageHistory.length}`,
            },
            timestamp: new Date().toLocaleTimeString(),
          });
        }
      }
    },
    methods: {
      // async sendQuery() {  // 假设从外部传入输入
      //   this.modelResponse = res.data.response.code || JSON.stringify(res.data.response.data);
      //   this.topKSimilar = res.data.top_k_similar || [];     
      // }       
    },
  }
  </script>
  
  <style>
  /* 可选：添加特定样式 */
    .branch-arrow {
    position: absolute;
    left: -20px;
    width: 20px;
    height: 2px;
    background-color: #000;
    }
  </style>