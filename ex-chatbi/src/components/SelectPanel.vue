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

    <ViewAvue/>
      
      <!-- <el-drawer :visible.sync="drawer" :direction="direction">
        <SelectBar />
      </el-drawer> -->
  </el-aside>
</template>
  
  <script>
  import { ref } from "vue";
  import axios from "axios";
  import { useQueryStore } from '@/stores/query';
  import ViewAvue from './ViewA.vue';
  import { nextTick } from "vue";

  export default {
    name: 'SelectPanel',
    components:{
      ViewAvue
    },
    props: {
      drawer: Boolean,
      direction: String,
      saveLog: Function,
    },
    methods: {
      // async sendQuery() {  // 假设从外部传入输入
      //   this.modelResponse = res.data.response.code || JSON.stringify(res.data.response.data);
      //   this.topKSimilar = res.data.top_k_similar || [];     
      // }       
    },
    hideExplanation() {
      this.activeCard = null;
    },
    // 你可以在这里定义其他方法

  // async sendQuery() {  // 假设从外部传入输入
  //   this.modelResponse = res.data.response.code || JSON.stringify(res.data.response.data);
  //   this.topKSimilar = res.data.top_k_similar || [];
  // }
};
</script>
  
  <style>
  /* 可选：添加特定样式 */
  </style>
