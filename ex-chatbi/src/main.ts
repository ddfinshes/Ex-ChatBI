import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia';
import router from './router'
import ElementPlus from 'element-plus';
// import 'element-plus/lib/theme-chalk/index.css';
import 'element-plus/dist/index.css'
import axios from 'axios';

const app = createApp(App)
const pinia = createPinia();

app.config.globalProperties.$http = axios;
app.use(router)
app.use(ElementPlus);
app.use(pinia);
app.mount('#app')