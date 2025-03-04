<template>
  <el-aside id="selectPanelContainer" width="605px">
    <button
      @click="drawer = true"
      type="button"
      class="btn btn-link"
      style="
        border-top: 10px;
        margin-bottom: 15px;
        border-left: 5px solid white;
        padding-left: 26px;
      "
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
      style="
        margin-bottom: 15px;
        border-left: 5px solid none;
        padding-left: 26px;
      "
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
      style="
        margin-bottom: 15px;
        border-left: 5px solid none;
        padding-left: 26px;
      "
    >
      <img
        style="width: 48px; height: 48px"
        src="@/assets/image/save.png"
        alt="..."
        :fit="`fill`"
      />
    </button>

    <el-row type="flex" justify="space-between" style="padding: 10px">
      <!-- User Input Card -->
      <el-col :span="8">
        <el-card shadow="hover" style="width: 180px; margin-right: 10px">
          <div slot="header">User Input</div>
          <!-- <div style="text-align: left;">{{ query }}</div> -->
          <div style="text-align: left">{{ currentQuery }}</div>
        </el-card>
      </el-col>

      <div
        class="arrow-connector"
        style="
          position: absolute;
          left: 180px;
          top: 50%;
          transform: translateY(-50%) rotate(0deg);
          width: 20px;
          height: 2px;
          background-color: #000;
        "
      >
        <!-- Arrowhead -->
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

      <!-- Model Understanding Card -->
      <el-col :span="10">
        <el-card shadow="hover" style="width: 220px; margin-right: 10px">
          <div slot="header">Model Understanding</div>
          <div style="text-align: left">{{ modelResponse }}</div>
        </el-card>
      </el-col>

      <!-- Previous Questions with Similarity -->
      <el-col :span="6">
        <div style="position: relative">
          <!-- Connecting Arrow -->
          <div
            v-for="(item, index) in topKSimilar"
            :key="'arrow-' + index"
            class="branch-arrow"
            :style="{
              top: index * 60 + 60 + 'px',
              width: '20px',
              height: `${Math.max(2, item.similarity * 10)}px`, // 粗细根据相似度
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

          <!-- Dynamically Render Cards -->
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

    <!-- 卡片容器 -->
    <div class="card-container" v-if="!activeCard">
      <!-- 第一行四列 -->
      <el-row :gutter="20" class="card-row">
        <el-col
          v-for="(card, index) in firstRowCards"
          :key="'first-' + index"
          :span="6"
        >
          <el-card
            shadow="hover"
            class="click-card"
            @click.native="showExplanation(card)"
          >
            <div slot="header" class="card-title">
              <i :class="card.icon" class="card-icon"></i>
              {{ card.title }}
            </div>
            <div class="card-content">{{ card.content }}</div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 第二行四列 -->
      <el-row :gutter="20" class="card-row">
        <el-col
          v-for="(card, index) in secondRowCards"
          :key="'second-' + index"
          :span="6"
        >
          <el-card
            shadow="hover"
            class="click-card"
            @click.native="showExplanation(card)"
          >
            <div slot="header" class="card-title">
              <i :class="card.icon" class="card-icon"></i>
              {{ card.title }}
            </div>
            <div class="card-content">{{ card.content }}</div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 解释视图 -->
    <transition name="explanation-slide">
      <div class="full-explanation" v-if="activeCard" :style="modalStyle">
        <div class="header">
          <el-button
            type="primary"
            icon="el-icon-arrow-left"
            circle
            @click="hideExplanation"
          ></el-button>
          <h1>{{ activeCard.title }}</h1>
        </div>
        <pre class="content">{{ activeCard.explanation }}</pre>
      </div>
    </transition>

    <!-- <el-drawer :visible.sync="drawer" :direction="direction">
        <SelectBar />
      </el-drawer> -->
  </el-aside>
</template>
  
  <script>
import { ref } from "vue";
import axios from "axios";
import { useQueryStore } from "@/stores/query";
import { nextTick } from "vue";

export default {
  name: "SelectPanel",
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
    },
  },
  data() {
    return {
      activeCard: null,
      firstRowCards: [
        {
          id: 1,
          title: "销售分析",
          icon: "el-icon-data-analysis",
          content: "季度销售数据统计",
          explanation:
            "包含QTD销售额、目标达成率、环比增长率等核心指标的计算逻辑\n计算公式：QTD销售额 = SUM(销售金额) WHERE 日期 BETWEEN 季度初 AND 当前日期",
          active: false,
        },
        {
          id: 2,
          title: "数据源",
          icon: "el-icon-document",
          content: "销售数据库2023",
          explanation:
            "数据表结构：\n- sales_fact: 销售事实表\n- product_dim: 产品维度表\n- date_dim: 日期维度表",
          active: false,
        },
        {
          id: 3,
          title: "模型版本",
          icon: "el-icon-cpu",
          content: "预测模型v2.1",
          explanation:
            "基于时间序列的ARIMA模型\n参数设置：\n- 周期: 7天\n- 预测区间: 30天\n- 置信度: 95%",
          active: false,
        },
        {
          id: 4,
          title: "权限管理",
          icon: "el-icon-lock",
          content: "访问控制列表",
          explanation:
            "角色权限分配：\n- 管理员: 完全访问\n- 分析师: 只读访问\n- 访客: 受限访问",
          active: false,
        },
      ],
      secondRowCards: [
        {
          id: 5,
          title: "数据质量",
          icon: "el-icon-check",
          content: "完整性检查",
          explanation:
            "数据校验规则：\n1. 非空字段检查\n2. 值域范围验证\n3. 外键约束检查\n4. 时间序列连续性",
          active: false,
        },
        {
          id: 6,
          title: "ETL日志",
          icon: "el-icon-notebook-2",
          content: "最近更新记录",
          explanation:
            "最新ETL任务状态：\n- 成功: 23次\n- 警告: 2次\n- 失败: 0次\n最后更新时间: 2023-07-20 14:30",
          active: false,
        },
        {
          id: 7,
          title: "系统监控",
          icon: "el-icon-monitor",
          content: "资源使用情况",
          explanation:
            "当前状态：\nCPU: 62%\n内存: 45%\n存储: 78%\n网络: 120Mbps",
          active: false,
        },
        {
          id: 8,
          title: "API文档",
          icon: "el-icon-document-checked",
          content: "接口规范v1.2",
          explanation:
            "主要接口：\n- GET /api/sales\n- POST /api/predict\n- GET /api/status\n认证方式: JWT Token",
          active: false,
        },
      ],

      previousQuestions: ["QTD Sales Total", "WTD vs Target"],
    };
  },
  watch: {
    currentQuery(newVal) {
      console.log("监听到新查询:", newVal);
      if (newVal) {
        // this.sendQuery();
      }
    },
    response(newVal) {
      console.log("监听到新响应:", newVal);
      if (newVal) {
        // 根据 response 更新本地数据
        this.modelResponse =
          newVal.response.code || JSON.stringify(newVal.response.data);
        this.topKSimilar = newVal.top_k_similar || [];
        this.messageHistory.push({
          type: "ai",
          code: {
            text: newVal.response.code || "",
            type: "code",
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
    },
  },
  methods: {
    showExplanation(card) {
      this.activeCard = card;
    },
    hideExplanation() {
      this.activeCard = null;
    },
    // 你可以在这里定义其他方法
  },
  // async sendQuery() {  // 假设从外部传入输入
  //   this.modelResponse = res.data.response.code || JSON.stringify(res.data.response.data);
  //   this.topKSimilar = res.data.top_k_similar || [];
  // }
};
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
/*新增*/
/* 卡片容器 */
.card-container {
  padding: 15px;
}

.click-card {
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 15px;
  min-height: 150px;
}

.click-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #2d3a4b;
}

.card-icon {
  margin-right: 8px;
  color: #409eff;
}

/* 全屏解释视图 */
.header {
  display: flex;
  align-items: center;
  margin-bottom: 0px;
  padding: 10px; /* 内边距 */
  background: #f4f4f4; /* 背景色 */
  border-top: 1px solid #dcdfe6; /* 上边框 */
  border-left: 1px solid #dcdfe6; /* 左边框 */
  border-right: 1px solid #dcdfe6; /* 右边框 */
  border-radius: 0; /* 清除圆角 */
  h1 {
    margin-left: 10px;
    color: #303133;
  }
}

.content {
  border-bottom: 1px solid #dcdfe6; /* 上边框 */
  border-left: 1px solid #dcdfe6; /* 左边框 */
  border-right: 1px solid #dcdfe6; /* 右边框 */
  white-space: pre-wrap;
  line-height: 1.8;
  font-size: 16px;
  padding: 20px;
  background: #ffffff; /* 背景色 */
  border-radius: 0; /* 清除圆角 */
  max-height: calc(100vh - 200px);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  justify-content: center; /* 垂直居中 */
  min-height: 200px;
}

/* 过渡动画 */
.explanation-slide-enter-active {
  transition: all 0.3s ease-out;
}
.explanation-slide-leave-active {
  transition: all 0.2s cubic-bezier(1, 0.5, 0.8, 1);
}
.explanation-slide-enter,
.explanation-slide-leave-to {
  transform: translateY(20px);
  opacity: 0;
}
#selectPanelContainer {
  position: static !important;
  transform: none !important;
  overflow: visible;
}
.top-buttons {
  border-bottom: 1px solid #ebeef5;
  padding-bottom: 15px;
}
</style>