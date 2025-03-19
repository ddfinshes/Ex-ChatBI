<template>
  <div class="selectpanel-main">
    <div ref="d3Canvas" class="d3-canvas"></div>

    <el-aside id="selectPanelContainer" width="100%">
    <ViewAVue ref="viewA" style="flex: 1;"/>
    <ViewBVue ref="viewB" style="flex: 1;" @card-hover="handleCardHover"/>
    <ViewCVue style="flex: 1;"/>
    </el-aside>
  </div>
</template>

<script>
import {ref} from "vue";
import axios from "axios";
import {useQueryStore} from "@/stores/query";
import {nextTick} from "vue";
import ViewAVue from "./ViewA.vue";
import ViewBVue from "./ViewB.vue";
import ViewCVue from "./ViewC.vue";
import * as d3 from 'd3';

export default {
  components: {
    ViewAVue,
    ViewBVue,
    ViewCVue,
  },
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
  data() {
    return {
      viewAPositions: null, // 新增坐标存储
      viewBPositions: null,
      d3SVG: null,
      updateInterval: null,
      currentHoveredId: null,
      liners: [1, 2],
    };
  },
  mounted() {
    this.initD3(); // 初始化 D3
    
    this.initConnectionUpdate(); // 增加初始化更新方法调用
    window.addEventListener('resize', this.handleResize);
  },
  beforeDestroy() {
    // 清理 D3 资源
    if (this.d3SVG) {
      this.d3SVG.selectAll("*").remove();
    }
    window.removeEventListener('resize', this.handleResize);
    clearInterval(this.updateInterval);
  },
  methods: {
    // 你可以在这里定义其他方法
    // 初始化 D3 画布
    initD3() {
      this.d3SVG = d3.select(this.$refs.d3Canvas)
        .append('svg')
        .style('position', 'fixed')
        .style('top', 0)
        .style('left', 0)
        .style('width', '100%')
        .style('height', '100%')
        .style('pointer-events', 'none')
        .style('z-index', 9999);
    },

    initConnectionUpdate() {
      const update = () => {
        this.viewAPositions = this.$refs.viewA?.getCardPositions?.() || {};
        this.viewBPositions = this.$refs.viewB?.getCardPositions?.() || {};
        // console.log('Coordinates:', {
        //   userInput: this.viewAPositions?.userInput,
        //   model: this.viewAPositions?.model,
        //   id1: this.viewBPositions?.[1]
        // });
        this.updateConnections();
      };

      // 初始更新
      this.$nextTick(update);
      
      // 设置定时更新
      this.updateInterval = setInterval(update, 100);
    },

    updateConnections() {
      const validatePosition = pos => pos && 
        Number.isFinite(pos.x) && 
        Number.isFinite(pos.y);

      // 新增曲度控制参数（可调整该值改变弯曲程度）
      const CURVATURE = 60;

    // 自定义曲线生成器（使用三次贝塞尔曲线）
      const linkGenerator = (d) => {
      const sx = d.source.x;
      const sy = d.source.y;
      const tx = d.target.x;
      const ty = d.target.y;
      
      // 计算控制点（垂直方向偏移曲度值）
      const cx1 = sx;
      const cy1 = sy + CURVATURE;
      const cx2 = tx;
      const cy2 = ty - CURVATURE;

      return `M ${sx},${sy} C ${cx1},${cy1} ${cx2},${cy2} ${tx},${ty}`;
     };

      // 生成所有连接：每个ID生成两条线
      const connections = [];
      for(let id of this.liners) {
        // UserInput到当前ID的连线
        if(this.viewAPositions?.userInput && this.viewBPositions?.[id]) {
          connections.push({
            source: this.viewAPositions.userInput,
            target: this.viewBPositions[id],
            color: '#5ce9ff',
            opacity: 0.4
          });
        }
        // ModelUnderstanding到当前ID的连线
        if(this.viewAPositions?.model && this.viewBPositions?.[id]) {
          connections.push({
            source: this.viewAPositions.model,
            target: this.viewBPositions[id],
            color: '#5ce9ff',
            opacity: 0.4
          });
        }
      }

      // D3数据绑定
      const paths = this.d3SVG.selectAll('.connection')
    .data(connections.filter(c => 
      validatePosition(c.source) && 
      validatePosition(c.target)
    ));

        // 更新现有元素
    paths.enter()
      .append('path')
      .attr('class', 'connection')
      .merge(paths)
      .attr('d', d => linkGenerator({
        source: d.source, 
      target: d.target
      }))
      .attr('stroke', d => d.color)
      .attr('stroke-opacity', d => d.opacity)
      .attr('fill', 'none')
      .attr('stroke-width', 2);

    // 移除失效元素
    paths.exit().remove();
   },
    handleResize() {
      this.$nextTick(this.updateConnections);
    }
  
  },
  // async sendQuery() {  // 假设从外部传入输入
  //   this.modelResponse = res.data.response.code || JSON.stringify(res.data.response.data);
  //   this.topKSimilar = res.data.top_k_similar || [];
  // }
  computed: {
    response() {
        return this.queryStore.response;
    }
  },
  watch: {
    response(newVal) {
        if (newVal) {

          this.liners = newVal.response.liners;
        }
      }
  }
};
</script>

<style>
/* 可选：添加特定样式 */
/* .selectpanel-main {
  height: 100vh;
} */
.d3-canvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 9999;
}
.connection {
  transition: all 0.3s ease;
}

#selectPanelContainer {
  position: static !important;
  transform: none !important;
  overflow: visible !important;
}

.top-buttons {
  border-bottom: 1px solid #ebf4f5;
  padding-bottom: 15px;
}
</style>
