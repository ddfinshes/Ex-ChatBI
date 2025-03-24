<!-- ViewB.vue -->
<template>
  <div class="view-header">Knowledge Base View</div>
  <div class="view-container" v-if="!activeCard">
    <!-- 左侧大卡片 -->
    <div class="left-carousel" ref="leftCarouselContainer">
      <el-carousel v-if="dynamicCards.length > 0" indicator-position="none" arrow="always" :interval="0"
        height="carouselHeight" :loop="false">
        <el-carousel-item v-for="(page, pageIndex) in chunkedDynamicCards" :key="'left-' + pageIndex">
          <el-row :gutter="60" class="card-row">
            <el-col v-for="(card, index) in page" :key="'left-card-' + pageIndex + '-' + index" :span="12">
              <el-card shadow="hover" class="click-card" @click="showExplanation(card)" :ref="'card-' + card.id">
                <template #header>
                  <div class="card-title">
                    <i :class="card.icon" class="card-icon"></i>
                    {{ card.title }}
                  </div>
                </template>
                <div class="card-content high-content">{{ card.content }}</div>
              </el-card>
            </el-col>
          </el-row>
        </el-carousel-item>
      </el-carousel>
    </div>

    <!-- 右侧小卡片 -->
    <div class="right-carousel" ref="rightCarouselContainer">
      <el-carousel v-if="dynamicSmallCards.length > 0" ref="rightCarousel" indicator-position="none" arrow="always"
        :interval="0" :height="carouselHeight" :loop="false">
        <el-carousel-item v-for="(page, pageIndex) in chunkedSmallCards" :key="'right-' + pageIndex">
          <el-row :gutter="60" class="card-row">
            <el-col v-for="(card, index) in page" :key="'right-card-' + pageIndex + '-' + index" :span="12">
              <el-card shadow="hover" class="click-card" @click="showExplanation(card)" :ref="'card-' + card.id">
                <template #header>
                  <div class="card-title">
                    <i :class="card.icon" class="card-icon"></i>
                    {{ card.title }}
                  </div>
                </template>
                <!-- <div class="card-content">{{ card.content }}</div> -->
                <div class="card-content high-content">{{ card.content }}</div>
              </el-card>
            </el-col>
          </el-row>
        </el-carousel-item>
      </el-carousel>
    </div>
  </div>

  <!-- 解释视图 -->
  <transition name="explanation-slide">
    <div class="viewc-container" v-if="activeCard" :key="activeCard.id">
      <el-card class="fullscreen-card">
        <!-- 使用原本的 header 样式 -->
        <template #header>
          <div class="header">
            <el-button icon="el-icon-arrow-left" @click="hideExplanation" class="back-btn"></el-button>
            <div class="activeCard-title">{{ activeCard.title }}</div>
          </div>
        </template>


        <div class="content">
          <!-- 显示高亮内容 -->
          <div class="highlighted-content" v-html="highlightedExplanation" v-if="!isEditing"></div>

          <el-input type="textarea" :autosize="{ minRows: 10, maxRows: 20 }" v-model="activeCard.explanation"
            placeholder="Please enter an explanation..." resize="none" class="explanation-input"
            v-if="isEditing"></el-input>

          <div class="button-group">
            <el-button type="primary" @click="toggleEdit" v-if="!isEditing">Edit</el-button>
            <el-button type="primary" @click="saveExplanation" v-if="isEditing">Save</el-button>
          </div>
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
      hightLightKB: [], // 高亮的知识库文本内容
      isEditing: false, // 控制编辑状态
      highlightedExplanation: '', // 初始化为空字符串
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
    },

    // highlightText(highlightList) {
    // const contentDivs = document.querySelectorAll('.high-content');

    // if (!contentDivs.length) {
    //   console.warn('未找到任何 .high-content 元素');
    //   return;
    // }

    // contentDivs.forEach(contentDiv => {
    //   let content = contentDiv.innerHTML;

    //   // highlightList.forEach(keyword => {
    //   //   if (keyword && keyword.trim()) {
    //   //     console.log('keyword', keyword)
    //   //     const regex = new RegExp(keyword.trim(), 'gi');
    //   //     content = content.replace(regex, match => `<span class="highlight">${match}</span>`);
    //   //   }
    //   // });
    //   console.log('sql_highlight_knowledges',highlightList);
    //   let understanding_highlightList = highlightList.hightLightKB.understanding_highlight_knowledges;
    //   console.log('understanding_highlightList', understanding_highlightList)
    //   let understanding_bus_highlight_knowledges = understanding_highlightList.bus_highlight_knowledges;
    //   let understanding_sql_highlight_knowledges = understanding_highlightList.sql_highlight_knowledges;

    //   understanding_sql_highlight_knowledges.forEach(keyword => {
    //     if (keyword && keyword.trim()) {
    //       console.log('keyword', keyword)
    //       const regex = new RegExp(keyword.trim(), 'gi');
    //       content = content.replace(regex, match => `<span class="highlight">${match}</span>`);
    //     }
    //   });
    //   understanding_bus_highlight_knowledges.forEach(keyword => {
    //     if (keyword && keyword.trim()) {
    //       console.log('keyword', keyword)
    //       const regex = new RegExp(keyword.trim(), 'gi');
    //       content = content.replace(regex, match => `<span class="highlight">${match}</span>`);
    //     }
    //   });


    //   let query_highlightList = highlightList.hightLightKB.query_highlight_knowledges;
    //   let query_sql_highlight_knowledges = query_highlightList.sql_highlight_knowledges;
    //   let query_bus_highlight_knowledges = query_highlightList.bus_highlight_knowledges;

    //   query_sql_highlight_knowledges.forEach(keyword => {
    //     if (keyword && keyword.trim()) {
    //       console.log('keyword', keyword)
    //       const regex = new RegExp(keyword.trim(), 'gi');
    //       content = content.replace(regex, match => `<span class="highlight">${match}</span>`);
    //     }
    //   });

    //   query_bus_highlight_knowledges.forEach(keyword => {
    //     if (keyword && keyword.trim()) {
    //       console.log('keyword', keyword)
    //       const regex = new RegExp(keyword.trim(), 'gi');
    //       content = content.replace(regex, match => `<span class="highlight">${match}</span>`);
    //     }
    //   });

    //   contentDiv.innerHTML = content;
    // });
    // },
  },
  methods: {
    hideExplanation() {
      this.activeCard = null;
    },
    // 获取卡片坐标的方法
    getCardPositions_right() {
      const positions = {};

      // 获取轮播容器元素
      const container = this.$refs.rightCarouselContainer;
      if (!container) return positions;

      // 获取容器的可视区域边界
      const containerRect = container.getBoundingClientRect();

      // 合并所有动态卡片（右侧）
      const allCards = [
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
    getCardPositions_left() {
      const positions = {};

      // 获取轮播容器元素
      const container = this.$refs.leftCarouselContainer;
      if (!container) return positions;

      // 获取容器的可视区域边界
      const containerRect = container.getBoundingClientRect();

      // 合并所有动态卡片（左侧）
      const allCards = [
        ...this.dynamicCards
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

    // 实现高亮
    highlightText(highlightList) {
      const contentDivs = document.querySelectorAll('.high-content');

      if (!contentDivs.length) {
        console.warn('未找到任何 .high-content 元素');
        return;
      }

      contentDivs.forEach(contentDiv => {
        let content = contentDiv.innerHTML;

        // highlightList.forEach(keyword => {
        //   if (keyword && keyword.trim()) {
        //     console.log('keyword', keyword)
        //     const regex = new RegExp(keyword.trim(), 'gi');
        //     content = content.replace(regex, match => `<span class="highlight">${match}</span>`);
        //   }
        // });
        console.log('sql_highlight_knowledges', highlightList);
        let understanding_highlightList = highlightList.understanding_highlight_knowledges;
        console.log('understanding_highlightList', understanding_highlightList)
        let understanding_bus_highlight_knowledges = understanding_highlightList.bus_highlight_knowledges;
        let understanding_sql_highlight_knowledges = understanding_highlightList.sql_highlight_knowledges;

        understanding_sql_highlight_knowledges.forEach(keyword => {
          if (keyword && keyword.trim()) {
            console.log('keyword', keyword)
            const regex = new RegExp(keyword.trim(), 'gi');
            content = content.replace(regex, match => `<span class="highlight">${match}</span>`);
          }
        });
        understanding_bus_highlight_knowledges.forEach(keyword => {
          if (keyword && keyword.trim()) {
            console.log('keyword', keyword)
            const regex = new RegExp(keyword.trim(), 'gi');
            content = content.replace(regex, match => `<span class="highlight">${match}</span>`);
          }
        });


        let query_highlightList = highlightList.query_highlight_knowledges;
        let query_sql_highlight_knowledges = query_highlightList.sql_highlight_knowledges;
        let query_bus_highlight_knowledges = query_highlightList.bus_highlight_knowledges;

        query_sql_highlight_knowledges.forEach(keyword => {
          if (keyword && keyword.trim()) {
            console.log('keyword', keyword)
            const regex = new RegExp(keyword.trim(), 'gi');
            content = content.replace(regex, match => `<span class="highlight">${match}</span>`);
          }
        });

        query_bus_highlight_knowledges.forEach(keyword => {
          if (keyword && keyword.trim()) {
            console.log('keyword', keyword)
            const regex = new RegExp(keyword.trim(), 'gi');
            content = content.replace(regex, match => `<span class="highlight">${match}</span>`);
          }
        });

        contentDiv.innerHTML = content;
      });
    },
    toggleEdit() {
      this.isEditing = !this.isEditing;
    },
    saveExplanation() {
      this.isEditing = false;
      // 这里可以添加保存逻辑，比如发送到后端
      this.queryStore.setKnowledge(this.activeCard.explanation);
      console.log('Saved explanation:', this.activeCard.explanation);
    },
    showExplanation(card) {
      this.activeCard = card;
      this.isEditing = false; // 默认显示高亮视图
      this.highlightedExplanation = this.getHighlightedExplanation(card.explanation, this.hightLightKB);
    },
    getHighlightedExplanation(explanation, highlightList) {
      let content = explanation || ''; // 确保 explanation 有默认值
      console.log('explanation:', explanation);

      // 防御性获取 allKeywords
      const allKeywords = [
        ...(highlightList.understanding_highlight_knowledges?.bus_highlight_knowledges || []),
        ...(highlightList.understanding_highlight_knowledges?.sql_highlight_knowledges || []),
        ...(highlightList.query_highlight_knowledges?.bus_highlight_knowledges || []),
        ...(highlightList.query_highlight_knowledges?.sql_highlight_knowledges || []),
      ];
      console.log('allKeywords:', allKeywords);

      // 按长度降序排序，避免替换冲突
      allKeywords.sort((a, b) => b.length - a.length);

      // 转义特殊字符的函数
      function escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      }

      // 对每个关键词进行高亮
      allKeywords.forEach(keyword => {
        if (keyword && keyword.trim()) {
          const regex = new RegExp(escapeRegExp(keyword.trim()), 'gi');
          content = content.replace(regex, match => `<span class="highlight">${match}</span>`);
        }
      });

      return content;
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
        const SQLdataLength = newVal.response.list_of_lists[0].length;
        const KnowledgedataLength = newVal.response.list_of_lists[1].length;

        //获取liners
        this.liners_1_1 = newVal.response.liners.query_liners.bus_lines;
        this.liners_1_2 = newVal.response.liners.query_liners.sql_lines;
        this.liners_2_1 = newVal.response.liners.understanding_liners.bus_lines;
        this.liners_2_2 = newVal.response.liners.understanding_liners.sql_lines;
        this.liners_1_2 = this.liners_1_2.map(num => num + KnowledgedataLength);
        this.liners_2_2 = this.liners_2_2.map(num => num + KnowledgedataLength);
        this.mergedBusLines = [...new Set([...this.liners_1_1, ...this.liners_2_1])];
        this.mergedSqlLines = [...new Set([...this.liners_1_2, ...this.liners_2_2])];
        //生成liners卡片
        for (let i = 0; i < this.mergedBusLines.length; i++) {
          this.dynamicCards.push({
            id: this.mergedBusLines[i]-1,
            title: `Knowledge Base ${this.dynamicCards.length + 1}`,
            content: newVal.response.list_of_lists[1][this.mergedBusLines[i]-1],
            explanation: newVal.response.list_of_lists[1][this.mergedBusLines[i]-1]
          });
        }
        for (let i = 0; i < this.mergedSqlLines.length; i++) {
          this.dynamicSmallCards.push({
            id: this.mergedSqlLines[i],
            title: `SQL Knowledge Base ${this.dynamicSmallCards + 1}`,
            content: newVal.response.list_of_lists[0][this.mergedSqlLines[i] - KnowledgedataLength - 1],
            explanation: newVal.response.list_of_lists[0][this.mergedSqlLines[i] - KnowledgedataLength - 1]
          });
        }
        // 创建查重Set
        const mergedBusSet = new Set(this.mergedBusLines);
        const mergedSqlOriginalSet = new Set(
          this.mergedSqlLines.map(num => num - KnowledgedataLength)
        );
        // 生成剩余卡片
        for (let i = 1; i < KnowledgedataLength; i++) {
          if (mergedBusSet.has(i + 1)) continue;
          this.dynamicCards.push({
            id: i,
            title: `Knowledge Base ${this.dynamicCards.length + 1}`,
            content: newVal.response.list_of_lists[1][i],
            explanation: newVal.response.list_of_lists[1][i]
          });
        }
        for (let i = 0; i < SQLdataLength; i++) {
          if (mergedSqlOriginalSet.has(i + 1)) continue;
          this.dynamicSmallCards.push({
            id: KnowledgedataLength + i + 1,
            title: `SQL Knowledge Base ${this.dynamicSmallCards + 1}`,
            content: newVal.response.list_of_lists[0][i],
            explanation: newVal.response.list_of_lists[0][i]
          });
        }
        this.hightLightKB = newVal.response.highlight_knowledges;
        if (this.hightLightKB) {
          // 使用 $nextTick 确保 DOM 更新后再执行高亮
          this.$nextTick(() => {
            this.highlightText(this.hightLightKB);
          });
        }
        console.log('------ViewB modelResponse--------------------', this.modelResponse)

      }
    }
  }
};
</script>

<style>
.view-container {
  display: flex;
  gap: 50px;
  padding: 20px 40px;
}

.left-carousel {
  min-height: 400px;
  flex: 1;
}


.right-carousel {
  min-height: 400px;
  flex: 1;
}

.click-card {
  flex: 1;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 20px;
  min-height: 150px;
  height: 190px;
  /* 根据实际需要调整 */
}

.click-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.el-carousel__container {
  min-height: 400px !important;
}

.card-title {
  font-size: 14px;
  font-weight: 600;
  color: #2d3a4b;
}

.activeCard-title {
  font-size: 14px;
}

.card-content {
  margin-top: 0;
  font-size: 14px;
  padding: 0px;
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
  padding: 0px;
  /* 内边距 */
  background: #dbf1d5;
  /* 背景色 */
  border-top: 1px solid #dcdfe6;
  /* 上边框 */
  border-bottom: 1px solid #dcdfe6;
  /* 下边框 */
  border-left: 1px solid #dcdfe6;
  /* 左边框 */
  border-right: 1px solid #dcdfe6;
  /* 右边框 */
  border-radius: 0;
  /* 清除圆角 */
}

.view-header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  /* 或 center，根据需求调整水平对齐 */
  margin-bottom: 0;
  font-size: 22px;
  font-weight: 550;
  /* 比 bold（700）稍轻，现代感更强 */
  color: #4e4e4e;
  /* 深灰色文字，确保对比度 */
  background: #dbf1d5;
  height: 40px;
  /* 固定高度 */
  padding: 0 15px;
  /* 左右padding增加，上下靠height控制 */
  box-sizing: border-box;
  /* 确保padding不增加总高度 */
  line-height: 1;
  /* 确保文字垂直居中更精确 */
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
  margin-top: 20px;
  width: 150px;
  height: 150px;
}

.explanation-input .el-textarea__inner:focus {
  box-shadow: none;
}

.content {
  padding: 0px;
  background: #ffffff;
  border-radius: 4px;
  height: 300px;
  display: block !important;
  /* 禁用 flex 布局 */
  flex-direction: column;
  position: relative;
  /* 为按钮定位提供参考 */
}

.el-textarea {
  width: 90% !important;
  margin: 0 auto;
  /* 居中对齐 */
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
  z-index: 10 !important;
  /* 确保在最顶层 */
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

.highlighted-content {
  min-height: 200px;
  max-height: 280px;
  overflow-y: auto;
  font-family: monospace;
  line-height: 1.8;
  font-size: 16px;
  white-space: pre-wrap;
  padding: 10px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background: #fff;
}

.button-group {
  margin-top: 10px;
  text-align: right;
}

.highlight {
  background-color: #ffe066;
  padding: 2px 4px;
  border-radius: 3px;
}
</style>