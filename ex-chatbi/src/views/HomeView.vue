<template>
	<el-container class="home">
		<el-header class="header">
			<el-row type="flex" align="middle">
				<img style="width: 50px; height: 50px" src="@/assets/image/icon.png" alt="..." :fit="`fill`" />
				<span class="header-title">TransBI</span>
			</el-row>
		</el-header>
		<el-container class="body">
			<el-main class="main">
				<el-container id="chat-container">
					<ChatInterfaceVue />
				</el-container>
			</el-main>

			<el-aside class="aside">
				<el-container id="select-container">
					<SelectPanelVue v-if="isDataReady && isDataReady !== null" />
				</el-container>

			</el-aside>
		</el-container>
	</el-container>
</template>

<script>
import ChatInterfaceVue from '../components/ChatInterface.vue'
import SelectPanelVue from '../components/SelectPanel.vue'
import { useQueryStore } from "@/stores/query";
// @ is an alias to /src
export default {
	name: "HomeView",
	components: {
		ChatInterfaceVue,
		SelectPanelVue,
	},
	
	data() {
		return {
			drawer: false,
			direction: "ltr",
			ActionRecord: {
				name: "uncreated",
				action: []
			},
			isDataReady: false, // false

		}
	},
	setup() {
		const queryStore = useQueryStore();
		return { queryStore };
	},
	computed: {
		setIsDataReady() {
			return this.queryStore.isDataReady;
		}
	},
	watch: {
		setIsDataReady(newVal) {
			console.log('监听到新数据:', { newVal,  timestamp: Date.now() });
			this.isDataReady = newVal;
			// this.isDataReady = true;
		}
	},
	methods: {

	},
	mounted() {
		
	}
}
</script>
<style scoped>
.home {
	height: 1351px;
	width: 2048px;
	border: 1px solid #dcdfe6;
}

.body {
	height: 100%;
	width: 100%;
	flex: 1;
	display: flex;
	justify-content: center;
	align-items: center;
}

.header {
	height: 55px;
	width: 100%;
	background-color: #dbf1d5;
	color: rgb(0, 0, 0);
	display: flex;
	align-items: center;
	padding: 0 20px;
}

.main {
	border: 0px;
	margin: 0px;
	margin-top: 0px;
	height: 100%;
	width: 40%;

}

.aside {
	/* display: flex; */
	width: 60%;
	border: 0px;
	margin: 0px;
	margin-top: 40px;
	height: 100%;
}

.header-title {
	font-size: 24px;
	font-weight: bold;
	margin-left: 10px;
}

#select-container {
	height: 99%;
	width: 100%;
	padding: 0px;
	margin-bottom: 20px;
	margin-top: 0px;
	background-color: #ffffff;
	overflow: clip;
	display: flex;
}

#chat-container {
	width: 100%;
	height: 99%;
	padding: 0px;
	margin: 2px;
	/* margin-bottom: 50px; */
	background-color: #ffffff;
	overflow: clip;
	display: flex;
}
</style>
