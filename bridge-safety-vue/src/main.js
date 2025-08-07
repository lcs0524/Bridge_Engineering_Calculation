import './assets/main.css'
import './assets/element-plus-override.css';

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 导入PDF报告组件
import PdfReportHeader from './components/PdfReportHeader.vue'
import PdfReportFooter from './components/PdfReportFooter.vue'

// 关键改动：全量引入 ECharts，而不是按需引入
import * as echarts from 'echarts';
// 通过副作用导入来注册`echarts-gl`的图表（包括 ContourChart）
import 'echarts-gl';


const app = createApp(App)

app.use(router)
app.use(ElementPlus)
app.config.globalProperties.$echarts = echarts

// 注册PDF报告组件
app.component('PdfReportHeader', PdfReportHeader)
app.component('PdfReportFooter', PdfReportFooter)

app.mount('#app')
