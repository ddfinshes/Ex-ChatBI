<template>
	<el-container class="home">
		<el-header
			id="headerContainer"
			height="87px">
			<el-row>
				<img
					style="width: 72px; height: 72px"
					src="@/assets/image/icon.png"
					alt="..."
					:fit="`fill`" />
				<span style="font-weight: bold; padding-left: 10px">TransBI</span>
			</el-row>
		</el-header>
		<el-container class="body">
			<el-main id="mainContainer">
				<el-container id="DBPanelContainerFather">
					<el-main id="mainView">
						<el-row :gutter="20">
							<el-col :span="22">
								<ChatInterfaceVue />
							</el-col>
						</el-row>
					</el-main>
				</el-container>
			</el-main>

			<el-aside
				id="selectPanelContainer"
				width="905px">
				<SelectPanelVue/>
			</el-aside>
		</el-container>
	</el-container>
</template>

<script>
import ChatInterfaceVue from '../components/ChatInterface.vue'
import SelectPanelVue from '../components/SelectPanel.vue'

// @ is an alias to /src
export default {
	name: "HomeView",
	components: {
		ChatInterfaceVue,
		SelectPanelVue
	},
	data() {
		return {
			drawer: false,
			direction: "ltr",
			ActionRecord: {
				name: "uncreated",
				action: []
			}
		}
	},
	methods: {
		
	},
	mounted() {
		
	}
}
</script>
<style>
#mainView {
	height: auto;
	width: auto;
	padding: 0%;
}
#headerContainer {
	height: 87px;
	background-color: #515151;
	font: bold large 94px inter;
	font-size: 64px;
	color: white;
}
#selectPanelContainer {
	height: 1352px;
	background-color: #f5f5f5;
}
#DBPanelContainer {
	height: 1352px;
	background-color: #f3f3f3;
}

#mainContainer {
	height: 1352px;
	width: 2455px;
	padding: 0px;
	overflow: clip;
}
#DBPanelContainerFather {
	background-color: #f3f3f3;
	padding: 0%;
}

/* .body {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
} */


</style>
