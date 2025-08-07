<template>
  <div class="foundation-stability-view">
    <div class="page-header">
      <h1>电线塔基础稳定性计算</h1>
      <p class="page-description">依据《建筑地基基础设计规范》(GB50007-2011)及相关电力行业规范，对电线塔基础的承载力、抗倾覆及抗滑移稳定性进行全面验算。</p>
    </div>

    <el-row :gutter="32">
      <!-- 左侧输入表单 -->
      <el-col :xs="24" :sm="24" :md="10" :lg="10" :xl="10">
        <el-card class="form-card" shadow="never">
            <template #header>
              <div class="card-header">
                <h2><el-icon class="header-icon"><Connection /></el-icon> 计算输入参数</h2>
                 <el-tooltip content="请依据地勘报告和设计图纸填写所有参数。">
                  <el-icon><QuestionFilled /></el-icon>
                </el-tooltip>
              </div>
            </template>
            
            <el-form :model="formData" label-position="top" class="calculation-form">
              <!-- 项目信息 -->
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
              
              <div class="schematic-diagram-container">
                <img src="@/assets/images/电线跨越简图.png" alt="电线跨越简图" class="schematic-diagram">
              </div>
              
              <!-- 基础与荷载参数 -->
              <div class="form-section">
                <h3><el-icon><Odometer /></el-icon> 基础与荷载参数</h3>
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="基础宽度 b (m)">
                      <el-input-number v-model="formData.foundationWidth_b" :min="0" :precision="2" :step="0.1" class="full-width" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="基础长度 l (m)">
                      <el-input-number v-model="formData.foundationLength_l" :min="0" :precision="2" :step="0.1" class="full-width" />
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="基础埋深 d (m)">
                      <el-input-number v-model="formData.foundationDepth_d" :min="0" :precision="2" :step="0.1" class="full-width" />
                    </el-form-item>
                  </el-col>
                   <el-col :span="12">
                     <el-form-item label="水平力作用高度 h (m)">
                      <el-input-number v-model="formData.horizontalForceHeight_h" :min="0" :precision="2" :step="0.1" class="full-width" />
                    </el-form-item>
                  </el-col>
                </el-row>
                 <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="塔腿轴向压力 N (kN)">
                      <el-input-number v-model="formData.towerAxialPressure_N" :min="0" :precision="2" :step="10" class="full-width" />
                    </el-form-item>
                  </el-col>
                   <el-col :span="12">
                     <el-form-item label="基础及覆土总重 G (kN)">
                      <el-input-number v-model="formData.foundationGravity_G" :min="0" :precision="2" :step="10" class="full-width" />
                    </el-form-item>
                  </el-col>
                </el-row>
                 <el-form-item label="水平力 Fw (kN)">
                  <el-input-number v-model="formData.horizontalForce_Fw" :min="0" :precision="2" :step="10" class="full-width" />
                </el-form-item>
              </div>
              
              <!-- 土质参数 -->
              <div class="form-section">
                <h3><el-icon><Files /></el-icon> 地质参数</h3>
                 <el-form-item label="地勘提供承载力标准值 fak (kPa)">
                  <el-input-number v-model="formData.bearingCapacityStandard_fak" :min="0" :precision="1" :step="10" class="full-width" />
                </el-form-item>
                <el-row :gutter="20">
                   <el-col :span="12">
                      <el-form-item label="基底以下土重度 γ (kN/m³)">
                        <el-input-number v-model="formData.soilUnitWeight_gamma" :min="0" :precision="1" :step="0.5" class="full-width" />
                      </el-form-item>
                   </el-col>
                   <el-col :span="12">
                     <el-form-item label="基底以上土平均重度 γm (kN/m³)">
                       <el-input-number v-model="formData.soilUnitWeight_gamma_m" :min="0" :precision="1" :step="0.5" class="full-width" />
                     </el-form-item>
                   </el-col>
                </el-row>
                <el-row :gutter="20">
                  <el-col :span="12">
                     <el-form-item label="宽度修正系数 ηb">
                       <el-input-number v-model="formData.widthCorrectionFactor_eta_b" :min="0" :precision="2" :step="0.1" class="full-width" />
                     </el-form-item>
                  </el-col>
                   <el-col :span="12">
                     <el-form-item label="深度修正系数 ηd">
                       <el-input-number v-model="formData.depthCorrectionFactor_eta_d" :min="0" :precision="2" :step="0.1" class="full-width" />
                     </el-form-item>
                  </el-col>
                </el-row>
                 <el-form-item label="基底摩擦系数 μ">
                  <el-input-number v-model="formData.frictionCoefficient_mu" :min="0" :max="1" :precision="2" :step="0.05" class="full-width" />
                </el-form-item>
                
                <!-- 土层参数管理 -->
                <div class="soil-layers-section">
                  <div class="section-header">
                    <h4><el-icon><Document /></el-icon> 土层参数</h4>
                    <div class="action-buttons">
                      <el-button type="primary" size="small" @click="showSoilLayerDialog = true">
                        <el-icon><Plus /></el-icon> 编辑土层
                      </el-button>
                      <el-button type="success" size="small" @click="addSoilLayer">
                        <el-icon><Plus /></el-icon> 添加土层
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
                    >
                      <el-table-column prop="depth" label="深度 (m)" width="120">
                        <template #default="scope">
                          <span>{{ scope.row.depthStart }}-{{ scope.row.depthEnd }}</span>
                        </template>
                      </el-table-column>
                      <el-table-column prop="soilType" label="土层名称" width="100">
                        <template #default="scope">
                          <span>{{ scope.row.soilType }}</span>
                        </template>
                      </el-table-column>
                      <el-table-column prop="bearingCapacity" label="Es值(MPa)" width="120">
                        <template #default="scope">
                          <span class="numeric-value">{{ scope.row.bearingCapacity }}</span>
                        </template>
                      </el-table-column>
                      <el-table-column prop="poissonRatio" label="泊松比ν" width="100">
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
                          >
                            删除
                          </el-button>
                        </template>
                      </el-table-column>
                    </el-table>
                  </div>
                </div>
              </div>
              
              <!-- 土层编辑对话框 -->
              <el-dialog
                v-model="showSoilLayerDialog"
                title="编辑土层"
                width="500px"
                :before-close="handleSoilLayerDialogClose"
              >
                <el-form :model="currentSoilLayer" label-position="top" class="soil-layer-form">
                  <el-row :gutter="20">
                    <el-col :span="12">
                      <el-form-item label="深度范围 (m)">
                        <div class="depth-range">
                          <el-input-number 
                            v-model="currentSoilLayer.depthStart" 
                            :min="0" 
                            :precision="1" 
                            :step="0.5" 
                            placeholder="起始深度"
                            class="depth-input"
                          />
                          <span class="depth-separator">-</span>
                          <el-input-number 
                            v-model="currentSoilLayer.depthEnd" 
                            :min="0" 
                            :precision="1" 
                            :step="0.5" 
                            placeholder="结束深度"
                            class="depth-input"
                          />
                        </div>
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="土层名称">
                        <el-select v-model="currentSoilLayer.soilType" placeholder="选择土层类型" class="full-width">
                          <el-option label="粘土" value="粘土" />
                          <el-option label="砂土" value="砂土" />
                          <el-option label="粉土" value="粉土" />
                          <el-option label="淤泥" value="淤泥" />
                          <el-option label="岩石" value="岩石" />
                        </el-select>
                      </el-form-item>
                    </el-col>
                  </el-row>
                  <el-row :gutter="20">
                    <el-col :span="12">
                      <el-form-item label="压缩模量 Es (MPa)">
                        <el-input-number 
                          v-model="currentSoilLayer.bearingCapacity" 
                          :min="0" 
                          :precision="1" 
                          :step="0.5" 
                          class="full-width"
                        />
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="泊松比 ν">
                        <el-select v-model="currentSoilLayer.poissonRatio" placeholder="选择泊松比" class="full-width">
                          <el-option label="0.35" value="0.35" />
                          <el-option label="0.30" value="0.30" />
                          <el-option label="0.28" value="0.28" />
                          <el-option label="0.25" value="0.25" />
                        </el-select>
                      </el-form-item>
                    </el-col>
                  </el-row>
                </el-form>
                
                <template #footer>
                  <span class="dialog-footer">
                    <el-button @click="handleSoilLayerDialogClose">取消</el-button>
                    <el-button type="primary" @click="saveSoilLayer">
                      {{ editingIndex === -1 ? '确定' : '保存' }}
                    </el-button>
                  </span>
                </template>
              </el-dialog>
              
              <!-- 塔体自重计算表格 -->
              <div class="form-section">
                <h3><el-icon><OfficeBuilding /></el-icon> 塔体自重计算</h3>
                <div class="tower-weight-table">
                  <el-table 
                    :data="towerWeightData" 
                    border 
                    style="width: 100%"
                    :header-cell-style="{ backgroundColor: '#f5f7fa', color: '#333', fontWeight: '600' }"
                    show-summary
                    sum-text="合计"
                    :summary-method="getTowerWeightSummaries"
                  >
                    <el-table-column prop="materialType" label="材料类别" width="120">
                      <template #default="scope">
                        <span>{{ scope.row.materialType }}</span>
                      </template>
                    </el-table-column>
                    <el-table-column prop="length" label="延米长度 (m)" width="130">
                      <template #default="scope">
                        <el-input-number 
                          v-model="scope.row.length" 
                          :min="0" 
                          :precision="2" 
                          :step="0.1" 
                          size="small"
                          @change="calculateRowWeight(scope.$index)"
                        />
                      </template>
                    </el-table-column>
                    <el-table-column prop="crossSectionArea" label="横截面积 (m²)" width="140">
                      <template #default="scope">
                        <el-input-number 
                          v-model="scope.row.crossSectionArea" 
                          :min="0" 
                          :precision="4" 
                          :step="0.001" 
                          size="small"
                          @change="calculateRowWeight(scope.$index)"
                        />
                      </template>
                    </el-table-column>
                    <el-table-column prop="density" label="密度 (kg/m³)" width="130">
                      <template #default="scope">
                        <el-input-number 
                          v-model="scope.row.density" 
                          :min="0" 
                          :precision="0" 
                          :step="100" 
                          size="small"
                          @change="calculateRowWeight(scope.$index)"
                        />
                      </template>
                    </el-table-column>
                    <el-table-column prop="totalMass" label="总质量 (kg)" width="120">
                      <template #default="scope">
                        <span class="numeric-value">{{ scope.row.totalMass.toFixed(2) }}</span>
                      </template>
                    </el-table-column>
                  </el-table>
                  
                  <div class="weight-summary">
                    <div class="summary-item">
                      <span class="summary-label">塔体总重量：</span>
                      <span class="summary-value">{{ getTotalTowerWeight() }} kg</span>
                    </div>
                    <div class="summary-item">
                      <span class="summary-label">塔体总重力：</span>
                      <span class="summary-value highlight">{{ (getTotalTowerWeight() * 9.8 / 1000).toFixed(2) }} kN</span>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="form-actions">
                <el-button type="primary" @click="performCalculations" :loading="calculating" size="large">
                  <el-icon><Cpu /></el-icon> 开始验算
                </el-button>
                <el-button @click="resetForm" size="large">
                  <el-icon><RefreshRight /></el-icon> 重置参数
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
                <el-tag v-if="hasResults" :type="results.isStable ? 'success' : 'danger'" effect="light" size="small">
                  {{ results.isStable ? '验算通过' : '验算不通过' }}
                </el-tag>
              </div>
            </template>
            
            <el-tabs v-model="activeTab" class="result-tabs">
              <el-tab-pane label="稳定性验算结果" name="stability-results">
            <div v-if="hasResults" class="result-content">
                  <!-- 可视化图片 -->
                  <div class="visualization-section">
                    <h4 class="section-title">
                      <el-icon><PieChart /></el-icon>
                      基础稳定性验算可视化
                    </h4>
                    <TowerFoundationVisualization
                      :bearingCapacityOk="results.bearingCapacityOk"
                      :overturningOk="results.overturningOk"
                      :slidingOk="results.slidingOk"
                      :maxPressure="results.Pmax_maxPressure"
                      :minPressure="results.Pmin_minPressure"
                      :overturningFactor="results.K_overturningSafetyFactor"
                      :slidingFactor="results.Kh_slidingSafetyFactor"
                    />
                  </div>

              <!-- 承载力验算 -->
              <el-descriptions title="1. 地基承载力验算" :column="2" border class="result-descriptions">
                <el-descriptions-item label="fa 修正后地基承载力" label-align="left" :span="2">
                  <span class="numeric-value">{{ results.fa_adjustedBearingCapacity }} kPa</span>
                </el-descriptions-item>
                <el-descriptions-item label="Pmax 基底最大压力" label-align="left">
                  <span class="numeric-value">{{ results.Pmax_maxPressure }} kPa</span>
                </el-descriptions-item>
                <el-descriptions-item label="Pmin 基底最小压力" label-align="left">
                   <span class="numeric-value">{{ results.Pmin_minPressure }} kPa</span>
                </el-descriptions-item>
                <el-descriptions-item label="验算结论" label-align="left" :span="2">
                  <el-tag :type="results.bearingCapacityOk ? 'success' : 'danger'" effect="dark" class="conclusion-tag">
                    <div>Pmax = {{ results.Pmax_maxPressure }} kPa ≤ 1.2 * fa = {{ (1.2 * results.fa_adjustedBearingCapacity).toFixed(2) }} kPa</div>
                    <div>Pmin = {{ results.Pmin_minPressure }} kPa ≥ 0</div>
                    <div class="conclusion-separator"></div>
                    <div class="conclusion-text">结论: {{ results.bearingCapacityOk ? '通过' : '不通过' }}</div>
                  </el-tag>
                </el-descriptions-item>
              </el-descriptions>

              <!-- 抗倾覆验算 -->
              <el-descriptions title="2. 抗倾覆验算" :column="2" border class="result-descriptions">
                <el-descriptions-item label="M倾 倾覆力矩" label-align="left">
                  <span class="numeric-value">{{ results.M_overturningMoment }} kN·m</span>
                </el-descriptions-item>
                <el-descriptions-item label="M抗 抗倾覆力矩" label-align="left">
                  <span class="numeric-value">{{ results.M_resistingMoment }} kN·m</span>
                </el-descriptions-item>
                <el-descriptions-item label="K 抗倾覆安全系数" label-align="left" :span="2">
                   <el-tag :type="results.overturningOk ? 'success' : 'danger'" effect="dark">
                    K = {{ results.K_overturningSafetyFactor }} ≥ 1.5
                    (结论: {{ results.overturningOk ? '通过' : '不通过' }})
                  </el-tag>
                </el-descriptions-item>
              </el-descriptions>
              
               <!-- 抗滑移验算 -->
              <el-descriptions title="3. 抗滑移验算" :column="2" border class="result-descriptions">
                <el-descriptions-item label="F滑 水平滑动力" label-align="left">
                  <span class="numeric-value">{{ results.F_slidingForce }} kN</span>
                </el-descriptions-item>
                <el-descriptions-item label="R抗 抗滑移力" label-align="left">
                  <span class="numeric-value">{{ results.R_resistingForce }} kN</span>
                </el-descriptions-item>
                <el-descriptions-item label="Kh 抗滑移安全系数" label-align="left" :span="2">
                   <el-tag :type="results.slidingOk ? 'success' : 'danger'" effect="dark">
                    Kh = {{ results.Kh_slidingSafetyFactor }} ≥ 1.3
                    (结论: {{ results.slidingOk ? '通过' : '不通过' }})
                  </el-tag>
                </el-descriptions-item>
              </el-descriptions>
            </div>
            <div v-else class="empty-result">
              <el-empty description="暂无数据，请先进行验算" />
            </div>
              </el-tab-pane>

              <!-- 安全评估报告 -->
              <el-tab-pane label="安全评估报告" name="safety-report">
                <div v-if="hasResults" class="safety-report">
                  <div class="report-header">
                    <h3><el-icon><Document /></el-icon> 电线塔基础稳定性安全评估报告</h3>
                    <div class="export-buttons">
                      <el-button type="primary" size="small" @click="exportPDFReport" :loading="exportingPDF">
                        <el-icon><Download /></el-icon> 导出PDF报告
                      </el-button>
                      <el-button type="info" size="small" @click="exportTXTReport">
                        <el-icon><Document /></el-icon> 导出TXT报告
                      </el-button>
                    </div>
                  </div>
                  
                  <!-- 报告内容 -->
                  <div class="report-content">
                    <!-- 计算结果概况 -->
                    <div class="report-section">
                      <h4>一、计算结果概况</h4>
                      <el-descriptions :column="2" border>
                        <el-descriptions-item label="修正后地基承载力">{{ results.fa_adjustedBearingCapacity }} kPa</el-descriptions-item>
                        <el-descriptions-item label="基底最大压力">{{ results.Pmax_maxPressure }} kPa</el-descriptions-item>
                        <el-descriptions-item label="基底最小压力">{{ results.Pmin_minPressure }} kPa</el-descriptions-item>
                        <el-descriptions-item label="抗倾覆安全系数">{{ results.K_overturningSafetyFactor }}</el-descriptions-item>
                        <el-descriptions-item label="抗滑移安全系数">{{ results.Kh_slidingSafetyFactor }}</el-descriptions-item>
                        <el-descriptions-item label="整体稳定性">
                          <el-tag :type="results.isStable ? 'success' : 'danger'" effect="light">
                            {{ results.isStable ? '稳定' : '不稳定' }}
                          </el-tag>
                        </el-descriptions-item>
                      </el-descriptions>
                    </div>

                    <!-- 规范要求对比 -->
                    <div class="report-section">
                      <h4>二、规范要求对比</h4>
                      <el-table :data="getComparisonTableData()" border>
                        <el-table-column prop="item" label="验算项目" />
                        <el-table-column prop="calculated" label="计算值" />
                        <el-table-column prop="standard" label="规范要求" />
                        <el-table-column prop="result" label="验算结果">
                          <template #default="scope">
                            <el-tag :type="scope.row.passed ? 'success' : 'danger'" effect="light">
                              {{ scope.row.passed ? '通过' : '不通过' }}
                            </el-tag>
                          </template>
                        </el-table-column>
                      </el-table>
                    </div>

                    <!-- 安全性评估 -->
                    <div class="report-section">
                      <h4>三、安全性评估</h4>
                      <div class="safety-assessment">
                        <el-alert 
                          :title="getSafetyTitle()" 
                          :type="getSafetyType()" 
                          :description="getSafetyDescription()" 
                          show-icon 
                          :closable="false"
                        />
                      </div>
                    </div>

                    <!-- 技术建议 -->
                    <div class="report-section">
                      <h4>四、技术建议</h4>
                      <ul class="recommendations-list">
                        <li v-for="(recommendation, index) in getRecommendations()" :key="index">
                          {{ recommendation }}
                        </li>
                      </ul>
                    </div>

                    <!-- 结论 -->
                    <div class="report-section">
                      <h4>五、评估结论</h4>
                      <div class="conclusion">
                        <p>{{ getConclusion() }}</p>
                        <div class="signature-section">
                          <p>计算日期：{{ getCurrentDate() }}</p>
                          <p>计算软件：桥梁跨越工程安全性评估软件 v2.0</p>
                          <p>技术支持：吉林省志安科技有限公司</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else class="empty-result">
                  <el-empty description="暂无数据，请先进行验算" />
                </div>
              </el-tab-pane>
            </el-tabs>

            <!-- PDF导出专用的隐藏模板 -->
            <div id="tower-pdf-report-template" style="display: none;">
              <div class="pdf-report-container">
                <!-- 报告头部 -->
                <PdfReportHeader reportTitle="电线塔基础稳定性安全评估报告" />
                
                <!-- 项目基本信息 -->
                <div class="pdf-section">
                  <h3 class="pdf-section-title">项目名称</h3>
                  <div class="pdf-divider-thin"></div>
                  <p class="pdf-project-name">{{ formData.projectName || '电线塔基础稳定性项目' }}</p>
                  <div class="pdf-divider-thin"></div>
                  
                  <h3 class="pdf-section-title">项目类型</h3>
                  <div class="pdf-divider-thin"></div>
                  <p>电线塔基础稳定性计算</p>
                  <div class="pdf-divider-thin"></div>
                  </div>

                <!-- 计算条件 -->
                <div class="pdf-section">
                  <h3 class="pdf-section-title">计算条件</h3>
                  <div class="pdf-divider-thin"></div>
                  
                  <h4 class="pdf-subsection-title">基础与荷载参数</h4>
                  <table class="pdf-table">
                    <tbody>
                      <tr>
                        <td class="pdf-table-label">基础宽度 b：</td>
                        <td>{{ formData.foundationWidth_b }}m</td>
                      </tr>
                      <tr>
                        <td class="pdf-table-label">基础长度 l：</td>
                        <td>{{ formData.foundationLength_l }}m</td>
                      </tr>
                      <tr>
                        <td class="pdf-table-label">基础埋深 d：</td>
                        <td>{{ formData.foundationDepth_d }}m</td>
                      </tr>
                      <tr>
                        <td class="pdf-table-label">水平力作用高度 h：</td>
                        <td>{{ formData.horizontalForceHeight_h }}m</td>
                      </tr>
                      <tr>
                        <td class="pdf-table-label">塔腿轴向压力 N：</td>
                        <td>{{ formData.towerAxialPressure_N }}kN</td>
                      </tr>
                      <tr>
                        <td class="pdf-table-label">基础及覆土总重 G：</td>
                        <td>{{ formData.foundationGravity_G }}kN</td>
                      </tr>
                      <tr>
                        <td class="pdf-table-label">水平力 Fw：</td>
                        <td>{{ formData.horizontalForce_Fw }}kN</td>
                      </tr>
                    </tbody>
                  </table>
                  
                  <h4 class="pdf-subsection-title">地质参数</h4>
                  <table class="pdf-table">
                    <tbody>
                      <tr>
                        <td class="pdf-table-label">地勘承载力标准值 fak：</td>
                        <td>{{ formData.bearingCapacityStandard_fak }}kPa</td>
                      </tr>
                      <tr>
                        <td class="pdf-table-label">基底以下土重度 γ：</td>
                        <td>{{ formData.soilUnitWeight_gamma }}kN/m³</td>
                      </tr>
                      <tr>
                        <td class="pdf-table-label">基底以上土平均重度 γm：</td>
                        <td>{{ formData.soilUnitWeight_gamma_m }}kN/m³</td>
                      </tr>
                      <tr>
                        <td class="pdf-table-label">宽度修正系数 ηb：</td>
                        <td>{{ formData.widthCorrectionFactor_eta_b }}</td>
                      </tr>
                      <tr>
                        <td class="pdf-table-label">深度修正系数 ηd：</td>
                        <td>{{ formData.depthCorrectionFactor_eta_d }}</td>
                      </tr>
                      <tr>
                        <td class="pdf-table-label">基底摩擦系数 μ：</td>
                        <td>{{ formData.frictionCoefficient_mu }}</td>
                      </tr>
                    </tbody>
                  </table>
                  
                  <div class="pdf-divider-thin"></div>
                </div>


                
                <!-- 计算依据和公式 -->
                <div class="pdf-section">
                  <h3 class="pdf-section-title">计算依据和公式</h3>
                  <div class="pdf-divider-thin"></div>
                  
                  <h4 class="pdf-subsection-title">规范依据</h4>
                  <div class="pdf-standards">
                    <p><strong>1. 《建筑地基基础设计规范》GB50007-2011</strong></p>
                    <p><strong>2. 《110kV~750kV架空输电线路设计规范》GB 50545-2010</strong></p>
                    <p><strong>3. 《架空输电线路基础设计技术规程》DL/T 5219-2014</strong></p>
                    <p><strong>4. 《电力工程高压送电线路设计手册》DL/T 5092-1999</strong></p>
                    <p><strong>5. 《岩土工程勘察规范》GB50021-2001</strong></p>
                  </div>
                  
                  <h4 class="pdf-subsection-title">主要计算公式</h4>
                  <div class="pdf-formulas">
                    <div class="formula-item">
                      <p><strong>1. 修正后地基承载力计算：</strong></p>
                      <p class="formula-text">fa = fak + ηb·γ·(b-3) + ηd·γm·(d-0.5)</p>
                      <p class="formula-desc">式中：fa - 修正后地基承载力；fak - 标准承载力；ηb,ηd - 宽度和深度修正系数；γ,γm - 土体重度</p>
                    </div>
                    
                    <div class="formula-item">
                      <p><strong>2. 基底压力计算：</strong></p>
                      <p class="formula-text">Pmax/min = N/A ± M/W</p>
                      <p class="formula-desc">式中：N - 总竖向力；A - 基底面积；M - 倾覆力矩；W - 截面抵抗矩</p>
                    </div>
                    
                    <div class="formula-item">
                      <p><strong>3. 地基承载力验算：</strong></p>
                      <p class="formula-text">Pmax ≤ 1.2fa，且 Pmin ≥ 0</p>
                      <p class="formula-desc">最大压力不超过修正承载力的1.2倍，最小压力不小于零（无拉应力）</p>
                    </div>
                    
                    <div class="formula-item">
                      <p><strong>4. 抗倾覆稳定性验算：</strong></p>
                      <p class="formula-text">Kov = Mr/Mo ≥ 1.5</p>
                      <p class="formula-desc">式中：Mr - 抗倾覆力矩；Mo - 倾覆力矩；1.5 - 抗倾覆安全系数</p>
                    </div>
                    
                    <div class="formula-item">
                      <p><strong>5. 抗滑移稳定性验算：</strong></p>
                      <p class="formula-text">Ks = (N·μ + c·A)/H ≥ 1.3</p>
                      <p class="formula-desc">式中：μ - 基底摩擦系数；c - 粘聚力；A - 基底面积；H - 水平力；1.3 - 抗滑移安全系数</p>
                    </div>
                    
                    <div class="formula-item">
                      <p><strong>6. 截面抵抗矩计算：</strong></p>
                      <p class="formula-text">W = b·l²/6</p>
                      <p class="formula-desc">式中：W - 截面抵抗矩；b - 基础宽度；l - 基础长度</p>
                    </div>
                    
                    <div class="formula-item">
                      <p><strong>7. 倾覆力矩计算：</strong></p>
                      <p class="formula-text">Mo = Fw·h</p>
                      <p class="formula-desc">式中：Fw - 水平风荷载；h - 风荷载作用点高度</p>
                    </div>
                  </div>
                  
                  <h4 class="pdf-subsection-title">计算步骤</h4>
                  <div class="pdf-calculation-steps">
                    <p><strong>步骤1：</strong>根据地质条件和基础尺寸计算修正后地基承载力fa</p>
                    <p><strong>步骤2：</strong>计算基底最大和最小压力Pmax、Pmin</p>
                    <p><strong>步骤3：</strong>验算地基承载力：Pmax ≤ 1.2fa且Pmin ≥ 0</p>
                    <p><strong>步骤4：</strong>验算抗倾覆稳定性：Kov = Mr/Mo ≥ 1.5</p>
                    <p><strong>步骤5：</strong>验算抗滑移稳定性：Ks ≥ 1.3</p>
                    <p><strong>步骤6：</strong>综合评估基础稳定性并提出优化建议</p>
                  </div>
                  
                  <div class="pdf-divider-thin"></div>
                </div>
                
                <!-- 计算结果与规范对比 -->
                <div class="pdf-section">
                  <h3 class="pdf-section-title">计算结果与规范对比</h3>
                  <div class="pdf-divider-thin"></div>
                  <table class="pdf-table">
                    <thead>
                      <tr>
                        <th width="25%">验算项目</th>
                        <th width="35%">计算值</th>
                        <th width="25%">规范要求</th>
                        <th width="15%">验算结果</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="item in getComparisonTableData()" :key="item.item">
                        <td>{{ item.item }}</td>
                        <td>{{ item.calculated }}</td>
                        <td>{{ item.standard }}</td>
                        <td>
                          <span :class="item.passed ? 'pdf-pass' : 'pdf-fail'">
                            {{ item.passed ? '通过' : '不通过' }}
                          </span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>

                <!-- 可视化结果 -->
                <div class="pdf-section">
                  <h3 class="pdf-section-title">可视化验算结果</h3>
                  <div class="pdf-divider-thin"></div>
                  <div id="pdf-tower-chart-container" class="pdf-chart">
                    <!-- 图表将在此处生成 -->
                  </div>
                </div>

                <!-- 安全评估 -->
                <div class="pdf-section">
                  <h3 class="pdf-section-title">电线塔基础稳定性安全评估报告</h3>
                  <div class="pdf-divider-thin"></div>
                  
                  <div class="pdf-assessment">
                    <p><strong>整体安全状况：</strong>{{ results.isStable ? '安全' : '需要关注' }}</p>
                    <p>{{ getConclusion() }}</p>
                    
                    <h4 class="pdf-subsection-title">验算通过情况统计：</h4>
                    <ul>
                      <li>地基承载力验算：{{ results.bearingCapacityOk ? '✓ 通过' : '✗ 不通过' }}</li>
                      <li>抗倾覆稳定性验算：{{ results.overturningOk ? '✓ 通过' : '✗ 不通过' }}</li>
                      <li>抗滑移稳定性验算：{{ results.slidingOk ? '✓ 通过' : '✗ 不通过' }}</li>
                    </ul>
                    
                    <h4 class="pdf-subsection-title">技术建议：</h4>
                    <ol>
                      <li v-for="(rec, index) in getRecommendations()" :key="index">
                        <strong>建议{{ index + 1 }}：</strong>{{ rec }}
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
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
// ShineBorder is no longer used
import { 
  Connection, 
  Odometer, 
  Files, 
  RefreshRight,
  QuestionFilled,
  TrendCharts,
  Cpu,
  Document,
  Download,
  OfficeBuilding,
  PieChart,
  Plus,
} from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import TowerFoundationVisualization from '@/components/TowerFoundationVisualization.vue';
import { jsPDF } from 'jspdf'; // 导入jspdf库
import html2pdf from 'html2pdf.js'
import html2canvas from 'html2canvas'
import fontBase64 from '@/assets/fonts/fontBase64.json';
// 引入logo图片 - 使用PNG格式
import logoImage from '@/assets/logo.png';

// --- 响应式状态定义 ---

const defaultFormData = {
  // 项目信息
  projectName: '电线塔基础稳定性项目',
  projectInfo: '',
  // 基础与荷载
  foundationWidth_b: 4.0,
  foundationLength_l: 4.0,
  foundationDepth_d: 2.0,
  horizontalForceHeight_h: 15.0,
  towerAxialPressure_N: 500.0,
  foundationGravity_G: 800.0,
  horizontalForce_Fw: 100.0,
  // 地质参数
  bearingCapacityStandard_fak: 200.0,
  soilUnitWeight_gamma: 18.0,
  soilUnitWeight_gamma_m: 18.0,
  widthCorrectionFactor_eta_b: 0.3,
  depthCorrectionFactor_eta_d: 1.6,
  frictionCoefficient_mu: 0.4,
};

const formData = reactive({ ...defaultFormData });

// 塔体自重计算数据
const towerWeightData = reactive([
  { materialType: '1', length: 0, crossSectionArea: 0, density: 7850, totalMass: 0 },
  { materialType: '2', length: 0, crossSectionArea: 0, density: 7850, totalMass: 0 },
  { materialType: '3', length: 0, crossSectionArea: 0, density: 7850, totalMass: 0 },
  { materialType: '4', length: 0, crossSectionArea: 0, density: 7850, totalMass: 0 },
  { materialType: '5', length: 0, crossSectionArea: 0, density: 7850, totalMass: 0 },
  { materialType: '6', length: 0, crossSectionArea: 0, density: 7850, totalMass: 0 },
  { materialType: '7', length: 0, crossSectionArea: 0, density: 7850, totalMass: 0 },
  { materialType: '8', length: 0, crossSectionArea: 0, density: 7850, totalMass: 0 },
  { materialType: '9', length: 0, crossSectionArea: 0, density: 7850, totalMass: 0 },
  { materialType: '10', length: 0, crossSectionArea: 0, density: 7850, totalMass: 0 }
]);

const results = reactive({
  // 承载力
  fa_adjustedBearingCapacity: 0,
  Pmax_maxPressure: 0,
  Pmin_minPressure: 0,
  bearingCapacityOk: false,
  // 抗倾覆
  M_overturningMoment: 0,
  M_resistingMoment: 0,
  K_overturningSafetyFactor: 0,
  overturningOk: false,
  // 抗滑移
  F_slidingForce: 0,
  R_resistingForce: 0,
  Kh_slidingSafetyFactor: 0,
  slidingOk: false,
  // 总体
  isStable: false,
});

const hasResults = ref(false);
const calculating = ref(false);
const activeTab = ref('stability-results');
const exportingPDF = ref(false);

// --- 方法 ---

const performCalculations = () => {
  calculating.value = true;
  hasResults.value = false;

  setTimeout(() => {
    try {
      calculateBearingCapacity();
      calculateOverturningStability();
      calculateSlidingStability();

      results.isStable = results.bearingCapacityOk && results.overturningOk && results.slidingOk;
      hasResults.value = true;
      ElMessage({ message: '稳定性验算完成！', type: 'success' });

    } catch (error) {
      ElMessage({ message: `计算出错: ${error.message}`, type: 'error' });
    } finally {
      calculating.value = false;
    }
  }, 500);
};

// 1. 地基承载力验算
const calculateBearingCapacity = () => {
  const { 
    bearingCapacityStandard_fak, widthCorrectionFactor_eta_b, soilUnitWeight_gamma, 
    foundationWidth_b, depthCorrectionFactor_eta_d, soilUnitWeight_gamma_m, foundationDepth_d,
    towerAxialPressure_N, foundationGravity_G, horizontalForce_Fw, horizontalForceHeight_h,
    foundationLength_l
  } = formData;

  // (1) 修正后的地基承载力 fa
  const fa = bearingCapacityStandard_fak + 
             widthCorrectionFactor_eta_b * soilUnitWeight_gamma * (foundationWidth_b - 3) + 
             depthCorrectionFactor_eta_d * soilUnitWeight_gamma_m * (foundationDepth_d - 0.5);
  results.fa_adjustedBearingCapacity = fa.toFixed(2);
  
  // (2) 基底压力计算
  const A = foundationWidth_b * foundationLength_l; // 基底面积
  const W = (foundationWidth_b * Math.pow(foundationLength_l, 2)) / 6; // 截面抵抗矩
  const M = horizontalForce_Fw * horizontalForceHeight_h; // 倾覆力矩
  const N_total = towerAxialPressure_N + foundationGravity_G; // 总竖向力
  
  const p_avg = N_total / A; // 平均压力
  const p_moment = M / W; // 弯矩引起的压力
  
  results.Pmax_maxPressure = (p_avg + p_moment).toFixed(2);
  results.Pmin_minPressure = (p_avg - p_moment).toFixed(2);

  // (3) 验算
  const condition1 = results.Pmax_maxPressure <= 1.2 * fa;
  const condition2 = results.Pmin_minPressure >= 0;
  results.bearingCapacityOk = condition1 && condition2;
};

// 2. 抗倾覆验算
const calculateOverturningStability = () => {
  const { horizontalForce_Fw, horizontalForceHeight_h, towerAxialPressure_N, foundationGravity_G, foundationWidth_b } = formData;
  
  // (1) 倾覆力矩 M倾
  results.M_overturningMoment = (horizontalForce_Fw * horizontalForceHeight_h).toFixed(2);
  
  // (2) 抗倾覆力矩 M抗
  const N_total = towerAxialPressure_N + foundationGravity_G;
  results.M_resistingMoment = (N_total * (foundationWidth_b / 2)).toFixed(2);
  
  // (3) 安全系数 K
  if (parseFloat(results.M_overturningMoment) > 0) {
    results.K_overturningSafetyFactor = (results.M_resistingMoment / results.M_overturningMoment).toFixed(2);
  } else {
    results.K_overturningSafetyFactor = "∞";
  }
  results.overturningOk = parseFloat(results.K_overturningSafetyFactor) >= 1.5;
};

// 3. 抗滑移验算
const calculateSlidingStability = () => {
    const { towerAxialPressure_N, foundationGravity_G, frictionCoefficient_mu, horizontalForce_Fw } = formData;

    // (1) 抗滑移力 R抗
    const N_total = towerAxialPressure_N + foundationGravity_G;
    results.R_resistingForce = (N_total * frictionCoefficient_mu).toFixed(2);

    // (2) 水平滑动力 F滑 (即 Fw)
    results.F_slidingForce = horizontalForce_Fw.toFixed(2);

    // (3) 安全系数 Kh
    if (parseFloat(results.F_slidingForce) > 0) {
      results.Kh_slidingSafetyFactor = (results.R_resistingForce / results.F_slidingForce).toFixed(2);
    } else {
      results.Kh_slidingSafetyFactor = "∞";
    }
    results.slidingOk = parseFloat(results.Kh_slidingSafetyFactor) >= 1.3;
};


// 重置表单
const resetForm = () => {
  Object.assign(formData, defaultFormData);
  Object.keys(results).forEach(key => {
    if (typeof results[key] === 'number') {
      results[key] = 0;
    } else if (typeof results[key] === 'boolean') {
      results[key] = false;
    }
  });
  
  // 重置塔体自重数据
  towerWeightData.forEach(row => {
    row.length = 0;
    row.crossSectionArea = 0;
    row.density = 7850; // 恢复钢材默认密度
    row.totalMass = 0;
  });
  
  // 重置土层数据
  soilLayersData.splice(0, soilLayersData.length);
  soilLayersData.push(
    { depthStart: 0, depthEnd: 5, soilType: '粘土', bearingCapacity: 10.0, poissonRatio: '0.35' },
    { depthStart: 5, depthEnd: 10, soilType: '砂土', bearingCapacity: 15.0, poissonRatio: '0.30' },
    { depthStart: 10, depthEnd: 15, soilType: '粉土', bearingCapacity: 12.0, poissonRatio: '0.35' },
    { depthStart: 15, depthEnd: 20, soilType: '岩石', bearingCapacity: 18.0, poissonRatio: '0.28' }
  );
  
  hasResults.value = false;
  activeTab.value = 'stability-results';
  ElMessage({ message: '所有参数已重置。', type: 'info' });
};

// --- 塔体自重计算相关方法 ---

// 计算单行重量
const calculateRowWeight = (index) => {
  const row = towerWeightData[index];
  if (row.length && row.crossSectionArea && row.density) {
    // 总质量 = 延米长度 × 横截面积 × 密度
    row.totalMass = row.length * row.crossSectionArea * row.density;
  } else {
    row.totalMass = 0;
  }
};

// 计算塔体总重量
const getTotalTowerWeight = () => {
  return towerWeightData.reduce((total, row) => total + row.totalMass, 0);
};

// 获取表格汇总数据
const getTowerWeightSummaries = (param) => {
  const { columns, data } = param;
  const sums = [];
  
  columns.forEach((column, index) => {
    if (index === 0) {
      sums[index] = '合计';
      return;
    }
    
    if (column.property === 'totalMass') {
      sums[index] = getTotalTowerWeight().toFixed(2);
      return;
    }
    
    if (column.property === 'length' || column.property === 'crossSectionArea' || column.property === 'density') {
      // 计算平均值或显示为空
      const values = data.map(item => Number(item[column.property])).filter(val => val > 0);
      if (values.length > 0) {
        const avg = values.reduce((prev, curr) => prev + curr, 0) / values.length;
        sums[index] = column.property === 'density' ? avg.toFixed(0) : avg.toFixed(2);
      } else {
        sums[index] = '-';
      }
      return;
    }
    
    sums[index] = '';
  });
  
  return sums;
};

// --- 安全评估报告相关方法 ---

// 获取规范要求对比表格数据
const getComparisonTableData = () => {
  return [
    {
      item: '地基承载力验算',
      calculated: `Pmax = ${results.Pmax_maxPressure} kPa, Pmin = ${results.Pmin_minPressure} kPa`,
      standard: `Pmax ≤ 1.2 × fa = ${(1.2 * results.fa_adjustedBearingCapacity).toFixed(2)} kPa, Pmin ≥ 0`,
      passed: results.bearingCapacityOk
    },
    {
      item: '抗倾覆稳定性验算',
      calculated: `K = ${results.K_overturningSafetyFactor}`,
      standard: 'K ≥ 1.5',
      passed: results.overturningOk
    },
    {
      item: '抗滑移稳定性验算',
      calculated: `Kh = ${results.Kh_slidingSafetyFactor}`,
      standard: 'Kh ≥ 1.3',
      passed: results.slidingOk
    }
  ];
};

// 获取安全评估标题
const getSafetyTitle = () => {
  if (results.isStable) {
    return '整体稳定性评估：通过';
  } else {
    return '整体稳定性评估：不通过';
  }
};

// 获取安全评估类型
const getSafetyType = () => {
  return results.isStable ? 'success' : 'error';
};

// 获取安全评估描述
const getSafetyDescription = () => {
  if (results.isStable) {
    return '电线塔基础各项稳定性验算均满足规范要求，基础设计符合安全标准，可保证电线塔在正常使用和极端工况下的安全运行。';
  } else {
    const failedItems = [];
    if (!results.bearingCapacityOk) failedItems.push('地基承载力验算');
    if (!results.overturningOk) failedItems.push('抗倾覆稳定性验算');
    if (!results.slidingOk) failedItems.push('抗滑移稳定性验算');
    
    return `电线塔基础稳定性验算中，${failedItems.join('、')}不满足规范要求，存在安全隐患，需要对基础设计进行优化调整。`;
  }
};

// 获取技术建议
const getRecommendations = () => {
  const recommendations = [];
  
  if (results.isStable) {
    recommendations.push('基础设计满足规范要求，建议按现有参数施工。');
    recommendations.push('施工过程中应严格控制混凝土质量，确保基础尺寸准确。');
    recommendations.push('定期检查基础周围排水情况，防止地基承载力降低。');
  } else {
    if (!results.bearingCapacityOk) {
      if (parseFloat(results.Pmax_maxPressure) > 1.2 * parseFloat(results.fa_adjustedBearingCapacity)) {
        recommendations.push('基底最大压力超过承载力限值，建议增大基础底面积或提高地基承载力。');
      }
      if (parseFloat(results.Pmin_minPressure) < 0) {
        recommendations.push('基底出现拉应力，建议增加基础自重或减小倾覆力矩。');
      }
    }
    
    if (!results.overturningOk) {
      recommendations.push('抗倾覆安全系数不足，建议增大基础宽度或增加基础自重。');
    }
    
    if (!results.slidingOk) {
      recommendations.push('抗滑移安全系数不足，建议增大基础自重或提高基底摩擦系数。');
    }
    
    recommendations.push('建议重新设计基础参数，确保所有验算项目均满足规范要求。');
    recommendations.push('如条件限制无法调整基础尺寸，可考虑地基处理措施提高承载力。');
  }
  
  return recommendations;
};

// 获取评估结论
const getConclusion = () => {
  if (results.isStable) {
    return '综合以上计算分析，该电线塔基础设计合理，各项稳定性指标均满足《建筑地基基础设计规范》(GB50007-2011)及电力行业相关规范要求，基础稳定可靠，可确保电线塔安全运行。';
  } else {
    return '综合以上计算分析，该电线塔基础设计存在安全隐患，部分稳定性指标不满足规范要求，需要对基础设计方案进行调整优化，确保基础稳定性满足安全要求后方可施工。';
  }
};

// 获取当前日期
const getCurrentDate = () => {
  return new Date().toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });
};

// 获取当前日期时间
const getCurrentDateTime = () => {
  return new Date().toLocaleString('zh-CN');
};

// 导出PDF报告 - 使用稳健的jsPDF + html2canvas方案
const exportPDFReport = async () => {
  if (!hasResults.value) {
    ElMessage.warning('请先进行计算，再导出报告');
    return;
  }

  try {
  exportingPDF.value = true;
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
          <h1 style="font-size: 20px; color: #2c5aa0; margin: 0; font-family: 'Microsoft YaHei', 'SimSun', sans-serif;">电线塔基础稳定性安全评估报告</h1>
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
          <td style="border: 1px solid #333; padding: 10px;">${formData.projectName || '电线塔基础稳定性项目'}</td>
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
      <table style="width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 12px;">
        <tr>
          <td style="border: 1px solid #333; padding: 8px; background: #f8f8f8;">基础长度 L</td><td style="border: 1px solid #333; padding: 8px;">${formData.foundationLength || 0} m</td>
          <td style="border: 1px solid #333; padding: 8px; background: #f8f8f8;">基础宽度 B</td><td style="border: 1px solid #333; padding: 8px;">${formData.foundationWidth || 0} m</td>
        </tr>
        <tr>
          <td style="border: 1px solid #333; padding: 8px; background: #f8f8f8;">垂直荷载 N</td><td style="border: 1px solid #333; padding: 8px;">${formData.verticalLoad || 0} kN</td>
          <td style="border: 1px solid #333; padding: 8px; background: #f8f8f8;">水平荷载 H</td><td style="border: 1px solid #333; padding: 8px;">${formData.horizontalLoad || 0} kN</td>
        </tr>
        <tr>
          <td style="border: 1px solid #333; padding: 8px; background: #f8f8f8;">地基承载力 fa</td><td style="border: 1px solid #333; padding: 8px;">${formData.bearingCapacity_fa || 0} kPa</td>
           <td style="border: 1px solid #333; padding: 8px; background: #f8f8f8;"></td><td style="border: 1px solid #333; padding: 8px;"></td>
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
    
    // 3.2 地基承载力验算 - 总标题
    const bearingCapacityMainTitleHtml = `
      <h3 style="font-size: 14px; margin: 15px 0 10px 0;">1. 地基承载力验算</h3>
    `
    await addHtmlBlock(bearingCapacityMainTitleHtml)
    
    // 3.3 基础平均压力计算
    const averagePressureHtml = `
      <div style="font-size: 12px;">
        <h4 style="font-size: 13px; margin: 10px 0 5px 0; color: #2c5aa0;">1.1 基础平均压力计算</h4>
        <p style="margin: 10px 0; padding: 10px; background: #f8f9fa; border-left: 4px solid #2c5aa0;">
          <strong>计算公式：</strong><br>
          p = N / A<br><br>
          <strong>参数说明：</strong><br>
          • N = 垂直荷载 = ${formData.verticalLoad || 0} kN<br>
          • A = 基础面积 = L × B = ${formData.foundationLength || 0} × ${formData.foundationWidth || 0} = ${((formData.foundationLength || 0) * (formData.foundationWidth || 0)).toFixed(2)} m²<br><br>
          <strong>计算过程：</strong><br>
          p = ${formData.verticalLoad || 0} / ${((formData.foundationLength || 0) * (formData.foundationWidth || 0)).toFixed(2)}<br>
          p = ${(results.pressure || 0).toFixed(2)} kPa<br><br>
          <strong>验算条件：</strong><br>
          p ≤ fa = ${formData.bearingCapacity_fa || 0} kPa<br>
          <strong>验算结果：</strong> ${results.bearingCapacityOk ? '满足要求' : '不满足要求'}
        </p>
      </div>
    `
    await addHtmlBlock(averagePressureHtml)
    
    // 3.4 地基承载力修正
    const bearingCapacityCorrectionHtml = `
      <div style="font-size: 12px;">
        <h4 style="font-size: 13px; margin: 10px 0 5px 0; color: #2c5aa0;">1.2 地基承载力修正</h4>
        <p style="margin: 10px 0; padding: 10px; background: #f8f9fa; border-left: 4px solid #2c5aa0;">
          <strong>修正公式：</strong><br>
          fa = fak + ηb×γ×(b-3) + ηd×γm×(d-0.5)<br><br>
          <strong>参数说明：</strong><br>
          • fak = 地基承载力特征值 = ${formData.bearingCapacity_fa || 0} kPa<br>
          • ηb = 基础宽度修正系数 = ${formData.widthCorrectionFactor_eta_b || 0.3}<br>
          • ηd = 基础深度修正系数 = ${formData.depthCorrectionFactor_eta_d || 1.6}<br>
          • γ = 土体重度 = ${formData.soilUnitWeight_gamma || 0} kN/m³<br>
          • γm = 基础底面以上土的加权平均重度 = ${formData.soilUnitWeight_gamma_m || 0} kN/m³<br>
          • b = 基础宽度 = ${formData.foundationWidth || 0} m<br>
          • d = 基础埋深 = ${formData.foundationDepth || 0} m
        </p>
      </div>
    `
    await addHtmlBlock(bearingCapacityCorrectionHtml)
    
    // 3.5 抗倾覆稳定性验算 - 总标题
    const overturningMainTitleHtml = `
      <h3 style="font-size: 14px; margin: 15px 0 10px 0;">2. 抗倾覆稳定性验算</h3>
    `
    await addHtmlBlock(overturningMainTitleHtml)
    
    // 3.6 倾覆力矩计算
    const overturningMomentHtml = `
      <div style="font-size: 12px;">
        <h4 style="font-size: 13px; margin: 10px 0 5px 0; color: #2c5aa0;">2.1 倾覆力矩计算</h4>
        <p style="margin: 10px 0; padding: 10px; background: #f8f9fa; border-left: 4px solid #2c5aa0;">
          <strong>倾覆力矩 Mo：</strong><br>
          Mo = H × h + M<br><br>
          <strong>参数说明：</strong><br>
          • H = 水平荷载 = ${formData.horizontalLoad || 0} kN<br>
          • h = 水平荷载作用高度 = ${formData.horizontalForceHeight || 0} m<br>
          • M = 附加弯矩 = ${formData.moment || 0} kN·m<br><br>
          <strong>计算过程：</strong><br>
          Mo = ${formData.horizontalLoad || 0} × ${formData.horizontalForceHeight || 0} + ${formData.moment || 0}<br>
          Mo = ${((formData.horizontalLoad || 0) * (formData.horizontalForceHeight || 0) + (formData.moment || 0)).toFixed(2)} kN·m
        </p>
      </div>
    `
    await addHtmlBlock(overturningMomentHtml)
    
    // 3.7 抗倾覆力矩计算
    const resistingMomentHtml = `
      <div style="font-size: 12px;">
        <h4 style="font-size: 13px; margin: 10px 0 5px 0; color: #2c5aa0;">2.2 抗倾覆力矩计算</h4>
        <p style="margin: 10px 0; padding: 10px; background: #f8f9fa; border-left: 4px solid #2c5aa0;">
          <strong>抗倾覆力矩 Mr：</strong><br>
          Mr = N × (B/2)<br><br>
          <strong>参数说明：</strong><br>
          • N = 垂直荷载 = ${formData.verticalLoad || 0} kN<br>
          • B = 基础宽度 = ${formData.foundationWidth || 0} m<br>
          • B/2 = 基础重心到倾覆边缘距离 = ${((formData.foundationWidth || 0) / 2).toFixed(2)} m<br><br>
          <strong>计算过程：</strong><br>
          Mr = ${formData.verticalLoad || 0} × ${((formData.foundationWidth || 0) / 2).toFixed(2)}<br>
          Mr = ${((formData.verticalLoad || 0) * (formData.foundationWidth || 0) / 2).toFixed(2)} kN·m
        </p>
      </div>
    `
    await addHtmlBlock(resistingMomentHtml)
    
    // 3.8 抗倾覆安全系数
    const overturningFactorHtml = `
      <div style="font-size: 12px;">
        <h4 style="font-size: 13px; margin: 10px 0 5px 0; color: #2c5aa0;">2.3 抗倾覆安全系数</h4>
        <p style="margin: 10px 0; padding: 10px; background: #e7f3ff; border-left: 4px solid #007bff;">
          <strong>计算公式：</strong><br>
          Ko = Mr / Mo<br><br>
          <strong>计算过程：</strong><br>
          Ko = ${((formData.verticalLoad || 0) * (formData.foundationWidth || 0) / 2).toFixed(2)} / ${((formData.horizontalLoad || 0) * (formData.horizontalForceHeight || 0) + (formData.moment || 0)).toFixed(2)}<br>
          Ko = ${(results.overturningFactor || 0).toFixed(2)}<br><br>
          <strong>验算条件：</strong> Ko ≥ 1.5<br>
          <strong>验算结果：</strong> ${results.overturningOk ? '满足要求' : '不满足要求'}
        </p>
      </div>
    `
    await addHtmlBlock(overturningFactorHtml)
    
    // 3.9 抗滑移稳定性验算 - 总标题
    const slidingMainTitleHtml = `
      <h3 style="font-size: 14px; margin: 15px 0 10px 0;">3. 抗滑移稳定性验算</h3>
    `
    await addHtmlBlock(slidingMainTitleHtml)
    
    // 3.10 滑动力计算
    const slidingForceHtml = `
      <div style="font-size: 12px;">
        <h4 style="font-size: 13px; margin: 10px 0 5px 0; color: #2c5aa0;">3.1 滑动力计算</h4>
        <p style="margin: 10px 0; padding: 10px; background: #f8f9fa; border-left: 4px solid #2c5aa0;">
          <strong>滑动力 F：</strong><br>
          F = H = ${formData.horizontalLoad || 0} kN<br><br>
          <strong>说明：</strong><br>
          水平荷载直接作为滑动力，不考虑倾覆力矩对滑动的影响。
        </p>
      </div>
    `
    await addHtmlBlock(slidingForceHtml)
    
    // 3.11 抗滑阻力计算
    const slidingResistanceHtml = `
      <div style="font-size: 12px;">
        <h4 style="font-size: 13px; margin: 10px 0 5px 0; color: #2c5aa0;">3.2 抗滑阻力计算</h4>
        <p style="margin: 10px 0; padding: 10px; background: #f8f9fa; border-left: 4px solid #2c5aa0;">
          <strong>抗滑阻力 R：</strong><br>
          R = N × tan φ + c × A<br><br>
          <strong>参数说明：</strong><br>
          • N = 垂直荷载 = ${formData.verticalLoad || 0} kN<br>
          • φ = 内摩擦角 = ${formData.frictionAngle_phi || 0}°<br>
          • tan φ = ${Math.tan((formData.frictionAngle_phi || 0) * Math.PI / 180).toFixed(3)}<br>
          • c = 黏聚力 = ${formData.cohesion_c || 0} kPa<br>
          • A = 基础面积 = ${((formData.foundationLength || 0) * (formData.foundationWidth || 0)).toFixed(2)} m²<br><br>
          <strong>计算过程：</strong><br>
          R = ${formData.verticalLoad || 0} × ${Math.tan((formData.frictionAngle_phi || 0) * Math.PI / 180).toFixed(3)} + ${formData.cohesion_c || 0} × ${((formData.foundationLength || 0) * (formData.foundationWidth || 0)).toFixed(2)}<br>
          R = ${((formData.verticalLoad || 0) * Math.tan((formData.frictionAngle_phi || 0) * Math.PI / 180) + (formData.cohesion_c || 0) * (formData.foundationLength || 0) * (formData.foundationWidth || 0)).toFixed(2)} kN
        </p>
      </div>
    `
    await addHtmlBlock(slidingResistanceHtml)
    
    // 3.12 抗滑移安全系数
    const slidingFactorHtml = `
      <div style="font-size: 12px;">
        <h4 style="font-size: 13px; margin: 10px 0 5px 0; color: #2c5aa0;">3.3 抗滑移安全系数</h4>
        <p style="margin: 10px 0; padding: 10px; background: #e7f3ff; border-left: 4px solid #007bff;">
          <strong>计算公式：</strong><br>
          Ks = R / F<br><br>
          <strong>计算过程：</strong><br>
          Ks = ${((formData.verticalLoad || 0) * Math.tan((formData.frictionAngle_phi || 0) * Math.PI / 180) + (formData.cohesion_c || 0) * (formData.foundationLength || 0) * (formData.foundationWidth || 0)).toFixed(2)} / ${formData.horizontalLoad || 0}<br>
          Ks = ${(results.slidingFactor || 0).toFixed(2)}<br><br>
          <strong>验算条件：</strong> Ks ≥ 1.3<br>
          <strong>验算结果：</strong> ${results.slidingOk ? '满足要求' : '不满足要求'}
        </p>
      </div>
    `
    await addHtmlBlock(slidingFactorHtml)
    
    // 3.13 规范依据
    const standardsHtml = `
      <div style="font-size: 12px;">
        <h3 style="font-size: 14px; margin: 15px 0 10px 0;">4. 规范依据</h3>
        <p style="margin: 10px 0; padding: 10px; background: #f0f8ff; border-left: 4px solid #4CAF50;">
          <strong>主要规范：</strong><br>
          • 《建筑地基基础设计规范》GB 50007-2011<br>
          • 《电力工程地基基础设计规范》DL/T 5024-2020<br>
          • 《建筑抗震设计规范》GB 50011-2010<br><br>
          <strong>安全系数要求：</strong><br>
          • 地基承载力：p ≤ fa<br>
          • 抗倾覆稳定：Ko ≥ 1.5<br>
          • 抗滑移稳定：Ks ≥ 1.3
        </p>
      </div>
    `
    await addHtmlBlock(standardsHtml)

    // 模块4: 验算结果
    const resultsHtml = `
      <h2 style="font-size: 18px; color: #2c5aa0; border-bottom: 1px solid #ddd; padding-bottom: 5px;">三、验算结果</h2>
      <table style="width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 12px;">
        <tr style="background: #f0f0f0;"><th style="border: 1px solid #333; padding: 8px;">验算项目</th><th style="border: 1px solid #333; padding: 8px;">计算值</th><th style="border: 1px solid #333; padding: 8px;">规范要求</th><th style="border: 1px solid #333; padding: 8px;">验算结果</th></tr>
        <tr><td style="border: 1px solid #333; padding: 8px;">地基承载力</td><td style="border: 1px solid #333; padding: 8px;">${(results.pressure || 0).toFixed(2)} kPa</td><td style="border: 1px solid #333; padding: 8px;">≤ ${formData.bearingCapacity_fa || 0} kPa</td><td style="border: 1px solid #333; padding: 8px; color: ${results.bearingCapacityOk ? '#198754' : '#dc3545'};">${results.bearingCapacityOk ? '通过' : '不通过'}</td></tr>
        <tr><td style="border: 1px solid #333; padding: 8px;">抗倾覆稳定</td><td style="border: 1px solid #333; padding: 8px;">${(results.overturningFactor || 0).toFixed(2)}</td><td style="border: 1px solid #333; padding: 8px;">≥ 1.5</td><td style="border: 1px solid #333; padding: 8px; color: ${results.overturningOk ? '#198754' : '#dc3545'};">${results.overturningOk ? '通过' : '不通过'}</td></tr>
        <tr><td style="border: 1px solid #333; padding: 8px;">抗滑移稳定</td><td style="border: 1px solid #333; padding: 8px;">${(results.slidingFactor || 0).toFixed(2)}</td><td style="border: 1px solid #333; padding: 8px;">≥ 1.3</td><td style="border: 1px solid #333; padding: 8px; color: ${results.slidingOk ? '#198754' : '#dc3545'};">${results.slidingOk ? '通过' : '不通过'}</td></tr>
      </table>
    `
    await addHtmlBlock(resultsHtml)

    // 模块5: 安全评估与建议
    const assessmentHtml = `
      <h2 style="font-size: 18px; color: #2c5aa0; border-bottom: 1px solid #ddd; padding-bottom: 5px;">四、安全评估与建议</h2>
      <div style="background: #f8f9fa; border-left: 4px solid #2c5aa0; padding: 15px; margin: 15px 0; font-size: 12px;">
        <h3 style="font-size: 14px; margin: 0 0 10px 0;">整体安全状况评估</h3>
        <p style="margin: 0;">${getSafetyDescription()}</p>
      </div>
       <div style="background: #e7f3ff; border-left: 4px solid #007bff; padding: 15px; margin: 15px 0; font-size: 12px;">
        <h3 style="font-size: 14px; margin: 0 0 10px 0;">评估结论</h3>
        <p style="margin: 0;">${getConclusion()}</p>
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

    pdf.save(`电线塔基础稳定性安全评估报告_${getCurrentDate().replace(/\//g, '')}.pdf`)
    
    ElMessage.success('PDF报告导出成功！包含完整的计算公式和稳定性分析')
    
  } catch (error) {
    console.error('PDF导出失败:', error);
    ElMessage.error(`PDF导出失败: ${error.message}`);
  } finally {
    exportingPDF.value = false;
  }
};

// 生成电线塔模块的HTML报告内容
const generateTowerReportHTML = () => {
  const safetyTitle = getSafetyTitle()
  const overallStatus = getSafetyDescription()
  
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
        <div class="report-title">电线塔基础稳定性安全评估报告</div>
        <div class="company-name">吉林省志安科技有限公司</div>
      </div>
      
      <!-- 项目基本信息 -->
      <div class="section">
        <div class="section-title">项目基本信息</div>
        <table class="info-table">
          <tr>
            <td class="label-cell">项目名称</td>
            <td>${formData.projectName || '电线塔基础稳定性项目'}</td>
          </tr>
          <tr>
            <td class="label-cell">项目类型</td>
            <td>电线塔基础稳定性分析计算</td>
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
        
        <div class="subsection-title">1. 基础几何参数</div>
        <table class="info-table">
          <tr><td class="label-cell">基础长度</td><td>${formData.foundationLength || 0} m</td></tr>
          <tr><td class="label-cell">基础宽度</td><td>${formData.foundationWidth || 0} m</td></tr>
          <tr><td class="label-cell">基础厚度</td><td>${formData.foundationHeight || 0} m</td></tr>
          <tr><td class="label-cell">埋深</td><td>${formData.buriedDepth || 0} m</td></tr>
        </table>
        
        <div class="subsection-title">2. 荷载参数</div>
        <table class="info-table">
          <tr><td class="label-cell">垂直荷载</td><td>${formData.verticalLoad || 0} kN</td></tr>
          <tr><td class="label-cell">水平荷载</td><td>${formData.horizontalLoad || 0} kN</td></tr>
          <tr><td class="label-cell">弯矩荷载</td><td>${formData.momentLoad || 0} kN·m</td></tr>
        </table>
        
        <div class="subsection-title">3. 材料参数</div>
        <table class="info-table">
          <tr><td class="label-cell">混凝土容重</td><td>${formData.concreteUnitWeight || 0} kN/m³</td></tr>
          <tr><td class="label-cell">土体容重</td><td>${formData.soilUnitWeight || 0} kN/m³</td></tr>
          <tr><td class="label-cell">地基承载力</td><td>${formData.bearingCapacity_fa || 0} kPa</td></tr>
          <tr><td class="label-cell">摩擦系数</td><td>${formData.frictionCoefficient_f || 0}</td></tr>
        </table>
      </div>
      
      <!-- 分页 -->
      <div class="page-break"></div>
      
      <!-- 计算结果 -->
      <div class="section">
        <div class="section-title">二、计算结果</div>
        
        <div class="subsection-title">1. 地基承载力验算结果</div>
        <table class="info-table">
          <tr>
            <th>验算项目</th>
            <th>计算值</th>
            <th>允许值</th>
            <th>验算结果</th>
          </tr>
          <tr>
            <td>基础平均压力</td>
            <td>${(results.pressure || 0).toFixed(2)} kPa</td>
            <td>${formData.bearingCapacity_fa} kPa</td>
            <td class="${results.bearingCapacityOk ? 'result-pass' : 'result-fail'}">${results.bearingCapacityOk ? '通过' : '不通过'}</td>
          </tr>
          <tr>
            <td>基础最大压力</td>
            <td>${(results.maxPressure || 0).toFixed(2)} kPa</td>
            <td>${(formData.bearingCapacity_fa * 1.2).toFixed(2)} kPa</td>
            <td class="${(results.maxPressureOk || false) ? 'result-pass' : 'result-fail'}">${(results.maxPressureOk || false) ? '通过' : '不通过'}</td>
          </tr>
        </table>
        
        <div class="subsection-title">2. 抗倾覆稳定性验算结果</div>
        <table class="info-table">
          <tr>
            <th>验算项目</th>
            <th>计算值</th>
            <th>规范要求</th>
            <th>验算结果</th>
          </tr>
          <tr>
            <td>抗倾覆安全系数</td>
            <td>${(results.overturningFactor || 0).toFixed(2)}</td>
            <td>≥ 1.5</td>
            <td class="${results.overturningOk ? 'result-pass' : 'result-fail'}">${results.overturningOk ? '通过' : '不通过'}</td>
          </tr>
          <tr>
            <td>抗倾覆力矩</td>
            <td>${(results.resistingMoment || 0).toFixed(2)} kN·m</td>
            <td>-</td>
            <td>-</td>
          </tr>
          <tr>
            <td>倾覆力矩</td>
            <td>${(results.overturningMoment || 0).toFixed(2)} kN·m</td>
            <td>-</td>
            <td>-</td>
          </tr>
        </table>
        
        <div class="subsection-title">3. 抗滑移稳定性验算结果</div>
        <table class="info-table">
          <tr>
            <th>验算项目</th>
            <th>计算值</th>
            <th>规范要求</th>
            <th>验算结果</th>
          </tr>
          <tr>
            <td>抗滑移安全系数</td>
            <td>${(results.slidingFactor || 0).toFixed(2)}</td>
            <td>≥ 1.3</td>
            <td class="${results.slidingOk ? 'result-pass' : 'result-fail'}">${results.slidingOk ? '通过' : '不通过'}</td>
          </tr>
          <tr>
            <td>摩擦阻力</td>
            <td>${(results.frictionResistance || 0).toFixed(2)} kN</td>
            <td>-</td>
            <td>-</td>
          </tr>
        </table>
      </div>
      
      <!-- 分页 -->
      <div class="page-break"></div>
      
      <!-- 安全评估报告 -->
      <div class="section">
        <div class="section-title">三、安全评估报告</div>
        
        <div class="assessment-box">
          <div class="subsection-title">${safetyTitle}</div>
          <p>${overallStatus}</p>
        </div>
        
        <div class="subsection-title">验算通过情况统计</div>
        <ul>
          <li>地基承载力验算：<span class="${results.bearingCapacityOk ? 'result-pass' : 'result-fail'}">${results.bearingCapacityOk ? '✓ 通过' : '✗ 不通过'}</span></li>
          <li>抗倾覆稳定性验算：<span class="${results.overturningOk ? 'result-pass' : 'result-fail'}">${results.overturningOk ? '✓ 通过' : '✗ 不通过'}</span></li>
          <li>抗滑移稳定性验算：<span class="${results.slidingOk ? 'result-pass' : 'result-fail'}">${results.slidingOk ? '✓ 通过' : '✗ 不通过'}</span></li>
        </ul>
        
        <div class="subsection-title">技术建议</div>
        <ul>
          ${!results.bearingCapacityOk ? `
            <li><strong>承载力不足：</strong>建议增加基础尺寸或提高地基承载力。</li>
          ` : ''}
          ${!results.overturningOk ? `
            <li><strong>抗倾覆不足：</strong>建议增加基础自重或调整基础尺寸。</li>
          ` : ''}
          ${!results.slidingOk ? `
            <li><strong>抗滑移不足：</strong>建议增加基础埋深或采用抗滑措施。</li>
          ` : ''}
          <li><strong>施工监测：</strong>建议在施工和使用过程中加强基础沉降和位移监测。</li>
          <li><strong>定期检查：</strong>建议定期检查基础结构和地基状况，确保长期稳定性。</li>
        </ul>
        
        <div class="subsection-title">评估结论</div>
        <div class="assessment-box">
          <p>${results.bearingCapacityOk && results.overturningOk && results.slidingOk ? 
            '综合评估认为，当前电线塔基础设计在技术上是可行的，各项稳定性验算均满足规范要求。建议按照设计参数进行施工，并在施工过程中严格控制质量，确保工程安全顺利完成。' :
            '综合评估认为，当前电线塔基础设计需要进一步优化。建议根据技术建议调整相关参数，并采取相应的加强措施后方可施工。'
          }</p>
        </div>
      </div>
      
      <!-- 报告页脚 -->
      <div style="margin-top: 40px; border-top: 1px solid #ddd; padding-top: 20px; text-align: center; font-size: 10px; color: #666;">
        <p style="margin: 5px 0;">技术支持：吉林省志安科技有限公司</p>
        <p style="margin: 5px 0;">生成日期：${currentDateTime}</p>
      </div>
    </body>
    </html>
  `
};

// 添加电线塔报告封面页
const addTowerReportCoverPage = async (pdf, margin, contentWidth, contentHeight) => {
  const pageNumber = 1
  
  // 设置中文字体
  setupChineseFont(pdf)
  
  // 公司LOGO和标题区域
  pdf.setFontSize(18)
  pdf.setTextColor(44, 90, 160)
  const title = '电线塔基础稳定性安全评估报告'
  const titleWidth = pdf.getTextWidth(title)
  pdf.text(title, (210 - titleWidth) / 2, margin + 30)
  
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
    ['项目名称', formData.projectName || '电线塔基础稳定性分析项目'],
    ['项目类型', '电线塔基础稳定性计算'],
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
    `基础宽度：${formData.foundationWidth_b}m`,
    `基础长度：${formData.foundationLength_l}m`,
    `基础埋深：${formData.foundationDepth_d}m`,
    `垂直荷载：${formData.verticalLoad_V}kN`,
    `水平荷载：${formData.horizontalLoad_H}kN`,
    `弯矩荷载：${formData.moment_M}kN·m`
  ]
  
  keyParams.forEach((param, index) => {
    if (index % 2 === 0) {
      pdf.text('• ' + param, margin, yPos + Math.floor(index / 2) * 8)
    } else {
      pdf.text('• ' + param, margin + contentWidth / 2, yPos + Math.floor(index / 2) * 8)
    }
  })
  
  // 添加页脚
  addTowerPageFooter(pdf, pageNumber, 4)
}

// 添加电线塔计算条件和依据页
const addTowerCalculationConditionsPage = async (pdf, margin, contentWidth, contentHeight) => {
  const pageNumber = 2
  let yPos = margin + 10
  
  // 页面标题
  pdf.setFont('helvetica', 'bold')
  pdf.setFontSize(16)
  pdf.setTextColor(44, 90, 160)
  pdf.text('计算条件与依据', margin, yPos)
  yPos += 15
  
  // 规范依据
  pdf.setFont('helvetica', 'bold')
  pdf.setFontSize(12)
  pdf.setTextColor(0, 0, 0)
  pdf.text('1. 规范依据', margin, yPos)
  yPos += 10
  
  pdf.setFont('helvetica', 'normal')
  pdf.setFontSize(9)
  const standards = [
    '《建筑地基基础设计规范》GB50007-2011',
    '《110kV~750kV架空输电线路设计规范》GB 50545-2010',
    '《架空输电线路基础设计技术规程》DL/T 5219-2014',
    '《电力工程高压送电线路设计手册》',
    '《岩土工程勘察规范》GB50021-2001'
  ]
  
  standards.forEach((standard, index) => {
    pdf.text(`(${index + 1}) ${standard}`, margin + 5, yPos + index * 6)
  })
  yPos += standards.length * 6 + 10
  
  // 主要计算公式
  pdf.setFont('helvetica', 'bold')
  pdf.setFontSize(12)
  pdf.text('2. 主要计算公式', margin, yPos)
  yPos += 10
  
  pdf.setFont('helvetica', 'normal')
  pdf.setFontSize(9)
  
  const formulas = [
    {
      title: '地基承载力验算',
      formula: 'p ≤ fa',
      desc: 'p-基础底面平均压力(kPa); fa-地基承载力特征值(kPa)'
    },
    {
      title: '抗倾覆稳定性验算',
      formula: 'K0 = M_R / M_0 ≥ 1.5',
      desc: 'K0-抗倾覆安全系数; M_R-抗倾覆力矩; M_0-倾覆力矩'
    },
    {
      title: '抗滑移稳定性验算',
      formula: 'Ks = f × N / H ≥ 1.3',
      desc: 'Ks-抗滑移安全系数; f-摩擦系数; N-法向力; H-水平力'
    },
    {
      title: '基础压力计算',
      formula: 'p = N/A ± M/W',
      desc: 'N-垂直荷载; A-基础面积; M-弯矩; W-截面模量'
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
  if (yPos + 100 < contentHeight + margin) {
    pdf.setFont('helvetica', 'bold')
    pdf.setFontSize(12)
    pdf.text('3. 详细计算参数', margin, yPos)
    yPos += 10
    
    // 基础几何参数表格
    const geometryData = [
      ['参数名称', '数值', '单位'],
      ['基础宽度 b', formData.foundationWidth_b.toString(), 'm'],
      ['基础长度 l', formData.foundationLength_l.toString(), 'm'],
      ['基础埋深 d', formData.foundationDepth_d.toString(), 'm'],
      ['基础面积 A', (formData.foundationWidth_b * formData.foundationLength_l).toFixed(2), 'm²']
    ]
    
    const tableHeight = drawTowerTable(pdf, geometryData, margin, yPos, contentWidth, 8)
    yPos += tableHeight + 10
    
    // 荷载参数表格
    if (yPos + 40 < contentHeight + margin) {
      const loadData = [
        ['荷载类型', '数值', '单位'],
        ['垂直荷载 V', formData.verticalLoad_V.toString(), 'kN'],
        ['水平荷载 H', formData.horizontalLoad_H.toString(), 'kN'],
        ['弯矩荷载 M', formData.moment_M.toString(), 'kN·m']
      ]
      
      drawTowerTable(pdf, loadData, margin, yPos, contentWidth, 8)
    }
  }
  
  addTowerPageFooter(pdf, pageNumber, 4)
}

// 添加电线塔计算结果页
const addTowerCalculationResultsPage = async (pdf, margin, contentWidth, contentHeight) => {
  const pageNumber = 3
  let yPos = margin + 10
  
  // 页面标题
  pdf.setFont('helvetica', 'bold')
  pdf.setFontSize(16)
  pdf.setTextColor(44, 90, 160)
  pdf.text('计算结果', margin, yPos)
  yPos += 15
  
  // 地基承载力验算结果
  pdf.setFont('helvetica', 'bold')
  pdf.setFontSize(12)
  pdf.setTextColor(0, 0, 0)
  pdf.text('1. 地基承载力验算结果', margin, yPos)
  yPos += 10
  
  const bearingData = [
    ['验算项目', '计算值', '允许值', '验算结果'],
    ['基础平均压力', `${(results.pressure || 0).toFixed(2)} kPa`, `${formData.bearingCapacity_fa} kPa`, results.bearingCapacityOk ? '通过' : '不通过'],
    ['基础最大压力', `${(results.maxPressure || 0).toFixed(2)} kPa`, `${(formData.bearingCapacity_fa * 1.2).toFixed(2)} kPa`, (results.maxPressureOk || false) ? '通过' : '不通过']
  ]
  
  const tableHeight1 = drawTowerTable(pdf, bearingData, margin, yPos, contentWidth, 8)
  yPos += tableHeight1 + 15
  
  // 抗倾覆稳定性验算结果
  pdf.setFont('helvetica', 'bold')
  pdf.setFontSize(12)
  pdf.text('2. 抗倾覆稳定性验算结果', margin, yPos)
  yPos += 10
  
  const overturningData = [
    ['验算项目', '计算值', '标准值', '验算结果'],
    ['抗倾覆安全系数', (results.overturningFactor || 0).toFixed(2), '≥ 1.5', results.overturningOk ? '通过' : '不通过'],
    ['抗倾覆力矩', `${(results.resistingMoment || 0).toFixed(2)} kN·m`, '-', '-'],
    ['倾覆力矩', `${(results.overturningMoment || 0).toFixed(2)} kN·m`, '-', '-']
  ]
  
  const tableHeight2 = drawTowerTable(pdf, overturningData, margin, yPos, contentWidth, 8)
  yPos += tableHeight2 + 15
  
  // 抗滑移稳定性验算结果
  pdf.setFont('helvetica', 'bold')
  pdf.setFontSize(12)
  pdf.text('3. 抗滑移稳定性验算结果', margin, yPos)
  yPos += 10
  
  const slidingData = [
    ['验算项目', '计算值', '标准值', '验算结果'],
    ['抗滑移安全系数', (results.slidingFactor || 0).toFixed(2), '≥ 1.3', results.slidingOk ? '通过' : '不通过'],
    ['摩擦阻力', `${(results.frictionResistance || 0).toFixed(2)} kN`, '-', '-'],
    ['水平荷载', `${formData.horizontalLoad_H} kN`, '-', '-']
  ]
  
  const tableHeight3 = drawTowerTable(pdf, slidingData, margin, yPos, contentWidth, 8)
  yPos += tableHeight3 + 15
  
  // 综合安全性评价
  pdf.setFont('helvetica', 'bold')
  pdf.setFontSize(12)
  pdf.text('4. 综合安全性评价', margin, yPos)
  yPos += 10
  
  pdf.setFont('helvetica', 'normal')
  pdf.setFontSize(10)
  const safetyAnalysis = [
    `地基承载力验算：${results.bearingCapacityOk ? '✓ 通过' : '✗ 不通过'}`,
    `抗倾覆稳定性验算：${results.overturningOk ? '✓ 通过' : '✗ 不通过'}`,
    `抗滑移稳定性验算：${results.slidingOk ? '✓ 通过' : '✗ 不通过'}`,
    `整体稳定性：${results.isStable ? '安全' : '需要关注'}`
  ]
  
  safetyAnalysis.forEach((analysis, index) => {
    pdf.text('• ' + analysis, margin + 5, yPos + index * 6)
  })
  
  addTowerPageFooter(pdf, pageNumber, 4)
}

// 添加电线塔安全评估报告页
const addTowerSafetyAssessmentPage = async (pdf, margin, contentWidth, contentHeight) => {
  const pageNumber = 4
  let yPos = margin + 10
  
  // 页面标题
  pdf.setFont('helvetica', 'bold')
  pdf.setFontSize(16)
  pdf.setTextColor(44, 90, 160)
  pdf.text('安全评估报告', margin, yPos)
  yPos += 15
  
  // 整体安全状况
  const safetyStatus = getTowerOverallSafetyStatus()
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
  
  // 验算结果统计
  pdf.setFont('helvetica', 'bold')
  pdf.setFontSize(12)
  pdf.text('2. 验算通过情况统计', margin, yPos)
  yPos += 10
  
  pdf.setFont('helvetica', 'normal')
  pdf.setFontSize(10)
  const verificationResults = [
    `• 地基承载力验算：${results.bearingCapacityOk ? '✓ 通过' : '✗ 不通过'}`,
    `• 抗倾覆稳定性验算：${results.overturningOk ? '✓ 通过' : '✗ 不通过'}`,
    `• 抗滑移稳定性验算：${results.slidingOk ? '✓ 通过' : '✗ 不通过'}`,
    `• 综合安全评价：${results.isStable ? '安全' : '需要关注'}`
  ]
  
  verificationResults.forEach((result, index) => {
    pdf.text(result, margin + 5, yPos + index * 6)
  })
  yPos += verificationResults.length * 6 + 15
  
  // 技术建议
  pdf.setFont('helvetica', 'bold')
  pdf.setFontSize(12)
  pdf.text('3. 技术建议', margin, yPos)
  yPos += 10
  
  pdf.setFont('helvetica', 'normal')
  pdf.setFontSize(9)
  const recommendations = getTowerRecommendations()
  
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
    const conclusion = getTowerConclusion()
    const wrappedConclusion = pdf.splitTextToSize(conclusion, contentWidth)
    
    // 结论背景框
    pdf.setFillColor(248, 249, 250)
    pdf.rect(margin, yPos - 3, contentWidth, wrappedConclusion.length * 5 + 6, 'F')
    pdf.setDrawColor(44, 90, 160)
    pdf.rect(margin, yPos - 3, contentWidth, wrappedConclusion.length * 5 + 6)
    
    pdf.text(wrappedConclusion, margin + 3, yPos + 2)
  }
  
  addTowerPageFooter(pdf, pageNumber, 4)
}

// 电线塔绘制表格的辅助函数
const drawTowerTable = (pdf, data, x, y, width, rowHeight) => {
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

// 电线塔添加页脚的辅助函数
const addTowerPageFooter = (pdf, pageNumber, totalPages) => {
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

// 获取电线塔整体安全状况
const getTowerOverallSafetyStatus = () => {
  const passedCount = [
    results.bearingCapacityOk,
    results.overturningOk,
    results.slidingOk
  ].filter(Boolean).length

  if (passedCount === 3) {
    return {
      title: '整体安全状况：优良',
      description: '所有验算项目均通过，电线塔基础在当前荷载条件下是安全稳定的，满足设计要求。'
    }
  } else if (passedCount >= 2) {
    return {
      title: '整体安全状况：一般',
      description: `有${3-passedCount}项验算未通过，建议采取加强措施或调整设计参数。`
    }
  } else {
    return {
      title: '整体安全状况：危险',
      description: '多项验算未通过，当前基础设计存在重大安全隐患，必须重新设计。'
    }
  }
}

// 获取电线塔技术建议
const getTowerRecommendations = () => {
  const recommendations = []
  let recId = 1

  if (!results.bearingCapacityOk) {
    recommendations.push({
      id: recId++,
      title: '地基承载力加强',
      content: '地基承载力不足，建议增大基础尺寸或进行地基处理。'
    })
  }

  if (!results.overturningOk) {
    recommendations.push({
      id: recId++,
      title: '抗倾覆稳定性加强',
      content: '抗倾覆安全系数不足，建议增大基础埋深或加重基础自重。'
    })
  }

  if (!results.slidingOk) {
    recommendations.push({
      id: recId++,
      title: '抗滑移稳定性加强',
      content: '抗滑移安全系数不足，建议增加基础底面粗糙度或设置抗滑键。'
    })
  }

  recommendations.push({
    id: recId++,
    title: '施工质量控制',
    content: '加强施工过程中的质量控制，确保基础几何尺寸和材料强度满足设计要求。'
  })

  recommendations.push({
    id: recId++,
    title: '运营期监测',
    content: '建议在运营期间定期检查基础状况，监测变形和沉降情况。'
  })

  return recommendations
}

// 获取电线塔评估结论
const getTowerConclusion = () => {
  const passedCount = [
    results.bearingCapacityOk,
    results.overturningOk,
    results.slidingOk
  ].filter(Boolean).length

  if (passedCount === 3) {
    return '综合评估认为，当前电线塔基础设计方案在技术上是安全可行的，各项稳定性验算均满足规范要求。建议按照设计参数进行施工，并在施工和运营过程中严格控制质量。'
  } else if (passedCount >= 2) {
    return '综合评估认为，当前基础设计基本可行，但需要对未通过的验算项目进行优化。建议根据技术建议调整相关参数，确保所有验算项目均满足安全要求。'
  } else {
    return '综合评估认为，当前基础设计存在重大安全风险，多项验算不满足规范要求。必须重新进行基础设计，确保所有安全验算均通过后方可实施。'
  }
}

// 导出TXT报告
const exportTXTReport = () => {
  const content = generateTXTReport();
  const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `电线塔基础稳定性安全评估报告_${getCurrentDate().replace(/\//g, '')}.txt`;
  link.click();
  URL.revokeObjectURL(link.href);
  ElMessage({ message: 'TXT报告导出成功！', type: 'success' });
};

// 生成TXT报告内容
const generateTXTReport = () => {
  // 使用全角空格和全角破折号以获得更好的中文格式化效果
  const fullWidthSpace = '　';
  const fullWidthDash = '──';
  const separator = fullWidthDash.repeat(33); // 66个字符宽度的分隔线

  return `
${fullWidthSpace.repeat(10)}电线塔基础稳定性安全评估报告
${separator}

一、计算依据
${fullWidthSpace}《建筑地基基础设计规范》(GB50007-2011)
${fullWidthSpace}《110kV~750kV架空输电线路设计规范》(GB 50545-2010)
${fullWidthSpace}《架空输电线路基础设计技术规程》(DL/T 5219-2014)

二、输入参数
${separator.substring(0, 30)}
基础与荷载参数：
${fullWidthSpace}基础宽度 b = ${formData.foundationWidth_b} m
${fullWidthSpace}基础长度 l = ${formData.foundationLength_l} m
${fullWidthSpace}基础埋深 d = ${formData.foundationDepth_d} m
${fullWidthSpace}水平力作用高度 h = ${formData.horizontalForceHeight_h} m
${fullWidthSpace}塔腿轴向压力 N = ${formData.towerAxialPressure_N} kN
${fullWidthSpace}基础及覆土总重 G = ${formData.foundationGravity_G} kN
${fullWidthSpace}水平力 Fw = ${formData.horizontalForce_Fw} kN

地质参数：
${fullWidthSpace}地勘提供承载力标准值 fak = ${formData.bearingCapacityStandard_fak} kPa
${fullWidthSpace}基底以下土重度 γ = ${formData.soilUnitWeight_gamma} kN/m³
${fullWidthSpace}基底以上土平均重度 γm = ${formData.soilUnitWeight_gamma_m} kN/m³
${fullWidthSpace}宽度修正系数 ηb = ${formData.widthCorrectionFactor_eta_b}
${fullWidthSpace}深度修正系数 ηd = ${formData.depthCorrectionFactor_eta_d}
${fullWidthSpace}基底摩擦系数 μ = ${formData.frictionCoefficient_mu}

三、计算依据和公式
${separator}

【规范依据】
${fullWidthSpace}《建筑地基基础设计规范》GB50007-2011
${fullWidthSpace}《110kV~750kV架空输电线路设计规范》GB 50545-2010
${fullWidthSpace}《架空输电线路基础设计技术规程》DL/T 5219-2014
${fullWidthSpace}《电力工程高压送电线路设计手册》DL/T 5092-1999
${fullWidthSpace}《岩土工程勘察规范》GB50021-2001

【主要计算公式】
1. 修正后地基承载力计算：
${fullWidthSpace}fa = fak + ηb·γ·(b-3) + ηd·γm·(d-0.5)
${fullWidthSpace}式中：fa - 修正后地基承载力；fak - 标准承载力；ηb,ηd - 宽度和深度修正系数；γ,γm - 土体重度

2. 基底压力计算：
${fullWidthSpace}Pmax/min = N/A ± M/W
${fullWidthSpace}式中：N - 总竖向力；A - 基底面积；M - 倾覆力矩；W - 截面抵抗矩

3. 地基承载力验算：
${fullWidthSpace}Pmax ≤ 1.2fa，且 Pmin ≥ 0
${fullWidthSpace}最大压力不超过修正承载力的1.2倍，最小压力不小于零（无拉应力）

4. 抗倾覆稳定性验算：
${fullWidthSpace}Kov = Mr/Mo ≥ 1.5
${fullWidthSpace}式中：Mr - 抗倾覆力矩；Mo - 倾覆力矩；1.5 - 抗倾覆安全系数

5. 抗滑移稳定性验算：
${fullWidthSpace}Ks = (N·μ + c·A)/H ≥ 1.3
${fullWidthSpace}式中：μ - 基底摩擦系数；c - 粘聚力；A - 基底面积；H - 水平力；1.3 - 抗滑移安全系数

6. 截面抵抗矩计算：
${fullWidthSpace}W = b·l²/6
${fullWidthSpace}式中：W - 截面抵抗矩；b - 基础宽度；l - 基础长度

7. 倾覆力矩计算：
${fullWidthSpace}Mo = Fw·h
${fullWidthSpace}式中：Fw - 水平风荷载；h - 风荷载作用点高度

【计算步骤】
步骤1：根据地质条件和基础尺寸计算修正后地基承载力fa
步骤2：计算基底最大和最小压力Pmax、Pmin
步骤3：验算地基承载力：Pmax ≤ 1.2fa且Pmin ≥ 0
步骤4：验算抗倾覆稳定性：Kov = Mr/Mo ≥ 1.5
步骤5：验算抗滑移稳定性：Ks ≥ 1.3
步骤6：综合评估基础稳定性并提出优化建议

四、计算结果
${separator.substring(0, 30)}
1. 地基承载力验算：
${fullWidthSpace}修正后地基承载力 fa = ${results.fa_adjustedBearingCapacity} kPa
${fullWidthSpace}基底最大压力 Pmax = ${results.Pmax_maxPressure} kPa
${fullWidthSpace}基底最小压力 Pmin = ${results.Pmin_minPressure} kPa
${fullWidthSpace}验算结果：${results.bearingCapacityOk ? '通过' : '不通过'}

2. 抗倾覆验算：
${fullWidthSpace}倾覆力矩 M倾 = ${results.M_overturningMoment} kN·m
${fullWidthSpace}抗倾覆力矩 M抗 = ${results.M_resistingMoment} kN·m
${fullWidthSpace}抗倾覆安全系数 K = ${results.K_overturningSafetyFactor}
${fullWidthSpace}验算结果：${results.overturningOk ? '通过' : '不通过'}

3. 抗滑移验算：
${fullWidthSpace}水平滑动力 F滑 = ${results.F_slidingForce} kN
${fullWidthSpace}抗滑移力 R抗 = ${results.R_resistingForce} kN
${fullWidthSpace}抗滑移安全系数 Kh = ${results.Kh_slidingSafetyFactor}
${fullWidthSpace}验算结果：${results.slidingOk ? '通过' : '不通过'}

四、安全性评估
${separator.substring(0, 30)}
整体稳定性：${results.isStable ? '稳定' : '不稳定'}

${getSafetyDescription()}

五、技术建议
${separator.substring(0, 30)}
${getRecommendations().map((rec, index) => `${index + 1}. ${rec}`).join('\n')}

六、评估结论
${separator.substring(0, 30)}
${getConclusion()}

${separator}
计算日期：${getCurrentDate()}
计算软件：桥梁跨越工程安全性评估软件 v2.0
技术支持：吉林省志安科技有限公司
${separator}
  `.trim();
};

// --- 土层参数管理相关方法 ---

const soilLayersData = reactive([
  { depthStart: 0, depthEnd: 5, soilType: '粘土', bearingCapacity: 10.0, poissonRatio: '0.35' },
  { depthStart: 5, depthEnd: 10, soilType: '砂土', bearingCapacity: 15.0, poissonRatio: '0.30' },
  { depthStart: 10, depthEnd: 15, soilType: '粉土', bearingCapacity: 12.0, poissonRatio: '0.35' },
  { depthStart: 15, depthEnd: 20, soilType: '岩石', bearingCapacity: 18.0, poissonRatio: '0.28' }
]);

const showSoilLayerDialog = ref(false);
const editingIndex = ref(-1);
const currentSoilLayer = reactive({
  depthStart: 0,
  depthEnd: 0,
  soilType: '',
  bearingCapacity: 0,
  poissonRatio: '0.35',
});

const addSoilLayer = () => {
  // 重置当前土层数据
  Object.assign(currentSoilLayer, {
    depthStart: 0,
    depthEnd: 0,
    soilType: '',
    bearingCapacity: 0,
    poissonRatio: '0.35',
  });
  editingIndex.value = -1;
  showSoilLayerDialog.value = true;
};

const editSoilLayer = (index) => {
  editingIndex.value = index;
  Object.assign(currentSoilLayer, soilLayersData[index]);
  showSoilLayerDialog.value = true;
};

const deleteSoilLayer = (index) => {
  ElMessage.confirm('确定要删除这个土层吗？', '确认删除', {
    type: 'warning',
  }).then(() => {
    soilLayersData.splice(index, 1);
    ElMessage({ message: '土层删除成功！', type: 'success' });
  }).catch(() => {
    // 用户取消删除
  });
};

const handleSoilLayerDialogClose = () => {
  showSoilLayerDialog.value = false;
  editingIndex.value = -1;
  // 重置当前土层数据
  Object.assign(currentSoilLayer, {
    depthStart: 0,
    depthEnd: 0,
    soilType: '',
    bearingCapacity: 0,
    poissonRatio: '0.35',
  });
};

const saveSoilLayer = () => {
  // 验证数据
  if (!currentSoilLayer.soilType) {
    ElMessage.error('请选择土层类型');
    return;
  }
  if (currentSoilLayer.depthStart >= currentSoilLayer.depthEnd) {
    ElMessage.error('结束深度必须大于起始深度');
    return;
  }
  if (currentSoilLayer.bearingCapacity <= 0) {
    ElMessage.error('压缩模量必须大于0');
    return;
  }

  if (editingIndex.value !== -1) {
    // 编辑现有土层
    Object.assign(soilLayersData[editingIndex.value], currentSoilLayer);
    ElMessage({ message: '土层更新成功！', type: 'success' });
  } else {
    // 添加新土层
    soilLayersData.push({ ...currentSoilLayer });
    ElMessage({ message: '土层添加成功！', type: 'success' });
  }
  
  handleSoilLayerDialogClose();
};
</script>

<style scoped>
/* 共享样式可以提取到全局CSS文件中 */
:root {
  --foundation-primary: #67c23a;
  --bg-card: #f9fafb; /* Changed from rgba(17, 24, 39, 0.8) */
  --bg-section: #f0f2f5; /* Changed from rgba(31, 41, 55, 0.6) */
  --bg-input: #ffffff; /* Changed from rgba(31, 41, 55, 0.9) */
  --vt-c-text-dark-1: #333; /* Changed from #e5e7eb */
  --vt-c-text-dark-2: #666; /* Changed from #9ca3af */
  --vt-c-text-numeric: #007bff; /* Changed from #67e8f9 */
}

.foundation-stability-view {
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
  font-size: 0.95rem;
  line-height: 1.6;
  max-width: 800px;
}

.schematic-diagram-container {
  margin-bottom: 24px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--el-border-color);
}

.schematic-diagram {
  width: 100%;
  height: auto;
  display: block;
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
  margin-bottom: 20px;
  background-color: var(--bg-section);
  border-radius: 8px;
  padding: 16px;
  border: 1px solid var(--el-border-color-light);
  transition: all 0.3s ease;
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

.calculation-form :deep(.el-form-item__label) {
  color: var(--text-primary);
  font-weight: 500;
}

.calculation-form :deep(.el-input__wrapper),
.calculation-form :deep(.el-input-number),
.calculation-form :deep(.el-select__wrapper) {
  background-color: var(--bg-input);
  box-shadow: none;
  border: 1px solid var(--el-border-color);
}

.calculation-form :deep(.el-input__inner),
.calculation-form :deep(.el-input-number__input) {
  color: var(--text-primary);
  font-weight: 500;
}

/* 确保下拉框内部的文字颜色也是正确的 */
.calculation-form :deep(.el-select .el-input__inner) {
    color: var(--text-primary) !important;
}

.calculation-form :deep(.el-input__wrapper:hover),
.calculation-form :deep(.el-input-number:hover),
.calculation-form :deep(.el-select__wrapper:hover) {
  border-color: var(--foundation-primary); /* Changed from var(--brand-primary) */
}

.calculation-form :deep(.el-input__wrapper.is-focus),
.calculation-form :deep(.el-input-number.is-focus),
.calculation-form :deep(.el-select__wrapper.is-focus) {
  border-color: var(--foundation-primary); /* Changed from var(--brand-primary) */
  box-shadow: 0 0 0 1px var(--foundation-primary); /* Changed from var(--brand-primary) */
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

.result-content {
  padding: 8px 0;
}

.result-descriptions {
  margin-top: 20px;
}

.result-descriptions :deep(.el-descriptions__header) {
  margin-bottom: 16px;
}

.result-descriptions :deep(.el-descriptions__title) {
  color: var(--text-primary);
  font-size: 1.125rem;
  font-weight: 600;
}

.result-descriptions :deep(.el-descriptions__cell) {
  border-color: var(--el-border-color) !important;
}

.result-descriptions :deep(.el-descriptions__label) {
  background: var(--bg-section) !important;
  color: var(--text-secondary) !important;
  font-weight: 500;
}

.result-descriptions :deep(.el-descriptions__content) {
  background: transparent !important;
  color: var(--text-primary);
}

.result-descriptions :deep(.el-tag) {
  white-space: pre-wrap;
  height: auto;
  line-height: 1.5;
  padding: 8px 12px;
}

.conclusion-tag {
  height: auto !important;
  white-space: normal !important;
  line-height: 1.6 !important;
  padding: 12px !important;
  display: block !important;
  text-align: left;
}

.conclusion-tag.el-tag--danger {
  background-color: var(--brand-accent) !important;
  color: var(--text-on-primary) !important;
}

.conclusion-separator {
  border-top: 1px solid rgba(255, 255, 255, 0.2); /* This will be removed */
  margin-top: 8px;
  padding-top: 8px;
}

.conclusion-text {
  font-weight: 600;
}

.numeric-value {
  color: var(--vt-c-text-numeric);
  font-weight: 500;
  font-size: 1.1rem;
}

.empty-result {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  color: var(--text-secondary);
}

/* 标签页样式 */
.result-tabs {
  margin-top: 16px;
}

.result-tabs :deep(.el-tabs__header) {
  margin: 0 0 20px 0;
  border-bottom: 2px solid var(--el-border-color);
}

.result-tabs :deep(.el-tabs__nav-wrap::after) {
  display: none;
}

.result-tabs :deep(.el-tabs__item) {
  color: var(--text-secondary);
  font-weight: 500;
  padding: 0 20px;
  height: 44px;
  line-height: 44px;
}

.result-tabs :deep(.el-tabs__item.is-active) {
  color: var(--foundation-primary);
  font-weight: 600;
}

.result-tabs :deep(.el-tabs__active-bar) {
  background-color: var(--foundation-primary);
  height: 3px;
}

/* 安全评估报告样式 */
.safety-report {
  padding: 20px 0;
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
  margin: 0;
  font-size: 1.25rem;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 8px;
}

.export-buttons {
  display: flex;
  gap: 12px;
}

.report-content {
  max-height: 600px;
  overflow-y: auto;
  padding-right: 8px;
}

.report-section {
  margin-bottom: 24px;
  background: var(--bg-section);
  border-radius: 8px;
  padding: 20px;
  border: 1px solid var(--el-border-color-light);
}

.report-section h4 {
  margin: 0 0 16px 0;
  font-size: 1.125rem;
  color: var(--text-primary);
  font-weight: 600;
  border-bottom: 1px solid var(--el-border-color);
  padding-bottom: 8px;
}

.safety-assessment {
  margin-top: 12px;
}

.recommendations-list {
  margin: 12px 0;
  padding-left: 20px;
  color: var(--text-primary);
}

.recommendations-list li {
  margin-bottom: 8px;
  line-height: 1.6;
}

.conclusion {
  color: var(--text-primary);
  line-height: 1.8;
}

.conclusion p {
  margin-bottom: 16px;
}

.signature-section {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid var(--el-border-color);
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.signature-section p {
  margin-bottom: 4px;
}

/* 表格样式调整 */
.report-section :deep(.el-table) {
  margin-top: 12px;
}

.report-section :deep(.el-table th) {
  background-color: var(--bg-input);
  color: var(--text-primary);
  font-weight: 600;
}

.report-section :deep(.el-table td) {
  color: var(--text-primary);
}

.report-section :deep(.el-descriptions) {
  margin-top: 12px;
}

.report-section :deep(.el-descriptions__label) {
  background: var(--bg-input) !important;
  color: var(--text-secondary) !important;
  font-weight: 500;
}

.report-section :deep(.el-descriptions__content) {
  background: transparent !important;
  color: var(--text-primary);
}

/* 滚动条样式 */
.report-content::-webkit-scrollbar {
  width: 6px;
}

.report-content::-webkit-scrollbar-track {
  background: var(--el-border-color-lighter);
  border-radius: 3px;
}

.report-content::-webkit-scrollbar-thumb {
  background: var(--el-border-color);
  border-radius: 3px;
}

.report-content::-webkit-scrollbar-thumb:hover {
  background: var(--el-border-color-dark);
}

/* 塔体自重计算表格样式 */
.tower-weight-table {
  margin-top: 16px;
}

.tower-weight-table :deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
}

.tower-weight-table :deep(.el-table__header-wrapper) {
  border-radius: 8px 8px 0 0;
}

.tower-weight-table :deep(.el-input-number) {
  width: 100%;
}

.tower-weight-table :deep(.el-input-number .el-input__inner) {
  text-align: center;
  font-size: 13px;
  padding: 0 8px;
}

.tower-weight-table :deep(.el-table__footer-wrapper) {
  background: #f8f9fa;
  font-weight: 600;
}

.tower-weight-table :deep(.el-table__footer .cell) {
  color: var(--text-primary);
  font-weight: 600;
}

.weight-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid var(--el-border-color-light);
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.summary-label {
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
}

.summary-value {
  color: var(--text-primary);
  font-size: 16px;
  font-weight: 600;
}

.summary-value.highlight {
  color: var(--foundation-primary);
  font-size: 18px;
}

/* PDF报告样式 */
.pdf-report-container {
  font-family: 'Microsoft YaHei', 'SimSun', 'SimHei', sans-serif; /* 使用系统中文字体 */
  color: #333;
  background-color: white;
  padding: 20px;
  box-sizing: border-box;
  width: 100%;
  max-width: 794px; /* A4宽度为210mm，约794px */
  margin: 0 auto;
}

.pdf-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 20px;
  width: 100%;
}

.pdf-header .logo-section {
  display: flex;
  align-items: center;
  width: 100%;
}

.pdf-header .pdf-logo {
  width: 90px;
  height: 54px; /* 保持SVG的宽高比 135:80 = 90:54 */
  margin-right: 20px;
  object-fit: contain;
}

.pdf-header .company-info h1 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: #000;
}

.pdf-header .company-info h2 {
  font-size: 14px;
  font-weight: 500;
  margin: 5px 0 0 0;
  color: #555;
}

.pdf-divider {
  border-bottom: 2px solid #0056b3;
  margin-bottom: 20px;
  width: 100%;
}

.pdf-divider-thin {
  border-bottom: 1px solid #e0e0e0;
  margin-bottom: 15px;
  width: 100%;
}

.pdf-section {
  margin-bottom: 20px;
  width: 100%;
}

.pdf-section-title {
  font-size: 14px;
  font-weight: 600;
  color: #0056b3;
  margin-bottom: 10px;
  width: 100%;
}

.pdf-info-grid,
.pdf-params-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px 20px;
  font-size: 12px;
  width: 100%;
}

.pdf-params-grid {
  grid-template-columns: repeat(3, 1fr);
}

.pdf-info-grid p,
.pdf-params-grid p {
  margin: 0;
  line-height: 1.6;
}

.pdf-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
  margin: 15px 0;
  table-layout: fixed; /* 固定表格布局 */
}

.pdf-table th,
.pdf-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
  word-wrap: break-word; /* 允许长文本换行 */
  overflow-wrap: break-word; /* 允许长文本换行 */
}

.pdf-table th {
  background-color: #f2f2f2;
  font-weight: 600;
}

.pdf-pass {
  color: green;
  font-weight: bold;
}

.pdf-fail {
  color: red;
  font-weight: bold;
}

.pdf-chart {
  width: 100%;
  margin: 15px 0;
  text-align: center;
}

.pdf-chart img {
  max-width: 100%;
  height: auto;
}

.pdf-conclusion p {
  font-size: 12px;
  margin-bottom: 8px;
  width: 100%;
}

.pdf-conclusion ul {
  font-size: 12px;
  padding-left: 20px;
  margin: 0 0 10px 0;
  width: 100%;
}

.pdf-conclusion li {
  margin-bottom: 5px;
}

.pdf-footer {
  margin-top: 30px;
  text-align: center;
  font-size: 10px;
  color: #888;
  width: 100%;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .weight-summary {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .summary-item {
    justify-content: space-between;
  }
}

/* 土层参数管理样式 */
.soil-layers-section {
  margin-top: 20px;
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

.soil-layers-table :deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
}

.soil-layers-table :deep(.el-table__header-wrapper) {
  border-radius: 8px 8px 0 0;
}

.soil-layers-table :deep(.el-input-number) {
  width: 100%;
}

.soil-layers-table :deep(.el-input-number .el-input__inner) {
  text-align: center;
  font-size: 13px;
  padding: 0 8px;
}

.soil-layers-table :deep(.el-table__footer-wrapper) {
  background: #f8f9fa;
  font-weight: 600;
}

.soil-layers-table :deep(.el-table__footer .cell) {
  color: var(--text-primary);
  font-weight: 600;
}

.depth-range {
  display: flex;
  gap: 10px;
}

.depth-input {
  width: 100%;
}

.depth-separator {
  font-size: 14px;
  line-height: 1;
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
.soil-layer-form :deep(.el-input-number__input) {
  color: var(--text-primary);
  font-weight: 500;
}

/* 确保下拉框内部的文字颜色也是正确的 */
.soil-layer-form :deep(.el-select .el-input__inner) {
    color: var(--text-primary) !important;
}

.soil-layer-form :deep(.el-input__wrapper:hover),
.soil-layer-form :deep(.el-input-number:hover),
.soil-layer-form :deep(.el-select__wrapper:hover) {
  border-color: var(--foundation-primary); /* Changed from var(--brand-primary) */
}

.soil-layer-form :deep(.el-input__wrapper.is-focus),
.soil-layer-form :deep(.el-input-number.is-focus),
.soil-layer-form :deep(.el-select__wrapper.is-focus) {
  border-color: var(--foundation-primary); /* Changed from var(--brand-primary) */
  box-shadow: 0 0 0 1px var(--foundation-primary); /* Changed from var(--brand-primary) */
}
</style> 