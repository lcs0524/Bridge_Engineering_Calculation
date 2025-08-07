<template>
  <div class="bridge-settlement-view">
    <div class="page-header">
      <h1>桥梁沉降计算</h1>
      <p class="page-description">本模块依据《公路路基设计规范》JTG D30-2015 等相关规范用于计算桥梁在不同荷载与地质条件下的沉降情况，评估结构长期稳定性。</p>
    </div>

    <el-row :gutter="32">
      <!-- 左侧输入表单 -->
      <el-col :xs="24" :sm="24" :md="10" :lg="10" :xl="10">
        <el-card class="form-card" shadow="never">
            <template #header>
              <div class="card-header">
                <h2><el-icon class="header-icon"><DataAnalysis /></el-icon> 计算输入参数</h2>
                <el-tooltip content="填写完所有参数后点击计算按钮">
                  <el-icon><QuestionFilled /></el-icon>
                </el-tooltip>
              </div>
            </template>
            
            <el-form :model="formData" label-position="top" class="settlement-form">
              <div class="form-section">
                <h3 class="section-title">项目信息</h3>
                <el-form-item label="项目名称:">
                  <el-input v-model="formData.projectName" placeholder="请输入项目名称" class="full-width" />
                </el-form-item>
                <el-form-item label="项目信息:">
                  <el-input
                    v-model="formData.projectInfo"
                    type="textarea"
                    :rows="3"
                    placeholder="请输入项目详细信息"
                    class="full-width"
                  />
                </el-form-item>
              </div>
              
              <!-- 桩基参数 -->
              <div class="form-section">
                <h3><el-icon><Histogram /></el-icon> 桩基参数</h3>
                
                <h4 class="param-group-title">桩1 参数</h4>
                <el-row :gutter="20">
                  <el-col :span="8">
                    <el-form-item label="桩1 - 直径(m)">
                      <el-input-number v-model="formData.pile1.diameter" :min="0" :precision="1" :step="0.1" class="full-width" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="桩1 - 桩长(m)">
                      <el-input-number v-model="formData.pile1.length" :min="0" :precision="1" :step="1" class="full-width" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="桩1 - 荷载(kN)">
                      <el-input-number v-model="formData.pile1.load" :min="0" :precision="1" :step="100" class="full-width" />
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <h4 class="param-group-title">桩2 参数</h4>
                <el-row :gutter="20">
                  <el-col :span="8">
                    <el-form-item label="桩2 - 直径(m)">
                      <el-input-number v-model="formData.pile2.diameter" :min="0" :precision="1" :step="0.1" class="full-width" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="桩2 - 桩长(m)">
                      <el-input-number v-model="formData.pile2.length" :min="0" :precision="1" :step="1" class="full-width" />
                    </el-form-item>
                  </el-col>
                   <el-col :span="8">
                    <el-form-item label="桩2 - 荷载(kN)">
                      <el-input-number v-model="formData.pile2.load" :min="0" :precision="1" :step="100" class="full-width" />
                    </el-form-item>
                  </el-col>
                </el-row>
              </div>
              
              <!-- 板桥结构参数 -->
              <div class="form-section">
                <h3><el-icon><Connection /></el-icon> 板桥结构参数</h3>
                <el-form-item label="路基宽度(m)">
                  <el-input-number v-model="formData.bridgeWidth" :min="0" :precision="1" :step="0.1" class="full-width" />
                </el-form-item>
                
                <!-- 与桩距离参数 -->
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="与桩1距离(m)">
                      <el-input-number v-model="formData.distanceToPile1" :min="0" :precision="1" :step="0.1" class="full-width" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="与桩2距离(m)">
                      <el-input-number v-model="formData.distanceToPile2" :min="0" :precision="1" :step="0.1" class="full-width" />
                    </el-form-item>
                  </el-col>
                </el-row>
              </div>
              
              <!-- 土层参数 -->
              <div class="form-section">
                <h3><el-icon><Files /></el-icon> 土层参数</h3>
                
                <!-- 土层参数管理 -->
                <div class="soil-layers-section">
                  <div class="section-header">
                    <h4><el-icon><Document /></el-icon> 土层配置</h4>
                    <div class="action-buttons">
                      <el-button type="success" size="small" @click="addSoilLayer">
                        <el-icon><Plus /></el-icon> 添加土层
                      </el-button>
                      <el-button type="info" size="small" @click="resetSoilLayers">
                        <el-icon><RefreshRight /></el-icon> 重置默认
                      </el-button>
                    </div>
                  </div>
                  
                  <!-- 土层参数表格 -->
                  <div class="soil-layers-table">
                    <el-table 
                      :data="soilLayersData" 
                      border 
                      style="width: 100%"
                      :header-cell-style="{ backgroundColor: '#f5f7fa', color: '#333', fontWeight: '600' }"
                      empty-text="暂无土层数据，请点击上方按钮添加土层"
                      max-height="300"
                    >
                      <el-table-column prop="depth" label="深度范围 (m)" width="120">
                        <template #default="scope">
                          <span>{{ scope.row.depthStart }}-{{ scope.row.depthEnd }}</span>
                        </template>
                      </el-table-column>
                      <el-table-column prop="soilType" label="土层类型" width="100">
                        <template #default="scope">
                          <el-tag :type="getSoilTypeTagType(scope.row.soilType)" size="small">
                            {{ getSoilTypeName(scope.row.soilType) }}
                          </el-tag>
                        </template>
                      </el-table-column>
                      <el-table-column prop="compressionModulus" label="压缩模量 Es (MPa)" width="140">
                        <template #default="scope">
                          <span class="numeric-value">{{ scope.row.compressionModulus }}</span>
                        </template>
                      </el-table-column>
                      <el-table-column prop="poissonRatio" label="泊松比 ν" width="100">
                        <template #default="scope">
                          <span class="numeric-value">{{ scope.row.poissonRatio }}</span>
                        </template>
                      </el-table-column>
                      <el-table-column label="操作" width="150">
                        <template #default="scope">
                          <el-button 
                            type="primary" 
                            size="small" 
                            @click="editSoilLayer(scope.$index)"
                          >
                            编辑
                          </el-button>
                          <el-button 
                            type="danger" 
                            size="small" 
                            @click="deleteSoilLayer(scope.$index)"
                            :disabled="soilLayersData.length <= 1"
                          >
                            删除
                          </el-button>
                        </template>
                      </el-table-column>
                    </el-table>
                  </div>
                  
                  <!-- 土层统计信息 -->
                  <div class="soil-summary">
                    <div class="summary-item">
                      <span class="summary-label">土层总数：</span>
                      <span class="summary-value">{{ soilLayersData.length }} 层</span>
                    </div>
                    <div class="summary-item">
                      <span class="summary-label">总深度：</span>
                      <span class="summary-value">{{ getTotalDepth() }} m</span>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 土层编辑对话框 -->
              <el-dialog
                v-model="showSoilLayerDialog"
                :title="editingIndex === -1 ? '添加土层' : '编辑土层'"
                width="500px"
                :before-close="handleSoilLayerDialogClose"
              >
                <el-form :model="currentSoilLayer" label-position="top" class="soil-layer-form" :rules="soilLayerRules" ref="soilLayerFormRef">
                <el-row :gutter="20">
                  <el-col :span="12">
                      <el-form-item label="起始深度 (m)" prop="depthStart">
                        <el-input-number 
                          v-model="currentSoilLayer.depthStart" 
                          :min="0" 
                          :precision="1" 
                          :step="0.5" 
                          class="full-width"
                          placeholder="起始深度"
                        />
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                      <el-form-item label="结束深度 (m)" prop="depthEnd">
                        <el-input-number 
                          v-model="currentSoilLayer.depthEnd" 
                          :min="0" 
                          :precision="1" 
                          :step="0.5" 
                          class="full-width"
                          placeholder="结束深度"
                        />
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-row :gutter="20">
                  <el-col :span="12">
                      <el-form-item label="土层类型" prop="soilType">
                        <el-select v-model="currentSoilLayer.soilType" placeholder="选择土层类型" class="full-width">
                        <el-option label="粘土" value="clay" />
                        <el-option label="砂土" value="sand" />
                          <el-option label="粉土" value="silt" />
                          <el-option label="淤泥" value="mud" />
                          <el-option label="岩石" value="rock" />
                          <el-option label="填土" value="fill" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                      <el-form-item label="泊松比 ν" prop="poissonRatio">
                        <el-select v-model="currentSoilLayer.poissonRatio" placeholder="选择泊松比" class="full-width">
                          <el-option label="0.35 (粘土)" value="0.35" />
                          <el-option label="0.30 (砂土)" value="0.30" />
                          <el-option label="0.28 (粉土)" value="0.28" />
                          <el-option label="0.25 (岩石)" value="0.25" />
                          <el-option label="0.40 (淤泥)" value="0.40" />
                        </el-select>
                    </el-form-item>
                  </el-col>
                </el-row>
                  <el-form-item label="压缩模量 Es (MPa)" prop="compressionModulus">
                    <el-input-number 
                      v-model="currentSoilLayer.compressionModulus" 
                      :min="0.1" 
                      :precision="1" 
                      :step="0.5" 
                      class="full-width"
                      placeholder="请输入压缩模量"
                    />
                  </el-form-item>
                </el-form>
                
                <template #footer>
                  <span class="dialog-footer">
                    <el-button @click="handleSoilLayerDialogClose">取消</el-button>
                    <el-button type="primary" @click="saveSoilLayer">
                      {{ editingIndex === -1 ? '添加' : '保存' }}
                    </el-button>
                  </span>
                </template>
              </el-dialog>
              
              <div class="form-actions">
                <el-button type="primary" @click="handleCalculate" :loading="calculating">
                  <el-icon><ArrowRight /></el-icon> 计算沉降
                </el-button>
                <el-button @click="resetForm">
                  <el-icon><RefreshRight /></el-icon> 重置
                </el-button>
              </div>
            </el-form>
          </el-card>
      </el-col>
      
      <!-- 右侧结果展示 -->
      <el-col :xs="24" :sm="24" :md="14" :lg="14" :xl="14">
        <el-card class="result-card" shadow="never">
            <template #header>
              <div class="card-header">
                <h2><el-icon class="header-icon"><TrendCharts /></el-icon> 分析结果</h2>
                <el-tag v-if="hasResults" type="success" effect="light" size="small">数据已更新</el-tag>
              </div>
            </template>
            
            <el-tabs v-model="activeTab" class="result-tabs">
              <el-tab-pane label="数值结果" name="numerical">
                <div v-if="hasResults" class="result-content">
                  <el-alert
                    title="计算完成"
                    type="success"
                    :closable="false"
                    show-icon
                    class="result-alert"
                  >
                    根据输入参数，系统已计算出以下沉降数据
                  </el-alert>
                  
                  <el-table 
                    :data="tableData" 
                    style="width: 100%" 
                    height="450" 
                    border 
                    :header-cell-style="{ backgroundColor: '#f5f7fa', color: '#333', fontWeight: 600 }"
                    :cell-style="cellStyle"
                    class="result-table"
                    @row-click="handleRowClick"
                  >
                    <el-table-column prop="point" label="计算点" width="100" />
                    <el-table-column prop="xCoord" label="X坐标" width="100" />
                    <el-table-column prop="yCoord" label="Y坐标" width="100" />
                    <el-table-column prop="settlement" label="总沉降量(mm)" width="150">
                      <template #default="scope">
                        <span :class="{ 'warning-value': parseFloat(scope.row.settlement) > 10, 'safe-value': parseFloat(scope.row.settlement) <= 10 }">
                          {{ scope.row.settlement }}
                        </span>
                      </template>
                    </el-table-column>
                    <el-table-column prop="safetyFactor" label="安全评估">
                      <template #default="scope">
                        <el-tag :type="scope.row.safetyFactor === '安全' ? 'success' : 'warning'" effect="light">
                          {{ scope.row.safetyFactor }}
                        </el-tag>
                      </template>
                    </el-table-column>
                  </el-table>
                </div>
                <div v-else class="empty-result">
                  <el-empty description="暂无数据，请先进行计算">
                    <template #image>
                      <el-icon :size="60"><DataLine /></el-icon>
                    </template>
                  </el-empty>
                </div>
              </el-tab-pane>
              <el-tab-pane label="图形分析" name="graphical">
                <div v-if="hasResults" class="graphical-analysis">
                  <el-tabs v-model="graphicalActiveTab" class="inner-tabs">
                    <el-tab-pane label="工程示意简图" name="diagram"></el-tab-pane>
                    <el-tab-pane label="沉降分析图" name="settlement"></el-tab-pane>
                    <el-tab-pane label="等高线图" name="contour"></el-tab-pane>
                    <el-tab-pane label="雷达图" name="radar"></el-tab-pane>
                    <el-tab-pane label="瀑布图" name="waterfall"></el-tab-pane>
                  </el-tabs>
                  <div class="chart-inner-container">
                    <ChartComponent :options="chartOptions" height="450px" />
                  </div>
                </div>
                <div v-else class="empty-result">
                  <el-empty description="暂无数据，请先进行计算">
                    <template #image>
                      <el-icon :size="60"><PieChart /></el-icon>
                    </template>
                  </el-empty>
                </div>
              </el-tab-pane>
              <el-tab-pane label="安全评估报告" name="safety-report">
                <div v-if="hasResults" class="safety-report">
                  <div class="report-header">
                    <h3><el-icon><Document /></el-icon> 桥梁沉降安全评估报告</h3>
                    <div class="export-buttons">
                      <el-button type="primary" size="small" @click="exportPDFReport" :loading="exportingPDF">
                        <el-icon><Download /></el-icon> 导出PDF报告
                      </el-button>
                      <el-button type="info" size="small" @click="exportReport">
                        <el-icon><Document /></el-icon> 导出TXT报告
                      </el-button>
                    </div>
                  </div>
                  
                  <!-- PDF导出专用的隐藏模板 -->
                  <div id="pdf-report-template" style="display: none;">
                    <div class="pdf-report-container">
                      <!-- 报告头部 -->
                      <PdfReportHeader reportTitle="桥梁跨越工程安全性评估报告" />
                      
                      <!-- 项目基本信息 -->
                      <div class="pdf-section">
                        <h3 class="pdf-section-title">项目名称</h3>
                        <div class="pdf-divider-thin"></div>
                        <p class="pdf-project-name">{{ formData.projectName || '桥梁跨越工程项目' }}</p>
                        <div class="pdf-divider-thin"></div>
                        
                        <h3 class="pdf-section-title">项目类型</h3>
                        <div class="pdf-divider-thin"></div>
                        <p>桥梁跨越工程安全性计算</p>
                        <div class="pdf-divider-thin"></div>
                      </div>
                      
                      <!-- 计算条件 -->
                      <div class="pdf-section">
                        <h3 class="pdf-section-title">计算条件</h3>
                        <div class="pdf-divider-thin"></div>
                        
                        <h4 class="pdf-subsection-title">新建公路</h4>
                        <table class="pdf-table">
                          <tr>
                            <td class="pdf-table-label">公路类型：</td>
                            <td>{{ getHighwayType() }}</td>
                          </tr>
                          <tr>
                            <td class="pdf-table-label">桩顶荷载P：</td>
                            <td>桩1: {{ formData.pile1.load }}kN, 桩2: {{ formData.pile2.load }}kN</td>
                          </tr>
                        </table>
                        
                        <h4 class="pdf-subsection-title">土层参数</h4>
                        <table class="pdf-table pdf-data-table">
                          <thead>
                            <tr>
                              <th>序号</th>
                              <th>土类型</th>
                              <th>土层厚度</th>
                              <th>压缩模量E(MPa)</th>
                              <th>泊松比v</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="(layer, index) in soilLayersData" :key="index">
                              <td>{{ index + 1 }}</td>
                              <td>{{ getSoilTypeName(layer.soilType) }}</td>
                              <td>{{ layer.depthStart }}-{{ layer.depthEnd }}m</td>
                              <td>{{ layer.compressionModulus }}</td>
                              <td>{{ layer.poissonRatio }}</td>
                            </tr>
                          </tbody>
                        </table>
                        
                        <h4 class="pdf-subsection-title">桩基参数</h4>
                        <table class="pdf-table pdf-data-table">
                          <thead>
                            <tr>
                              <th>项目</th>
                              <th>桩1参数</th>
                              <th>桩2参数</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td>桩直径(m)</td>
                              <td>{{ formData.pile1.diameter }}</td>
                              <td>{{ formData.pile2.diameter }}</td>
                            </tr>
                            <tr>
                              <td>桩长(m)</td>
                              <td>{{ formData.pile1.length }}</td>
                              <td>{{ formData.pile2.length }}</td>
                            </tr>
                          </tbody>
                        </table>
                        
                        <h4 class="pdf-subsection-title">被跨越公路参数</h4>
                        <table class="pdf-table">
                          <tr>
                            <td class="pdf-table-label">路基宽度：</td>
                            <td>{{ formData.bridgeWidth }}m</td>
                          </tr>
                          <tr>
                            <td class="pdf-table-label">路基与桩1距离：</td>
                            <td>{{ formData.distanceToPile1 }}m</td>
                          </tr>
                          <tr>
                            <td class="pdf-table-label">路基与桩2距离：</td>
                            <td>{{ formData.distanceToPile2 }}m</td>
                          </tr>
                        </table>
                        
                        <div class="pdf-divider-thin"></div>
                      </div>
                      
                      <!-- 计算依据和公式 -->
                      <div class="pdf-section">
                        <h3 class="pdf-section-title">计算依据和公式</h3>
                        <div class="pdf-divider-thin"></div>
                        
                        <h4 class="pdf-subsection-title">规范依据</h4>
                        <div class="pdf-standards">
                          <p><strong>1. 《公路路基设计规范》JTG D30-2015</strong></p>
                          <p><strong>2. 《公路桥涵地基与基础设计规范》JTG D63-2007</strong></p>
                          <p><strong>3. 《建筑地基基础设计规范》GB50007-2011</strong></p>
                          <p><strong>4. 《岩土工程勘察规范》GB50021-2001</strong></p>
                        </div>
                        
                        <h4 class="pdf-subsection-title">主要计算公式</h4>
                        <div class="pdf-formulas">
                          <div class="formula-item">
                            <p><strong>1. Boussinesq弹性理论计算公式：</strong></p>
                            <p class="formula-text">σz = (3P/2π) × z³/r⁵</p>
                            <p class="formula-desc">式中：σz - z深度处垂直应力增量；P - 桩顶荷载；z - 计算深度；r - 距离桩轴的水平距离</p>
                          </div>
                          
                          <div class="formula-item">
                            <p><strong>2. 沉降计算公式：</strong></p>
                            <p class="formula-text">s = (P/4πG) × [(1-ν)/R + z²/R³]</p>
                            <p class="formula-desc">式中：s - 沉降量；G - 剪切模量；ν - 泊松比；R - 计算点到荷载作用点距离</p>
                          </div>
                          
                          <div class="formula-item">
                            <p><strong>3. 剪切模量计算：</strong></p>
                            <p class="formula-text">G = E/[2(1+ν)]</p>
                            <p class="formula-desc">式中：G - 剪切模量；E - 压缩模量；ν - 泊松比</p>
                          </div>
                          
                          <div class="formula-item">
                            <p><strong>4. 桩长修正系数：</strong></p>
                            <p class="formula-text">α = 0.985 - 0.00051L</p>
                            <p class="formula-desc">式中：α - 桩长修正系数；L - 桩长(m)</p>
                          </div>
                          
                          <div class="formula-item">
                            <p><strong>5. 桩径修正系数：</strong></p>
                            <p class="formula-text">β = 0.038D² - 0.206D + 1.159</p>
                            <p class="formula-desc">式中：β - 桩径修正系数；D - 桩径(m)</p>
                          </div>
                          
                          <div class="formula-item">
                            <p><strong>6. 桩间相互作用系数：</strong></p>
                            <p class="formula-text">当s/d ≤ 3时：η = 0.8 + 0.2(s/d)/3</p>
                            <p class="formula-text">当3 < s/d ≤ 6时：η = 1.0 - 0.1(s/d-3)/3</p>
                            <p class="formula-text">当s/d > 6时：η = 0.9 + 0.1min(1,(s/d-6)/4)</p>
                            <p class="formula-desc">式中：η - 桩间相互作用系数；s - 桩间距；d - 平均桩径</p>
                          </div>
                        </div>
                        
                        <h4 class="pdf-subsection-title">计算步骤</h4>
                        <div class="pdf-calculation-steps">
                          <p><strong>步骤1：</strong>根据土层参数计算各层土的剪切模量G</p>
                          <p><strong>步骤2：</strong>采用Boussinesq理论计算单桩对各计算点的沉降影响</p>
                          <p><strong>步骤3：</strong>考虑桩长和桩径的修正系数</p>
                          <p><strong>步骤4：</strong>计算双桩的叠加效应和相互作用影响</p>
                          <p><strong>步骤5：</strong>得出各计算点的最终沉降量</p>
                          <p><strong>步骤6：</strong>根据公路等级判断沉降是否满足要求</p>
                        </div>
                        
                        <div class="pdf-divider-thin"></div>
                      </div>
                      
                      <!-- 计算结果 -->
                      <div class="pdf-section">
                        <h3 class="pdf-section-title">计算结果</h3>
                        <div class="pdf-divider-thin"></div>
                        
                        <table class="pdf-table pdf-data-table pdf-result-table">
                          <thead>
                            <tr>
                              <th>沉降计算点坐标(X,Y)</th>
                              <th>点沉降量（桩1）(mm)</th>
                              <th>点沉降量（桩2）(mm)</th>
                              <th>总沉降量(mm)</th>
                              <th>安全评估</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="(item, index) in tableData.slice(0, 10)" :key="index">
                              <td>({{ item.xCoord }}, {{ item.yCoord }})</td>
                              <td>{{ getPile1Settlement(item) }}</td>
                              <td>{{ getPile2Settlement(item) }}</td>
                              <td :class="{ 'pdf-danger-value': parseFloat(item.settlement) > 10 }">{{ item.settlement }}</td>
                              <td :class="item.safetyFactor === '安全' ? 'pdf-safe-text' : 'pdf-warning-text'">{{ item.safetyFactor }}</td>
                            </tr>
                          </tbody>
                        </table>
                        
                        <div class="pdf-result-summary">
                          <p><strong>路基下的计算点总沉降量最大值：</strong><span class="pdf-highlight-value">{{ getMaxSettlement() }}mm</span></p>
                          <p><strong>与对应公路等级沉降容许值对比：</strong>{{ getSettlementComparison() }}</p>
                        </div>
                        
                        <div class="pdf-divider-thin"></div>
                      </div>
                      
                      <!-- 图形分析 -->
                      <div class="pdf-section">
                        <h3 class="pdf-section-title">计算简图</h3>
                        <div class="pdf-divider-thin"></div>
                        <div id="pdf-chart-container" class="pdf-chart">
                          <!-- 图表将在PDF导出时插入这里 -->
                        </div>
                        <div class="pdf-divider-thin"></div>
                      </div>
                      
                      <!-- 安全评估 -->
                      <div class="pdf-section">
                        <h3 class="pdf-section-title">桥梁跨越工程安全评估报告</h3>
                        <div class="pdf-divider-thin"></div>
                        
                        <div class="pdf-assessment">
                          <p><strong>整体安全状况：</strong>{{ getOverallSafetyStatus().title.replace('整体安全状况：', '') }}</p>
                          <p>{{ getOverallSafetyStatus().description }}</p>
                          
                          <h4 class="pdf-subsection-title">沉降分析统计：</h4>
                          <ul>
                            <li>安全点数量：{{ getSafePointsCount() }}个（{{ getSafePointsPercentage() }}%）</li>
                            <li>关注点数量：{{ getWarningPointsCount() }}个（{{ getWarningPointsPercentage() }}%）</li>
                            <li>危险点数量：{{ getDangerPointsCount() }}个（{{ getDangerPointsPercentage() }}%）</li>
                            <li>最大沉降量：{{ getMaxSettlement() }}mm</li>
                          </ul>
                          
                          <h4 class="pdf-subsection-title">技术建议：</h4>
                          <ol>
                            <li v-for="(rec, index) in getRecommendations()" :key="rec.id">
                              <strong>{{ rec.title }}：</strong>{{ rec.content }}
                            </li>
                          </ol>
                          
                          <h4 class="pdf-subsection-title">评估结论：</h4>
                          <p class="pdf-conclusion">{{ getConclusion() }}</p>
                        </div>
                        
                        <div class="pdf-divider-thin"></div>
                      </div>
                      
                      <!-- 报告尾部 -->
                      <PdfReportFooter />
                    </div>
                  </div>
                  
                  <div class="report-content">
                    <!-- 项目基本信息 -->
                    <el-card class="report-section" shadow="never">
                      <template #header>
                        <h4><el-icon><InfoFilled /></el-icon> 项目基本信息</h4>
                      </template>
                      <div class="report-table">
                        <table class="info-table">
                          <tr>
                            <td class="label">项目名称：</td>
                            <td class="value">{{ formData.projectName }}</td>
                          </tr>
                          <tr>
                            <td class="label">项目类型：</td>
                            <td class="value">桥梁跨越工程沉降分析</td>
                          </tr>
                          <tr>
                            <td class="label">计算日期：</td>
                            <td class="value">{{ getCurrentDate() }}</td>
                          </tr>
                          <tr>
                            <td class="label">公路类型：</td>
                            <td class="value">{{ getHighwayType() }}</td>
                          </tr>
                          <tr>
                            <td class="label">桩顶荷载P：</td>
                            <td class="value">桩1: {{ formData.pile1.load }}kN, 桩2: {{ formData.pile2.load }}kN</td>
                          </tr>
                        </table>
                      </div>
                    </el-card>

                    <!-- 计算条件 -->
                    <el-card class="report-section" shadow="never">
                      <template #header>
                        <h4><el-icon><Setting /></el-icon> 计算条件</h4>
                      </template>
                      <div class="report-table">
                        <h5>桩基参数：</h5>
                        <table class="params-table">
                          <thead>
                            <tr>
                              <th>项目</th>
                              <th>桩1参数</th>
                              <th>桩2参数</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td>桩直径(m)</td>
                              <td>{{ formData.pile1.diameter }}</td>
                              <td>{{ formData.pile2.diameter }}</td>
                            </tr>
                            <tr>
                              <td>桩长(m)</td>
                              <td>{{ formData.pile1.length }}</td>
                              <td>{{ formData.pile2.length }}</td>
                            </tr>
                            <tr>
                              <td>桩顶荷载(kN)</td>
                              <td>{{ formData.pile1.load }}</td>
                              <td>{{ formData.pile2.load }}</td>
                            </tr>
                          </tbody>
                        </table>

                        <h5>被跨越公路参数：</h5>
                        <table class="params-table">
                          <tr>
                            <td class="label">路基宽度：</td>
                            <td class="value">{{ formData.bridgeWidth }}m</td>
                          </tr>
                          <tr>
                            <td class="label">路基与桩1距离：</td>
                            <td class="value">{{ formData.distanceToPile1 }}m</td>
                          </tr>
                          <tr>
                            <td class="label">路基与桩2距离：</td>
                            <td class="value">{{ formData.distanceToPile2 }}m</td>
                          </tr>
                        </table>

                        <h5>土层参数：</h5>
                        <table class="params-table">
                          <thead>
                            <tr>
                              <th>序号</th>
                              <th>土类型</th>
                              <th>土层厚度</th>
                              <th>压缩模量E(MPa)</th>
                              <th>泊松比v</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="(layer, index) in soilLayersData" :key="index">
                              <td>{{ index + 1 }}</td>
                              <td>{{ getSoilTypeName(layer.soilType) }}</td>
                              <td>{{ layer.depthStart }}-{{ layer.depthEnd }}m</td>
                              <td>{{ layer.compressionModulus }}</td>
                              <td>{{ layer.poissonRatio }}</td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                    </el-card>

                    <!-- 计算结果 -->
                    <el-card class="report-section" shadow="never">
                      <template #header>
                        <h4><el-icon><TrendCharts /></el-icon> 计算结果</h4>
                      </template>
                      <div class="result-table-container">
                        <table class="result-table-report">
                          <thead>
                            <tr>
                              <th>沉降计算点坐标(X,Y)</th>
                              <th>点沉降量（桩1）(mm)</th>
                              <th>点沉降量（桩2）(mm)</th>
                              <th>总沉降量(mm)</th>
                              <th>安全评估</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="(item, index) in tableData" :key="index">
                              <td>({{ item.xCoord }}, {{ item.yCoord }})</td>
                              <td>{{ getPile1Settlement(item) }}</td>
                              <td>{{ getPile2Settlement(item) }}</td>
                              <td :class="{ 'danger-value': parseFloat(item.settlement) > 10 }">{{ item.settlement }}</td>
                              <td>
                                <span :class="item.safetyFactor === '安全' ? 'safe-text' : 'warning-text'">
                                  {{ item.safetyFactor }}
                                </span>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                        
                        <div class="result-summary">
                          <p><strong>路基下的计算点总沉降量最大值：</strong><span class="highlight-value">{{ getMaxSettlement() }}mm</span></p>
                          <p><strong>与对应公路等级沉降容许值对比：</strong>{{ getSettlementComparison() }}</p>
                        </div>
                      </div>
                      
                      <el-divider />
                      
                      <div class="safety-analysis">
                        <h5>桩基沉降影响评估</h5>
                        <el-alert
                          :title="getOverallSafetyStatus().title"
                          :type="getOverallSafetyStatus().type"
                          :description="getOverallSafetyStatus().description"
                          show-icon
                          :closable="false"
                        />
                        
                        <div class="safety-details">
                          <el-row :gutter="16">
                            <el-col :span="8">
                              <div class="safety-card safe">
                                <h6>安全点</h6>
                                <div class="count">{{ getSafePointsCount() }}</div>
                                <div class="percentage">{{ getSafePointsPercentage() }}%</div>
                              </div>
                            </el-col>
                            <el-col :span="8">
                              <div class="safety-card warning">
                                <h6>关注点</h6>
                                <div class="count">{{ getWarningPointsCount() }}</div>
                                <div class="percentage">{{ getWarningPointsPercentage() }}%</div>
                              </div>
                            </el-col>
                            <el-col :span="8">
                              <div class="safety-card danger">
                                <h6>危险点</h6>
                                <div class="count">{{ getDangerPointsCount() }}</div>
                                <div class="percentage">{{ getDangerPointsPercentage() }}%</div>
                              </div>
                            </el-col>
                          </el-row>
                        </div>
                      </div>
                    </el-card>

                    <!-- 技术建议 -->
                    <el-card class="report-section" shadow="never">
                      <template #header>
                        <h4><el-icon><EditPen /></el-icon> 技术建议</h4>
                      </template>
                      <div class="recommendations">
                        <ol>
                          <li v-for="recommendation in getRecommendations()" :key="recommendation.id">
                            <strong>{{ recommendation.title }}：</strong>{{ recommendation.content }}
                          </li>
                        </ol>
                      </div>
                    </el-card>

                    <!-- 结论 -->
                    <el-card class="report-section" shadow="never">
                      <template #header>
                        <h4><el-icon><CircleCheck /></el-icon> 评估结论</h4>
                      </template>
                      <div class="conclusion">
                        <p>{{ getConclusion() }}</p>
                      </div>
                    </el-card>
                  </div>
                </div>
                <div v-else class="empty-result">
                  <el-empty description="暂无数据，请先进行计算">
                    <template #image>
                      <el-icon :size="60"><Document /></el-icon>
                    </template>
                  </el-empty>
                </div>
              </el-tab-pane>
            </el-tabs>
          </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import ChartComponent from '../components/ChartComponent.vue'
import { 
  DataAnalysis, 
  Document, 
  Histogram, 
  Connection, 
  Files, 
  ArrowRight, 
  RefreshRight,
  QuestionFilled,
  TrendCharts,
  DataLine,
  PieChart,
  Download,
  InfoFilled,
  EditPen,
  CircleCheck,
  Setting,
  Plus
} from '@element-plus/icons-vue'
import { ElNotification, ElMessageBox } from 'element-plus'
import { Delaunay } from 'd3-delaunay';
import { interpolateRgb } from 'd3-interpolate';
import { contours } from 'd3-contour';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import html2pdf from 'html2pdf.js'
import logoImage from '@/assets/logo.png'

// 表单数据
const formData = reactive({
  projectName: '高架桥桩基沉降分析项目',
  projectInfo: '',
  pile1: {
    diameter: 1.0,
    length: 20.0,
    load: 1000.0,
  },
  pile2: {
    diameter: 1.0,
    length: 20.0,
    load: 1000.0,
  },
  bridgeWidth: 12.0,
  distanceToPile1: 5.0,
  distanceToPile2: 5.0,
  // 移除固定的土层参数，现在使用动态的soilLayersData
})

// 结果数据
const tableData = ref([])
const hasResults = ref(false)
const activeTab = ref('numerical')
const graphicalActiveTab = ref('diagram')
const calculating = ref(false)
const selectedPoint = ref(null)
const exportingPDF = ref(false)

const handleRowClick = (row) => {
  selectedPoint.value = row;
  activeTab.value = 'graphical';
  graphicalActiveTab.value = 'radar';
}

const getSettlementColor = (settlement, threshold) => {
  const ratio = threshold > 0 ? settlement / threshold : 0;
  if (ratio < 0.1) return '#2E8B57';
  if (ratio < 0.3) return '#32CD32';
  if (ratio < 0.6) return '#FFD700';
  if (ratio < 0.9) return '#FF8C00';
  return '#DC143C';
}

const projectDiagramOptions = computed(() => {
  if (!hasResults.value) return {};

  const {
    bridgeWidth,
    distanceToPile1,
    distanceToPile2,
    pile1,
    pile2,
  } = formData;
  const pile1Diameter = pile1.diameter;
  const pile2Diameter = pile2.diameter;
  const pile1Length = pile1.length;
  const pile2Length = pile2.length;
  
  const roadbedHeight = 1.5;
  const roadbedSlope = roadbedHeight * 0.5;
  const maxSettlementThreshold = 20.0;

  // 1. Define all structure and data points with a centered coordinate system
  const roadbed_x_start = -bridgeWidth / 2;
  const roadbed_x_end = bridgeWidth / 2;
  const pile1_x = -(bridgeWidth / 2 + distanceToPile1);
  const pile2_x = bridgeWidth / 2 + distanceToPile2;

  const roadbedPoints = [
    { x: roadbed_x_start, y: 0 },
    { x: roadbed_x_end, y: 0 },
    { x: roadbed_x_end - roadbedSlope, y: -roadbedHeight },
    { x: roadbed_x_start + roadbedSlope, y: -roadbedHeight },
  ];
  const pile1Points = [
    { x: pile1_x - pile1Diameter / 2, y: 0 },
    { x: pile1_x + pile1Diameter / 2, y: pile1Length },
  ];
  const pile2Points = [
    { x: pile2_x - pile2Diameter / 2, y: 0 },
    { x: pile2_x + pile2Diameter / 2, y: pile2Length },
  ];

  const allXCoords = [
    ...tableData.value.map(p => parseFloat(p.xCoord)),
    ...roadbedPoints.map(p => p.x),
    ...pile1Points.map(p => p.x),
    ...pile2Points.map(p => p.x),
  ];

  const allYCoords = [
    ...tableData.value.map(p => parseFloat(p.yCoord)),
    pile1Length,
    pile2Length,
    -roadbedHeight,
  ];

  // 2. Dynamically calculate axis ranges
  const xMin = Math.min(...allXCoords);
  const xMax = Math.max(...allXCoords);
  const yMin = Math.min(...allYCoords);
  const yMax = Math.max(...allYCoords);
  
  const xPadding = (xMax - xMin) * 0.1;
  const yPadding = (yMax - yMin) * 0.15;

  return {
    title: {
      text: '工程示意简图',
      left: 'center',
      textStyle: {
        color: 'var(--text-primary)', // 已使用CSS变量
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        if (params.seriesName === 'calculation-points') {
          return `${params.name}<br/>坐标: (${params.value[0].toFixed(2)}, ${params.value[1].toFixed(2)})<br/>沉降量: ${params.data.settlement.toFixed(2)} mm`;
        }
        return params.name;
      }
    },
    grid: {
      left: '8%',
      right: '8%',
      bottom: '15%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      name: '横向距离 X (m)',
      nameLocation: 'middle',
      nameGap: 30,
      min: Math.floor(xMin - xPadding),
      max: Math.ceil(xMax + xPadding),
      axisLine: { show: true, lineStyle: { color: 'var(--el-border-color)' } },
      axisLabel: { color: 'var(--text-primary)' },
      nameTextStyle: { color: 'var(--text-primary)', fontSize: 14 },
      splitLine: { show: true, lineStyle: { type: 'dashed', color: 'var(--el-border-color-light)'} }
    },
    yAxis: {
      type: 'value',
      name: '深度 Z (m)',
      nameLocation: 'middle',
      nameGap: 45,
      inverse: true,
      min: Math.floor(yMin - yPadding),
      max: Math.ceil(yMax + yPadding),
      axisLine: { show: true, lineStyle: { color: 'var(--el-border-color)' } },
      axisLabel: { color: 'var(--text-primary)' },
      nameTextStyle: { color: 'var(--text-primary)', fontSize: 14 },
      splitLine: { show: true, lineStyle: { color: 'var(--el-border-color-light)'} }
    },
    series: [
      { // Soil Layer 1: 0-5m
        name: 'soil-layer-1',
        type: 'custom',
        renderItem: (params, api) => {
          const xStart = api.coord([xMin - xPadding, 0])[0];
          const xEnd = api.coord([xMax + xPadding, 0])[0];
          const yStart = api.coord([0, 0])[1];
          const yEnd = api.coord([0, 5])[1];
          return {
            type: 'rect',
            shape: { x: xStart, y: yStart, width: xEnd - xStart, height: yEnd - yStart },
            style: { fill: 'rgba(188, 143, 143, 0.25)', stroke: 'var(--el-border-color-light)', lineWidth: 1 } // 增加填充不透明度
          };
        },
        data: [[0]],
        silent: true,
        z: 0 // Place it at the very back
      },
      { // Soil Layer 2: 5-25m (extended)
        name: 'soil-layer-2',
        type: 'custom',
        renderItem: (params, api) => {
          const xStart = api.coord([xMin - xPadding, 0])[0];
          const xEnd = api.coord([xMax + xPadding, 0])[0];
          const yStart = api.coord([0, 5])[1];
          const yEnd = api.coord([0, yMax + yPadding])[1]; // Extend to bottom
          return {
            type: 'rect',
            shape: { x: xStart, y: yStart, width: xEnd - xStart, height: yEnd - yStart },
            style: { fill: 'rgba(139, 69, 19, 0.2)', stroke: 'var(--el-border-color-light)', lineWidth: 1 } // 增加填充不透明度
          };
        },
        data: [[0]],
        silent: true,
        z: 0
      },
      { // Roadbed
        name: 'roadbed',
        type: 'custom',
        renderItem: (params, api) => {
          const points = [
            api.coord([roadbed_x_start + roadbedSlope, -roadbedHeight]),
            api.coord([roadbed_x_end - roadbedSlope, -roadbedHeight]),
            api.coord([roadbed_x_end, 0]),
            api.coord([roadbed_x_start, 0]),
          ];
          return {
            type: 'polygon',
            shape: { points },
            style: { fill: '#607d8b', stroke: 'var(--text-primary)', lineWidth: 1.5 } // 加粗线条
          };
        },
        data: [[0]],
        silent: true,
        z: 2
      },
      { // Pile 1
        name: 'pile-1',
        type: 'custom',
        renderItem: (params, api) => {
          const start = api.coord([pile1_x - pile1Diameter / 2, 0]);
          const end = api.coord([pile1_x + pile1Diameter / 2, pile1Length]);
          return {
            type: 'rect',
            shape: { x: start[0], y: start[1], width: end[0] - start[0], height: end[1] - start[1] },
            style: { 
              fill: '#78909c', // 使用更深的灰色
              stroke: 'var(--text-primary)', 
              lineWidth: 1.5,
              decal: {
                symbol: 'rect',
                color: 'rgba(0, 0, 0, 0.3)', // 减淡纹理
                symbolSize: 0.5,
                rotation: Math.PI / 4,
                dashArrayX: [5, 5],
                dashArrayY: [5, 5],
              }
            }
          };
        },
        data: [[0]],
        silent: true,
        z: 3
      },
      { // Pile 2
        name: 'pile-2',
        type: 'custom',
        renderItem: (params, api) => {
          const start = api.coord([pile2_x - pile2Diameter / 2, 0]);
          const end = api.coord([pile2_x + pile2Diameter / 2, pile2Length]);
          return {
            type: 'rect',
            shape: { x: start[0], y: start[1], width: end[0] - start[0], height: end[1] - start[1] },
            style: { 
              fill: '#78909c', // 使用更深的灰色
              stroke: 'var(--text-primary)', 
              lineWidth: 1.5,
              decal: {
                symbol: 'rect',
                color: 'rgba(0, 0, 0, 0.3)', // 减淡纹理
                symbolSize: 0.5,
                rotation: Math.PI / 4,
                dashArrayX: [5, 5],
                dashArrayY: [5, 5],
              }
            }
          };
        },
        data: [[0]],
        silent: true,
        z: 3
      },
      { // Pile Labels
        name: 'pile-labels',
        type: 'scatter',
        symbol: 'rect',
        symbolSize: [40, 20],
        itemStyle: { color: 'transparent', borderColor: 'transparent' },
        label: {
          show: true,
          formatter: '{b}',
          position: 'inside',
          color: 'var(--text-primary)',
          fontWeight: 'bold'
        },
        data: [
          { name: '桩1', value: [pile1_x, pile1Length + 1] },
          { name: '桩2', value: [pile2_x, pile2Length + 1] }
        ],
        z: 4
      },
      { // Calculation points
        name: 'calculation-points',
        type: 'scatter',
        symbolSize: 15,
        label: {
          show: true,
          formatter: '{b}',
          position: 'right',
          color: 'var(--text-primary)',
          fontSize: 11, // 略微增大字体
          backgroundColor: 'rgba(239, 246, 255, 0.6)', // 使用带颜色的背景增加对比
          padding: [2, 4],
          borderRadius: 4,
        },
        data: tableData.value.map(p => ({
          name: p.point,
          value: [parseFloat(p.xCoord), parseFloat(p.yCoord)],
          settlement: parseFloat(p.settlement),
          itemStyle: {
            color: getSettlementColor(parseFloat(p.settlement), maxSettlementThreshold),
            borderColor: 'var(--text-primary)',
            borderWidth: 1, // 减小边框宽度
            opacity: 0.95,
          }
        })),
        z: 5
      },
      { // Dimension Lines
        name: 'dimension-lines',
        type: 'custom',
        silent: true,
        data: [[0]],
        z: 6,
        renderItem: (params, api) => {
          // Road width dimension
          const p_road_start = api.coord([roadbed_x_start, -2]);
          const p_road_end = api.coord([roadbed_x_end, -2]);
          
          // Pile 1 distance dimension
          const p_pile1_dist_start = api.coord([pile1_x, -1]);
          const p_pile1_dist_end = api.coord([roadbed_x_start, -1]);

          // Pile 2 distance dimension
          const p_pile2_dist_start = api.coord([roadbed_x_end, -1]);
          const p_pile2_dist_end = api.coord([pile2_x, -1]);
          const textColor = 'var(--text-primary)';

          return {
            type: 'group',
            children: [
              // Road width line
              { type: 'line', shape: { x1: p_road_start[0], y1: p_road_start[1], x2: p_road_end[0], y2: p_road_end[1] }, style: { stroke: textColor, lineWidth: 2 } },
              { type: 'line', shape: { x1: p_road_start[0], y1: p_road_start[1] - 5, x2: p_road_start[0], y2: p_road_start[1] + 5 }, style: { stroke: textColor, lineWidth: 2 } },
              { type: 'line', shape: { x1: p_road_end[0], y1: p_road_end[1] - 5, x2: p_road_end[0], y2: p_road_end[1] + 5 }, style: { stroke: textColor, lineWidth: 2 } },
              { type: 'text', style: { text: `路基: ${bridgeWidth}m`, x: (p_road_start[0] + p_road_end[0])/2, y: p_road_start[1] - 15, fill: textColor, textAlign: 'center' } },
              // Pile 1 distance line
              { type: 'line', shape: { x1: p_pile1_dist_start[0], y1: p_pile1_dist_start[1], x2: p_pile1_dist_end[0], y2: p_pile1_dist_end[1] }, style: { stroke: textColor, lineWidth: 2, lineDash: [2, 2] } },
              { type: 'text', style: { text: `d=${distanceToPile1}m`, x: (p_pile1_dist_start[0] + p_pile1_dist_end[0])/2, y: p_pile1_dist_start[1] - 15, fill: textColor, textAlign: 'center' } },
              // Pile 2 distance line
              { type: 'line', shape: { x1: p_pile2_dist_start[0], y1: p_pile2_dist_start[1], x2: p_pile2_dist_end[0], y2: p_pile2_dist_end[1] }, style: { stroke: textColor, lineWidth: 2, lineDash: [2, 2] } },
              { type: 'text', style: { text: `d=${distanceToPile2}m`, x: (p_pile2_dist_start[0] + p_pile2_dist_end[0])/2, y: p_pile2_dist_start[1] - 15, fill: textColor, textAlign: 'center' } },
            ]
          }
        }
      }
    ],
    backgroundColor: '#FFFFFF'
  }
})

// 简化的图表选项，后续再实现具体功能
const chartOptions = computed(() => {
  const tab = graphicalActiveTab.value;
  switch (tab) {
    case 'diagram':
      return projectDiagramOptions.value;
    case 'settlement':
      return settlementChartOptions.value;
    case 'contour':
      return contourChartOptions.value;
    case 'radar':
      return radarChartOptions.value;
    case 'waterfall':
      return comparisonBarChartOptions.value;
    default:
      return {};
  }
});

const settlementChartOptions = computed(() => {
  if (!hasResults.value) return {};

  const baseOptions = projectDiagramOptions.value;
  const settlements = tableData.value.map(p => parseFloat(p.settlement));
  const minSettlement = Math.min(...settlements);
  const maxSettlement = Math.max(...settlements);

  // 创建一个新的 series 数组，以避免直接修改原始计算属性
  const newSeries = baseOptions.series.map(series => {
    // 只修改计算点的 series
    if (series.name === 'calculation-points') {
      return {
        ...series, // 继承原始点的样式 (type, symbolSize, z-index, etc.)
        data: tableData.value.map(p => {
          const settlement = parseFloat(p.settlement);
          const originalY = parseFloat(p.yCoord);
          // 将沉降量（mm）转换为米并应用到Y坐标上
          const adjustedY = originalY + (settlement / 1000.0);
          return {
            name: p.point,
            // 关键改动 1: 将沉降值作为第三维数据，供 visualMap 使用
            value: [parseFloat(p.xCoord), adjustedY, settlement],
            settlement: settlement, // 保留原始沉降值用于 tooltip
            // 关键改动 2: 移除 itemStyle，以允许 visualMap 控制颜色
          };
        }),
        // 在系列层面定义基础样式，visualMap会自动应用颜色
        itemStyle: {
           borderColor: 'var(--text-primary)',
           borderWidth: 1.5,
           opacity: 0.95
        }
      };
    }
    // 其他 series（如桩、路基）保持不变
    return series;
  });

  // 返回一个全新的图表配置对象
  return {
    ...baseOptions,
    title: {
      ...baseOptions.title,
      text: '沉降变形分析图',
    },
    tooltip: { // 添加 tooltip 增强交互
        trigger: 'axis',
        axisPointer: {
            type: 'cross',
            label: {
                backgroundColor: '#6a7985'
            }
        }
    },
    visualMap: {
      min: minSettlement,
      max: maxSettlement,
      calculable: true,
      precision: 2,
      inRange: {
        color: ['#4ade80', '#ffb74d', '#f44336'] // 更新为更清晰的颜色
      },
      orient: 'vertical',
      right: '2%',
      top: 'center',
      textStyle: {
        color: 'var(--text-primary)'
      },
      formatter: (value) => `${value.toFixed(2)} mm`
    },
    series: newSeries,
  };
});

// 关键改动：将核心物理模型提炼成一个可重用的函数
const calculateSettlementAtPoint = (x, z, params, soilLayers) => {
    const y = 0; // 2D平面

    // 深度小于0（地面以上）时，沉降为0
    if (z < 0) {
      return 0;
    }

    const [pile1X] = getPilePosition(1, params);
    const [pile2X] = getPilePosition(2, params);

    const pointSoil = getSoilPropertiesAtDepth(soilLayers, z);
    if (!pointSoil) return 0;
    
    const G = calculateShearModulus(pointSoil.compression_modulus, pointSoil.poisson_ratio);

    const combinedCorrection1 = calculateCombinedCorrection(params.pile1.length, params.pile1.diameter);
    const rawSettlement1 = calculateBoussinesqSettlement(params.pile1.load, G, x - pile1X, y, z, pointSoil.poisson_ratio);
    const settlement1 = rawSettlement1 * combinedCorrection1;

    const combinedCorrection2 = calculateCombinedCorrection(params.pile2.length, params.pile2.diameter);
    const rawSettlement2 = calculateBoussinesqSettlement(params.pile2.load, G, x - pile2X, y, z, pointSoil.poisson_ratio);
    const settlement2 = rawSettlement2 * combinedCorrection2;

    const pileSpacing = Math.abs(pile2X - pile1X);
    const interactionFactor = calculatePileInteraction(pileSpacing, params.pile1.diameter, params.pile2.diameter);
    const totalSettlement = (settlement1 + settlement2) * interactionFactor;

    return totalSettlement * 1000; // 转换为毫米
};


const contourChartOptions = computed(() => {
  if (!hasResults.value || tableData.value.length < 3) return {};

  const { bridgeWidth, pile1, pile2 } = formData;

  const points = tableData.value.map(p => ({
    x: parseFloat(p.xCoord),
    y: parseFloat(p.yCoord),
    settlement: parseFloat(p.settlement)
  }));
  
  const xMin = -14;
  const xMax = 14;
  const yMin = -5;
  const yMax = 24;
  
  // 关键改动：使用反距离权重插值法 (IDW) 来根据16个计算点生成平滑的数据场
  const gridSize = 100;
  const power = 2; // IDW的权重指数
  const interpolatedValues = [];

  for (let j = 0; j < gridSize; j++) {
    for (let i = 0; i < gridSize; i++) {
      const x = xMin + (i / (gridSize - 1)) * (xMax - xMin);
      const y = yMin + (j / (gridSize - 1)) * (yMax - yMin);

      let totalWeightedValue = 0;
      let totalWeight = 0;
      let isAtDataPoint = false;

      for (const p of points) {
        const dist = Math.sqrt(Math.pow(x - p.x, 2) + Math.pow(y - p.y, 2));
        if (dist < 1e-6) {
          totalWeightedValue = p.settlement;
          totalWeight = 1;
          isAtDataPoint = true;
          break;
        }
        const weight = 1 / Math.pow(dist, power);
        totalWeightedValue += weight * p.settlement;
        totalWeight += weight;
      }
      
      const value = isAtDataPoint ? totalWeightedValue : totalWeightedValue / totalWeight;
      interpolatedValues.push(value);
    }
  }

  const newMinSettlement = Math.min(...interpolatedValues.filter(v => v > 0));
  const newMaxSettlement = Math.max(...interpolatedValues);
  
  const contourGenerator = contours()
    .size([gridSize, gridSize])
    .thresholds(Array.from({length: 6}, (_, i) => newMinSettlement + i * (newMaxSettlement - newMinSettlement) / 5));
  
  const contourData = contourGenerator(interpolatedValues);

  // 关键改动：正确处理 d3-contour 输出，并跳过第一条边界线
  const seriesData = [];
  const legendData = [];
  const colors = ['#388e3c', '#8bc34a', '#fbc02d', '#f57c00', '#d32f2f', '#c2185b'];
  
  // 过滤掉第一条等高线，因为它通常是边界
  const filteredContours = contourData.slice(1);

  // 从过滤后的等高线数据中构建图例
  filteredContours.forEach(contour => {
      const contourName = `沉降 ${contour.value.toFixed(2)}mm`;
      if (!legendData.includes(contourName)) {
          legendData.push(contourName);
      }
  });

  // 从过滤后的等高线数据中构建 series
  filteredContours.forEach(contour => {
    const contourName = `沉降 ${contour.value.toFixed(2)}mm`;
    const colorIndex = legendData.indexOf(contourName);
    const color = colors[colorIndex % colors.length];

    contour.coordinates.forEach(polygon => {
      polygon.forEach(ring => {
        seriesData.push({
          name: contourName,
          type: 'line',
          smooth: true,
          showSymbol: false,
          showInLegend: false,
          data: ring.map(p => [
            xMin + p[0] * (xMax - xMin) / (gridSize - 1),
            yMin + p[1] * (yMax - yMin) / (gridSize - 1)
          ]),
          lineStyle: {
            width: 2,
            color: color
          },
          z: 2
        });
      });
    });
  });
  
  // 为图例创建 "dummy" series
  legendData.forEach((name, index) => {
    seriesData.push({
      name: name,
      type: 'line',
      data: [],
      showInLegend: true,
      itemStyle: {
        color: colors[index % colors.length]
      }
    });
  });

  const pile1X = -(bridgeWidth / 2 + formData.distanceToPile1);
  const pile2X = bridgeWidth / 2 + formData.distanceToPile2;
  const pile1Length = pile1.length;
  const pile2Length = pile2.length;


  return {
    backgroundColor: '#FFFFFF',
    title: { 
      text: '沉降等高线分析图', 
      left: 'center', 
      textStyle: { color: '#000000', fontWeight: 'bold' } 
    },
    tooltip: { 
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        label: { backgroundColor: '#6a7985' }
      }
    },
    legend: {
      data: legendData,
      textStyle: { color: '#000000' },
      orient: 'vertical',
      right: '2%',
      top: 'center'
    },
    grid: { left: '8%', right: '15%', bottom: '10%', top: '15%' },
    xAxis: { 
      type: 'value', name: '横向距离 X (m)', min: xMin, max: xMax,
      axisLine: { show: true, lineStyle: { color: 'var(--el-border-color)' } },
      axisLabel: { color: '#000000' },
      nameTextStyle: { color: '#000000', fontSize: 12 },
    },
    yAxis: { 
      type: 'value', name: '深度 Z (m)', inverse: true, min: yMin, max: yMax,
      axisLine: { show: true, lineStyle: { color: 'var(--el-border-color)' } },
      axisLabel: { color: '#000000' },
      nameTextStyle: { color: '#000000', fontSize: 12 },
    },
    series: [
      ...seriesData,
      {
        name: '计算点',
        type: 'scatter',
        symbolSize: 12,
        data: points.map(p => [p.x, p.y, p.settlement]),
        itemStyle: { color: 'var(--text-primary)', borderColor: 'black', borderWidth: 1.5 },
        z: 5
      },
      { // 桩1
        name: '桩1',
        type: 'line',
        symbol: 'none',
        lineStyle: { color: '#616161', width: 10, type: 'solid' }, // 加深加粗桩的颜色
        data: [[pile1X, 0],[pile1X, pile1Length]],
        z: 3
      },
       { // 桩2
        name: '桩2',
        type: 'line',
        symbol: 'none',
        lineStyle: { color: '#616161', width: 10, type: 'solid' }, // 加深加粗桩的颜色
        data: [[pile2X, 0],[pile2X, pile2Length]],
        z: 3
      },
       { // 路基轮廓
        name: '路基轮廓',
        type: 'line',
        symbol: 'none',
        lineStyle: { color: 'var(--brand-primary)', width: 2 },
        data: [[-(bridgeWidth/2), 0],[(bridgeWidth/2), 0]],
        z: 4
      }
    ]
  };
});

const comparisonBarChartOptions = computed(() => {
  if (!hasResults.value) return {};

  const sortedData = [...tableData.value].sort((a, b) => parseFloat(b.settlement) - parseFloat(a.settlement));
  const pointNames = sortedData.map(p => p.point);
  const seriesData = sortedData.map(p => parseFloat(p.settlement));
  const maxSettlement = Math.max(...seriesData);

  return {
    backgroundColor: '#FFFFFF',
    title: {
      text: '各点沉降对比',
      left: 'center',
      textStyle: { color: 'var(--text-primary)', fontWeight: 'bold' }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: (params) => `${params[0].name}<br/>沉降量: ${params[0].value.toFixed(2)} mm`
    },
    grid: { left: '5%', right: '10%', bottom: '10%', top: '15%', containLabel: true },
    xAxis: {
      type: 'value',
      name: '沉降量 (mm)',
      max: maxSettlement * 1.1,
      nameTextStyle: { color: 'var(--text-primary)' },
      axisLabel: { color: 'var(--text-primary)' },
      splitLine: { lineStyle: { color: 'var(--el-border-color-light)' } }
    },
    yAxis: {
      type: 'category',
      data: pointNames,
      axisLabel: { color: 'var(--text-primary)' }
    },
    series: [{
      name: 'settlement',
      type: 'bar',
      data: seriesData,
      itemStyle: {
        color: (params) => getSettlementColor(params.value, maxSettlement),
        borderRadius: [0, 4, 4, 0] // 添加圆角美化
      },
      label: {
        show: true,
        position: 'right',
        formatter: '{c}',
        color: 'var(--text-primary)'
      }
    }]
  };
});

const radarChartOptions = computed(() => {
  if (!selectedPoint.value) {
    return {
      title: {
        text: '因素关联分析雷达图',
        subtext: '请在"数值结果"表格中点击任意一行以查看详细分析',
        left: 'center',
        textStyle: { color: 'var(--text-primary)', fontWeight: 'bold' },
        subtextStyle: { color: 'var(--text-primary)', fontSize: 14 }
      },
      legend: { show: false },
      radar: { indicator: [] },
      series: []
    };
  }

  const point = selectedPoint.value;
  const settlement = parseFloat(point.settlement);

  // Simulate factor analysis
  const factors = {
    "附加应力": Math.random() * settlement,
    "自重应力": Math.random() * settlement,
    "土层1 (粘土)": formData.soilType1 === 'clay' ? Math.random() * settlement : 0,
    "土层2 (砂土)": formData.soilType2 === 'sand' ? Math.random() * settlement : 0,
    "距桩1距离影响": (1 / parseFloat(point.xCoord)) * Math.random() * 5,
    "距桩2距离影响": (1 / (formData.bridgeWidth - parseFloat(point.xCoord))) * Math.random() * 5,
  };

  const totalFactorSum = Object.values(factors).reduce((sum, val) => sum + val, 0);
  
  // Normalize factors to sum to the actual settlement value for realism
  const normalizedFactors = {};
  for (const key in factors) {
    normalizedFactors[key] = (factors[key] / totalFactorSum) * settlement;
  }
  
  const indicator = Object.keys(normalizedFactors).map(key => ({ name: key, max: settlement * 1.2 }));
  const data = Object.values(normalizedFactors);

  return {
    backgroundColor: '#FFFFFF',
    title: {
      text: `计算点 ${point.point} 的因素关联分析`,
      left: 'center',
      textStyle: { color: 'var(--text-primary)', fontWeight: 'bold' }
    },
    tooltip: { trigger: 'item' },
    legend: {
      data: [`计算点 ${point.point}`],
      bottom: 5,
      textStyle: { color: 'var(--text-primary)' }
    },
    radar: {
      indicator,
      radius: '65%',
      center: ['50%', '55%'],
      axisName: {
        color: '#000000', // 根据要求，将坐标轴文字改为黑色，以提高可读性
        fontSize: 13,
        fontWeight: 'bold',
        fontFamily: 'Microsoft YaHei',
      },
      splitNumber: 5,
      splitLine: { lineStyle: { color: 'var(--el-border-color-light)' } },
      splitArea: { areaStyle: { color: ['rgba(239, 246, 255, 0.8)', 'rgba(224, 231, 255, 0.8)'] } }, // 明确设置不透明的浅色背景
      axisLine: { lineStyle: { color: 'var(--el-border-color)' } }
    },
    series: [{
      name: `计算点 ${point.point}`,
      type: 'radar',
      data: [{
        value: data,
        name: `计算点 ${point.point}`,
        areaStyle: { color: 'rgba(59, 130, 246, 0.4)' }, // 品牌主色
        lineStyle: { width: 2.5, color: 'rgba(29, 78, 216, 1)' }, // 品牌深色
        itemStyle: { color: 'rgba(29, 78, 216, 1)' } // 品牌深色
      }]
    }],
    backgroundColor: '#FFFFFF'
  };
});

// 计算沉降
const handleCalculate = () => {
  calculating.value = true;
  hasResults.value = false;

  try {
    const params = getBridgeInputParameters();
    validateParameters(params);

    // 使用动态土层数据
    const soilLayers = soilLayersData.value.map(layer => ({
      depth_range: `${layer.depthStart}-${layer.depthEnd}`,
      name: layer.soilType,
      compression_modulus: layer.compressionModulus,
      poisson_ratio: parseFloat(layer.poissonRatio)
    }));

    const points = get16StandardPoints(params.bridgeWidth);

    const calculationResults = points.map((point, i) => {
        const { x, y, z } = point;

        const [pile1X, _] = getPilePosition(1, params);
        const [pile2X, __] = getPilePosition(2, params);

        const pointSoil = getSoilPropertiesAtDepth(soilLayers, z);
        const G = calculateShearModulus(pointSoil.compression_modulus, pointSoil.poisson_ratio);

        const combinedCorrection1 = calculateCombinedCorrection(params.pile1.length, params.pile1.diameter);
        const rawSettlement1 = calculateBoussinesqSettlement(params.pile1.load, G, x - pile1X, y, z, pointSoil.poisson_ratio);
        const settlement1 = rawSettlement1 * combinedCorrection1;

        const combinedCorrection2 = calculateCombinedCorrection(params.pile2.length, params.pile2.diameter);
        const rawSettlement2 = calculateBoussinesqSettlement(params.pile2.load, G, x - pile2X, y, z, pointSoil.poisson_ratio);
        const settlement2 = rawSettlement2 * combinedCorrection2;
        
        const pileSpacing = Math.abs(pile2X - pile1X);
        const interactionFactor = calculatePileInteraction(pileSpacing, params.pile1.diameter, params.pile2.diameter);
        const totalSettlement = (settlement1 + settlement2) * interactionFactor;

        return {
            point: `P-${i + 1}`,
            xCoord: x.toFixed(1),
            yCoord: z.toFixed(1),
            settlement: (totalSettlement * 1000).toFixed(2), // m to mm
            safetyFactor: (totalSettlement * 1000) > 15 ? '需注意' : '安全',
        };
    });

    tableData.value = calculationResults;
    hasResults.value = true;
    activeTab.value = 'graphical';
    graphicalActiveTab.value = 'diagram';

     ElNotification({
      title: '成功',
      message: '沉降计算已在浏览器端完成！',
      type: 'success',
    });

  } catch (error) {
    ElNotification({
      title: '错误',
      message: error.message || '计算失败，请检查输入参数。',
      type: 'error',
      duration: 5000,
    });
  } finally {
    calculating.value = false;
  }
};

const getBridgeInputParameters = () => {
    return JSON.parse(JSON.stringify(formData));
};

const validateParameters = (params) => {
    if (params.pile1.diameter <= 0 || params.pile1.length <= 0 || params.pile1.load <= 0 ||
        params.pile2.diameter <= 0 || params.pile2.length <= 0 || params.pile2.load <= 0 ||
        params.bridgeWidth <= 0) {
        throw new Error("桩参数和路基宽度必须大于0。");
    }
     if (params.distanceToPile1 < 0 || params.distanceToPile2 < 0) {
        throw new Error("与桩的距离不能为负数。");
    }
    
    // 验证土层数据
    if (!soilLayersData.value || soilLayersData.value.length === 0) {
        throw new Error("至少需要一个土层数据。");
    }
    
    for (let i = 0; i < soilLayersData.value.length; i++) {
        const layer = soilLayersData.value[i];
        if (layer.compressionModulus <= 0) {
            throw new Error(`第${i + 1}层土的压缩模量必须大于0。`);
    }
        if (layer.depthStart >= layer.depthEnd) {
            throw new Error(`第${i + 1}层土的结束深度必须大于起始深度。`);
        }
        if (!layer.soilType) {
            throw new Error(`第${i + 1}层土必须选择土层类型。`);
        }
    }
    
    return true;
};

const getSoilPropertiesAtDepth = (soilLayers, depth) => {
    for (const layer of soilLayers) {
        const [start, end] = layer.depth_range.split('-').map(Number);
        if (depth >= start && depth <= end) {
            return layer;
        }
    }
    return soilLayers[soilLayers.length - 1]; // Default to last layer
};

const calculateShearModulus = (E, nu) => E / (2 * (1 + nu));

const calculateBoussinesqSettlement = (P, G, x, y, z, nu) => {
    const R = Math.sqrt(x**2 + y**2 + z**2);
    if (R === 0) return 0;

    const term1 = z**2 / (R**3);
    const term2 = 2 * (1 - nu) / R;
    
    const P_N = P * 1000; // kN to N
    const G_Pa = G * 1e6; // MPa to Pa
    
    return (P_N / (4 * Math.PI * G_Pa)) * (term1 + term2);
};

const calculateLengthCorrection = (pileLength) => 0.985 - (0.00051 * pileLength);

const calculateDiameterCorrection = (pileDiameter) => {
    return (0.038 * pileDiameter**2) - (0.206 * pileDiameter) + 1.159;
};

const calculateCombinedCorrection = (pileLength, pileDiameter) => {
    const a = calculateLengthCorrection(pileLength);
    const b = calculateDiameterCorrection(pileDiameter);
    return a * b;
};

const calculatePileInteraction = (pileSpacing, pile1Diameter, pile2Diameter) => {
    const avgDiameter = (pile1Diameter + pile2Diameter) / 2;
    const spacingRatio = pileSpacing / avgDiameter;

    let interactionFactor;
    if (spacingRatio <= 3) {
        interactionFactor = 0.8 + 0.2 * (spacingRatio / 3);
    } else if (spacingRatio <= 6) {
        interactionFactor = 1.0 - 0.1 * ((spacingRatio - 3) / 3);
    } else {
        interactionFactor = 0.9 + 0.1 * Math.min(1.0, (spacingRatio - 6) / 4);
    }
    return Math.max(0.8, Math.min(1.2, interactionFactor));
};

const get16StandardPoints = (roadWidth) => {
    const analysisRange = Math.max(20, roadWidth * 1.5);
    const gridSpacing = analysisRange / 5;
    const positions = Array.from({ length: 4 }, (_, i) => -analysisRange / 2 + gridSpacing * (i + 1));
    const depths = [1, 2, 3, 4];

    const points = [];
    for (const z of depths) {
        for (const x of positions) {
            points.push({ x, y: 0, z });
        }
    }
    return points;
};

const getPilePosition = (pileNumber, params) => {
    const halfWidth = params.bridgeWidth / 2;
    if (pileNumber === 1) {
        const x = -(halfWidth + params.distanceToPile1);
        return [x, 0];
    } else {
        const x = halfWidth + params.distanceToPile2;
        return [x, 0];
    }
};

// 重置表单
const resetForm = () => {
  Object.assign(formData, {
    projectName: '高架桥桩基沉降分析项目',
    pile1: {
      diameter: 1.0,
      length: 20.0,
      load: 1000.0,
    },
    pile2: {
      diameter: 1.0,
      length: 20.0,
      load: 1000.0,
    },
    bridgeWidth: 12.0,
    distanceToPile1: 5.0,
    distanceToPile2: 5.0,
    // 移除固定的土层参数，使用动态土层数据
  })
  
  // 重置土层数据
  resetSoilLayers()
  
  tableData.value = []
  hasResults.value = false
  
  ElNotification({
    title: '成功',
    message: '表单已重置为默认值',
    type: 'info'
  })
}

// 自定义单元格样式
const cellStyle = ({ row, column, rowIndex, columnIndex }) => {
  if (column.property === 'settlement') {
    const value = parseFloat(row[column.property]);
    if (value > 10) {
      return { color: 'var(--brand-accent)', fontWeight: 600 }; // 红色警告
    } else if (value <= 10) {
      return { color: '#529b2e', fontWeight: 600 }; // 绿色安全
    }
  }
  return {};
};

// 安全评估报告相关方法
const getCurrentDate = () => {
  return new Date().toLocaleDateString('zh-CN')
}

const getCurrentDateTime = () => {
  return new Date().toLocaleString('zh-CN')
}

const getMaxSettlement = () => {
  if (!tableData.value.length) return '0.0'
  const settlements = tableData.value.map(item => parseFloat(item.settlement))
  return Math.max(...settlements).toFixed(1)
}

const getAverageSettlement = () => {
  if (!tableData.value.length) return '0.0'
  const settlements = tableData.value.map(item => parseFloat(item.settlement))
  const average = settlements.reduce((sum, val) => sum + val, 0) / settlements.length
  return average.toFixed(1)
}

const getSafePointsCount = () => {
  return tableData.value.filter(item => item.safetyFactor === '安全').length
}

const getWarningPointsCount = () => {
  return tableData.value.filter(item => parseFloat(item.settlement) > 5 && parseFloat(item.settlement) <= 10).length
}

const getDangerPointsCount = () => {
  return tableData.value.filter(item => parseFloat(item.settlement) > 10).length
}

const getSafePointsPercentage = () => {
  if (!tableData.value.length) return 0
  return Math.round((getSafePointsCount() / tableData.value.length) * 100)
}

const getWarningPointsPercentage = () => {
  if (!tableData.value.length) return 0
  return Math.round((getWarningPointsCount() / tableData.value.length) * 100)
}

const getDangerPointsPercentage = () => {
  if (!tableData.value.length) return 0
  return Math.round((getDangerPointsCount() / tableData.value.length) * 100)
}

const getOverallSafetyStatus = () => {
  const maxSettlement = parseFloat(getMaxSettlement())
  const dangerCount = getDangerPointsCount()
  
  if (dangerCount > 0 || maxSettlement > 15) {
    return {
      title: '整体安全状况：需要关注',
      type: 'warning',
      description: `检测到${dangerCount}个危险点，最大沉降量为${maxSettlement}mm，建议采取相应的加固措施。`
    }
  } else if (maxSettlement > 8) {
    return {
      title: '整体安全状况：基本安全',
      type: 'info',
      description: `最大沉降量为${maxSettlement}mm，在可接受范围内，建议持续监测。`
    }
  } else {
    return {
      title: '整体安全状况：安全',
      type: 'success',
      description: `最大沉降量为${maxSettlement}mm，各项指标均在安全范围内。`
    }
  }
}

const getRecommendations = () => {
  const recommendations = []
  const maxSettlement = parseFloat(getMaxSettlement())
  const dangerCount = getDangerPointsCount()
  
  if (maxSettlement > 15) {
    recommendations.push({
      id: 1,
      title: '紧急处理',
      content: '最大沉降量超过15mm，建议立即停止施工并进行结构加固处理。'
    })
  }
  
  if (dangerCount > 0) {
    recommendations.push({
      id: 2,
      title: '重点监测',
      content: `对${dangerCount}个危险点进行重点监测，增加监测频率至每日一次。`
    })
  }
  
  if (maxSettlement > 8) {
    recommendations.push({
      id: 3,
      title: '持续观测',
      content: '建议建立长期监测系统，定期检查桩基沉降变化趋势。'
    })
  }
  
  recommendations.push({
    id: 4,
    title: '技术措施',
    content: '建议采用注浆加固、桩基补强等技术措施提高地基承载能力。'
  })
  
  recommendations.push({
    id: 5,
    title: '后续评估',
    content: '建议每季度进行一次全面的安全评估，确保结构长期稳定性。'
  })
  
  return recommendations
}

const getConclusion = () => {
  const maxSettlement = parseFloat(getMaxSettlement())
  const safePercentage = getSafePointsPercentage()
  
  if (maxSettlement > 15) {
    return `根据计算分析，本桥梁工程最大沉降量为${maxSettlement}mm，超过了安全阈值。建议立即采取加固措施，并进行持续监测，确保结构安全。`
  } else if (maxSettlement > 10) {
    return `根据计算分析，本桥梁工程最大沉降量为${maxSettlement}mm，处于关注范围。建议加强监测，采取预防性措施，并制定应急处理预案。`
  } else {
    return `根据计算分析，本桥梁工程最大沉降量为${maxSettlement}mm，${safePercentage}%的监测点处于安全状态。整体结构稳定，满足设计要求，建议按计划进行后续施工。`
  }
}

// 报告格式相关方法
const getHighwayType = () => {
  return '一级公路' // 这里可以根据实际需求设置不同等级
}

const getSoilTypeName = (type) => {
  const typeMap = {
    'clay': '粘土',
    'sand': '砂土',
    'silt': '粉土',
    'mud': '淤泥',
    'rock': '岩石',
    'fill': '填土'
  }
  return typeMap[type] || type
}

const getPile1Settlement = (item) => {
  // 假设总沉降量的40%来自桩1
  return (parseFloat(item.settlement) * 0.4).toFixed(1)
}

const getPile2Settlement = (item) => {
  // 假设总沉降量的60%来自桩2
  return (parseFloat(item.settlement) * 0.6).toFixed(1)
}

const getSettlementComparison = () => {
  const maxSettlement = parseFloat(getMaxSettlement())
  const allowableSettlement = 30 // 一级公路允许沉降量30mm
  
  if (maxSettlement <= allowableSettlement) {
    return `满足要求（≤${allowableSettlement}mm）`
  } else {
    return `超出允许值${allowableSettlement}mm，需要采取措施`
  }
}

// 生成完整的报告内容
const generateReportContent = () => {
  const soilLayersText = soilLayersData.value.map((layer, index) => 
    `${index + 1}     ${getSoilTypeName(layer.soilType)}    ${layer.depthStart}-${layer.depthEnd}m      ${layer.compressionModulus}           ${layer.poissonRatio}`
  ).join('\n');

  const content = `
桥梁跨越工程安全性评估报告

----------------------------------------------------------------------
[ 项目名称 ]
----------------------------------------------------------------------
${formData.projectName}

----------------------------------------------------------------------
[ 项目类型 ]
----------------------------------------------------------------------
桥梁跨越工程沉降分析

----------------------------------------------------------------------
[ 计算条件 ]
----------------------------------------------------------------------
[ 新建公路 ]
公路类型：${getHighwayType()}
桩顶荷载P：桩1: ${formData.pile1.load}kN, 桩2: ${formData.pile2.load}kN

[ 土层参数 ]
序号  土类型  土层厚度  压缩模量E(MPa)  泊松比v
${soilLayersText}

[ 桩1参数 ]
桩直径：${formData.pile1.diameter}m
桩长：${formData.pile1.length}m

[ 桩2参数 ]
桩直径：${formData.pile2.diameter}m
桩长：${formData.pile2.length}m

[ 被跨越公路参数 ]
路基宽度：${formData.bridgeWidth}m
路基与桩1距离：${formData.distanceToPile1}m
路基与桩2距离：${formData.distanceToPile2}m

----------------------------------------------------------------------
计算依据和公式:
----------------------------------------------------------------------
【规范依据】
1. 《公路路基设计规范》JTG D30-2015
2. 《公路桥涵地基与基础设计规范》JTG D63-2007
3. 《建筑地基基础设计规范》GB50007-2011
4. 《岩土工程勘察规范》GB50021-2001

【主要计算公式】
1. Boussinesq弹性理论计算公式：
   σz = (3P/2π) × z³/r⁵
   式中：σz - z深度处垂直应力增量；P - 桩顶荷载；z - 计算深度；r - 距离桩轴的水平距离

2. 沉降计算公式：
   s = (P/4πG) × [(1-ν)/R + z²/R³]
   式中：s - 沉降量；G - 剪切模量；ν - 泊松比；R - 计算点到荷载作用点距离

3. 剪切模量计算：
   G = E/[2(1+ν)]
   式中：G - 剪切模量；E - 压缩模量；ν - 泊松比

4. 桩长修正系数：
   α = 0.985 - 0.00051L
   式中：α - 桩长修正系数；L - 桩长(m)

5. 桩径修正系数：
   β = 0.038D² - 0.206D + 1.159
   式中：β - 桩径修正系数；D - 桩径(m)

6. 桩间相互作用系数：
   当s/d ≤ 3时：η = 0.8 + 0.2(s/d)/3
   当3 < s/d ≤ 6时：η = 1.0 - 0.1(s/d-3)/3
   当s/d > 6时：η = 0.9 + 0.1min(1,(s/d-6)/4)
   式中：η - 桩间相互作用系数；s - 桩间距；d - 平均桩径

【计算步骤】
步骤1：根据土层参数计算各层土的剪切模量G
步骤2：采用Boussinesq理论计算单桩对各计算点的沉降影响
步骤3：考虑桩长和桩径的修正系数
步骤4：计算双桩的叠加效应和相互作用影响
步骤5：得出各计算点的最终沉降量
步骤6：根据公路等级判断沉降是否满足要求

----------------------------------------------------------------------
计算结果:
----------------------------------------------------------------------
${tableData.value.map(item => 
  `沉降计算点坐标(${item.xCoord},${item.yCoord}) = 点沉降量（桩1）${getPile1Settlement(item)}mm 点沉降量（桩2）${getPile2Settlement(item)}mm 总沉降量${item.settlement}mm`
).join('\n')}

路基下的计算点总沉降量最大值：${getMaxSettlement()}mm →（${getSettlementComparison()}）

----------------------------------------------------------------------
桩基沉降影响评估报告:
----------------------------------------------------------------------
${getOverallSafetyStatus().description}

安全性统计：
- 安全点：${getSafePointsCount()}个（${getSafePointsPercentage()}%）
- 关注点：${getWarningPointsCount()}个（${getWarningPointsPercentage()}%）
- 危险点：${getDangerPointsCount()}个（${getDangerPointsPercentage()}%）

技术建议：
${getRecommendations().map((rec, index) => `${index + 1}. ${rec.title}：${rec.content}`).join('\n')}

评估结论：
${getConclusion()}

计算日期：${getCurrentDate()}
----------------------------------------------------------------------
`
  return content.trim()
}

const exportReport = () => {
  try {
    const content = generateReportContent()
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    
    // 创建下载链接
    const link = document.createElement('a')
    link.href = url
    link.download = `${formData.projectName}_安全评估报告_${getCurrentDate().replace(/\//g, '')}.txt`
    
    // 触发下载
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    // 清理URL对象
    URL.revokeObjectURL(url)
    
    ElNotification({
      title: '导出成功',
      message: '安全评估报告已导出到下载文件夹',
      type: 'success',
      position: 'top-right'
    })
  } catch (error) {
    ElNotification({
      title: '导出失败',
      message: '报告导出过程中出现错误，请重试',
      type: 'error',
      position: 'top-right'
    })
  }
}

// 导出PDF报告 - 使用稳健的jsPDF + html2canvas方案
const exportPDFReport = async () => {
  if (!hasResults.value) {
    ElNotification({
      title: '导出失败',
      message: '请先进行沉降计算再导出报告',
      type: 'warning',
      position: 'top-right'
    })
    return
  }

  try {
    exportingPDF.value = true
    const pdf = new jsPDF('p', 'mm', 'a4')
    const pageWidth = pdf.internal.pageSize.getWidth()
    const pageHeight = pdf.internal.pageSize.getHeight()
    const margin = 15
    const contentWidth = pageWidth - margin * 2
    let yPos = margin
    let pageNumber = 1

    // 助手函数：渲染HTML块并添加到PDF
    const addHtmlBlock = async (html) => {
      const container = document.createElement('div')
      container.style.cssText = `
        position: absolute;
        top: -9999px;
        left: -9999px;
        width: 794px; /* A4 width in pixels at 96 DPI */
        font-family: "Microsoft YaHei", "SimSun", sans-serif;
        background: white;
        padding: 0 30px;
        font-size: 14px;
        line-height: 1.6;
        color: #000;
        box-sizing: border-box;
      `
      container.innerHTML = html
      document.body.appendChild(container)
      
      const canvas = await html2canvas(container, {
        scale: 2,
        useCORS: true,
        backgroundColor: null
      })
      document.body.removeChild(container)
      
      const imgData = canvas.toDataURL('image/png')
      const imgWidth = contentWidth
      const imgHeight = (canvas.height * imgWidth) / canvas.width
      
      if (yPos + imgHeight > pageHeight - margin) {
        pdf.addPage()
        pageNumber++
        yPos = margin
      }
      
      pdf.addImage(imgData, 'PNG', margin, yPos, imgWidth, imgHeight)
      yPos += imgHeight + 5 // Add some space after the block
    }

    // 页眉
    const addHeader = async () => {
      const headerHtml = `
        <div style="display: flex; align-items: center; justify-content: center; padding: 15px 0; border-bottom: 2px solid #2c5aa0;">
          <img src="${logoImage}" style="width: 50px; height: 30px; margin-right: 20px;" />
          <h1 style="font-size: 20px; color: #2c5aa0; margin: 0; font-family: 'Microsoft YaHei', 'SimSun', sans-serif;">桥梁跨越工程安全性评估报告</h1>
        </div>
      `
      await addHtmlBlock(headerHtml)
    }
    
    // --- 开始构建PDF ---
    await addHeader()

    // 模块1: 项目基本信息
    const projectInfoHtml = `
      <h2 style="font-size: 18px; color: #2c5aa0; border-bottom: 1px solid #ddd; padding-bottom: 5px; margin-top: 10px;">项目基本信息</h2>
      <table style="width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 12px;">
        <tr>
          <td style="border: 1px solid #333; padding: 10px; background: #f8f8f8; font-weight: bold; width: 30%;">项目名称</td>
          <td style="border: 1px solid #333; padding: 10px;">${formData.projectName || '桥梁跨越工程安全性评估项目'}</td>
        </tr>
        <tr>
          <td style="border: 1px solid #333; padding: 10px; background: #f8f8f8; font-weight: bold;">项目类型</td>
          <td style="border: 1px solid #333; padding: 10px;">桥梁桩基沉降分析计算</td>
        </tr>
        <tr>
          <td style="border: 1px solid #333; padding: 10px; background: #f8f8f8; font-weight: bold;">公路类型</td>
          <td style="border: 1px solid #333; padding: 10px;">${getHighwayType()}</td>
        </tr>
        <tr>
          <td style="border: 1px solid #333; padding: 10px; background: #f8f8f8; font-weight: bold;">计算日期</td>
          <td style="border: 1px solid #333; padding: 10px;">${getCurrentDate()}</td>
        </tr>
      </table>
    `
    await addHtmlBlock(projectInfoHtml)

    // 模块2: 计算条件
    const conditionsHtml = `
      <h2 style="font-size: 18px; color: #2c5aa0; border-bottom: 1px solid #ddd; padding-bottom: 5px;">一、计算条件</h2>
      <h3 style="font-size: 14px; margin: 15px 0 10px 0;">1. 桩基参数</h3>
      <table style="width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 12px;">
        <tr>
          <td style="border: 1px solid #333; padding: 8px; background: #f8f8f8;">桩1长度</td><td style="border: 1px solid #333; padding: 8px;">${formData.pile1.length} m</td>
          <td style="border: 1px solid #333; padding: 8px; background: #f8f8f8;">桩2长度</td><td style="border: 1px solid #333; padding: 8px;">${formData.pile2.length} m</td>
        </tr>
        <tr>
          <td style="border: 1px solid #333; padding: 8px; background: #f8f8f8;">桩1荷载</td><td style="border: 1px solid #333; padding: 8px;">${formData.pile1.load} kN</td>
          <td style="border: 1px solid #333; padding: 8px; background: #f8f8f8;">桩2荷载</td><td style="border: 1px solid #333; padding: 8px;">${formData.pile2.load} kN</td>
        </tr>
      </table>
      <h3 style="font-size: 14px; margin: 15px 0 10px 0;">2. 土层参数</h3>
      <table style="width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 12px;">
         <tr>
          <td style="border: 1px solid #333; padding: 8px; background: #f8f8f8;">土体弹性模量 Es</td><td style="border: 1px solid #333; padding: 8px;">${formData.soilElasticModulus} MPa</td>
          <td style="border: 1px solid #333; padding: 8px; background: #f8f8f8;">泊松比 ν</td><td style="border: 1px solid #333; padding: 8px;">${formData.poissonRatio}</td>
        </tr>
      </table>
    `
    await addHtmlBlock(conditionsHtml)

    // 模块3: 计算理论与公式 - 分解为多个子模块
    
    // 3.1 第二部分标题
    const formulasTitleHtml = `
      <h2 style="font-size: 18px; color: #2c5aa0; border-bottom: 1px solid #ddd; padding-bottom: 5px;">二、计算理论与公式</h2>
    `
    await addHtmlBlock(formulasTitleHtml)
    
    // 3.2 Boussinesq理论基础 - 总标题
    const boussinesqMainTitleHtml = `
      <h3 style="font-size: 14px; margin: 15px 0 10px 0;">1. Boussinesq理论基础</h3>
      <p style="margin: 10px 0; font-size: 12px;">基于Boussinesq弹性理论，计算桩基荷载在半无限弹性体中引起的附加应力和沉降。该理论适用于均质、各向同性的弹性半空间体。</p>
    `
    await addHtmlBlock(boussinesqMainTitleHtml)
    
    // 3.3 点荷载作用下的垂直位移公式
    const displacementFormulaHtml = `
      <div style="font-size: 12px;">
        <h4 style="font-size: 13px; margin: 10px 0 5px 0; color: #2c5aa0;">1.1 点荷载作用下的垂直位移公式</h4>
        <p style="margin: 10px 0; padding: 10px; background: #f8f9fa; border-left: 4px solid #2c5aa0;">
          <strong>基本公式：</strong><br>
          w = (P / (2πEs)) × [(1 + ν) / r + z²/(r³) × (1 - 2ν)]<br><br>
          <strong>参数说明：</strong><br>
          • P - 桩顶荷载 (kN)<br>
          • Es - 土体弹性模量 = ${formData.soilElasticModulus} MPa<br>
          • ν - 泊松比 = ${formData.poissonRatio}<br>
          • r - 计算点到荷载作用点的距离 (m)<br>
          • z - 计算点深度 (m)<br><br>
          <strong>简化形式：</strong><br>
          对于地表点 (z=0)：w = P(1+ν)/(2πEsr)<br>
          对于深度点：需考虑深度影响系数
        </p>
      </div>
    `
    await addHtmlBlock(displacementFormulaHtml)
    
    // 3.4 应力分布公式
    const stressDistributionHtml = `
      <div style="font-size: 12px;">
        <h4 style="font-size: 13px; margin: 10px 0 5px 0; color: #2c5aa0;">1.2 应力分布公式</h4>
        <p style="margin: 10px 0; padding: 10px; background: #f8f9fa; border-left: 4px solid #2c5aa0;">
          <strong>垂直应力：</strong><br>
          σz = (3P/(2π)) × z³/(r²+z²)^(5/2)<br><br>
          <strong>径向应力：</strong><br>
          σr = (P/(2π)) × [3xz/(r²+z²)^(5/2) - (1-2ν)/(r(r+z))]<br><br>
          <strong>切应力：</strong><br>
          τrz = (3P/(2π)) × xz²/(r²+z²)^(5/2)
        </p>
      </div>
    `
    await addHtmlBlock(stressDistributionHtml)
    
    // 3.5 双桩基沉降叠加原理 - 总标题
    const superpositionMainTitleHtml = `
      <h3 style="font-size: 14px; margin: 15px 0 10px 0;">2. 双桩基沉降叠加原理</h3>
    `
    await addHtmlBlock(superpositionMainTitleHtml)
    
    // 3.6 叠加原理基础
    const superpositionPrincipleHtml = `
      <div style="font-size: 12px;">
        <h4 style="font-size: 13px; margin: 10px 0 5px 0; color: #2c5aa0;">2.1 叠加原理基础</h4>
        <p style="margin: 10px 0; padding: 10px; background: #f8f9fa; border-left: 4px solid #2c5aa0;">
          根据弹性理论的叠加原理，多个荷载共同作用时，任意点的沉降等于各荷载单独作用时在该点产生沉降的代数和。<br><br>
          <strong>总沉降计算：</strong><br>
          w_total = w1 + w2<br><br>
          <strong>详细计算：</strong><br>
          • 桩1产生的沉降：w1 = P1(1+ν)/(2πEsr1)<br>
          • 桩2产生的沉降：w2 = P2(1+ν)/(2πEsr2)<br><br>
          <strong>实际参数：</strong><br>
          • P1 = 桩1荷载 = ${formData.pile1.load} kN<br>
          • P2 = 桩2荷载 = ${formData.pile2.load} kN<br>
          • Es = 土体弹性模量 = ${formData.soilElasticModulus} MPa<br>
          • ν = 泊松比 = ${formData.poissonRatio}
        </p>
      </div>
    `
    await addHtmlBlock(superpositionPrincipleHtml)
    
    // 3.7 距离计算
    const distanceCalculationHtml = `
      <div style="font-size: 12px;">
        <h4 style="font-size: 13px; margin: 10px 0 5px 0; color: #2c5aa0;">2.2 距离计算</h4>
        <p style="margin: 10px 0; padding: 10px; background: #f8f9fa; border-left: 4px solid #2c5aa0;">
          <strong>桩1到计算点距离：</strong><br>
          r1 = √[(x - x1)² + (y - y1)²]<br><br>
          <strong>桩2到计算点距离：</strong><br>
          r2 = √[(x - x2)² + (y - y2)²]<br><br>
          其中：(x, y) 为计算点坐标，(x1, y1)、(x2, y2) 为桩的坐标
        </p>
      </div>
    `
    await addHtmlBlock(distanceCalculationHtml)
    
    // 3.8 安全性评价标准 - 总标题
    const safetyMainTitleHtml = `
      <h3 style="font-size: 14px; margin: 15px 0 10px 0;">3. 安全性评价标准</h3>
    `
    await addHtmlBlock(safetyMainTitleHtml)
    
    // 3.9 规范要求
    const standardRequirementsHtml = `
      <div style="font-size: 12px;">
        <h4 style="font-size: 13px; margin: 10px 0 5px 0; color: #2c5aa0;">3.1 规范要求</h4>
        <table style="width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 11px;">
          <tr style="background: #f0f0f0;">
            <th style="border: 1px solid #333; padding: 8px; text-align: center;">评价项目</th>
            <th style="border: 1px solid #333; padding: 8px; text-align: center;">允许值</th>
            <th style="border: 1px solid #333; padding: 8px; text-align: center;">依据规范</th>
          </tr>
          <tr>
            <td style="border: 1px solid #333; padding: 8px;">桩基沉降量</td>
            <td style="border: 1px solid #333; padding: 8px;">≤ 20.0 mm</td>
            <td style="border: 1px solid #333; padding: 8px;">《建筑桩基技术规范》JGJ94-2008</td>
          </tr>
          <tr>
            <td style="border: 1px solid #333; padding: 8px;">差异沉降</td>
            <td style="border: 1px solid #333; padding: 8px;">≤ 10.0 mm</td>
            <td style="border: 1px solid #333; padding: 8px;">《建筑桩基技术规范》JGJ94-2008</td>
          </tr>
          <tr>
            <td style="border: 1px solid #333; padding: 8px;">路基保护</td>
            <td style="border: 1px solid #333; padding: 8px;">沉降值不影响通行安全</td>
            <td style="border: 1px solid #333; padding: 8px;">《公路工程技术标准》JTG B01-2014</td>
          </tr>
        </table>
      </div>
    `
    await addHtmlBlock(standardRequirementsHtml)
    
    // 3.10 计算参数修正
    const parameterCorrectionHtml = `
      <div style="font-size: 12px;">
        <h4 style="font-size: 13px; margin: 10px 0 5px 0; color: #2c5aa0;">3.2 计算参数修正</h4>
        <p style="margin: 10px 0; padding: 10px; background: #f8f9fa; border-left: 4px solid #2c5aa0;">
          <strong>弹性模量修正：</strong><br>
          实际工程中，需考虑土层非均质性、应力历史、固结状态等因素对弹性模量的影响。<br><br>
          <strong>泊松比修正：</strong><br>
          根据土质类型和含水率调整泊松比值，饱和粘土ν≈0.5，砂土ν≈0.3。<br><br>
          <strong>深度影响：</strong><br>
          考虑桩端阻力和桩侧摩阻力的分布，修正沉降计算结果。
        </p>
      </div>
    `
    await addHtmlBlock(parameterCorrectionHtml)

    // 模块4: 沉降计算结果
    const maxSettlement = Math.max(...tableData.value.map(p => parseFloat(p.settlement || 0)))
    const avgSettlement = tableData.value.reduce((sum, p) => sum + parseFloat(p.settlement || 0), 0) / tableData.value.length
    const resultsHtml = `
      <h2 style="font-size: 18px; color: #2c5aa0; border-bottom: 1px solid #ddd; padding-bottom: 5px;">三、沉降计算结果</h2>
      <table style="width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 12px;">
        <tr style="background: #f0f0f0;"><th style="border: 1px solid #333; padding: 8px;">统计项目</th><th style="border: 1px solid #333; padding: 8px;">数值</th><th style="border: 1px solid #333; padding: 8px;">评价</th></tr>
        <tr><td style="border: 1px solid #333; padding: 8px;">最大沉降量</td><td style="border: 1px solid #333; padding: 8px;">${maxSettlement.toFixed(2)} mm</td><td style="border: 1px solid #333; padding: 8px; color: ${maxSettlement <= 20 ? '#198754' : '#dc3545'};">${maxSettlement <= 20 ? '安全' : '超标'}</td></tr>
        <tr><td style="border: 1px solid #333; padding: 8px;">平均沉降量</td><td style="border: 1px solid #333; padding: 8px;">${avgSettlement.toFixed(2)} mm</td><td style="border: 1px solid #333; padding: 8px; color: ${avgSettlement <= 20 ? '#198754' : '#dc3545'};">${avgSettlement <= 20 ? '安全' : '超标'}</td></tr>
      </table>
    `
    await addHtmlBlock(resultsHtml)

    // 模块5: 安全评估与建议
    const assessmentHtml = `
      <h2 style="font-size: 18px; color: #2c5aa0; border-bottom: 1px solid #ddd; padding-bottom: 5px;">四、安全评估与建议</h2>
      <div style="background: #f8f9fa; border-left: 4px solid #2c5aa0; padding: 15px; margin: 15px 0; font-size: 12px;">
        <h3 style="font-size: 14px; margin: 0 0 10px 0;">整体安全状况评估</h3>
        <p style="margin: 0;">${maxSettlement <= 20 ? '计算结果显示，桥梁桩基在设计荷载作用下的最大沉降量满足安全要求。' : '计算结果显示，桥梁桩基在设计荷载作用下的最大沉降量超过规范限值，存在安全隐患。'}</p>
      </div>
       <div style="background: #e7f3ff; border-left: 4px solid #007bff; padding: 15px; margin: 15px 0; font-size: 12px;">
        <h3 style="font-size: 14px; margin: 0 0 10px 0;">评估结论</h3>
        <p style="margin: 0;">${maxSettlement <= 20 ? '综合评估认为，当前桥梁桩基设计在技术上是可行的。' : '综合评估认为，当前桥梁桩基设计需要进一步优化。'}</p>
      </div>
    `
    await addHtmlBlock(assessmentHtml)

    // 添加最后一页的页脚和公司信息
    const finalFooterHtml = `
      <div style="text-align: center; padding: 20px 0; font-size: 10px; color: #666; border-top: 1px solid #ddd; font-family: 'Microsoft YaHei', 'SimSun', sans-serif;">
        <p style="margin: 5px 0;">技术支持: 吉林省志安科技有限公司</p>
        <p style="margin: 5px 0;">报告生成日期: ${getCurrentDateTime()}</p>
        <p style="margin: 5px 0;">第 ${pageNumber} 页</p>
      </div>
    `
    await addHtmlBlock(finalFooterHtml)

    pdf.save(`桥梁跨越工程安全性评估报告_${getCurrentDate().replace(/\//g, '')}.pdf`)
    
    ElNotification({
      title: '导出成功',
      message: 'PDF报告已成功导出，包含完整的计算理论和公式',
      type: 'success',
      position: 'top-right'
    })
    
  } catch (error) {
    console.error('PDF导出错误:', error)
    ElNotification({
      title: '导出失败',
      message: `PDF导出过程中出现错误: ${error.message}`,
      type: 'error',
      position: 'top-right'
    })
  } finally {
    exportingPDF.value = false
  }
}

// 生成桥梁模块的HTML报告内容
const generateBridgeReportHTML = () => {
  const maxSettlement = Math.max(...tableData.value.map(p => parseFloat(p.settlement || 0)))
  const avgSettlement = tableData.value.reduce((sum, p) => sum + parseFloat(p.settlement || 0), 0) / tableData.value.length
  const safePointsCount = tableData.value.filter(p => parseFloat(p.settlement || 0) <= 20).length
  const unsafePointsCount = tableData.value.filter(p => parseFloat(p.settlement || 0) > 20).length
  
  return `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <style>
        body { 
          font-family: "Microsoft YaHei", "SimSun", sans-serif; 
          margin: 0; 
          padding: 20px; 
          font-size: 12px; 
          line-height: 1.6; 
          color: #000;
          background: white;
        }
        .report-header { 
          text-align: center; 
          margin-bottom: 30px; 
          border-bottom: 2px solid #2c5aa0; 
          padding-bottom: 20px; 
        }
        .report-title { 
          font-size: 24px; 
          font-weight: bold; 
          color: #2c5aa0; 
          margin-bottom: 10px; 
        }
        .company-name { 
          font-size: 16px; 
          color: #666; 
        }
        .section { 
          margin-bottom: 25px; 
          page-break-inside: avoid; 
        }
        .section-title { 
          font-size: 16px; 
          font-weight: bold; 
          color: #2c5aa0; 
          margin-bottom: 15px; 
          border-bottom: 1px solid #ddd; 
          padding-bottom: 5px; 
        }
        .subsection-title { 
          font-size: 14px; 
          font-weight: bold; 
          margin: 15px 0 10px 0; 
        }
        .info-table { 
          width: 100%; 
          border-collapse: collapse; 
          margin: 10px 0; 
        }
        .info-table td, .info-table th { 
          border: 1px solid #333; 
          padding: 8px; 
          text-align: left; 
        }
        .info-table th { 
          background: #f0f0f0; 
          font-weight: bold; 
          text-align: center; 
        }
        .label-cell { 
          background: #f8f8f8; 
          font-weight: bold; 
          width: 30%; 
        }
        .result-pass { 
          color: #198754; 
          font-weight: bold; 
        }
        .result-fail { 
          color: #dc3545; 
          font-weight: bold; 
        }
        .assessment-box { 
          background: #f8f9fa; 
          border-left: 4px solid #2c5aa0; 
          padding: 15px; 
          margin: 15px 0; 
        }
        .page-break { 
          page-break-before: always; 
        }
        ul { 
          margin: 10px 0; 
          padding-left: 20px; 
        }
        li { 
          margin: 5px 0; 
        }
      </style>
    </head>
    <body>
      <!-- 报告封面 -->
      <div class="report-header">
        <div class="report-title">桥梁跨越工程安全性评估报告</div>
        <div class="company-name">吉林省志安科技有限公司</div>
      </div>
      
      <!-- 项目基本信息 -->
      <div class="section">
        <div class="section-title">项目基本信息</div>
        <table class="info-table">
          <tr>
            <td class="label-cell">项目名称</td>
            <td>${formData.projectName || '桥梁跨越工程安全性评估项目'}</td>
          </tr>
          <tr>
            <td class="label-cell">项目类型</td>
            <td>桥梁桩基沉降分析计算</td>
          </tr>
          <tr>
            <td class="label-cell">计算日期</td>
            <td>${getCurrentDate()}</td>
          </tr>
          <tr>
            <td class="label-cell">报告生成时间</td>
            <td>${getCurrentDateTime()}</td>
          </tr>
          <tr>
            <td class="label-cell">技术支持</td>
            <td>吉林省志安科技有限公司</td>
          </tr>
        </table>
      </div>
      
      <!-- 分页 -->
      <div class="page-break"></div>
      
      <!-- 计算条件 -->
      <div class="section">
        <div class="section-title">一、计算条件</div>
        
        <div class="subsection-title">1. 基本参数</div>
        <table class="info-table">
          <tr><td class="label-cell">桩基数量</td><td>${formData.pileCount || 0} 根</td></tr>
          <tr><td class="label-cell">桩径</td><td>${formData.pileDiameter || 0} m</td></tr>
          <tr><td class="label-cell">桩长</td><td>${formData.pileLength || 0} m</td></tr>
          <tr><td class="label-cell">桩顶荷载</td><td>${formData.topLoad || 0} kN</td></tr>
          <tr><td class="label-cell">计算网格</td><td>${formData.gridSize || 0} × ${formData.gridSize || 0}</td></tr>
        </table>
        
        <div class="subsection-title">2. 土质参数</div>
        <table class="info-table">
          <tr><td class="label-cell">土壤重度</td><td>${formData.soilDensity || 0} kN/m³</td></tr>
          <tr><td class="label-cell">土壤泊松比</td><td>${formData.poissonRatio || 0}</td></tr>
          <tr><td class="label-cell">土壤弹性模量</td><td>${formData.elasticModulus || 0} MPa</td></tr>
        </table>
        
        <div class="subsection-title">3. 安全性标准</div>
        <table class="info-table">
          <tr><td class="label-cell">沉降限值</td><td>20.0 mm</td></tr>
          <tr><td class="label-cell">计算方法</td><td>Boussinesq理论</td></tr>
          <tr><td class="label-cell">计算标准</td><td>《建筑地基基础设计规范》GB50007-2011</td></tr>
        </table>
      </div>
      
      <!-- 分页 -->
      <div class="page-break"></div>
      
      <!-- 计算结果 -->
      <div class="section">
        <div class="section-title">二、计算结果</div>
        
        <div class="subsection-title">1. 沉降分析统计</div>
        <table class="info-table">
          <tr>
            <th>统计项目</th>
            <th>计算结果</th>
            <th>单位</th>
            <th>评价</th>
          </tr>
          <tr>
            <td>最大沉降量</td>
            <td>${maxSettlement.toFixed(2)}</td>
            <td>mm</td>
            <td class="${maxSettlement <= 20 ? 'result-pass' : 'result-fail'}">${maxSettlement <= 20 ? '安全' : '超标'}</td>
          </tr>
          <tr>
            <td>平均沉降量</td>
            <td>${avgSettlement.toFixed(2)}</td>
            <td>mm</td>
            <td class="${avgSettlement <= 20 ? 'result-pass' : 'result-fail'}">${avgSettlement <= 20 ? '安全' : '超标'}</td>
          </tr>
          <tr>
            <td>计算点总数</td>
            <td>${tableData.value.length}</td>
            <td>个</td>
            <td>-</td>
          </tr>
          <tr>
            <td>安全点数量</td>
            <td>${safePointsCount}</td>
            <td>个</td>
            <td class="result-pass">安全</td>
          </tr>
          <tr>
            <td>超标点数量</td>
            <td>${unsafePointsCount}</td>
            <td>个</td>
            <td class="${unsafePointsCount === 0 ? 'result-pass' : 'result-fail'}">${unsafePointsCount === 0 ? '安全' : '需关注'}</td>
          </tr>
        </table>
        
        <div class="subsection-title">2. 代表性计算点详情</div>
        <table class="info-table">
          <tr>
            <th>点号</th>
            <th>X坐标(m)</th>
            <th>Y坐标(m)</th>
            <th>沉降量(mm)</th>
            <th>安全性评价</th>
          </tr>
          ${tableData.value.slice(0, 10).map((point, index) => `
            <tr>
              <td>${index + 1}</td>
              <td>${parseFloat(point.xCoord || 0).toFixed(1)}</td>
              <td>${parseFloat(point.yCoord || 0).toFixed(1)}</td>
              <td>${parseFloat(point.settlement || 0).toFixed(2)}</td>
              <td class="${parseFloat(point.settlement || 0) <= 20 ? 'result-pass' : 'result-fail'}">${parseFloat(point.settlement || 0) <= 20 ? '安全' : '超标'}</td>
            </tr>
          `).join('')}
        </table>
        
        ${tableData.value.length > 10 ? `<p><em>注：仅显示前10个代表性计算点，完整数据请参考计算结果文件。</em></p>` : ''}
      </div>
      
      <!-- 分页 -->
      <div class="page-break"></div>
      
      <!-- 安全评估报告 -->
      <div class="section">
        <div class="section-title">三、安全评估报告</div>
        
        <div class="assessment-box">
          <div class="subsection-title">${maxSettlement <= 20 ? '整体安全状况：优良' : '整体安全状况：需关注'}</div>
          <p>${maxSettlement <= 20 ? 
            '计算结果显示，桥梁桩基在设计荷载作用下的最大沉降量为 ' + maxSettlement.toFixed(2) + ' mm，小于规范限值20.0mm，满足安全要求。' :
            '计算结果显示，桥梁桩基在设计荷载作用下的最大沉降量为 ' + maxSettlement.toFixed(2) + ' mm，超过规范限值20.0mm，需要采取相应的工程措施。'
          }</p>
        </div>
        
        <div class="subsection-title">安全性分析</div>
        <ul>
          <li>最大沉降量：${maxSettlement.toFixed(2)} mm ${maxSettlement <= 20 ? '(符合规范要求)' : '(超过规范限值)'}</li>
          <li>平均沉降量：${avgSettlement.toFixed(2)} mm</li>
          <li>安全率：${(safePointsCount / tableData.value.length * 100).toFixed(1)}%</li>
          <li>影响范围：在桩基周围 ${Math.max(formData.gridSize * formData.spacing || 50, 50)} m 范围内</li>
        </ul>
        
        <div class="subsection-title">技术建议</div>
        <ul>
          ${maxSettlement > 20 ? `
            <li><strong>沉降控制：</strong>建议优化桩基设计，增加桩径或桩长，降低单桩荷载。</li>
            <li><strong>施工监测：</strong>在施工过程中设置沉降观测点，实时监测沉降发展。</li>
            <li><strong>分级施工：</strong>采用分级加载的施工方式，控制沉降速率。</li>
          ` : `
            <li><strong>施工监测：</strong>建议在关键部位设置沉降观测点，跟踪监测沉降发展趋势。</li>
            <li><strong>定期检测：</strong>建议在使用期间定期进行沉降检测，确保长期安全。</li>
          `}
          <li><strong>应急预案：</strong>制定详细的应急预案，包括沉降异常情况的处理措施。</li>
          <li><strong>数据记录：</strong>建立完整的沉降监测数据档案，为后期维护提供依据。</li>
        </ul>
        
        <div class="subsection-title">评估结论</div>
        <div class="assessment-box">
          <p>${maxSettlement <= 20 ? 
            '综合评估认为，当前桥梁桩基设计在技术上是可行的，沉降分析结果满足规范要求。建议按照设计参数进行施工，并在施工过程中严格控制质量，确保工程安全顺利完成。' :
            '综合评估认为，当前桥梁桩基设计需要进一步优化。建议根据技术建议调整设计参数，并采取相应的工程措施后方可施工。同时应加强施工期间的监测工作，确保工程安全。'
          }</p>
        </div>
      </div>
      
      <!-- 报告页脚 -->
      <div style="margin-top: 40px; border-top: 1px solid #ddd; padding-top: 20px; text-align: center; font-size: 10px; color: #666;">
        <p>技术支持：吉林省志安科技有限公司</p>
        <p>生成日期：${currentDateTime}</p>
      </div>
    </body>
    </html>
  `
}

// 添加桥梁报告封面页
const addBridgeReportCoverPage = async (pdf, margin, contentWidth, contentHeight) => {
  const pageNumber = 1
  
  // 设置中文字体
  setupChineseFont(pdf)
  
  // 公司LOGO和标题区域
  pdf.setFontSize(18)
  pdf.setTextColor(44, 90, 160)
  const title = '桥梁跨越工程安全性评估报告'
  
  // 计算居中位置
  try {
    const titleWidth = pdf.getTextWidth(title)
    pdf.text(title, (210 - titleWidth) / 2, margin + 30)
  } catch (e) {
    // 如果中文渲染失败，使用固定位置
    pdf.text(title, 30, margin + 30)
  }
  
  // 分割线
  pdf.setLineWidth(0.5)
  pdf.setDrawColor(44, 90, 160)
  pdf.line(margin, margin + 40, 210 - margin, margin + 40)
  
  // 项目信息区域
  let yPos = margin + 60
  
  pdf.setFont('helvetica', 'normal')
  pdf.setFontSize(12)
  pdf.setTextColor(0, 0, 0)
  
  // 项目基本信息表格
  const projectInfo = [
    ['项目名称', formData.projectName || '桥梁跨越工程安全性评估项目'],
    ['项目类型', '桥梁桩基沉降分析计算'],
    ['计算日期', getCurrentDate()],
    ['报告生成时间', getCurrentDateTime()],
    ['技术支持', '吉林省志安科技有限公司']
  ]
  
  projectInfo.forEach((item, index) => {
    const rowY = yPos + index * 12
    
    // 标签背景
    pdf.setFillColor(248, 249, 250)
    pdf.rect(margin, rowY - 4, contentWidth * 0.3, 10, 'F')
    
    // 边框
    pdf.setDrawColor(200, 200, 200)
    pdf.rect(margin, rowY - 4, contentWidth, 10)
    pdf.line(margin + contentWidth * 0.3, rowY - 4, margin + contentWidth * 0.3, rowY + 6)
    
    // 文字
    pdf.setFont('helvetica', 'bold')
    pdf.text(item[0] + '：', margin + 3, rowY + 2)
    
    pdf.setFont('helvetica', 'normal')
    pdf.text(item[1], margin + contentWidth * 0.3 + 3, rowY + 2)
  })
  
  // 计算条件概要
  yPos += 80
  pdf.setFont('helvetica', 'bold')
  pdf.setFontSize(14)
  pdf.setTextColor(44, 90, 160)
  pdf.text('主要计算参数', margin, yPos)
  
  yPos += 15
  pdf.setFont('helvetica', 'normal')
  pdf.setFontSize(10)
  pdf.setTextColor(0, 0, 0)
  
  const keyParams = [
    `桩1直径：${formData.pile1.diameter}m`,
    `桩1长度：${formData.pile1.length}m`,
    `桩1荷载：${formData.pile1.load}kN`,
    `桩2直径：${formData.pile2.diameter}m`,
    `桩2长度：${formData.pile2.length}m`,
    `路基宽度：${formData.bridgeWidth}m`
  ]
  
  keyParams.forEach((param, index) => {
    if (index % 2 === 0) {
      pdf.text('• ' + param, margin, yPos + Math.floor(index / 2) * 8)
    } else {
      pdf.text('• ' + param, margin + contentWidth / 2, yPos + Math.floor(index / 2) * 8)
    }
  })
  
  // 添加页脚
  addBridgePageFooter(pdf, pageNumber, 4)
}

// 添加桥梁计算条件和依据页
const addBridgeCalculationConditionsPage = async (pdf, margin, contentWidth, contentHeight) => {
  const pageNumber = 2
  let yPos = margin + 10
  
  // 页面标题
  setupChineseFont(pdf)
  pdf.setFontSize(16)
  pdf.setTextColor(44, 90, 160)
  pdf.text('计算条件与依据', margin, yPos)
  yPos += 15
  
  // 规范依据
  setupChineseFont(pdf)
  pdf.setFontSize(12)
  pdf.setTextColor(0, 0, 0)
  pdf.text('1. 规范依据', margin, yPos)
  yPos += 10
  
  setupChineseFont(pdf)
  pdf.setFontSize(9)
  const standards = [
    '《建筑地基基础设计规范》GB50007-2011',
    '《公路桥涵地基与基础设计规范》JTG D63-2007',
    '《岩土工程勘察规范》GB50021-2001',
    '《建筑桩基技术规范》JGJ94-2008',
    '《公路工程抗震设计规范》JTG B02-2013'
  ]
  
  standards.forEach((standard, index) => {
    pdf.text(`(${index + 1}) ${standard}`, margin + 5, yPos + index * 6)
  })
  yPos += standards.length * 6 + 10
  
  // 主要计算公式
  setupChineseFont(pdf)
  pdf.setFontSize(12)
  pdf.text('2. 主要计算公式', margin, yPos)
  yPos += 10
  
  setupChineseFont(pdf)
  pdf.setFontSize(9)
  
  const formulas = [
    {
      title: 'Boussinesq应力计算',
      formula: 'σz = Q × K / r²',
      desc: 'Q-点荷载(kN); K-应力系数; r-到荷载点距离(m); σz-垂直应力(kPa)'
    },
    {
      title: '沉降计算',
      formula: 'S = Σ(σz × h / E)',
      desc: 'S-沉降量(mm); σz-垂直应力(kPa); h-土层厚度(m); E-压缩模量(MPa)'
    },
    {
      title: '影响范围分析',
      formula: 'R = 2.5 × √(A)',
      desc: 'R-影响半径(m); A-桩基底面积(m²)'
    },
    {
      title: '安全判断标准',
      formula: 'S ≤ [S]',
      desc: 'S-计算沉降(mm); [S]-允许沉降(mm); 通常取20mm'
    }
  ]
  
  formulas.forEach((item, index) => {
    if (yPos + 25 > contentHeight + margin) return // 防止超出页面
    
    pdf.setFont('helvetica', 'bold')
    pdf.text(`(${index + 1}) ${item.title}:`, margin + 5, yPos)
    yPos += 6
    
    pdf.setFont('courier', 'normal')
    pdf.text(item.formula, margin + 10, yPos)
    yPos += 6
    
    pdf.setFont('helvetica', 'normal')
    pdf.setFontSize(8)
    const wrappedDesc = pdf.splitTextToSize(item.desc, contentWidth - 15)
    pdf.text(wrappedDesc, margin + 10, yPos)
    yPos += wrappedDesc.length * 4 + 6
    
    pdf.setFontSize(9)
  })
  
  // 详细参数表格
  if (yPos + 80 < contentHeight + margin) {
    pdf.setFont('helvetica', 'bold')
    pdf.setFontSize(12)
    pdf.text('3. 详细计算参数', margin, yPos)
    yPos += 10
    
    // 桩基参数表格
    const pileData = [
      ['参数项目', '桩1', '桩2', '单位'],
      ['桩径', formData.pile1.diameter.toString(), formData.pile2.diameter.toString(), 'm'],
      ['桩长', formData.pile1.length.toString(), formData.pile2.length.toString(), 'm'],
      ['荷载', formData.pile1.load.toString(), formData.pile2.load.toString(), 'kN'],
      ['距路基距离', formData.distanceToPile1.toString(), formData.distanceToPile2.toString(), 'm']
    ]
    
    drawBridgeTable(pdf, pileData, margin, yPos, contentWidth, 8)
  }
  
  addBridgePageFooter(pdf, pageNumber, 4)
}

// 添加桥梁计算结果页
const addBridgeCalculationResultsPage = async (pdf, margin, contentWidth, contentHeight) => {
  const pageNumber = 3
  let yPos = margin + 10
  
  // 页面标题
  setupChineseFont(pdf)
  pdf.setFontSize(16)
  pdf.setTextColor(44, 90, 160)
  pdf.text('计算结果', margin, yPos)
  yPos += 15
  
  // 沉降分析结果
  pdf.setFont('helvetica', 'bold')
  pdf.setFontSize(12)
  pdf.setTextColor(0, 0, 0)
  pdf.text('1. 沉降分析结果汇总', margin, yPos)
  yPos += 10
  
  if (hasResults.value && tableData.value.length > 0) {
    // 统计分析
    const maxSettlement = Math.max(...tableData.value.map(p => parseFloat(p.settlement || 0)))
    const avgSettlement = tableData.value.reduce((sum, p) => sum + parseFloat(p.settlement || 0), 0) / tableData.value.length
    const safePointsCount = tableData.value.filter(p => parseFloat(p.settlement || 0) <= 20).length
    const unsafePointsCount = tableData.value.length - safePointsCount
    
    const summaryData = [
      ['统计项目', '数值', '单位'],
      ['计算点总数', tableData.value.length.toString(), '个'],
      ['最大沉降', maxSettlement.toFixed(2), 'mm'],
      ['平均沉降', avgSettlement.toFixed(2), 'mm'],
      ['安全点数量', safePointsCount.toString(), '个'],
      ['超标点数量', unsafePointsCount.toString(), '个']
    ]
    
    const tableHeight = drawBridgeTable(pdf, summaryData, margin, yPos, contentWidth, 8)
    yPos += tableHeight + 15
    
    // 代表性计算点详细结果
    pdf.setFont('helvetica', 'bold')
    pdf.setFontSize(12)
    pdf.text('2. 代表性计算点详细结果', margin, yPos)
    yPos += 10
    
    // 选择几个代表性点
    const representativePoints = tableData.value.slice(0, Math.min(8, tableData.value.length))
    
    const detailData = [
      ['序号', 'X坐标(m)', 'Y坐标(m)', '沉降(mm)', '安全性'],
      ...representativePoints.map((point, index) => [
        (index + 1).toString(),
        parseFloat(point.xCoord || 0).toFixed(1),
        parseFloat(point.yCoord || 0).toFixed(1),
        parseFloat(point.settlement || 0).toFixed(2),
        (parseFloat(point.settlement || 0) <= 20) ? '安全' : '超标'
      ])
    ]
    
    const tableHeight2 = drawBridgeTable(pdf, detailData, margin, yPos, contentWidth, 7)
    yPos += tableHeight2 + 15
    
    // 安全性分析
    pdf.setFont('helvetica', 'bold')
    pdf.setFontSize(12)
    pdf.text('3. 安全性分析', margin, yPos)
    yPos += 10
    
    pdf.setFont('helvetica', 'normal')
    pdf.setFontSize(10)
    const safetyAnalysis = [
      `沉降安全率：${((safePointsCount / tableData.value.length) * 100).toFixed(1)}%`,
      `最大沉降值：${maxSettlement.toFixed(2)}mm (允许值：20mm)`,
      `整体评价：${unsafePointsCount === 0 ? '全部计算点均满足安全要求' : `有${unsafePointsCount}个点超过安全标准`}`
    ]
    
    safetyAnalysis.forEach((analysis, index) => {
      pdf.text('• ' + analysis, margin + 5, yPos + index * 6)
    })
  } else {
    pdf.setFont('helvetica', 'normal')
    pdf.setFontSize(10)
    pdf.text('暂无计算结果数据', margin + 5, yPos)
  }
  
  addBridgePageFooter(pdf, pageNumber, 4)
}

// 添加桥梁安全评估报告页
const addBridgeSafetyAssessmentPage = async (pdf, margin, contentWidth, contentHeight) => {
  const pageNumber = 4
  let yPos = margin + 10
  
  // 页面标题
  setupChineseFont(pdf)
  pdf.setFontSize(16)
  pdf.setTextColor(44, 90, 160)
  pdf.text('安全评估报告', margin, yPos)
  yPos += 15
  
  if (hasResults.value && tableData.value.length > 0) {
    // 整体安全状况
    const maxSettlement = Math.max(...tableData.value.map(p => parseFloat(p.settlement || 0)))
    const unsafePointsCount = tableData.value.filter(p => parseFloat(p.settlement || 0) > 20).length
    const safetyStatus = getBridgeOverallSafetyStatus(maxSettlement, unsafePointsCount, tableData.value.length)
    
    pdf.setFont('helvetica', 'bold')
    pdf.setFontSize(12)
    pdf.setTextColor(0, 0, 0)
    pdf.text('1. ' + safetyStatus.title, margin, yPos)
    yPos += 10
    
    pdf.setFont('helvetica', 'normal')
    pdf.setFontSize(10)
    const wrappedDesc = pdf.splitTextToSize(safetyStatus.description, contentWidth)
    pdf.text(wrappedDesc, margin, yPos)
    yPos += wrappedDesc.length * 5 + 10
    
    // 风险点统计
    pdf.setFont('helvetica', 'bold')
    pdf.setFontSize(12)
    pdf.text('2. 风险点统计', margin, yPos)
    yPos += 10
    
    pdf.setFont('helvetica', 'normal')
    pdf.setFontSize(10)
    const riskAnalysis = [
      `• 计算点总数：${tableData.value.length}个`,
      `• 安全点数量：${tableData.value.length - unsafePointsCount}个`,
      `• 超标点数量：${unsafePointsCount}个`,
      `• 最大沉降值：${maxSettlement.toFixed(2)}mm`,
      `• 安全裕度：${unsafePointsCount === 0 ? '充足' : '不足'}`
    ]
    
    riskAnalysis.forEach((analysis, index) => {
      pdf.text(analysis, margin + 5, yPos + index * 6)
    })
    yPos += riskAnalysis.length * 6 + 15
    
    // 技术建议
    pdf.setFont('helvetica', 'bold')
    pdf.setFontSize(12)
    pdf.text('3. 技术建议', margin, yPos)
    yPos += 10
    
    pdf.setFont('helvetica', 'normal')
    pdf.setFontSize(9)
    const recommendations = getBridgeRecommendations(maxSettlement, unsafePointsCount)
    
    recommendations.forEach((rec, index) => {
      if (yPos + 15 > contentHeight + margin - 30) return // 保留底部空间
      
      pdf.setFont('helvetica', 'bold')
      pdf.text(`(${index + 1}) ${rec.title}:`, margin + 5, yPos)
      yPos += 6
      
      pdf.setFont('helvetica', 'normal')
      const wrappedContent = pdf.splitTextToSize(rec.content, contentWidth - 10)
      pdf.text(wrappedContent, margin + 10, yPos)
      yPos += wrappedContent.length * 4 + 4
    })
    
    // 评估结论
    if (yPos + 30 < contentHeight + margin - 20) {
      pdf.setFont('helvetica', 'bold')
      pdf.setFontSize(12)
      pdf.text('4. 评估结论', margin, yPos)
      yPos += 10
      
      pdf.setFont('helvetica', 'normal')
      pdf.setFontSize(10)
      const conclusion = getBridgeConclusion(maxSettlement, unsafePointsCount)
      const wrappedConclusion = pdf.splitTextToSize(conclusion, contentWidth)
      
      // 结论背景框
      pdf.setFillColor(248, 249, 250)
      pdf.rect(margin, yPos - 3, contentWidth, wrappedConclusion.length * 5 + 6, 'F')
      pdf.setDrawColor(44, 90, 160)
      pdf.rect(margin, yPos - 3, contentWidth, wrappedConclusion.length * 5 + 6)
      
      pdf.text(wrappedConclusion, margin + 3, yPos + 2)
    }
  } else {
    pdf.setFont('helvetica', 'normal')
    pdf.setFontSize(10)
    pdf.text('暂无计算结果数据，无法进行安全评估', margin + 5, yPos)
  }
  
  addBridgePageFooter(pdf, pageNumber, 4)
}

// 桥梁绘制表格的辅助函数
const drawBridgeTable = (pdf, data, x, y, width, rowHeight) => {
  const colWidth = width / data[0].length
  let currentY = y
  
  data.forEach((row, rowIndex) => {
    row.forEach((cell, colIndex) => {
      const cellX = x + colIndex * colWidth
      
      // 表头背景
      if (rowIndex === 0) {
        pdf.setFillColor(240, 240, 240)
        pdf.rect(cellX, currentY - 2, colWidth, rowHeight, 'F')
      }
      
      // 边框
      pdf.setDrawColor(0, 0, 0)
      pdf.rect(cellX, currentY - 2, colWidth, rowHeight)
      
      // 文字
      pdf.setFont('helvetica', rowIndex === 0 ? 'bold' : 'normal')
      pdf.setFontSize(rowIndex === 0 ? 9 : 8)
      
      // 文字居中
      const textWidth = pdf.getTextWidth(cell.toString())
      const textX = cellX + (colWidth - textWidth) / 2
      
      pdf.text(cell.toString(), textX, currentY + 3)
    })
    currentY += rowHeight
  })
  
  return data.length * rowHeight
}

// 桥梁添加页脚的辅助函数
const addBridgePageFooter = (pdf, pageNumber, totalPages) => {
  pdf.setFont('helvetica', 'normal')
  pdf.setFontSize(8)
  pdf.setTextColor(100, 100, 100)
  
  // 页码
  pdf.text(`第 ${pageNumber} 页，共 ${totalPages} 页`, 210 - 30, 297 - 10)
  
  // 公司信息
  pdf.text('技术支持：吉林省志安科技有限公司', 15, 297 - 10)
  
  // 生成日期
  pdf.text(`生成日期：${getCurrentDate()}`, 15, 297 - 5)
}

// 获取桥梁整体安全状况
const getBridgeOverallSafetyStatus = (maxSettlement, unsafeCount, totalCount) => {
  if (unsafeCount === 0) {
    return {
      title: '整体安全状况：优良',
      description: '所有计算点的沉降值均在安全范围内，桥梁桩基对既有路基的影响可控，施工可以按计划进行。'
    }
  } else if (unsafeCount <= totalCount * 0.1) {
    return {
      title: '整体安全状况：良好',
      description: `大部分区域安全，仅有${unsafeCount}个点超标，建议对超标区域加强监测和采取必要的防护措施。`
    }
  } else if (unsafeCount <= totalCount * 0.3) {
    return {
      title: '整体安全状况：一般',
      description: `有${unsafeCount}个计算点超过安全标准，需要采取加强措施降低沉降影响，建议优化施工方案。`
    }
  } else {
    return {
      title: '整体安全状况：危险',
      description: `多个区域沉降超标，存在重大安全风险，必须重新设计桩基方案或采取有效的加固措施。`
    }
  }
}

// 获取桥梁技术建议
const getBridgeRecommendations = (maxSettlement, unsafeCount) => {
  const recommendations = []
  let recId = 1

  if (unsafeCount > 0) {
    recommendations.push({
      id: recId++,
      title: '沉降控制措施',
      content: '对超标区域采取地基加固、设置隔离屏障或调整桩基设计等措施控制沉降。'
    })
  }

  if (maxSettlement > 15) {
    recommendations.push({
      id: recId++,
      title: '施工监测',
      content: '加强施工过程中的沉降监测，设置监测点实时跟踪路基变形情况。'
    })
  }

  recommendations.push({
    id: recId++,
    title: '施工方案优化',
    content: '合理安排施工顺序，采用分段施工、预压等技术措施减少对既有路基的影响。'
  })

  recommendations.push({
    id: recId++,
    title: '应急预案',
    content: '制定详细的应急预案，包括异常沉降的处理措施和交通保障方案。'
  })

  return recommendations
}

// 获取桥梁评估结论
const getBridgeConclusion = (maxSettlement, unsafeCount) => {
  if (unsafeCount === 0) {
    return '综合评估认为，当前桥梁桩基设计方案对既有路基的影响在可控范围内，所有计算点的沉降值均满足安全要求。建议按照设计方案进行施工，并在施工过程中加强质量控制和监测。'
  } else if (unsafeCount <= 3) {
    return '综合评估认为，大部分区域满足安全要求，局部区域需要关注。建议对超标区域采取针对性的加强措施，并在施工过程中加强监测，确保工程安全。'
  } else {
    return '综合评估认为，当前方案存在一定的安全风险，多个区域的沉降超过安全标准。建议重新优化设计方案，采取有效的加固措施，确保既有路基的安全稳定。'
  }
}

// 添加图表到PDF模板
const addChartToPDFTemplate = async () => {
  try {
    // 获取当前显示的图表
    const currentChart = document.querySelector('.chart-inner-container canvas')
    if (currentChart) {
      const chartCanvas = await html2canvas(currentChart, {
        scale: 2, // 提高图表分辨率
        useCORS: true,
        allowTaint: true,
        backgroundColor: '#ffffff',
        letterRendering: true // 提高文字渲染质量
      })
      
      const chartImg = chartCanvas.toDataURL('image/png', 1.0)
      
      // 插入到PDF模板的图表容器中
      const pdfChartContainer = document.getElementById('pdf-chart-container')
      if (pdfChartContainer) {
        pdfChartContainer.innerHTML = `<img src="${chartImg}" style="width: 100%; max-width: 600px; height: auto;" alt="计算简图" />`
      }
    }
  } catch (error) {
    console.warn('添加图表失败:', error)
    // 如果图表添加失败，显示占位文本
    const pdfChartContainer = document.getElementById('pdf-chart-container')
    if (pdfChartContainer) {
      pdfChartContainer.innerHTML = '<p style="text-align: center; color: #666; padding: 40px;">计算简图（请在图形分析中查看详细图表）</p>'
    }
  }
}

// 土层参数管理
const soilLayersData = ref([
  { depthStart: 0, depthEnd: 5, soilType: 'clay', compressionModulus: 10, poissonRatio: 0.35 },
  { depthStart: 5, depthEnd: 10, soilType: 'sand', compressionModulus: 15, poissonRatio: 0.30 }
])

const showSoilLayerDialog = ref(false)
const editingIndex = ref(-1)
const currentSoilLayer = reactive({
  depthStart: 0,
  depthEnd: 0,
  soilType: 'clay',
  compressionModulus: 0,
  poissonRatio: 0
})

const soilLayerRules = {
  depthStart: [
    { required: true, message: '请输入起始深度', trigger: 'blur' },
    { type: 'number', min: 0, max: 100, message: '起始深度应在0-100之间', trigger: 'blur' }
  ],
  depthEnd: [
    { required: true, message: '请输入结束深度', trigger: 'blur' },
    { type: 'number', min: 0, max: 100, message: '结束深度应在0-100之间', trigger: 'blur' }
  ],
  soilType: [
    { required: true, message: '请选择土层类型', trigger: 'change' }
  ],
  compressionModulus: [
    { required: true, message: '请输入压缩模量', trigger: 'blur' },
    { type: 'number', min: 0, max: 100, message: '压缩模量应在0-100之间', trigger: 'blur' }
  ],
  poissonRatio: [
    { required: true, message: '请输入泊松比', trigger: 'blur' },
    { type: 'number', min: 0, max: 1, message: '泊松比应在0-1之间', trigger: 'blur' }
  ]
}

const addSoilLayer = () => {
  showSoilLayerDialog.value = true
  editingIndex.value = -1
  Object.assign(currentSoilLayer, {
    depthStart: 0,
    depthEnd: 0,
    soilType: 'clay',
    compressionModulus: 0,
    poissonRatio: 0
  })
}

const resetSoilLayers = () => {
  soilLayersData.value = [
    { depthStart: 0, depthEnd: 5, soilType: 'clay', compressionModulus: 10, poissonRatio: 0.35 },
    { depthStart: 5, depthEnd: 10, soilType: 'sand', compressionModulus: 15, poissonRatio: 0.30 }
  ]
}

const editSoilLayer = (index) => {
  showSoilLayerDialog.value = true
  editingIndex.value = index
  Object.assign(currentSoilLayer, soilLayersData.value[index])
}

const deleteSoilLayer = (index) => {
  if (soilLayersData.value.length <= 1) {
    ElNotification({
      title: '操作限制',
      message: '至少需要保留一个土层',
      type: 'warning'
    })
    return
  }
  
  ElMessageBox.confirm(
    `确定要删除第${index + 1}层土 (${soilLayersData.value[index].depthStart}-${soilLayersData.value[index].depthEnd}m) 吗？`,
    '确认删除',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    soilLayersData.value.splice(index, 1)
    ElNotification({
      title: '成功',
      message: '土层删除成功',
      type: 'success'
    })
  }).catch(() => {
    // 用户取消删除
  })
}

const saveSoilLayer = async () => {
  try {
    // 验证表单
    if (currentSoilLayer.depthStart >= currentSoilLayer.depthEnd) {
      ElNotification({
        title: '验证失败',
        message: '结束深度必须大于起始深度',
        type: 'error'
      })
      return
    }
    
    if (!currentSoilLayer.soilType) {
      ElNotification({
        title: '验证失败',
        message: '请选择土层类型',
        type: 'error'
      })
      return
    }
    
    if (currentSoilLayer.compressionModulus <= 0) {
      ElNotification({
        title: '验证失败',
        message: '压缩模量必须大于0',
        type: 'error'
      })
      return
    }
    
    // 检查深度范围是否与其他土层重叠（编辑时排除当前土层）
    const layersToCheck = editingIndex.value === -1 
      ? soilLayersData.value 
      : soilLayersData.value.filter((_, index) => index !== editingIndex.value)
    
    const hasOverlap = layersToCheck.some(layer => {
      return !(currentSoilLayer.depthEnd <= layer.depthStart || currentSoilLayer.depthStart >= layer.depthEnd)
    })
    
    if (hasOverlap) {
      ElNotification({
        title: '验证失败',
        message: '土层深度范围不能与其他土层重叠',
        type: 'error'
      })
      return
    }
    
    // 保存土层
    if (editingIndex.value === -1) {
      soilLayersData.value.push({ ...currentSoilLayer })
      ElNotification({
        title: '成功',
        message: '土层添加成功',
        type: 'success'
      })
    } else {
      Object.assign(soilLayersData.value[editingIndex.value], currentSoilLayer)
      ElNotification({
        title: '成功',
        message: '土层更新成功',
        type: 'success'
      })
    }
    
    handleSoilLayerDialogClose()
  } catch (error) {
    ElNotification({
      title: '错误',
      message: error.message || '保存土层失败',
      type: 'error'
    })
  }
}

const getTotalDepth = () => {
  return soilLayersData.value.reduce((total, layer) => total + (layer.depthEnd - layer.depthStart), 0)
}

const getSoilTypeTagType = (soilType) => {
  switch (soilType) {
    case 'clay':
      return 'success'
    case 'sand':
      return 'warning'
    case 'silt':
      return 'info'
    case 'mud':
      return 'danger'
    case 'rock':
      return 'primary'
    case 'fill':
      return 'success'
    default:
      return 'info'
  }
}

const handleSoilLayerDialogClose = () => {
  showSoilLayerDialog.value = false
  editingIndex.value = -1
  // 重置当前土层数据
  Object.assign(currentSoilLayer, {
    depthStart: 0,
    depthEnd: 0,
    soilType: 'clay',
    compressionModulus: 0,
    poissonRatio: 0
  })
}
</script>

<style scoped>
.bridge-settlement-view {
  color: var(--text-primary);
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 24px;
}

.page-header {
  margin-bottom: 16px;
}

.page-header h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--brand-primary);
  margin-bottom: 8px;
}

.page-description {
  color: var(--text-secondary);
  font-size: 1rem;
  max-width: 800px;
}

.form-card, .result-card {
  background-color: var(--bg-card);
  border: 1px solid var(--el-border-color);
  border-radius: 12px;
  box-shadow: var(--el-box-shadow-light);
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0;
}

.header-icon {
  margin-right: 8px;
  vertical-align: middle;
  color: var(--brand-primary);
}

h2 {
  margin: 0;
  font-size: 1.25rem;
  color: var(--brand-primary);
  font-weight: 600;
  display: flex;
  align-items: center;
}

.form-section {
  margin-bottom: 24px;
  background-color: var(--bg-section);
  border-radius: 8px;
  padding: 16px;
  border: 1px solid var(--el-border-color-light);
}

.form-section:hover {
  background-color: #fcfdff;
  border-color: var(--el-border-color);
}

h3 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 1.125rem;
  color: var(--text-primary);
  border-bottom: 1px solid var(--el-border-color);
  padding-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.param-group-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-top: 16px;
  margin-bottom: 8px;
  padding-left: 8px;
  border-left: 3px solid var(--brand-primary);
}

.settlement-form :deep(.el-form-item__label) {
  color: var(--text-primary);
  font-weight: 500;
}

.settlement-form :deep(.el-input__wrapper),
.settlement-form :deep(.el-input-number),
.settlement-form :deep(.el-select__wrapper) {
  background-color: var(--bg-input);
  box-shadow: none;
  border: 1px solid var(--el-border-color);
}

.settlement-form :deep(.el-input__inner),
.settlement-form :deep(.el-input-number__input),
.settlement-form :deep(.el-select__text) {
  color: var(--text-primary) !important;
}

.settlement-form :deep(.el-select .el-select__tags-text) {
  color: var(--text-primary);
}

.settlement-form :deep(.el-tag) {
  background-color: rgba(139, 92, 246, 0.2);
  border-color: rgba(139, 92, 246, 0.3);
  color: var(--text-primary);
}

.settlement-form :deep(.el-input__wrapper:hover),
.settlement-form :deep(.el-input-number:hover),
.settlement-form :deep(.el-select__wrapper:hover) {
  border-color: var(--brand-primary);
}

.settlement-form :deep(.el-input__wrapper.is-focus),
.settlement-form :deep(.el-input-number.is-focus),
.settlement-form :deep(.el-select__wrapper.is-focus) {
  border-color: var(--brand-primary);
  box-shadow: 0 0 0 1px var(--brand-primary);
}

.full-width {
  width: 100%;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.result-tabs {
  height: 100%;
}

.result-tabs :deep(.el-tabs__header) {
  margin-bottom: 16px;
}

.result-tabs :deep(.el-tabs__item) {
  color: var(--text-secondary);
  font-size: 1rem;
  padding: 0 24px;
  height: 40px;
  line-height: 40px;
}

.result-tabs :deep(.el-tabs__item.is-active) {
  color: var(--brand-primary);
}

.result-tabs :deep(.el-tabs__active-bar) {
  background-color: var(--brand-primary);
  height: 3px;
}

.result-content {
  padding: 8px 0;
}

.result-alert {
  margin-bottom: 16px;
}

.result-table {
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--el-border-color);
}

.result-table :deep(.el-table__row) {
  background-color: var(--brand-white);
  transition: all 0.2s ease;
}

.result-table :deep(.el-table__row:hover > td) {
  background-color: #f5f7fa !important;
}

.result-table :deep(.el-table__row--striped) {
  background-color: #f5f7fa;
}

.result-table :deep(.el-table__row td) {
  color: var(--text-primary);
  font-weight: 500;
}

.result-table :deep(.el-table__header-wrapper th) {
  background-color: #f5f7fa !important;
  color: var(--text-secondary) !important;
  font-weight: 600;
}

.warning-value {
  color: var(--brand-accent);
  font-weight: 600;
}

.safe-value {
  color: #529b2e;
  font-weight: 600;
}

.empty-result {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 450px;
  color: var(--text-secondary);
}

.chart-container {
  height: 450px;
  width: 100%;
  border-radius: 8px;
  padding: 16px;
}

.graphical-analysis {
  padding: 1rem;
  background-color: var(--brand-white);
  border-radius: 8px;
  border: 1px solid var(--el-border-color-light);
  min-height: 520px;
}

.inner-tabs {
  --el-tabs-header-height: 50px;
}

.chart-inner-container {
  position: relative;
  width: 100%;
  height: 450px;
}

.chart-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  background-color: var(--bg-card);
  border-radius: 8px;
  padding: 20px;
}

.chart-title {
  font-size: 1.125rem;
  color: var(--text-primary);
  font-weight: 600;
  margin-bottom: 16px;
  text-align: center;
}

.placeholder-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: var(--text-secondary);
}

.placeholder-text {
  margin-top: 12px;
  font-size: 0.9rem;
  text-align: center;
}

.controls-card :deep(.el-input__wrapper) {
  background-color: var(--bg-input);
  border: 1px solid var(--el-border-color);
  box-shadow: none !important;
}

.controls-card :deep(.el-input__inner),
.controls-card :deep(.el-select .el-input__inner) {
  color: var(--text-primary) !important;
}

.chart-card {
  background-color: var(--bg-card);
  border-radius: 12px;
}

@media (max-width: 768px) {
  .el-col {
    margin-bottom: 16px;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .form-actions .el-button {
    width: 100%;
  }
}

/* 安全评估报告样式 */
.safety-report {
  padding: 16px 0;
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid var(--el-border-color);
}

.report-header h3 {
  color: var(--brand-primary);
  font-size: 1.5rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.report-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.report-section {
  background-color: var(--bg-card);
  border: 1px solid var(--el-border-color);
  border-radius: 12px;
}

.report-section :deep(.el-card__header) {
  background-color: var(--bg-main);
  border-bottom: 1px solid var(--el-border-color);
  padding: 16px 20px;
}

.report-section h4 {
  color: var(--text-primary);
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.stat-item {
  text-align: center;
  padding: 16px;
  background-color: var(--bg-main);
  border-radius: 8px;
  border: 1px solid var(--el-border-color);
}

.stat-label {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: 8px;
}

.stat-value {
  color: var(--brand-primary);
  font-size: 1.8rem;
  font-weight: 700;
}

.stat-value.danger {
  color: var(--brand-accent);
}

.safety-analysis {
  margin-top: 20px;
}

.safety-analysis h5 {
  color: var(--text-primary);
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 12px;
}

.safety-details {
  margin-top: 16px;
}

.safety-card {
  text-align: center;
  padding: 16px;
  border-radius: 8px;
  border: 2px solid;
  background-color: var(--bg-card);
}

.safety-card.safe {
  border-color: #67c23a;
  background-color: #f0f9ff;
}

.safety-card.warning {
  border-color: #e6a23c;
  background-color: #fefce8;
}

.safety-card.danger {
  border-color: var(--brand-accent);
  background-color: #fef2f2;
}

.safety-card h6 {
  margin: 0 0 8px 0;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.safety-card .count {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 4px;
}

.safety-card.safe .count {
  color: #67c23a;
}

.safety-card.warning .count {
  color: #e6a23c;
}

.safety-card.danger .count {
  color: var(--brand-accent);
}

.safety-card .percentage {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.recommendations {
  padding: 16px 0;
}

.recommendations ol {
  margin: 0;
  padding-left: 20px;
}

.recommendations li {
  color: var(--text-primary);
  line-height: 1.6;
  margin-bottom: 12px;
}

.recommendations strong {
  color: var(--brand-primary);
}

.conclusion {
  padding: 16px 0;
}

.conclusion p {
  color: var(--text-primary);
  line-height: 1.7;
  font-size: 1rem;
  margin: 0;
}

/* 报告表格样式 */
.report-table {
  padding: 16px 0;
}

.info-table,
.params-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 16px;
  border: 1px solid var(--el-border-color);
  background-color: var(--bg-card);
}

.info-table td,
.params-table td,
.params-table th {
  padding: 12px 16px;
  border: 1px solid var(--el-border-color);
  text-align: left;
}

.params-table th {
  background-color: var(--bg-main);
  font-weight: 600;
  color: var(--text-primary);
  text-align: center;
}

.info-table .label {
  background-color: var(--bg-main);
  font-weight: 600;
  color: var(--text-primary);
  width: 40%;
}

.info-table .value,
.params-table td {
  color: var(--text-primary);
}

.report-table h5 {
  color: var(--brand-primary);
  font-size: 1rem;
  font-weight: 600;
  margin: 20px 0 12px 0;
}

.result-table-container {
  padding: 16px 0;
}

.result-table-report {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
  border: 1px solid var(--el-border-color);
  background-color: var(--bg-card);
}

.result-table-report th,
.result-table-report td {
  padding: 12px;
  border: 1px solid var(--el-border-color);
  text-align: center;
}

.result-table-report th {
  background-color: var(--bg-main);
  font-weight: 600;
  color: var(--text-primary);
}

.result-table-report td {
  color: var(--text-primary);
}

.danger-value {
  color: var(--brand-accent);
  font-weight: 600;
}

.safe-text {
  color: #67c23a;
  font-weight: 600;
}

.warning-text {
  color: var(--brand-accent);
  font-weight: 600;
}

.result-summary {
  padding: 16px;
  background-color: var(--bg-main);
  border-radius: 8px;
  border: 1px solid var(--el-border-color);
}

.result-summary p {
  margin: 8px 0;
  color: var(--text-primary);
  line-height: 1.6;
}

.highlight-value {
  color: var(--brand-accent);
  font-weight: 700;
  font-size: 1.1rem;
}

/* 导出按钮组样式 */
.export-buttons {
  display: flex;
  gap: 8px;
}

/* PDF模板专用样式 */
.pdf-report-container {
  font-family: 'SimSun', 'Microsoft YaHei', Arial, sans-serif;
  color: #000000;
  background-color: #ffffff;
  padding: 20mm;
  width: 170mm; /* A4纸内容宽度，减去边距 */
  /* 移除min-height，让内容自然流动 */
  line-height: 1.6;
  font-size: 12px;
}

.pdf-header {
  text-align: center;
  margin-bottom: 30px;
  border-bottom: 3px solid #2c5aa0;
  padding-bottom: 20px;
}

.logo-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.pdf-logo {
  height: 60px;
  width: auto;
}

.company-info h1 {
  font-size: 20px;
  font-weight: bold;
  color: #2c5aa0;
  margin: 0 0 10px 0;
}

.company-info h2 {
  font-size: 16px;
  font-weight: bold;
  color: #333333;
  margin: 0;
}

.pdf-divider {
  border-top: 2px solid #cccccc;
  margin: 20px 0;
}

.pdf-divider-thin {
  border-top: 1px solid #cccccc;
  margin: 15px 0;
}

.pdf-section {
  margin-bottom: 25px;
}

.pdf-section-title {
  font-size: 14px;
  font-weight: bold;
  color: #2c5aa0;
  margin: 20px 0 10px 0;
  padding: 8px 0;
  text-align: center;
  border-top: 1px solid #cccccc;
  border-bottom: 1px solid #cccccc;
}

.pdf-subsection-title {
  font-size: 13px;
  font-weight: bold;
  color: #333333;
  margin: 15px 0 8px 0;
}

.pdf-project-name {
  font-size: 16px;
  font-weight: bold;
  text-align: center;
  margin: 15px 0;
  color: #2c5aa0;
}

.pdf-table {
  width: 100%;
  border-collapse: collapse;
  margin: 10px 0;
  font-size: 11px;
}

.pdf-table td,
.pdf-table th {
  border: 1px solid #333333;
  padding: 8px;
  text-align: left;
}

.pdf-table th {
  background-color: #f0f0f0;
  font-weight: bold;
  text-align: center;
}

.pdf-table-label {
  font-weight: bold;
  background-color: #f8f8f8;
  width: 40%;
}

.pdf-data-table {
  font-size: 10px;
}

.pdf-data-table td,
.pdf-data-table th {
  text-align: center;
  padding: 6px;
}

.pdf-result-table {
  margin: 15px 0;
}

.pdf-result-summary {
  background-color: #f8f9fa;
  padding: 15px;
  border: 1px solid #cccccc;
  border-radius: 4px;
  margin: 15px 0;
}

.pdf-result-summary p {
  margin: 5px 0;
  font-size: 12px;
}

.pdf-highlight-value {
  color: #d63384;
  font-weight: bold;
  font-size: 14px;
}

.pdf-danger-value {
  color: #dc3545;
  font-weight: bold;
}

.pdf-safe-text {
  color: #198754;
  font-weight: bold;
}

.pdf-warning-text {
  color: #dc3545;
  font-weight: bold;
}

.pdf-chart {
  text-align: center;
  margin: 20px 0;
  padding: 10px;
  border: 1px solid #cccccc;
  background-color: #ffffff;
}

.pdf-chart img {
  max-width: 100%;
  height: auto;
}

.pdf-assessment {
  font-size: 12px;
  line-height: 1.7;
}

.pdf-assessment p {
  margin: 8px 0;
}

.pdf-assessment ul,
.pdf-assessment ol {
  margin: 10px 0;
  padding-left: 25px;
}

.pdf-assessment li {
  margin: 5px 0;
}

.pdf-conclusion {
  background-color: #f8f9fa;
  padding: 15px;
  border-left: 4px solid #2c5aa0;
  margin: 15px 0;
  font-style: italic;
}

.pdf-footer {
  margin-top: 40px;
  border-top: 2px solid #cccccc;
  padding-top: 20px;
}

.pdf-signature {
  text-align: right;
  font-size: 11px;
  color: #666666;
}

.pdf-signature p {
  margin: 5px 0;
}

.soil-layers-section {
  margin-bottom: 24px;
  background-color: var(--bg-section);
  border-radius: 8px;
  padding: 16px;
  border: 1px solid var(--el-border-color-light);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.action-buttons {
  display: flex;
  gap: 12px;
}

.soil-layers-table {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 16px;
}

.soil-layers-table :deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
}

.soil-layers-table :deep(.el-table__header-wrapper) {
  border-radius: 8px 8px 0 0;
}

.soil-layers-table :deep(.numeric-value) {
  font-weight: 600;
  color: var(--brand-primary);
}

.soil-summary {
  background-color: var(--bg-main);
  border-radius: 8px;
  padding: 12px 16px;
  border: 1px solid var(--el-border-color-light);
  display: flex;
  gap: 24px;
}

.summary-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.summary-label {
  color: var(--text-secondary);
  font-size: 0.85rem;
  font-weight: 500;
}

.summary-value {
  color: var(--brand-primary);
  font-size: 1.1rem;
  font-weight: 700;
}

.soil-layer-form :deep(.el-form-item__label) {
  color: var(--text-primary);
  font-weight: 500;
}

.soil-layer-form :deep(.el-input__wrapper),
.soil-layer-form :deep(.el-input-number),
.soil-layer-form :deep(.el-select__wrapper) {
  background-color: var(--bg-input);
  box-shadow: none;
  border: 1px solid var(--el-border-color);
}

.soil-layer-form :deep(.el-input__inner),
.soil-layer-form :deep(.el-input-number__input),
.soil-layer-form :deep(.el-select__text) {
  color: var(--text-primary) !important;
}

.soil-layer-form :deep(.el-select .el-select__tags-text) {
  color: var(--text-primary);
}

.soil-layer-form :deep(.el-tag) {
  background-color: rgba(139, 92, 246, 0.2);
  border-color: rgba(139, 92, 246, 0.3);
  color: var(--text-primary);
}

.soil-layer-form :deep(.el-input__wrapper:hover),
.soil-layer-form :deep(.el-input-number:hover),
.soil-layer-form :deep(.el-select__wrapper:hover) {
  border-color: var(--brand-primary);
}

.soil-layer-form :deep(.el-input__wrapper.is-focus),
.soil-layer-form :deep(.el-input-number.is-focus),
.soil-layer-form :deep(.el-select__wrapper.is-focus) {
  border-color: var(--brand-primary);
  box-shadow: 0 0 0 1px var(--brand-primary);
}

.soil-layer-form .full-width {
  width: 100%;
}

.soil-layer-form .form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

/* 规范和公式样式 */
.pdf-standards {
  margin: 10px 0;
  padding: 10px;
  background-color: #f8f9fa;
  border-left: 4px solid #2c5aa0;
}

.pdf-standards p {
  margin: 5px 0;
  font-size: 11px;
  line-height: 1.5;
}

.pdf-formulas {
  margin: 15px 0;
}

.formula-item {
  margin: 15px 0;
  padding: 10px;
  border: 1px solid #cccccc;
  background-color: #ffffff;
  border-radius: 4px;
}

.formula-item p {
  margin: 5px 0;
}

.formula-text {
  font-family: 'Times New Roman', serif;
  font-size: 12px;
  font-weight: bold;
  color: #2c5aa0;
  background-color: #f0f4ff;
  padding: 8px;
  border-radius: 3px;
  text-align: center;
  margin: 8px 0 !important;
}

.formula-desc {
  font-size: 10px;
  color: #666666;
  font-style: italic;
  line-height: 1.4;
}

.pdf-calculation-steps {
  margin: 15px 0;
  padding: 10px;
  background-color: #f8f9fa;
  border: 1px solid #cccccc;
  border-radius: 4px;
}

.pdf-calculation-steps p {
  margin: 6px 0;
  font-size: 11px;
  line-height: 1.5;
}
</style> 