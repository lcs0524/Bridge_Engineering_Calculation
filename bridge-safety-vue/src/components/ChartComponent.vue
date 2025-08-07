<template>
  <div ref="chartRef" class="chart-container" :style="{ height: height, width: width }"></div>
</template>

<script setup>
import { 
  ref, 
  onMounted, 
  onBeforeUnmount, 
  watch, 
  shallowRef, 
  getCurrentInstance 
} from 'vue'

// 不再从这里导入 echarts，而是使用全局实例

const { proxy } = getCurrentInstance();

const props = defineProps({
  options: {
    type: Object,
    required: true
  },
  theme: {
    type: String,
    default: 'dark'
  },
  height: {
    type: String,
    default: '100%'
  },
  width: {
    type: String,
    default: '100%'
  }
})

const chartRef = ref(null)
const chartInstance = shallowRef(null)
let resizeObserver = null

// 图表主题配置
const darkTheme = {
  backgroundColor: 'transparent',
  textStyle: {
    color: 'rgba(255, 255, 255, 0.95)',
    fontWeight: 500,
    fontSize: 14
  },
  title: {
    textStyle: {
      color: '#ffffff',
      fontSize: 16,
      fontWeight: 600
    }
  },
  legend: {
    textStyle: {
      color: 'rgba(255, 255, 255, 0.85)'
    }
  },
  tooltip: {
    backgroundColor: 'rgba(17, 24, 39, 0.9)',
    borderColor: '#4b5563',
    textStyle: {
      color: '#ffffff'
    }
  },
  xAxis: {
    axisLine: {
      lineStyle: {
        color: '#4b5563'
      }
    },
    axisTick: {
      lineStyle: {
        color: '#4b5563'
      }
    },
    axisLabel: {
      color: 'rgba(255, 255, 255, 0.85)',
      fontSize: 12
    },
    splitLine: {
      lineStyle: {
        color: 'rgba(75, 85, 99, 0.3)'
      }
    }
  },
  yAxis: {
    axisLine: {
      lineStyle: {
        color: '#4b5563'
      }
    },
    axisTick: {
      lineStyle: {
        color: '#4b5563'
      }
    },
    axisLabel: {
      color: 'rgba(255, 255, 255, 0.85)',
      fontSize: 12
    },
    splitLine: {
      lineStyle: {
        color: 'rgba(75, 85, 99, 0.3)'
      }
    }
  },
  visualMap: {
    textStyle: {
      color: 'rgba(255, 255, 255, 0.85)'
    }
  }
}

// 初始化图表 - 只在 onMounted 中调用一次
const initChart = () => {
  if (chartRef.value) {
    chartInstance.value = proxy.$echarts.init(chartRef.value, props.theme);
    chartInstance.value.setOption(props.options, true);
  }
}

// 调整图表大小
const resizeChart = () => {
  if (chartInstance.value) {
    chartInstance.value.resize();
  }
}

// 监听 options 的变化 - 只更新，不销毁
watch(() => props.options, 
  (newOptions) => {
    if (chartInstance.value && newOptions && Object.keys(newOptions).length > 0) {
      chartInstance.value.setOption(newOptions, true);
    }
  }, 
  { deep: true }
);

// 组件挂载时初始化图表
onMounted(() => {
  if (props.options && Object.keys(props.options).length > 0) {
    initChart();
  }
  if (chartRef.value) {
    proxy.$echarts.registerTheme('dark', darkTheme);
    resizeObserver = new ResizeObserver(resizeChart);
    resizeObserver.observe(chartRef.value);
  }
});

// 组件卸载时销毁图表
onBeforeUnmount(() => {
  if (resizeObserver && chartRef.value) {
    resizeObserver.unobserve(chartRef.value);
  }
  if (chartInstance.value) {
    chartInstance.value.dispose();
    chartInstance.value = null;
  }
});
</script>

<style scoped>
.chart-container {
  /* Basic styling for the chart container */
}
</style> 