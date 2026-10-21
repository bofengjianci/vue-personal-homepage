import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import App from './App.vue'
import router from './router'

// 注册 Pinia：createPinia() 创建状态管理实例，全局共享 user/project/article 三个 Store
const app = createApp(App)
app.use(createPinia())
app.use(router)
// 注册 Element Plus 组件库（中文 locale；全量引入，便于实验中查阅各组件文档用法）
app.use(ElementPlus, { locale: zhCn })
app.mount('#app')
