# Vue3组件开发规范文档

## 组件设计原则

### 1. 单一职责原则
每个组件应该专注于一个特定的功能，保持简洁和可维护性。

### 2. 可复用性
通过props和slots实现组件的高度可配置性。

### 3. 类型安全
所有组件使用TypeScript定义props和emits。

### 4. 响应式设计
确保组件在不同屏幕尺寸下都能良好显示。

## 原子组件开发

### 1. 基础输入组件

#### NumberInput.vue
```vue
<template>
  <div class="form-field">
    <label v-if="label" class="block text-sm font-medium mb-1">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    <div class="relative">
      <el-input-number
        v-model="internalValue"
        :min="min"
        :max="max"
        :step="step"
        :precision="precision"
        :disabled="disabled"
        :placeholder="placeholder"
        class="w-full"
        @change="handleChange"
      />
      <span v-if="unit" class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 text-sm">
        {{ unit }}
      </span>
    </div>
    <p v-if="error" class="mt-1 text-sm text-red-600">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
interface Props {
  modelValue: number
  label?: string
  min?: number
  max?: number
  step?: number
  precision?: number
  disabled?: boolean
  required?: boolean
  unit?: string
  placeholder?: string
  error?: string
}

interface Emits {
  'update:modelValue': [value: number]
  change: [value: number]
}

const props = withDefaults(defineProps<Props>(), {
  min: -Infinity,
  max: Infinity,
  step: 1,
  precision: 2,
  disabled: false,
  required: false
})

const emit = defineEmits<Emits>()

const internalValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const handleChange = (value: number) => {
  emit('change', value)
}
</script>
```

#### SelectField.vue
```vue
<template>
  <div class="form-field">
    <label v-if="label" class="block text-sm font-medium mb-1">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    <el-select
      v-model="internalValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :clearable="clearable"
      class="w-full"
      @change="handleChange"
    >
      <el-option
        v-for="option in options"
        :key="option.value"
        :label="option.label"
        :value="option.value"
        :disabled="option.disabled"
      />
    </el-select>
    <p v-if="error" class="mt-1 text-sm text-red-600">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
interface Option {
  label: string
  value: string | number
  disabled?: boolean
}

interface Props {
  modelValue: string | number
  label?: string
  options: Option[]
  placeholder?: string
  disabled?: boolean
  required?: boolean
  clearable?: boolean
  error?: string
}

interface Emits {
  'update:modelValue': [value: string | number]
  change: [value: string | number]
}

const props = withDefaults(defineProps<Props>(), {
  clearable: true
})

const emit = defineEmits<Emits>()

const internalValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const handleChange = (value: string | number) => {
  emit('change', value)
}
</script>
```

### 2. 图表组件

#### SettlementChart.vue
```vue
<template>
  <div class="chart-container">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-lg font-semibold">{{ title }}</h3>
      <div class="flex gap-2">
        <el-button size="small" @click="exportChart">导出</el-button>
        <el-button size="small" @click="toggleFullscreen">
          <el-icon>
            <FullScreen v-if="!isFullscreen" />
            <Close v-else />
          </el-icon>
        </el-button>
      </div>
    </div>
    
    <div ref="chartRef" class="chart-wrapper" :style="{ height: chartHeight + 'px' }" />
    
    <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-white/80">
      <el-loading :loading="loading" text="加载中..." />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import type { EChartsOption } from 'echarts'

interface Props {
  title: string
  data: any[]
  type: 'contour' | 'radar' | 'waterfall'
  loading?: boolean
  chartHeight?: number
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  chartHeight: 400
})

const emit = defineEmits<{
  export: []
  fullscreen: [isFullscreen: boolean]
}>()

const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null
const isFullscreen = ref(false)

const initChart = () => {
  if (!chartRef.value) return
  
  chart = echarts.init(chartRef.value)
  updateChart()
}

const updateChart = () => {
  if (!chart) return
  
  const option: EChartsOption = getChartOption()
  chart.setOption(option)
}

const getChartOption = (): EChartsOption => {
  switch (props.type) {
    case 'contour':
      return getContourOption()
    case 'radar':
      return getRadarOption()
    case 'waterfall':
      return getWaterfallOption()
    default:
      return {}
  }
}

const getContourOption = (): EChartsOption => {
  // 等高线图配置
  return {
    title: { text: props.title, left: 'center' },
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}mm'
    },
    visualMap: {
      min: 0,
      max: 100,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: 0,
      inRange: {
        color: ['#10b981', '#f59e0b', '#ef4444']
      }
    },
    series: [{
      type: 'heatmap',
      data: props.data,
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  }
}

const getRadarOption = (): EChartsOption => {
  // 雷达图配置
  return {
    title: { text: props.title, left: 'center' },
    radar: {
      indicator: [
        { name: '沉降值', max: 100 },
        { name: '安全系数', max: 100 },
        { name: '影响范围', max: 100 },
        { name: '经济性', max: 100 },
        { name: '施工难度', max: 100 }
      ]
    },
    series: [{
      type: 'radar',
      data: [{
        value: props.data,
        name: '当前方案'
      }]
    }]
  }
}

const getWaterfallOption = (): EChartsOption => {
  // 瀑布图配置
  return {
    title: { text: props.title, left: 'center' },
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: props.data.map((_, index) => `点${index + 1}`)
    },
    yAxis: { type: 'value', name: '沉降量 (mm)' },
    series: [{
      type: 'bar',
      data: props.data,
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#3b82f6' },
          { offset: 1, color: '#1e3a8a' }
        ])
      }
    }]
  }
}

const exportChart = () => {
  if (chart) {
    const url = chart.getDataURL({
      type: 'png',
      pixelRatio: 2,
      backgroundColor: '#fff'
    })
    const link = document.createElement('a')
    link.download = `${props.title}.png`
    link.href = url
    link.click()
  }
  emit('export')
}

const toggleFullscreen = () => {
  isFullscreen.value = !isFullscreen.value
  emit('fullscreen', isFullscreen.value)
  
  setTimeout(() => {
    chart?.resize()
  }, 100)
}

const resize = () => {
  chart?.resize()
}

onMounted(() => {
  initChart()
})

watch(() => props.data, updateChart, { deep: true })

defineExpose({ resize })
</script>
```

## 复合组件开发

### 1. 参数表单组件

#### SettlementForm.vue
```vue
<template>
  <div class="space-y-6">
    <!-- 项目信息 -->
    <Card title="项目信息">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <TextInput
          v-model="form.projectName"
          label="项目名称"
          placeholder="请输入项目名称"
          required
        />
        <SelectField
          v-model="form.roadLevel"
          label="路线等级"
          :options="roadLevelOptions"
          required
        />
      </div>
    </Card>

    <!-- 桩参数 -->
    <Card title="桩基础参数">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <PileParameters
          v-model="form.pile1"
          title="桩1参数"
          :index="1"
        />
        <PileParameters
          v-model="form.pile2"
          title="桩2参数"
          :index="2"
        />
      </div>
    </Card>

    <!-- 道路参数 -->
    <Card title="道路参数">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <NumberInput
          v-model="form.roadParams.width"
          label="路基宽度"
          unit="m"
          :min="1"
          :max="50"
          required
        />
        <NumberInput
          v-model="form.roadParams.pile1Distance"
          label="桩1距路基距离"
          unit="m"
          :min="0"
          required
        />
        <NumberInput
          v-model="form.roadParams.pile2Distance"
          label="桩2距路基距离"
          unit="m"
          :min="0"
          required
        />
      </div>
    </Card>

    <!-- 土层参数 -->
    <Card title="土层参数">
      <SoilLayerEditor v-model="form.soilLayers" />
    </Card>

    <!-- 操作按钮 -->
    <div class="flex justify-end gap-4">
      <el-button @click="resetForm">重置</el-button>
      <el-button type="primary" :loading="calculating" @click="handleCalculate">
        开始计算
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import type { SettlementParams } from '@/types/settlement'

interface Props {
  modelValue: SettlementParams
}

interface Emits {
  'update:modelValue': [value: SettlementParams]
  calculate: [params: SettlementParams]
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const calculating = ref(false)

const form = reactive(props.modelValue)

const roadLevelOptions = [
  { label: '高速公路', value: '高速公路' },
  { label: '一级公路', value: '一级公路' },
  { label: '二级公路', value: '二级公路' },
  { label: '三级公路', value: '三级公路' },
  { label: '四级公路', value: '四级公路' }
]

const resetForm = () => {
  Object.assign(form, {
    projectName: '',
    roadLevel: '一级公路',
    pile1: { diameter: 1.2, length: 15, load: 2000 },
    pile2: { diameter: 1.0, length: 12, load: 1800 },
    roadParams: { width: 12, pile1Distance: 5, pile2Distance: 6 },
    soilLayers: []
  })
}

const handleCalculate = async () => {
  calculating.value = true
  try {
    await validateForm()
    emit('calculate', form)
  } catch (error) {
    ElMessage.error(error.message)
  } finally {
    calculating.value = false
  }
}

const validateForm = async () => {
  // 表单验证逻辑
  return Promise.resolve()
}
</script>
```

### 2. 结果展示组件

#### ResultsPanel.vue
```vue
<template>
  <div class="space-y-6">
    <!-- 计算结果概览 -->
    <Card title="计算结果概览">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard
          title="最大沉降"
          :value="results.statistics.maxSettlementMm"
          unit="mm"
          :color="getSettlementColor(results.statistics.maxSettlementMm)"
        />
        <StatCard
          title="平均沉降"
          :value="results.statistics.avgSettlementMm"
          unit="mm"
          color="blue"
        />
        <StatCard
          title="安全等级"
          :value="results.safetyAssessment.safetyLevel"
          :color="results.safetyAssessment.safetyColor"
        />
        <StatCard
          title="影响面积"
          :value="results.safetyAssessment.influenceArea"
          unit="m²"
          color="purple"
        />
      </div>
    </Card>

    <!-- 可视化图表 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <Card title="沉降等高线图">
        <SettlementChart
          :data="contourData"
          type="contour"
          chart-height="400"
        />
      </Card>
      
      <Card title="安全评估">
        <SettlementChart
          :data="radarData"
          type="radar"
          chart-height="400"
        />
      </Card>
    </div>

    <!-- 详细数据表格 -->
    <Card title="详细计算结果">
      <el-table :data="results.points" style="width: 100%">
        <el-table-column prop="point_id" label="测点" width="80" />
        <el-table-column prop="x" label="X坐标(m)" />
        <el-table-column prop="z" label="深度(m)" />
        <el-table-column prop="settlement_mm" label="沉降量(mm)" />
        <el-table-column prop="pile1_settlement" label="桩1影响(mm)" />
        <el-table-column prop="pile2_settlement" label="桩2影响(mm)" />
      </el-table>
    </Card>

    <!-- 安全建议 -->
    <Card title="安全评估与建议">
      <div class="space-y-4">
        <div class="flex items-center gap-2">
          <el-tag :type="getTagType(results.safetyAssessment.safetyLevel)">
            {{ results.safetyAssessment.safetyLevel }}
          </el-tag>
          <span class="text-sm text-gray-600">
            最大沉降: {{ results.safetyAssessment.maxSettlementMm }}mm
          </span>
        </div>
        
        <div class="space-y-2">
          <h4 class="font-medium">建议:</h4>
          <ul class="list-disc list-inside text-sm text-gray-600 space-y-1">
            <li v-for="recommendation in results.safetyAssessment.recommendations" :key="recommendation">
              {{ recommendation }}
            </li>
          </ul>
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { SettlementResult } from '@/types/settlement'

interface Props {
  results: SettlementResult
  loading?: boolean
}

const props = defineProps<Props>()

const contourData = computed(() => {
  return props.results.points.map(point => ({
    name: point.point_id,
    value: [point.x, point.z, point.settlement_mm]
  }))
})

const radarData = computed(() => {
  // 计算雷达图数据
  const maxSettlement = props.results.statistics.maxSettlementMm
  const safetyScore = Math.max(0, 100 - maxSettlement)
  return [safetyScore, 85, 75, 90, 80]
})

const getSettlementColor = (value: number) => {
  if (value > 50) return 'red'
  if (value > 30) return 'orange'
  if (value > 10) return 'yellow'
  return 'green'
}

const getTagType = (level: string) => {
  const map = {
    '安全': 'success',
    '警告': 'warning',
    '危险': 'danger'
  }
  return map[level as keyof typeof map] || 'info'
}
</script>
```

## 组件通信规范

### 1. Props和Emits规范
```typescript
// 统一的命名规范
interface Props {
  modelValue: T           // v-model绑定
  disabled?: boolean      // 禁用状态
  loading?: boolean       // 加载状态
  error?: string          // 错误信息
}

interface Emits {
  'update:modelValue': [value: T]  // 更新值
  change: [value: T]               // 值变化
  blur: []                         // 失去焦点
  focus: []                        // 获得焦点
}
```

### 2. 状态管理规范
```typescript
// 使用Pinia store管理复杂状态
export const useSettlementStore = defineStore('settlement', () => {
  const params = ref<SettlementParams>(defaultParams)
  const results = ref<SettlementResult | null>(null)
  const loading = ref(false)
  
  const calculate = async () => {
    loading.value = true
    try {
      results.value = await settlementService.calculate(params.value)
    } finally {
      loading.value = false
    }
  }
  
  return { params, results, loading, calculate }
})
```

### 3. 事件处理规范
```typescript
// 组件内事件处理
const handleSubmit = async () => {
  try {
    await validate()
    emit('submit', formData.value)
  } catch (error) {
    ElMessage.error(error.message)
  }
}
```

## 样式规范

### 1. CSS命名规范
- 使用BEM命名法：`block__element--modifier`
- Tailwind类名优先
- 自定义CSS类使用kebab-case

### 2. 响应式设计
```vue
<!-- 响应式布局示例 -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div v-for="item in items" :key="item.id" class="col-span-1">
    <!-- 内容 -->
  </div>
</div>
```

### 3. 主题切换支持
```typescript
// 主题配置
const themes = {
  light: {
    background: '#ffffff',
    surface: '#f8fafc',
    primary: '#1e3a8a',
    text: '#1f2937'
  },
  dark: {
    background: '#0f172a',
    surface: '#1e293b',
    primary: '#3b82f6',
    text: '#f1f5f9'
  }
}
```

## 性能优化指南

### 1. 组件懒加载
```typescript
// 路由级懒加载
const SettlementAnalysisView = () => import('@/views/SettlementAnalysisView.vue')

// 组件级懒加载
const ChartComponent = defineAsyncComponent(() => 
  import('@/components/charts/SettlementChart.vue')
)
```

### 2. 计算属性缓存
```typescript
const expensiveData = computed(() => {
  // 复杂计算，自动缓存
  return processLargeDataset(props.data)
})
```

### 3. 防抖和节流
```typescript
import { useDebounceFn } from '@vueuse/core'

const debouncedSearch = useDebounceFn((value: string) => {
  // 搜索逻辑
}, 300)
```

## 测试规范

### 1. 组件测试示例
```typescript
// SettlementForm.spec.ts
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import SettlementForm from '@/components/SettlementForm.vue'

describe('SettlementForm', () => {
  it('renders correctly', () => {
    const wrapper = mount(SettlementForm)
    expect(wrapper.find('.settlement-form')).toBeTruthy()
  })
  
  it('emits calculate event', async () => {
    const wrapper = mount(SettlementForm)
    await wrapper.find('button[type="submit"]').trigger('click')
    expect(wrapper.emitted('calculate')).toBeTruthy()
  })
})
```

### 2. 测试覆盖率要求
- 单元测试覆盖率 ≥ 80%
- 关键业务逻辑全覆盖
- 用户交互场景全覆盖