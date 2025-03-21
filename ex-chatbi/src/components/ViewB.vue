<!-- ViewB.vue -->
<template>
  <div class="header">Knowledge Base View</div>
  <div class="main-container" v-if="!activeCard">
    <!-- 左侧大卡片 -->
    <div class="left-carousel">
      <el-carousel 
        v-if="dynamicCards.length > 0"
        indicator-position="none"
        arrow="always"
        :interval="0"
        height="carouselHeight"
        :loop="false"
      >
      <el-carousel-item v-for="(page, pageIndex) in chunkedDynamicCards" :key="'left-'+pageIndex">
          <el-row :gutter="60" class="card-row">
            <el-col
              v-for="(card, index) in page"
              :key="'left-card-'+pageIndex+'-'+index"
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
        v-if="dynamicSmallCards.length > 0"
        ref="rightCarousel"
        indicator-position="none"
        arrow="always"
        :interval="0"
        :height="carouselHeight"
        :loop="false"
      >
      <el-carousel-item v-for="(page, pageIndex) in chunkedSmallCards" :key="'right-'+pageIndex">
          <el-row :gutter="60" class="card-row">
            <el-col
              v-for="(card, index) in page"
              :key="'right-card-'+pageIndex+'-'+index"
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
import { useQueryStore } from '@/stores/query';

export default {
  name: "ViewB",
  components: {
  },
    setup() {
      const queryStore = useQueryStore();
      return { queryStore };
    },
  data() {
    return {
      modelResponse: null,
      activeCard: null,
      carouselHeight: '400px', // 默认两行高度
      dynamicCards: [],    // 左侧卡片数据
      dynamicSmallCards: [], // 右侧卡片数据
    };
  },
  computed: {
    response() {
        return this.queryStore.response;
      },
    // 将左侧卡片分页（每页4个）
    chunkedDynamicCards() {
      return this.chunkArray(this.dynamicCards, 4);
    },
    // 将右侧卡片分页（每页4个）
    chunkedSmallCards() {
      return this.chunkArray(this.dynamicSmallCards, 4);
    }
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

      // 合并所有动态卡片（左侧+右侧）
    const allCards = [
      ...this.dynamicCards,
      ...this.dynamicSmallCards
    ];

      // 遍历所有动态生成的卡片
    allCards.forEach(card => {
      const cardRef = this.$refs[`card-${card.id}`];
      if (!cardRef) return;

      // 处理数组类型的ref（ElementUI组件特性）
      const element = Array.isArray(cardRef) 
        ? cardRef[0]?.$el  // 取第一个元素
        : cardRef?.$el;     // 直接获取元素
      
      if (!element) return;

      // 获取卡片位置
      const cardRect = element.getBoundingClientRect();

      // 可见性判断（带容错边界）
      const isVisible = (
        cardRect.top >= containerRect.top - 20 &&
        cardRect.bottom <= containerRect.bottom + 40 &&
        cardRect.left >= containerRect.left - 10 && 
        cardRect.right <= containerRect.right + 10
      );

      if (isVisible) {
        positions[card.id] = {
          x: cardRect.left + cardRect.width / 2,
          y: cardRect.top,
          width: cardRect.width,
          height: cardRect.height
        };
      }
    });

      return positions;
    },
    // 数组分块方法
    chunkArray(arr, chunkSize) {
      return Array.from(
        { length: Math.ceil(arr.length / chunkSize) },
        (_, i) => arr.slice(i * chunkSize, i * chunkSize + chunkSize)
      );
    },
  },
  watch: {
    response(newVal) {
        console.log('监听到新响应1111:', newVal);
        if (newVal) {
          this.modelResponse = newVal.response.list_of_lists[0][1];
          // 清空原有数据
          this.dynamicCards = [];
          this.dynamicSmallCards = [];
          // 获取数据长度
          const dataLength = newVal.response.list_of_lists.length;

          // 生成左侧卡片
          for(let i = 0; i < dataLength; i++) {        
            this.dynamicCards.push({
              id: dataLength + i + 1,
              title: `SQL ${i + 1}`,
              content: newVal.response.list_of_lists[i][1],
              explanation: newVal.response.list_of_lists[i][1]
            });
            this.dynamicSmallCards.push({
            id: i + 1,
            title: `Knowledge Base ${i + 1}`,
            content: newVal.response.list_of_lists[i][0],
            explanation: newVal.response.list_of_lists[i][0]
          });
          }



          console.log(newVal)
          console.log(this.modelResponse)
        }
      }
  }
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


/* 全屏解释视图 */
.header {
  display: flex;
  align-items: center;
  margin-bottom: 0px;
  padding: 10px; /* 内边距 */
  background: #dbf1d5; /* 背景色 */
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