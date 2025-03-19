<!-- QueryDisplay.vue -->
<template>
  <div class="container">
    <div class="header">View A</div>
    <el-row type="flex" justify="space-between" style="padding: 10px">
      <!-- User Input Card -->
      <el-col :span="5" style="display: flex; justify-content: center;">
        <!-- <el-card shadow="hover" style="width: 180px; margin-right: 10px">
          <div slot="header">User Input</div>
          <div style="text-align: left">{{ currentQuery }}</div>
        </el-card> -->

        <el-card ref="userInputCard"
          shadow="hover" 
          style="width: 180px; margin-right: 10px; padding: 0; border: none;"
          body-style="padding: 0;"
        >
          <div slot="header" style="background-color: #909aa3; color: white; padding: 10px; border-radius: 4px 4px 0 0; text-transform: uppercase; text-align: center;">
            User Requirements
          </div>
          <div style="background-color: #ffffff; color: #303133; padding: 10px; text-align: left; border-radius: 0 0 4px 4px; min-height: 40px;">
            {{ currentQuery }}
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="4" style="display: flex; justify-content: center;">
      <div
        class="arrow-connector"
        style="
          position: relative;
          display: flex;
          align-items: center;
          justify-content: center;
          width: 60px;
          justify-content: space-between;
        "
      >
        <!-- 左箭头 -->
        <div
          style="
            width: 0;
            height: 0;
            border-top: 10px solid transparent;
            border-bottom: 10px solid transparent;
            border-right: 16px solid #409EFF;
          "
        ></div>
        
        <!-- 中间圆点 -->
        <div
          style="
            width: 25px;
            height: 25px;
            background-color: #3da59b;
            border-radius: 50%;
          "
        ></div>
        
        <!-- 右箭头 -->
        <div
          style="
            width: 0;
            height: 0;
            border-top: 10px solid transparent;
            border-bottom: 10px solid transparent;
            border-left: 16px solid #409EFF;
          "
        ></div>
      </div>
      </el-col>

      <!-- Model Understanding Card -->
      <el-col :span="5" style="display: flex; justify-content: flex-end;">
        <el-card
          ref="modelUnderstandingCard"
          shadow="hover"
          style="width: 230px; padding: 0; border: none; position: relative;"
          body-style="padding: 0;"
        >
          <div
            slot="header"
            style="background-color: #909aa3; color: white; padding: 10px; border-radius: 4px 4px 0 0; text-transform: uppercase; text-align: center;"
          >
            Model Understanding
          </div>
          <div
            style="background-color: #ffffff; color: #303133; border-radius: 0 0 4px 4px; height: 150px; display: flex; justify-content: center; align-items: center;"
          >
            <el-input
              type="textarea"
              v-model="modelResponse"
              placeholder="Enter your response"
              :rows="5"
              style="width: 100%; max-width: 200px; height: 100%; max-height: 130px;"
            ></el-input>
          <div
            style="background-color: #ffffff; color: #303133; padding: 10px; text-align: left; border-radius: 0 0 4px 4px; min-height: 40px;"
          >
            <p v-html="highlightText(modelResponse, searchtext)"></p>
          </div>

          <!-- Confirm 按钮 -->
          <el-button
            type="primary"
            style="position: absolute; top: 200px; left: 150px;"
            @click="handleConfirm"
            v-show="modelResponse"
          >
            Confirm
          </el-button>

        </div></el-card>
      </el-col>

      <!-- SVG 连接线 -->
      <el-col :span="4" style="position: relative;">
        <svg
          style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;"
          ref="svgContainer"
        >
          <path
            v-for="(item, index) in topKSimilar"
            :key="'line-' + index"
            :d="`M0,${modelCardCenter} Q46,${modelCardCenter} 190,${getCardCenter(index)}`"
            fill="none"
            stroke="#088EA6"
            :stroke-width="getStrokeWidth(item.similarity)"
            stroke-opacity="0.7"
            style="cursor: pointer;"
            @click="handleLineClick(index, $event)"
            @mouseenter="showAddButton(index, $event)"
            @mouseleave="hideAddButton"
          />
        </svg>
        <!-- Unlinking 按钮 -->
        <el-button
          v-for="(item, index) in topKSimilar"
          :key="'unlink-' + index"
          v-show="activeLine === index"
          type="danger"
          size="default"
          style="position: absolute;"
          :style="getButtonPosition(index)"
          @click="handleUnlink(index)"
        >
          Unlinking
        </el-button>
        <!-- 加号按钮 -->
        <img
          src="../assets/image/add.png"
          v-show="showAdd"
          class="add-button"
          style="position: absolute; width: 30px; height: 30px"
          :style="addButtonPosition"
          @click.stop="toggleHistoryWindow"
        />
        <!-- 自定义历史记录窗口 -->
        <div
          v-if="showHistoryWindow"
          class="history-window"
          :style="historyWindowPosition"
          @mouseleave="hideHistoryWindow"
        >
          <el-card shadow="hover" style="width: 300px; max-height: 400px; overflow-y: auto;">
            <div slot="header" class="clearfix">
              <span>History Questions</span>
              <el-button style="float: right;" type="text" @click="hideHistoryWindow">Close</el-button>
            </div>
            <el-checkbox-group v-model="selectedHistory">
              <el-checkbox
                v-for="(historyItem, idx) in historyList"
                :key="idx"
                :label="historyItem.query"
                style="display: block; margin: 5px 0;"
              >
                {{ historyItem.query }} ({{ historyItem.similarity.toFixed(2) }})
              </el-checkbox>
            </el-checkbox-group>
            <el-button type="primary" size="small" @click="addSelectedHistory" style="margin-top: 10px;">
              Add Selected
            </el-button>
          </el-card>
        </div>
      </el-col>

      <!-- Communication History Card -->
      <el-col :span="6" style="display: flex; justify-content: flex-start;">
        <el-card
          shadow="hover"
          style="width: 230px; padding: 0; border: none; position: relative;"
          body-style="padding: 0;"
        >
          <div
            slot="header"
            style="background-color: #909aa3; color: white; padding: 10px; border-radius: 4px 4px 0 0; text-transform: uppercase; text-align: center;"
          >
            Communication History
          </div>
          <div style="position: relative; text-align: center;">
            <!-- 内部卡片 -->
            <el-collapse v-model="activeNames">
              <el-collapse-item
                v-for="(item, index) in topKSimilar"
                :key="index"
                :name="index.toString()"
                :ref="'card-' + index"
                :title="truncateText(item.query, 20)"
                :style="{
                  width: '200px',
                  marginTop: index === 0 ? '20px' : '10px',
                  display: 'inline-block',
                  position: 'relative'
                }"
              >
                <!-- 展开时显示的完整内容 -->
                <div style="padding: 10px;">
                  <div>{{ item.query }}</div>
                  <div>Similarity: {{ item.similarity.toFixed(2) }}</div>
                </div>
              </el-collapse-item>
            </el-collapse>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
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
        highlight: [],
        searchtext:[],
        topKSimilar: [{ similarity: 0.95, query: "What is AI?" },
            { similarity: 0.85, query: "How does AI work?" },
            { similarity: 0.65, query: "AI applications" },
            { similarity: 0.40, query: "Machine learning basics" }],
        // 测试用
        historyList:[{ similarity: 0.95, query: "What is aaaaaaa?" },
            { similarity: 0.85, query: "How does aaaaaaa work?" },
            { similarity: 0.65, query: "aaaaaa applications" },
            { similarity: 0.40, query: "aaaaaa basics" }],
        modelCardCenter: 50, // 默认值，避免初始渲染问题
        cardCenters: [],
        activeLine: null, // 当前激活的线索引
        buttonPositions: [],
        showAdd: false,
        addButtonPosition: { left: '50px', top: '50px' },
        addTimeout: null,
        showHistoryWindow: false,
        historyWindowPosition: { left: '60px', top: '60px' },
        selectedHistory: []
      };
    },
    mounted() {
      this.updateCardCenters();
      document.addEventListener('contextmenu', this.handleOutsideRightClick);
    },
    beforeDestroy() {
      // 移除事件监听，避免内存泄漏
      document.removeEventListener('contextmenu', this.handleOutsideRightClick);
    },
    updated() {
      this.updateCardCenters(); // 当数据更新时重新计算高度
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
          // this.topKSimilar = newVal.top_k_similar || [];
          this.topKSimilar = [{ similarity: 0.95, query: "What is AI?" },
            { similarity: 0.85, query: "How does AI work?" },
            { similarity: 0.65, query: "AI applications" },
            { similarity: 0.40, query: "Machine learning basics" }]
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
      //获取元素底部中心坐标
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
      },

      updateCardCenters() {
        this.$nextTick(() => {
          // 获取 Model Understanding 卡片的中心高度
          const modelCardEl = this.$refs.modelUnderstandingCard.$el;
          const modelRect = modelCardEl.getBoundingClientRect();
          this.modelCardCenter = modelCardEl.offsetTop + modelRect.height / 2;

          // 获取 Communication History 子卡片的中心高度
          console.log(this.topKSimilar)
          this.cardCenters = this.topKSimilar.map((_, index) => {
            const cardEl = this.$refs[`card-${index}`][0].$el;
            const rect = cardEl.getBoundingClientRect();
            return cardEl.offsetTop + 44 + rect.height / 2; // 减去 padding: 10px
          });
        });
      },
      getCardCenter(index) {
        return this.cardCenters[index] || 50 + index * 80; // 默认值避免未加载
      },
      getStrokeWidth(similarity) {
        return Math.max(1, similarity * 20); // 粗细范围 1px 至 5px
      },
      handleConfirm() {
        console.log("Confirmed value:", this.modelResponse);
      },
      truncateText(text, maxLength) {
        // 截断文本，超过 maxLength 显示省略号
        if (text.length > maxLength) {
          console.log(text.substring(0, maxLength) + "...")
          return text.substring(0, maxLength) + "...";
        }
        return text;
      },
      handleLineClick(index, event) {
        this.activeLine = this.activeLine === index ? null : index; // 切换显示
        if (this.activeLine === index) {
          // 计算按钮位置（基于点击事件坐标）
          const svgRect = this.$refs.svgContainer.getBoundingClientRect();
          this.buttonPositions[index] = {
            left: `${event.clientX - svgRect.left - 30}px`, // 偏移调整
            top: `${event.clientY - svgRect.top - 10}px`
          };
        }
      },
      getButtonPosition(index) {
        return this.buttonPositions[index] || { left: '50px', top: '50px' }; // 默认位置
      },
      handleUnlink(index) {
        console.log(`Unlinking line ${index}`);
        // 示例：移除该线对应的项
        this.topKSimilar.splice(index, 1);
        this.cardCenters.splice(index, 1);
        this.activeLine = null;
        this.updateCardCenters()
      },
      handleOutsideRightClick(event) {
        // 阻止默认右键菜单
        event.preventDefault();

        // 检查点击是否在 <path> 或按钮之外
        const svg = this.$refs.svgContainer;
        const paths = svg.querySelectorAll('path');
        const buttons = this.$el.querySelectorAll('.el-button');
        const isClickOnPath = Array.from(paths).some(path => path.contains(event.target));
        const isClickOnButton = Array.from(buttons).some(button => button.contains(event.target));

        if (!isClickOnPath && !isClickOnButton && this.activeLine !== null) {
          this.activeLine = null; // 隐藏按钮
        }
      },
      showAddButton(index, event) {
        clearTimeout(this.addTimeout); // 清除之前的隐藏定时器
        this.showAdd = true;
        const svgRect = this.$refs.svgContainer.getBoundingClientRect();

        this.addButtonPosition = {
          left: '80px', // 居中调整
          top: '220px'
        };
      },
      hideAddButton() {
        this.addTimeout = setTimeout(() => {
          this.showAdd = false;
        }, 2000);
      },
      toggleHistoryWindow() {
        this.showHistoryWindow = !this.showHistoryWindow;
        if (this.showHistoryWindow) {
          this.historyWindowPosition = {
            left: `${parseInt(this.addButtonPosition.left) + 20}px`, // 加号右侧
            top: this.addButtonPosition.top
          };
          this.selectedHistory = [];
          clearTimeout(this.addTimeout); // 保持加号可见
        }
      },
      hideHistoryWindow() {
        this.showHistoryWindow = false;
        this.showAdd = false; // 同时隐藏加号
      },
      addSelectedHistory() {
        const newItems = this.historyList
          .filter(item => this.selectedHistory.includes(item.query))
          .map(item => ({ ...item }));
        this.topKSimilar.push(...newItems);
        this.cardCenters.push(...newItems.map((_, i) => 50 + (this.topKSimilar.length - newItems.length + i) * 80));
        this.showHistoryWindow = false;
        this.showAdd = false;
        this.updateCardCenters()
      }
    }
  };
  </script>
  
  <style>
  .header {
    background-color: #AEC6EA;
    /* 设置背景颜色 */
    padding: 10px;
    text-align: center;
    font-size: 18px;
    font-weight: bold;
  }
  .el-collapse-item__header {
    background-color: #f5f5f5 !important;
    padding: 10px !important;
    height: 40px;
    line-height: 40px;
  }
  .el-collapse-item__content {
    background-color: #f9f9f9;
    border-radius: 0 0 4px 4px;
  }

  .history-window {
    position: absolute;
    z-index: 20;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  }
  .clearfix:after {
    content: '';
    display: table;
    clear: both;
  }
div[contenteditable] {
border: 1px solid #ccc;
padding: 8px;
min-height: 40px;
}

  .highlight {


  background-color: yellow;


}
  </style>
