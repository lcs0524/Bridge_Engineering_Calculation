# Vue3项目初始化完整指南

## 环境准备

### 系统要求
- Node.js ≥ 18.0.0
- npm ≥ 9.0.0 或 pnpm ≥ 8.0.0
- Git ≥ 2.30.0
- VS Code + Volar插件

### 开发工具推荐
- **VS Code插件**:
  - Volar (Vue3官方插件)
  - TypeScript Vue Plugin
  - Tailwind CSS IntelliSense
  - Element Plus Snippets
  - Auto Rename Tag

## 项目初始化步骤

### 1. 创建Vue3 + TypeScript项目

```bash
# 使用Vite创建项目
npm create vite@latest bridge-vue-frontend -- --template vue-ts

# 进入项目目录
cd bridge-vue-frontend

# 安装基础依赖
npm install
```

### 2. 安装核心依赖包

```bash
# UI组件库
npm install element-plus @element-plus/icons-vue

# 状态管理
npm install pinia

# 路由
npm install vue-router@4

# HTTP客户端
npm install axios

# 数据可视化
npm install echarts vue-echarts

# CSS框架
npm install -D tailwindcss postcss autoprefixer
npm install -D @tailwindcss/forms @tailwindcss/typography

# 图标库
npm install @iconify/vue

# 工具库
npm install @vueuse/core dayjs

# 开发工具
npm install -D @types/node sass
```

### 3. 配置Tailwind CSS

```bash
# 初始化Tailwind配置
npx tailwindcss init -p
```

**tailwind.config.js**:
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        engineering: {
          orange: '#f59e0b',
          red: '#ef4444',
          green: '#10b981',
          blue: '#3b82f6',
        }
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui'],
        chinese: ['Source Han Sans', 'Noto Sans CJK SC', 'sans-serif'],
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
```

**src/styles/index.css**:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html {
    font-family: 'Inter', 'Source Han Sans', system-ui, sans-serif;
  }
}

@layer components {
  .btn-primary {
    @apply bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-lg transition-colors;
  }
  
  .card {
    @apply bg-white rounded-lg shadow-md border border-gray-200 p-6;
  }
  
  .input-field {
    @apply block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500;
  }
}
```

### 4. 配置Element Plus

**src/plugins/element-plus.ts**:
```typescript
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

export default (app: any) => {
  app.use(ElementPlus, { locale: zhCn })
}
```

### 5. 配置Pinia状态管理

**src/stores/index.ts**:
```typescript
import { createPinia } from 'pinia'

const pinia = createPinia()

export default pinia

// 导出所有store
export * from './modules/settlement'
export * from './modules/pipeline'
export * from './modules/tower'
export * from './modules/export'
```

### 6. 配置Vue Router

**src/router/index.ts**:
```typescript
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue'),
    redirect: '/settlement',
    children: [
      {
        path: '/settlement',
        name: 'SettlementAnalysis',
        component: () => import('@/views/SettlementAnalysisView.vue'),
        meta: { title: '桥梁沉降分析' }
      },
      {
        path: '/pipeline',
        name: 'PipelineAnalysis',
        component: () => import('@/views/PipelineAnalysisView.vue'),
        meta: { title: '路基顶管分析' }
      },
      {
        path: '/tower',
        name: 'TowerAnalysis',
        component: () => import('@/views/TowerAnalysisView.vue'),
        meta: { title: '电线塔基础分析' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
```

### 7. 配置TypeScript

**tsconfig.json**:
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "preserve",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src/**/*.ts", "src/**/*.d.ts", "src/**/*.tsx", "src/**/*.vue"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### 8. 配置Vite

**vite.config.ts**:
```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    rollupOptions: {
      output: {
        manualChunks: {
          'element-plus': ['element-plus'],
          'echarts': ['echarts', 'vue-echarts'],
        },
      },
    },
  },
})
```

### 9. 项目目录结构

```
src/
├── api/                    # API接口
│   ├── settlement.ts
│   ├── pipeline.ts
│   └── tower.ts
├── assets/                 # 静态资源
│   ├── images/
│   ├── icons/
│   └── styles/
├── components/             # 组件
│   ├── common/            # 通用组件
│   ├── charts/            # 图表组件
│   ├── forms/             # 表单组件
│   └── layout/            # 布局组件
├── composables/           # 组合式函数
│   ├── useCalculation.ts
│   ├── useExport.ts
│   └── useTheme.ts
├── router/                # 路由配置
├── stores/                # 状态管理
│   ├── modules/
│   └── index.ts
├── types/                 # 类型定义
│   ├── settlement.d.ts
│   ├── pipeline.d.ts
│   └── tower.d.ts
├── utils/                 # 工具函数
│   ├── request.ts
│   ├── validation.ts
│   └── formatters.ts
├── views/                 # 页面组件
│   ├── SettlementAnalysisView.vue
│   ├── PipelineAnalysisView.vue
│   ├── TowerAnalysisView.vue
│   └── HomeView.vue
├── App.vue
└── main.ts
```

### 10. 主入口文件配置

**src/main.ts**:
```typescript
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import pinia from './stores'
import ElementPlus from './plugins/element-plus'
import './styles/index.css'

const app = createApp(App)

app.use(pinia)
app.use(router)
app.use(ElementPlus)

app.mount('#app')
```

### 11. 环境变量配置

**.env.development**:
```
VITE_API_BASE_URL=http://localhost:5000
VITE_APP_TITLE=桥梁工程安全评估系统
```

**.env.production**:
```
VITE_API_BASE_URL=http://localhost:5000
VITE_APP_TITLE=桥梁工程安全评估系统
```

### 12. 开发脚本配置

**package.json**:
```json
{
  "name": "bridge-vue-frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc && vite build",
    "preview": "vite preview",
    "type-check": "vue-tsc --noEmit",
    "lint": "eslint . --ext .vue,.js,.jsx,.cjs,.mjs,.ts,.tsx,.cts,.mts --fix --ignore-path .gitignore"
  },
  "dependencies": {
    "vue": "^3.3.4",
    "vue-router": "^4.2.4",
    "pinia": "^2.1.6",
    "element-plus": "^2.3.14",
    "@element-plus/icons-vue": "^2.1.0",
    "echarts": "^5.4.3",
    "vue-echarts": "^6.6.1",
    "axios": "^1.5.0",
    "@vueuse/core": "^10.4.1",
    "dayjs": "^1.11.9"
  },
  "devDependencies": {
    "@types/node": "^20.5.9",
    "@vitejs/plugin-vue": "^4.3.4",
    "autoprefixer": "^10.4.15",
    "postcss": "^8.4.29",
    "tailwindcss": "^3.3.3",
    "@tailwindcss/forms": "^0.5.6",
    "@tailwindcss/typography": "^0.5.10",
    "typescript": "^5.0.2",
    "vite": "^4.4.5",
    "vue-tsc": "^1.8.5"
  }
}
```

### 13. 初始化验证

创建基础验证文件确保配置正确：

**src/App.vue**:
```vue
<template>
  <div class="min-h-screen bg-gray-50">
    <router-view />
  </div>
</template>

<script setup lang="ts">
// 基础验证组件
</script>
```

### 14. 启动项目

```bash
# 启动开发服务器
npm run dev

# 访问 http://localhost:5173
```

### 15. 验证安装成功

访问 `http://localhost:5173` 应该能看到Vue3 + TypeScript + Element Plus的基础页面。

## 常见问题解决

### 1. 端口占用
```bash
# 修改端口
npm run dev -- --port 3000
```

### 2. 依赖版本冲突
```bash
# 清理缓存
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### 3. TypeScript类型错误
```bash
# 检查类型
npm run type-check
```

### 4. 构建优化
```bash
# 分析包大小
npm run build -- --analyze
```