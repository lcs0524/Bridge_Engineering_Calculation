<template>
  <div class="splash-screen">
    <svg class="grid-pattern" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
          <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#e5e7eb" stroke-width="0.5"/>
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#grid)" />
    </svg>
    <div class="splash-content">
      <img src="../../logo.png" alt="吉林省志安科技有限公司 Logo" class="splash-logo" />
      <h1 class="splash-title">工程安全评估与计算软件</h1>
      <div class="spinner-container">
        <div class="spinner"></div>
        <p class="splash-loading">正在加载, 请稍候...</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.splash-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: var(--brand-white, #ffffff);
  z-index: 9999;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  overflow: hidden;
}

.grid-pattern {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.splash-content {
  text-align: center;
  padding: 2rem;
  position: relative;
  z-index: 2;
}

.splash-logo {
  max-width: 450px;
  width: 100%;
  height: auto;
  margin-bottom: 2.5rem;
}

.splash-title {
  font-size: 2.25rem;
  font-weight: 600;
  color: var(--text-primary, #1e293b);
  margin-bottom: 2rem;
}

.spinner-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid var(--brand-primary-light, #dbeafe);
  border-top-color: var(--brand-primary, #3b82f6);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.splash-loading {
  font-size: 1.1rem;
  color: var(--text-secondary, #64748b);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style> 