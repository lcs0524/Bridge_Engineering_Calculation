<template>
  <div class="pipeline-stability-visualization">
    <div class="diagram-container">
      <div class="base-image-container">
        <img 
          :src="diagramImage" 
          alt="稳定性综合验算结果"
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
import bothOkImage from '@/assets/images/路基顶管工程计算-稳定性综合验算—管道承压通过—后背墙滑移稳定性通过.jpg';
import pressureOkImage from '@/assets/images/路基顶管工程计算-稳定性综合验算—管道承压通过—后背墙滑移稳定性不通过.jpg';
import stabilityOkImage from '@/assets/images/路基顶管工程计算-稳定性综合验算—管道承压不通过—后背墙滑移稳定性通过.jpg';
import bothFailImage from '@/assets/images/路基顶管工程计算-稳定性综合验算—管道承压不通过—后背墙滑移稳定性不通过.jpg';

const props = defineProps({
  pipePressureCheckOk: {
    type: Boolean,
    default: false
  },
  backWallStabilityCheckOk: {
    type: Boolean,
    default: false
  },
  totalPushForce: {
    type: String,
    default: '0'
  },
  pipeMaxPressureCapacity: {
    type: String,
    default: '0'
  },
  backWallTotalResistance: {
    type: String,
    default: '0'
  }
});

const diagramImage = computed(() => {
  if (props.pipePressureCheckOk && props.backWallStabilityCheckOk) {
    return bothOkImage;
  } else if (props.pipePressureCheckOk && !props.backWallStabilityCheckOk) {
    return pressureOkImage;
  } else if (!props.pipePressureCheckOk && props.backWallStabilityCheckOk) {
    return stabilityOkImage;
  } else {
    return bothFailImage;
  }
});

// 获取状态标题
const getStatusTitle = () => {
  if (props.pipePressureCheckOk && props.backWallStabilityCheckOk) {
    return '稳定性综合验算：全部通过';
  } else if (!props.pipePressureCheckOk && !props.backWallStabilityCheckOk) {
    return '稳定性综合验算：均不通过';
  } else {
    return '稳定性综合验算：部分通过';
  }
};

// 获取状态类型
const getStatusType = () => {
  if (props.pipePressureCheckOk && props.backWallStabilityCheckOk) {
    return 'success';
  } else if (!props.pipePressureCheckOk && !props.backWallStabilityCheckOk) {
    return 'error';
  } else {
    return 'warning';
  }
};

// 获取状态描述
const getStatusDescription = () => {
  const results = [];
  
  if (props.pipePressureCheckOk) {
    results.push(`管道承压能力验算通过 (F = ${props.totalPushForce} kN ≤ ${props.pipeMaxPressureCapacity} kN)`);
  } else {
    results.push(`管道承压能力验算不通过 (F = ${props.totalPushForce} kN > ${props.pipeMaxPressureCapacity} kN)`);
  }
  
  if (props.backWallStabilityCheckOk) {
    results.push(`后背墙抗滑移验算通过 (F = ${props.totalPushForce} kN ≤ ${props.backWallTotalResistance} kN)`);
  } else {
    results.push(`后背墙抗滑移验算不通过 (F = ${props.totalPushForce} kN > ${props.backWallTotalResistance} kN)`);
  }
  
  return results.join('；');
};
</script>

<style scoped>
.pipeline-stability-visualization {
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