<!-- QueryDisplay.vue -->
<template>
  <el-row type="flex" justify="space-between" style="padding: 10px">
    <!-- User Input Card -->
    <el-col :span="8">
      <el-card shadow="hover" style="width: 180px; margin-right: 10px">
        <div slot="header">User Input</div>
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
        <div
          v-for="(item, index) in topKSimilar"
          :key="'arrow-' + index"
          class="branch-arrow"
          :style="{
            top: index * 60 + 60 + 'px',
            width: '20px',
            height: `${Math.max(2, item.similarity * 10)}px`,
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
</template>
  
  <script>
import { useQueryStore } from "@/stores/query"; // 假设这是你的 Pinia store 路径

export default {
  name: "QueryDisplay",
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
    },
  },
  data() {
    return {
      query: "",
      messageHistory: [],
      modelResponse: "",
      topKSimilar: [],
    };
  },
  watch: {
    currentQuery(newVal) {
      console.log("监听到新查询:", newVal);
      if (newVal) {
        // this.sendQuery(); // 如果需要发送查询，可以在这里实现或通过 emit 通知父组件
      }
    },
    response(newVal) {
      console.log("监听到新响应:", newVal);
      if (newVal) {
        this.modelResponse =
          newVal.response.code || JSON.stringify(newVal.response.data);
        this.topKSimilar = newVal.top_k_similar || [];
        this.messageHistory = newVal.message_history || [];
      }
    },
  },
  methods: {
    // 如果需要发送查询，可以取消注释并实现
    // async sendQuery() {
    //   const res = await someApiCall(this.currentQuery);
    //   this.modelResponse = res.data.response.code || JSON.stringify(res.data.response.data);
    //   this.topKSimilar = res.data.top_k_similar || [];
    // }
  },
};
</script>
  
  <style>
.branch-arrow {
  position: absolute;
  left: -20px;
  width: 20px;
  height: 2px;
  background-color: #000;
}
</style>