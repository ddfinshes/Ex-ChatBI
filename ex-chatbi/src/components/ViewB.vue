<!-- ViewB.vue -->
<template>
  <div class="header">View B</div>
  <div class="main-container" v-if="!activeCard">
    <!-- 左侧大卡片 -->
    <div class="left-carousel">
      <el-carousel 
        indicator-position="none"
        arrow="always"
        :interval="0"
        height="carouselHeight"
        :loop="false"
      >
        <!-- 第一页 -->
        <el-carousel-item >
            <el-row :gutter="60" class="card-row">
              <el-col
              v-for="(card, index) in thirdRowCards"
              :key="'first-' + index"
              :span="12"
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
          </el-carousel-item>

            <!-- 第二页 -->
          <el-carousel-item>
            <el-row :gutter="60" class="card-row">
            <el-col
              v-for="(card, index) in fourthRowCards"
              :key="'second-' + index"
              :span="12"
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
          </el-carousel-item>
      </el-carousel>
    </div>

    <!-- 右侧小卡片 -->
    <div class="right-carousel"  ref="rightCarouselContainer">
      <el-carousel 
        ref="rightCarousel"
        indicator-position="none"
        arrow="always"
        :interval="0"
        :height="carouselHeight"
        :loop="false"
      >
            <!-- 第一页 -->
            <el-carousel-item >
            <el-row :gutter="60" class="card-row">
              <el-col
              v-for="(card, index) in firstRowCards"
              :key="'first-' + index"
              :span="12"
            >
            <el-card
                shadow="hover"
                class="click-card"
                @click="showExplanation(card)"
                :ref="'card-' + card.id"
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
          </el-carousel-item>

            <!-- 第二页 -->
          <el-carousel-item>
            <el-row :gutter="60" class="card-row">
            <el-col
              v-for="(card, index) in secondRowCards"
              :key="'second-' + index"
              :span="12"
            >
              <el-card
                shadow="hover"
                class="click-card"
                @click="showExplanation(card)"
                :ref="'card-' + card.id"
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
          </el-carousel-item>
      </el-carousel>
    </div>
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
            <el-input
              type="textarea"
              :autosize="{ minRows: 10, maxRows: 20 }"
              v-model="activeCard.explanation"
              placeholder="请输入解释内容"
              resize="none"
              class="explanation-input"
            ></el-input>
            <el-button 
              type="primary" 
              class="save-btn"
              style="margin-left: auto;"
            >
              Save
            </el-button>
          </div>
        </el-card>
      </div>
    </transition>

</template>

<script>

export default {
  name: "ViewB",
  components: {
  },
  data() {
    return {
      activeCard: null,
      carouselHeight: '400px', // 默认两行高度
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
      fourthRowCards: [ // 新增的第三行卡片
        {
          id: 13,
          title: "SQL5",
          icon: "el-icon-pie-chart",
          content: "SQL5",
          explanation: "SQL5说明..."
        },
        {
          id: 14,
          title: "SQL6",
          icon: "el-icon-map-location",
          content: "SQL6",
          explanation: "SQL6说明..."
        },
        {
          id: 15,
          title: "SQL7",
          icon: "el-icon-alarm-clock",
          content: "SQL7",
          explanation: "SQL7说明..."
        },
        {
          id: 16,
          title: "SQL8",
          icon: "el-icon-coin",
          content: "SQL8",
          explanation: "SQL8说明..."
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
    // 获取卡片坐标的方法
    getCardPositions() {
      const positions = {};
      
      // 获取轮播容器元素
      const container = this.$refs.rightCarouselContainer;
      if (!container) return positions;
      
      // 获取容器的可视区域边界
      const containerRect = container.getBoundingClientRect();
      
      // 遍历所有卡片（ID 1-8）
      for (let id = 1; id <= 8; id++) {
        const cardRef = this.$refs[`card-${id}`];
        if (!cardRef) continue;

        // 获取卡片元素（处理数组引用）
        const element = Array.isArray(cardRef) 
          ? cardRef[0]?.$el 
          : cardRef?.$el;
        if (!element) continue;

        // 获取卡片边界
        const cardRect = element.getBoundingClientRect();
        
        // 判断卡片是否在可视区域内
        const isVisible = (
          cardRect.top >= containerRect.top - 20 && // 允许顶部溢出20px
          cardRect.bottom <= containerRect.bottom + 40 && // 允许底部溢出40px
          cardRect.left >= containerRect.left - 10 && // 允许左侧溢出10px
          cardRect.right <= containerRect.right + 10 // 允许右侧溢出10px
        );  

        if (isVisible) {
          positions[id] = {
            x: cardRect.left + cardRect.width / 2,
            y: cardRect.top
          };
        }
      }
      
      return positions;
    }
  },
};
</script>

<style>
.main-container {
  display: flex;
  gap: 50px;
  padding: 20px 40px;
}

.left-carousel {
  flex: 1;
}


.right-carousel {
  flex: 1;
}

.click-card {
  flex: 1;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 20px;
  min-height: 150px;
  height: 190px; /* 根据实际需要调整 */
}

.click-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.el-carousel__container{
  min-height: 400px !important;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #2d3a4b;
}

.card-content{
  font-size: 15px;
}

.card-icon {
  margin-right: 8px;
  color: #409eff;
}


/* 解释视图 */
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


.explanation-input textarea {
  font-family: monospace;
  line-height: 1.8;
  font-size: 16px;
  white-space: pre-wrap;
  border: none;
  background: transparent;
}
.explanation-input .el-textarea__inner:focus {
  box-shadow: none;
}
.content {
  padding: 0px;
  background: #ffffff;
  border-radius: 4px;
  height: 300px;
  display: block !important; /* 禁用 flex 布局 */
  flex-direction: column;
  position: relative; /* 为按钮定位提供参考 */
}
.el-textarea {
  width: 90% !important;
  margin: 0 auto; /* 居中对齐 */
  height: 90% !important;
}
.save-btn {
  position: absolute;
  right: 20px;
  bottom: 20px;
  padding: 12px 24px;
  font-weight: bold;
  letter-spacing: 1px;
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
  z-index: 10 !important; /* 确保在最顶层 */
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