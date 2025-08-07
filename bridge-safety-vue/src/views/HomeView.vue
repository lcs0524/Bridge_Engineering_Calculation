<template>
  <div class="home-view">
    <div class="welcome-container">
      <h2 class="welcome-title">欢迎使用桥梁路线工程综合安全评估软件</h2>
      <p class="welcome-subtitle">
        本软件致力于提供精确、高效的工程安全计算与分析功能。请从左侧菜单选择功能模块开始使用。
      </p>
    </div>
    
    <el-row :gutter="24" class="feature-cards">
      <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8" v-for="feature in features" :key="feature.title" class="feature-col">
          <div class="feature-card" @click="navigateTo(feature.path)">
            <div class="card-header">
              <el-icon :size="32" class="card-icon" :class="feature.colorClass"><component :is="feature.icon" /></el-icon>
            </div>
            <div class="card-content">
              <h3>{{ feature.title }}</h3>
              <p>{{ feature.description }}</p>
            </div>
          </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { shallowRef } from 'vue'
import { useRouter } from 'vue-router'
import { Histogram, Connection, Odometer } from '@element-plus/icons-vue'

const router = useRouter()

const features = shallowRef([
  {
    title: '桥梁沉降分析',
    description: '计算桥梁在不同荷载与地质条件下的沉降情况，评估结构长期稳定性。',
    icon: Histogram,
    path: '/bridge-settlement',
    colorClass: 'icon-blue'
  },
  {
    title: '路基顶管计算',
    description: '精确计算管道顶进力与预期沉降量，为路基施工提供科学依据。',
    icon: Connection,
    path: '/roadbed-calculation',
    colorClass: 'icon-red'
  },
  {
    title: '塔基稳定性分析',
    description: '评估电缆塔基在各种复杂荷载下的地基承载力与整体稳定性。',
    icon: Odometer,
    path: '/foundation-stability',
    colorClass: 'icon-blue-dark'
  }
])

const navigateTo = (path) => {
  if (path) {
    router.push(path)
  }
}
</script>

<style scoped>
.home-view {
  width: 100%;
  display: flex;
  flex-direction: column;
}

.welcome-container {
  text-align: center;
  padding: 3rem 2rem;
  background-color: var(--brand-white);
  border-radius: 12px;
  margin-bottom: 2rem;
  border: 1px solid var(--el-border-color-light);
}

.welcome-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.welcome-subtitle {
  font-size: 1.125rem;
  color: var(--text-secondary);
  margin: 0 auto;
}

.feature-cards {
  width: 100%;
}

.feature-col {
  margin-bottom: 1.5rem;
}

.feature-card {
  background-color: var(--brand-white);
  border-radius: 12px;
  padding: 2rem;
  height: 100%;
  min-height: 250px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid var(--el-border-color-light);
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--el-box-shadow-light);
  border-color: var(--brand-primary);
}

.card-header {
  margin-bottom: 1.5rem;
}

.card-icon {
  padding: 18px;
  border-radius: 50%;
  background-color: #f0f2f5;
  color: var(--brand-primary);
}

.icon-blue {
  background-color: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}
.icon-red {
  background-color: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}
.icon-blue-dark {
   background-color: rgba(29, 78, 216, 0.1);
   color: #1d4ed8;
}

.feature-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.feature-card p {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.6;
}
</style> 