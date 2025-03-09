<!-- ViewB.vue -->
<template>
  <div>
    <!-- 卡片容器 -->
    <div class="card-container" v-show="!activeCard"  style="margin: 0 50px;">
      <el-carousel 
        indicator-position="none" 
        arrow="always" 
        :interval="0"
        :height="carouselHeight"
      >
        <!-- 第一页：原有两行四列 -->
  <el-carousel-item>
    <div class="carousel-page">
      <!-- 第一行四列 -->
      <el-row :gutter="60" class="card-row">
        <el-col
          v-for="(card, index) in firstRowCards"
          :key="'first-' + index"
          :span="6"
        >
          <el-card
            shadow="hover"
            class="click-card"
            @click="showExplanation(card)"
          >
            <template #header>
              <div class="card-title">
              <i :class="card.icon" class="card-icon"></i>
              {{ card.title }}
              </div>
            </template>
            <div class="card-content">{{ card.content }}</div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 第二行四列 -->
      <el-row :gutter="60" class="card-row">
        <el-col
          v-for="(card, index) in secondRowCards"
          :key="'second-' + index"
          :span="6"
        >
          <el-card
            shadow="hover"
            class="click-card"
            @click="showExplanation(card)"
          >
            <template #header>
              <div class="card-title">
              <i :class="card.icon" class="card-icon"></i>
              {{ card.title }}
              </div>
            </template>
            <div class="card-content">{{ card.content }}</div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    </el-carousel-item>
    <!-- 第二页：新增一行四列 -->
        <el-carousel-item>
          <div class="carousel-page">
            <el-row :gutter="60" class="card-row">
              <el-col v-for="(card, index) in thirdRowCards" :key="'third-'+index" :span="6">
                <el-card shadow="hover" class="click-card third-row-card" @click="showExplanation(card)">
                  <template #header>
                    <div class="card-title">
                      <i :class="card.icon" class="card-icon"></i>
                      {{ card.title }}
                    </div>
                  </template>
                  <div class="card-content">{{ card.content }}</div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </el-carousel-item>
      </el-carousel>
    </div>

    <!-- 解释视图 -->
    <transition name="explanation-slide">
      <div 
        class="viewc-container" 
        v-if="activeCard"
        :key="activeCard.id"
      >
        <el-card class="fullscreen-card">
          <!-- 使用原本的 header 样式 -->
          <template #header>
            <div class="header">
              <el-button
                icon="el-icon-arrow-left"
                @click="hideExplanation"
                class="back-btn"
              ></el-button>
              <h1>{{ activeCard.title }}</h1>
            </div>
          </template>


          <div class="content">
            {{ activeCard.explanation }}
          </div>
        </el-card>
      </div>
    </transition>
  </div>
</template>

<script>

export default {
  name: "ViewB",
  components: {
  },
  data() {
    return {
      activeCard: null,
      carouselHeight: '350px', // 默认两行高度
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
      thirdRowCards: [ // 新增的第三行卡片
        {
          id: 9,
          title: "SQL1",
          icon: "el-icon-pie-chart",
          content: "SQL1",
          explanation: "SQL1说明..."
        },
        {
          id: 10,
          title: "SQL2",
          icon: "el-icon-map-location",
          content: "SQL2",
          explanation: "SQL2说明..."
        },
        {
          id: 11,
          title: "SQL3",
          icon: "el-icon-alarm-clock",
          content: "SQL3",
          explanation: "SQL3说明..."
        },
        {
          id: 12,
          title: "SQL4",
          icon: "el-icon-coin",
          content: "SQL4",
          explanation: "SQL4说明..."
        }
      ],
    };
  },
  methods: {
    showExplanation(card) {
      this.activeCard = card;
    },
    hideExplanation() {
      this.activeCard = null;
    },
  },
};
</script>

<style>
/* 卡片容器 */
.card-container {
  padding: 50px;
  overflow: visible !important;
  position: relative;
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

/* 新增第三行专用高度样式 */
.third-row-card {
  min-height: 300px !important; /* 覆盖原有高度 */
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
  border-bottom: 1px solid #dcdfe6; /* 下边框 */
  border-left: 1px solid #dcdfe6; /* 左边框 */
  border-right: 1px solid #dcdfe6; /* 右边框 */
  border-radius: 0; /* 清除圆角 */
}

  .header h1 {
    margin-left: 10px;
    color: #303133;
    margin-bottom: 0;
    font-size: 20px;
    font-weight: 600;
}

.content {
  border-top: 1px solid #dcdfe6; /* 上边框 */
  border-bottom: 1px solid #dcdfe6; /* 下边框 */
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
  flex: 1;
}
/*按钮*/ 
.back-btn.el-button {
  padding: 8px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #409eff !important;
  color: white;
  margin-right: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  transition: all 0.3s;
}

.back-btn.el-button:hover {
  background: #66b1ff !important;
  transform: scale(1.1);
}

.back-btn.el-button:active {
  background: #3a8ee6 !important;
  transform: scale(0.95);
}

.back-btn.el-button i {
  font-size: 16px;
  margin-right: 0;
}

/*箭头位置*/
.el-carousel__arrow {
  position: absolute !important;
  top: 50% !important;
  transform: translateY(-50%) !important;
  width: 40px !important;
  height: 40px !important;
  font-size: 24px !important;
  background: rgba(184, 208, 232, 0.8) !important;
  border-radius: 50%;
  transition: all 0.3s !important;
  z-index: 9999 !important; /* 确保在最顶层 */
}

.el-carousel__arrow--left.el-carousel__arrow {
  left: 5px !important; 
}

.el-carousel__arrow--right.el-carousel__arrow {
  right: 5px !important;
}

.el-carousel__arrow:hover {
  background: #409EFF !important;
  transform: translateY(-50%) scale(1.1) !important;
}
</style>