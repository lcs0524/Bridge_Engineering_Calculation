<script setup>
import { ref, onMounted } from 'vue';
import { RouterView, useRouter } from 'vue-router';
import { ElAside, ElContainer, ElMain, ElMenu, ElMenuItem, ElSubMenu, ElIcon } from 'element-plus';
import { Monitor, Files } from '@element-plus/icons-vue';
import SplashScreen from '@/components/SplashScreen.vue'; // 导入启动界面组件

const router = useRouter();
const activeIndex = ref('/');

const handleSelect = (index) => {
  router.push(index);
};

const isLoading = ref(true); // 控制启动界面显示的状态

onMounted(() => {
  // 模拟加载过程
  setTimeout(() => {
    isLoading.value = false;
  }, 3000); // 3秒后隐藏启动界面
});
</script>

<template>
  <!-- 全屏启动动画 -->
  <SplashScreen v-if="isLoading" />

  <!-- 主应用布局 -->
  <el-container v-else class="main-container">
    <el-aside width="260px" class="sidebar-container">
      <div class="logo-container">
        <img alt="Zhi'an Technology Logo" class="logo" src="@/assets/logo.png" />
      </div>
      <el-menu
        :default-active="activeIndex"
        class="el-menu-vertical-demo"
        router
      >
        <el-menu-item index="/">
          <el-icon>
            <Monitor />
          </el-icon>
          <span>工程安全评估与计算软件</span>
        </el-menu-item>
        <el-sub-menu index="/calculation">
          <template #title>
            <el-icon>
              <Files />
            </el-icon>
            <span>安全计算模块</span>
          </template>
          <el-menu-item index="/bridge-settlement">
            桥梁跨越工程计算
          </el-menu-item>
          <el-menu-item index="/roadbed-calculation">
            路基顶管工程计算
          </el-menu-item>
          <el-menu-item index="/foundation-stability">
            电线跨越塔基计算
          </el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>

    <!-- 主内容区 -->
    <el-main class="content-wrapper">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </el-main>
  </el-container>
</template>

<style scoped>
/* 主题变量 */
:root {
  --sidebar-bg: #ffffff;
  --sidebar-text: #374151;
  --sidebar-text-hover: #111827;
  --sidebar-item-active-bg: #eef2ff;
  --sidebar-item-active-text: #3b82f6;
  --main-bg: #f3f4f6;
  --content-bg: #ffffff;
  --border-color: #e5e7eb;
}

.main-container {
  height: 100vh;
  width: 100vw;
  background-color: var(--main-bg);
}

.sidebar-container {
  background-color: var(--sidebar-bg);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  padding: 1rem;
}

.logo-container {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 1rem 0.5rem;
  margin-bottom: 1.5rem;
}

.logo {
  height: 48px;
  width: auto;
  margin-right: 0.75rem;
}

.title {
  font-weight: 600;
  font-size: 1.1rem;
  color: var(--sidebar-text-hover);
}

.el-menu {
  background-color: transparent;
  border-right: none;
  --el-menu-text-color: var(--sidebar-text);
  --el-menu-hover-text-color: var(--sidebar-text-hover);
  --el-menu-bg-color: transparent;
  --el-menu-hover-bg-color: var(--sidebar-item-active-bg);
  --el-menu-active-color: var(--sidebar-item-active-text);
}

.el-menu-item,
.el-sub-menu :deep(.el-sub-menu__title) {
  border-radius: 8px;
  margin-bottom: 0.5rem;
  transition: all 0.2s ease-in-out;
  color: var(--el-menu-text-color);
}

.el-menu-item:hover,
.el-sub-menu :deep(.el-sub-menu__title:hover) {
  background-color: var(--el-menu-hover-bg-color);
  color: var(--el-menu-hover-text-color);
}

.el-menu-item.is-active {
  background-color: var(--sidebar-item-active-bg);
  color: var(--sidebar-item-active-text) !important;
  font-weight: 600;
}

.el-sub-menu.is-active :deep(.el-sub-menu__title) {
  color: var(--sidebar-item-active-text) !important;
}

.el-menu-item .el-icon,
.el-sub-menu .el-icon {
  margin-right: 12px;
  font-size: 1.2rem;
}

.content-wrapper {
  padding: 2rem;
  background-color: var(--main-bg);
  height: 100vh;
  overflow-y: auto;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
