<template>
  <div class="selectpanel-main">
    <el-aside id="selectPanelContainer" width="100%">
    <ViewAVue />
    <ViewBVue />
    <ViewCVue />
    </el-aside>
  </div>
  
</template>
  
  <script>
import { ref } from "vue";
import axios from "axios";
import { useQueryStore } from "@/stores/query";
import { nextTick } from "vue";
import ViewAVue from "./ViewA.vue";
import ViewBVue from "./ViewB.vue";
import ViewCVue from "./ViewC.vue";

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
  data() {
    return {};
  },
  methods: {
    // 你可以在这里定义其他方法

  // async sendQuery() {  // 假设从外部传入输入
  //   this.modelResponse = res.data.response.code || JSON.stringify(res.data.response.data);
  //   this.topKSimilar = res.data.top_k_similar || [];
  // }
};
</script>
  
<style>
/* 可选：添加特定样式 */
.selectpanel-main {
  height: 100vh;
}
#selectPanelContainer {
  position: static !important;
  transform: none !important;
  overflow: visible !important;
}
.top-buttons {
  border-bottom: 1px solid #ebeef5;
  padding-bottom: 15px;
}
</style>
