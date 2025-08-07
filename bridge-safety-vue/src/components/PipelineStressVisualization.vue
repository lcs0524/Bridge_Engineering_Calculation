<template>
  <div class="pipeline-stress-visualization">
    <div class="diagram-container">
      <div class="base-image-container">
        <img 
          :src="diagramImage" 
          alt="管道强度与变形验算结果"
          class="base-diagram"
        />
      </div>
      
      <!-- 图例说明 -->
      <div class="legend">
        <div class="legend-item">
          <div class="legend-color success"></div>
          <span>验算通过（安全）</span>
        </div>
        <div class="legend-item">
          <div class="legend-color danger"></div>
          <span>验算不通过（需调整）</span>
        </div>
      </div>
      
      <!-- 状态说明 -->
      <div class="status-summary">
        <el-alert
          :title="getStatusTitle()"
          :type="getStatusType()"
          :description="getStatusDescription()"
          show-icon
          :closable="false"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import safeImage from '@/assets/images/路基顶管工程计算-管道强度与变形-安全.jpg';
import unsafeImage from '@/assets/images/路基顶管工程计算-管道强度与变形-不安全.jpg';

const props = defineProps({
  pipeStrengthOk: {
    type: Boolean,
    default: false
  },
  pipeDeformationOk: {
    type: Boolean,
    default: false
  },
  strengthValue: {
    type: String,
    default: '0'
  },
  deformationValue: {
    type: String,
    default: '0'
  }
});

const diagramImage = computed(() => {
  if (props.pipeStrengthOk && props.pipeDeformationOk) {
    return safeImage;
  } else {
    return unsafeImage;
  }
});

// 获取状态标题
const getStatusTitle = () => {
  if (props.pipeStrengthOk && props.pipeDeformationOk) {
    return '管道强度与变形验算：全部通过';
  } else if (!props.pipeStrengthOk && !props.pipeDeformationOk) {
    return '管道强度与变形验算：均不通过';
  } else {
    return '管道强度与变形验算：部分通过';
  }
};

// 获取状态类型
const getStatusType = () => {
  if (props.pipeStrengthOk && props.pipeDeformationOk) {
    return 'success';
  } else if (!props.pipeStrengthOk && !props.pipeDeformationOk) {
    return 'error';
  } else {
    return 'warning';
  }
};

// 获取状态描述
const getStatusDescription = () => {
  const results = [];
  
  if (props.pipeStrengthOk) {
    results.push(`环向应力验算通过 (σ = ${props.strengthValue} MPa)`);
  } else {
    results.push(`环向应力验算不通过 (σ = ${props.strengthValue} MPa)`);
  }
  
  if (props.pipeDeformationOk) {
    results.push(`管体变形验算通过 (S = ${props.deformationValue} mm)`);
  } else {
    results.push(`管体变形验算不通过 (S = ${props.deformationValue} mm)`);
  }
  
  return results.join('；');
};
</script>

<style scoped>
.pipeline-stress-visualization {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

.diagram-container {
  position: relative;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.base-image-container {
  position: relative;
  width: 100%;
  line-height: 0;
}

.base-diagram {
  width: 100%;
  height: auto;
  display: block;
}

.legend {
  display: flex;
  justify-content: center;
  gap: 24px;
  padding: 16px;
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #495057;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 2px;
}

.legend-color.success {
  background-color: #67c23a;
}

.legend-color.danger {
  background-color: #f56c6c;
}

.status-summary {
  padding: 16px;
  background: #f8f9fa;
}

.status-summary :deep(.el-alert) {
  border: none;
  background: transparent;
  padding: 8px 0;
}

.status-summary :deep(.el-alert__content) {
  line-height: 1.5;
}
</style> 