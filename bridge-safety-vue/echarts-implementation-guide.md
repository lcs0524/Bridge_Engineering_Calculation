# 桥梁沉降分析图表 - ECharts 实现指南

本文档提供将 [`visualization/plotter.py`](../visualization/plotter.py) 中定义的桥梁沉降分析图表转换为 Vue + ECharts 实现的详细指导。

## 目录
1. [总体思路](#总体思路)
2. [工程示意简图](#工程示意简图)
3. [沉降分析图](#沉降分析图)
4. [等高线图](#等高线图)
5. [雷达图](#雷达图)
6. [瀑布图](#瀑布图)
7. [数据处理与转换](#数据处理与转换)

## 总体思路

将 Python Matplotlib 图表转换为 ECharts 需要理解原始图表的构成元素，并找到 ECharts 中对应的实现方式。

关键步骤：
1. 分析原始 Python 代码中的数据结构和图表元素
2. 识别 ECharts 中的对应图表类型和组件
3. 将数据转换为 ECharts 支持的格式
4. 实现自定义图形和组合图表

每个图表将在 Vue 组件中实现，通过 `ChartComponent.vue` 作为通用 ECharts 容器来渲染。

## 工程示意简图

原始实现: `settlement_distribution_plot` 函数

### 关键元素
- 桩体 (两个桩基)
- 路基结构 (桥面和路基)
- 计算点标注
- 尺寸标注 (L1, L2, 路基宽度)

### ECharts 实现思路

使用 ECharts 的 **自定义图形** (custom series) 结合 **图形组件** (graphic components)：

```javascript
// 工程示意简图 ECharts 配置
const projectDiagramOptions = {
  title: {
    text: '工程示意简图',
    left: 'center',
    textStyle: {
      color: '#8b5cf6',
      fontWeight: 600
    }
  },
  tooltip: {
    trigger: 'item',
    formatter: '{b}: {c}'
  },
  grid: {
    left: '5%', 
    right: '5%',
    bottom: '10%',
    top: '10%',
    containLabel: true
  },
  xAxis: {
    type: 'value',
    name: '横向距离 X (m)',
    nameLocation: 'middle',
    nameGap: 30,
    axisLine: { show: true },
    axisLabel: { color: 'rgba(255, 255, 255, 0.85)' },
    nameTextStyle: { color: 'rgba(255, 255, 255, 0.85)' }
  },
  yAxis: {
    type: 'value',
    name: '深度 Z (m)',
    nameLocation: 'middle',
    nameGap: 30,
    inverse: true, // 上小下大
    axisLine: { show: true },
    axisLabel: { color: 'rgba(255, 255, 255, 0.85)' },
    nameTextStyle: { color: 'rgba(255, 255, 255, 0.85)' }
  },
  series: [
    // 背景分层
    {
      type: 'custom',
      renderItem: function(params, api) {
        // 实现上部灰色背景区域
        return {
          type: 'rect',
          shape: {
            // 计算坐标
            x: api.coord([-xRange, 0])[0],
            y: api.coord([-xRange, 0])[1],
            width: api.size([2*xRange, 0])[0],
            height: api.size([0, yRange*0.3])[1]
          },
          style: {
            fill: 'rgba(211, 211, 211, 0.3)'
          }
        };
      },
      data: [0] // 占位数据
    },
    // 路基绘制
    {
      type: 'custom',
      renderItem: function(params, api) {
        // 实现梯形路基
        return {
          type: 'polygon',
          shape: {
            points: [
              api.coord([-roadbedTopWidth/2, roadbedTopLevel]),
              api.coord([roadbedTopWidth/2, roadbedTopLevel]),
              api.coord([roadbedBottomWidth/2, roadbedTopLevel - roadbedHeight]),
              api.coord([-roadbedBottomWidth/2, roadbedTopLevel - roadbedHeight])
            ]
          },
          style: {
            fill: '#A0522D',
            opacity: 0.8,
            stroke: '#000',
            lineWidth: 1.5
          }
        };
      },
      data: [0] // 占位数据
    },
    // 桩1绘制
    {
      type: 'custom',
      renderItem: function(params, api) {
        // 实现左侧桩体
        // ...桩体渲染逻辑...
      },
      data: [0]
    },
    // 桩2绘制
    {
      type: 'custom',
      renderItem: function(params, api) {
        // 实现右侧桩体
        // ...桩体渲染逻辑...
      },
      data: [0]
    },
    // 计算点绘制
    {
      type: 'scatter',
      symbolSize: 20,
      itemStyle: {
        opacity: 0.9
      },
      data: points.map((point, index) => {
        return {
          value: [point.x, point.z],
          name: `点${index+1}`,
          // 根据沉降值确定颜色
          itemStyle: {
            color: getSettlementColor(point.settlement, maxSettlementThreshold)
          }
        };
      })
    }
  ],
  backgroundColor: 'transparent'
};
```

关键实现点：
1. 使用 `custom` 系列类型创建桩体和路基
2. 使用 `polygon` 绘制梯形路基
3. 使用 `scatter` 系列绘制计算点
4. 根据沉降值自定义计算点颜色

## 沉降分析图

原始实现: `create_settlement_plot` 函数

### 关键元素
- 基于工程示意简图
- 显示沉降后的计算点位置
- 使用颜色编码表示沉降程度
- 添加颜色条图例

### ECharts 实现思路

扩展工程示意简图，添加沉降后的点位置和颜色图例：

```javascript
// 沉降分析图 ECharts 配置
const settlementChartOptions = {
  // 沿用工程示意简图的基本配置
  ...projectDiagramOptions,
  
  title: {
    text: '沉降分析图',
    left: 'center',
    textStyle: {
      color: '#8b5cf6',
      fontWeight: 600
    }
  },
  
  // 添加视觉映射组件
  visualMap: {
    min: minSettlement,
    max: maxSettlement,
    calculable: true,
    precision: 2,
    inRange: {
      color: ['#4ade80', '#fbbf24', '#f87171'] // 绿-黄-红颜色渐变
    },
    orient: 'vertical',
    right: '5%',
    top: 'center',
    textStyle: {
      color: 'rgba(255, 255, 255, 0.85)'
    }
  },
  
  series: [
    // 保留工程示意简图的基本元素...
    
    // 修改计算点系列，显示沉降后的位置
    {
      type: 'scatter',
      symbolSize: 20,
      itemStyle: {
        opacity: 0.9,
        borderColor: '#000',
        borderWidth: 1
      },
      data: points.map((point, index) => {
        // 计算沉降后的位置
        const adjustedZ = point.z + (point.settlement_mm / 1000.0);
        return {
          value: [point.x, adjustedZ],
          name: `点${index+1}`,
          settlement: point.settlement_mm,
          itemStyle: {
            color: getSettlementColor(point.settlement_mm, maxSettlementThreshold)
          }
        };
      })
    },
    
    // 添加警戒线
    {
      type: 'line',
      markLine: {
        silent: true,
        lineStyle: {
          color: '#fbbf24',
          type: 'dashed',
          width: 2
        },
        data: [
          {
            name: '安全阈值',
            yAxis: safetyThreshold,
            label: {
              formatter: '安全阈值: {c} mm',
              position: 'end',
              color: '#fbbf24',
              backgroundColor: 'rgba(31, 41, 55, 0.8)',
              padding: [4, 8],
              fontWeight: 600
            }
          }
        ]
      }
    }
  ]
};
```

关键实现点：
1. 添加 `visualMap` 组件实现颜色映射
2. 调整计算点位置以显示沉降效果
3. 使用 `markLine` 显示安全阈值线

## 等高线图

原始实现: `create_contour_plot` 函数

### 关键元素
- 使用插值生成等高线
- 显示桩基和路基结构
- 颜色填充表示沉降程度
- 等高线标签

### ECharts 实现思路

使用 ECharts 的 **热力图** (heatmap) 和 **等值线图** (visualMap + contour)：

```javascript
// 等高线图 ECharts 配置
const contourChartOptions = {
  title: {
    text: '沉降等高线分析图',
    left: 'center',
    textStyle: {
      color: '#8b5cf6',
      fontWeight: 600
    }
  },
  tooltip: {
    trigger: 'item',
    formatter: function(params) {
      if (params.seriesType === 'scatter') {
        return `位置: (${params.value[0]}m, ${Math.abs(params.value[1])}m)<br/>沉降量: ${params.data.settlement}mm`;
      }
      return '';
    }
  },
  grid: {
    left: '5%',
    right: '15%',
    bottom: '10%',
    top: '15%',
    containLabel: true
  },
  xAxis: {
    type: 'value',
    name: '横向距离 X (m)',
    nameLocation: 'middle',
    nameGap: 30,
    axisLine: { show: true },
    axisLabel: { color: 'rgba(255, 255, 255, 0.85)' },
    nameTextStyle: { color: 'rgba(255, 255, 255, 0.85)' }
  },
  yAxis: {
    type: 'value',
    name: '深度 Z (m)',
    nameLocation: 'middle',
    nameGap: 30,
    inverse: true, // 上小下大
    axisLine: { show: true },
    axisLabel: { color: 'rgba(255, 255, 255, 0.85)' },
    nameTextStyle: { color: 'rgba(255, 255, 255, 0.85)' }
  },
  visualMap: {
    min: minSettlement,
    max: maxSettlement,
    calculable: true,
    precision: 2,
    inRange: {
      color: ['#4ade80', '#fbbf24', '#f87171'] // 绿-黄-红颜色渐变
    },
    orient: 'vertical',
    right: '5%',
    top: 'center',
    textStyle: {
      color: 'rgba(255, 255, 255, 0.85)'
    }
  },
  series: [
    // 等高线图 - 使用surface系列
    {
      type: 'contour',
      data: interpolatedData, // 需要进行数据插值处理
      smooth: true
    },
    
    // 桩基和路基结构绘制
    // ... 复用工程示意简图中的结构绘制逻辑 ...
    
    // 计算点标记
    {
      type: 'scatter',
      symbolSize: 20,
      itemStyle: {
        borderColor: '#000',
        borderWidth: 1
      },
      data: points.map((point, index) => {
        return {
          value: [point.x, -point.z],
          settlement: point.settlement_mm,
          name: `点${index+1}`,
          itemStyle: {
            color: getSettlementColor(point.settlement_mm, maxSettlementThreshold)
          }
        };
      })
    }
  ],
  backgroundColor: 'transparent'
};
```

关键实现点：
1. 使用 `echarts-gl` 的 `contour` 系列绘制等高线
2. 对原始点数据进行插值处理
3. 使用 `visualMap` 实现颜色映射
4. 添加 `scatter` 系列标记计算点位置

> 注意：ECharts 原生不支持直接绘制等高线图，需要使用 `echarts-gl` 扩展或者基于热力图自行实现等高线效果。

## 雷达图

原始实现: `create_radar_plot` 函数

### 关键元素
- 按深度分层的雷达图
- 距离-沉降雷达图

### ECharts 实现思路

使用 ECharts 的 **雷达图** (radar)：

```javascript
// 雷达图 ECharts 配置
const radarChartOptions = {
  title: {
    text: '沉降雷达分析图',
    left: 'center',
    textStyle: {
      color: '#8b5cf6',
      fontWeight: 600
    }
  },
  tooltip: {
    trigger: 'item'
  },
  grid: {
    left: '5%',
    right: '5%',
    bottom: '10%',
    top: '15%',
    containLabel: true
  },
  legend: {
    data: depthLabels,
    bottom: 0,
    textStyle: {
      color: 'rgba(255, 255, 255, 0.85)'
    }
  },
  radar: {
    indicator: pointNames.map(name => {
      return { name, max: maxSettlement * 1.2 };
    }),
    radius: '65%',
    splitNumber: 5,
    axisName: {
      color: 'rgba(255, 255, 255, 0.85)'
    },
    splitLine: {
      lineStyle: {
        color: 'rgba(75, 85, 99, 0.3)'
      }
    },
    splitArea: {
      show: true,
      areaStyle: {
        color: ['rgba(31, 41, 55, 0.2)', 'rgba(31, 41, 55, 0.4)']
      }
    },
    axisLine: {
      lineStyle: {
        color: 'rgba(75, 85, 99, 0.5)'
      }
    }
  },
  series: depthGroups.map((group, index) => {
    return {
      name: `深度 ${group.depth}m`,
      type: 'radar',
      data: [
        {
          value: group.settlements,
          name: `深度 ${group.depth}m`,
          areaStyle: {
            color: colors[index % colors.length],
            opacity: 0.4
          },
          lineStyle: {
            width: 2,
            color: colors[index % colors.length]
          },
          itemStyle: {
            color: colors[index % colors.length]
          }
        }
      ]
    };
  }),
  backgroundColor: 'transparent'
};
```

关键实现点：
1. 使用 `radar` 类型图表
2. 将计算点按深度分组
3. 为每个深度组创建一个雷达系列
4. 为不同深度使用不同颜色

## 瀑布图

原始实现: `create_waterfall_plot` 函数

### 关键元素
- 按计算点顺序的瀑布图
- 按深度分层的瀑布图

### ECharts 实现思路

使用 ECharts 的 **自定义系列** (custom series) 实现瀑布图效果：

```javascript
// 瀑布图 ECharts 配置
const waterfallChartOptions = {
  title: {
    text: '沉降瀑布分析图',
    left: 'center',
    textStyle: {
      color: '#8b5cf6',
      fontWeight: 600
    }
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    },
    formatter: function(params) {
      const param = params[0];
      const cumulative = param.data.cumulative;
      const value = param.data.value;
      return `${param.name}<br/>沉降增量: ${value.toFixed(2)} mm<br/>累计沉降: ${cumulative.toFixed(2)} mm`;
    }
  },
  grid: {
    left: '5%',
    right: '5%',
    bottom: '15%',
    top: '15%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: pointNames,
    axisLabel: {
      color: 'rgba(255, 255, 255, 0.85)',
      rotate: 45
    }
  },
  yAxis: {
    type: 'value',
    name: '沉降值 (mm)',
    nameTextStyle: {
      color: 'rgba(255, 255, 255, 0.85)'
    },
    axisLabel: {
      color: 'rgba(255, 255, 255, 0.85)'
    },
    splitLine: {
      lineStyle: {
        color: 'rgba(75, 85, 99, 0.3)'
      }
    }
  },
  series: [
    {
      type: 'custom',
      renderItem: function(params, api) {
        const value = api.value(1);
        const cumulativeStart = api.value(2);
        const cumulativeEnd = cumulativeStart + value;
        
        const startX = api.coord([params.dataIndex, cumulativeStart])[0];
        const startY = api.coord([params.dataIndex, cumulativeStart])[1];
        const endX = api.coord([params.dataIndex, cumulativeEnd])[0];
        const endY = api.coord([params.dataIndex, cumulativeEnd])[1];
        const width = api.size([1, 0])[0] * 0.6;
        
        // 确定颜色
        let color = '#4ade80'; // 默认绿色
        if (value > 20) color = '#f87171'; // 红色
        else if (value > 10) color = '#fbbf24'; // 黄色
        
        // 绘制柱状图
        const rectShape = {
          x: startX - width / 2,
          y: endY,
          width: width,
          height: startY - endY
        };
        
        // 绘制连接线
        const lineShape = {
          x1: startX + width / 2,
          y1: startY,
          x2: startX + api.size([1, 0])[0] * 0.9,
          y2: startY
        };
        
        // 返回多个图形元素
        return {
          type: 'group',
          children: [
            {
              type: 'rect',
              shape: rectShape,
              style: {
                fill: color,
                stroke: 'rgba(0, 0, 0, 0.7)'
              }
            },
            // 只对非最后一个点绘制连接线
            params.dataIndex < pointNames.length - 1 ? {
              type: 'line',
              shape: lineShape,
              style: {
                stroke: '#333',
                lineDash: [4, 4]
              }
            } : {}
          ]
        };
      },
      dimensions: ['name', 'value', 'cumulative'],
      encode: {
        x: 0,
        y: [1, 2]
      },
      data: waterfallData
    }
  ],
  backgroundColor: 'transparent'
};
```

关键实现点：
1. 使用 `custom` 系列类型实现瀑布图效果
2. 在 `renderItem` 函数中自定义柱形图和连接线的绘制
3. 使用 `dimensions` 和 `encode` 定义数据维度
4. 预处理数据计算累积值

## 数据处理与转换

从后端 API 获取的数据需要转换为 ECharts 可用的格式。

### 原始数据结构

后端返回的数据格式大致如下：

```javascript
{
  "points": [
    {
      "x": 5.0,
      "y": 0.0,
      "z": 2.0,
      "settlement_mm": 12.73,
      "safety_factor": "需注意"
    },
    // 更多计算点...
  ],
  "input_parameters": {
    "pile1": {
      "diameter": 1.0,
      "length": 20.0
    },
    "pile2": {
      "diameter": 1.0,
      "length": 20.0
    },
    "road_params": {
      "width": 12.0,
      "pile1_distance": 5.0,
      "pile2_distance": 5.0
    }
  },
  "safety_assessment": {
    "bridge_limit": 20.0,
    "general_limit": 10.0
  }
}
```

### 数据转换工具函数

```javascript
// 按深度分组数据
function groupByDepth(points) {
  const depthGroups = {};
  
  points.forEach(point => {
    const depth = point.z;
    if (!depthGroups[depth]) {
      depthGroups[depth] = {
        depth,
        points: [],
        settlements: []
      };
    }
    depthGroups[depth].points.push(point);
    depthGroups[depth].settlements.push(point.settlement_mm);
  });
  
  return Object.values(depthGroups);
}

// 生成瀑布图数据
function generateWaterfallData(points) {
  let cumulative = 0;
  return points.map((point, index) => {
    const value = point.settlement_mm;
    const data = {
      name: `点${index+1}`,
      value: value,
      cumulative: cumulative
    };
    cumulative += value;
    return data;
  });
}

// 根据沉降值确定颜色
function getSettlementColor(settlement, threshold) {
  const ratio = threshold > 0 ? settlement / threshold : 0;
  
  if (ratio < 0.1) return '#2E8B57'; // 极低沉降 - 深海绿
  if (ratio < 0.3) return '#32CD32'; // 低沉降 - 酸橙绿
  if (ratio < 0.6) return '#FFD700'; // 中等沉降 - 金色
  if (ratio < 0.9) return '#FF8C00'; // 高沉降 - 深橙色
  return '#DC143C'; // 最高沉降 - 深红色
}
```

将这些工具函数与图表配置结合，可以完成 Python 图表到 ECharts 的转换。每个图表组件都应封装在单独的 Vue 组件中，以便在 BridgeSettlementView 中灵活使用。 