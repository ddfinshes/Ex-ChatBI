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
            <div style="text-align: left;">
              QTD sales total, target sales, and variance.
            </div>
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
            <div style="text-align: left;">
              Write an SQL query to calculate the current QTD (Quarter-To-Date) sales total, target sales, and variance (target - actual sales).
            </div>
          </el-card>
        </el-col>
  
        <!-- Branch Structure -->
      <el-col :span="6">
        <div style="position: relative;">
          <!-- Connecting Arrow -->
          <div
            v-for="(question, index) in previousQuestions"
            :key="'arrow-' + index"
            class="branch-arrow"
            :style="{ top: (index * 60 + 60) + 'px' }"
          >
            <!-- Arrow Head -->
            <div style="position: absolute; top: -5px; right: -8px; width: 0; height: 0; border-top: 5px solid transparent; border-bottom: 5px solid transparent; border-left: 8px solid #000;"></div>
          </div>
          <!-- Dynamically Render Cards -->
          <el-card
            v-for="(question, index) in previousQuestions"
            :key="index"
            shadow="hover"
            :style="{ width: '150px', marginTop: index === 0 ? '20px' : '10px' }"
          >
            <div slot="header">{{ question }}</div>
          </el-card>
        </div>
      </el-col>
      </el-row>
  
      
      <el-drawer :visible.sync="drawer" :direction="direction">
        <!-- <SelectBar /> -->
      </el-drawer>
    </el-aside>
  </template>
  
  <script>
  import { ref } from "vue";
  import axios from "axios";

  export default {
    name: 'SelectPanel',
    props: {
        drawer: Boolean,
        direction: String,
        saveLog: Function
    },
    data() {
      return {
        previousQuestions: ['QTD Sales Total', 'WTD vs Target']
      };
    },
    methods: {
      // 你可以在这里定义其他方法
    }
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