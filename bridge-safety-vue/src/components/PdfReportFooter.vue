<template>
  <div class="pdf-footer">
    <div class="pdf-signature">
      <p><strong>计算日期：</strong>{{ currentDate }}</p>
      <p><strong>报告生成时间：</strong>{{ currentDateTime }}</p>
      <p><strong>技术支持：</strong>吉林省志安科技有限公司</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const currentDate = ref('')
const currentDateTime = ref('')

onMounted(() => {
  // 获取当前日期
  currentDate.value = new Date().toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
  
  // 获取当前日期时间
  currentDateTime.value = new Date().toLocaleString('zh-CN')
})
</script>

<style scoped>
/* 样式已在全局CSS中定义 */
</style> 