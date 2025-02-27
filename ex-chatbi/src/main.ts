import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus';
// import 'element-plus/lib/theme-chalk/index.css';
import 'element-plus/dist/index.css'
import axios from 'axios';

const app = createApp(App)
app.config.globalProperties.$http = axios;
app.use(router)
app.use(ElementPlus);
app.mount('#app')
