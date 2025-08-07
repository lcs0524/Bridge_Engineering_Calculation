<template>
  <div class="tower-foundation-visualization">
    <div class="diagram-container">
      <div class="base-image-container">
        <img 
          :src="diagramImage" 
          alt="电线塔基础稳定性计算结果"
          class="base-diagram"
        />
      </div>
      
      <!-- 图例说明 -->
      <div class="legend">
        <div class="legend-item">
          <div class="legend-color success"></div>
          <span>全部验算通过（安全）</span>
        </div>
        <div class="legend-item">
          <div class="legend-color danger"></div>
          <span>存在验算不通过（需调整）</span>
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
import safeImage from '@/assets/images/电线塔基础稳定性计算—安全.jpg';
import unsafeImage from '@/assets/images/电线塔基础稳定性计算—不安全.jpg';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

const props = defineProps({
  bearingCapacityOk: {
    type: Boolean,
    default: false
  },
  overturningOk: {
    type: Boolean,
    default: false
  },
  slidingOk: {
    type: Boolean,
    default: false
  },
  maxPressure: {
    type: String,
    default: '0'
  },
  minPressure: {
    type: String,
    default: '0'
  },
  overturningFactor: {
    type: String,
    default: '0'
  },
  slidingFactor: {
    type: String,
    default: '0'
  }
});

const diagramImage = computed(() => {
  if (props.bearingCapacityOk && props.overturningOk && props.slidingOk) {
    return safeImage;
  } else {
    return unsafeImage;
  }
});

// 获取状态标题
const getStatusTitle = () => {
  const passedCount = [props.bearingCapacityOk, props.overturningOk, props.slidingOk].filter(Boolean).length;
  
  if (passedCount === 3) {
    return '基础稳定性验算：全部通过';
  } else if (passedCount === 0) {
    return '基础稳定性验算：全部不通过';
  } else {
    return `基础稳定性验算：${passedCount}/3 项通过`;
  }
};

// 获取状态类型
const getStatusType = () => {
  if (props.bearingCapacityOk && props.overturningOk && props.slidingOk) {
    return 'success';
  } else if (!props.bearingCapacityOk && !props.overturningOk && !props.slidingOk) {
    return 'error';
  } else {
    return 'warning';
  }
};

// 获取状态描述
const getStatusDescription = () => {
  const results = [];
  
  // 地基承载力验算
  if (props.bearingCapacityOk) {
    results.push(`地基承载力验算通过 (Pmax = ${props.maxPressure} kPa, Pmin = ${props.minPressure} kPa)`);
  } else {
    results.push(`地基承载力验算不通过 (Pmax = ${props.maxPressure} kPa, Pmin = ${props.minPressure} kPa)`);
  }
  
  // 抗倾覆验算
  if (props.overturningOk) {
    results.push(`抗倾覆验算通过 (K = ${props.overturningFactor} ≥ 1.5)`);
  } else {
    results.push(`抗倾覆验算不通过 (K = ${props.overturningFactor} < 1.5)`);
  }
  
  // 抗滑移验算
  if (props.slidingOk) {
    results.push(`抗滑移验算通过 (Kh = ${props.slidingFactor} ≥ 1.3)`);
  } else {
    results.push(`抗滑移验算不通过 (Kh = ${props.slidingFactor} < 1.3)`);
  }
  
  return results.join('；');
};
</script>

<style scoped>
.tower-foundation-visualization {
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