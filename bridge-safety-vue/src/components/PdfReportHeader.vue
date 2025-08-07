<template>
  <div class="pdf-header">
    <div class="logo-section">
      <img src="/logo.png" alt="公司Logo" class="pdf-logo" />
      <div class="company-info">
        <h1>吉林省志安科技有限公司</h1>
        <h2>{{ reportTitle }}</h2>
      </div>
    </div>
  </div>
  <div class="pdf-divider"></div>
</template>

<script setup>
defineProps({
  reportTitle: {
    type: String,
    required: true
  }
})
</script>

<style scoped>
/* 样式已在全局CSS中定义 */
</style> 