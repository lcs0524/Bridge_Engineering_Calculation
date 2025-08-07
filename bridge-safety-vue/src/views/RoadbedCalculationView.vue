<template>
  <div class="roadbed-calculation-view">
    <div class="page-header">
      <h1>路基顶管施工稳定性计算</h1>
      <p class="page-description">本模块依据《给水排水管道工程施工及验收规范》(GB50268-2008)及相关工程实践，综合计算顶推力、管道承压能力及后背墙稳定性，确保施工安全。</p>
    </div>

    <el-row :gutter="32">
      <!-- 左侧输入表单 -->
      <el-col :xs="24" :sm="24" :md="10" :lg="10" :xl="10">
        <el-card shadow="hover">
            <template #header>
              <div class="card-header">
              <span>路基顶管施工稳定性计算</span>
              </div>
            </template>
          
          <el-form :model="formData" label-position="top" class="calculation-form">
            <!-- 项目信息 -->
            <div class="form-section">
              <h3 class="section-title">项目信息</h3>
              <el-form-item label="项目名称">
                <el-input v-model="formData.projectName" placeholder="请输入项目名称" class="full-width" />
              </el-form-item>
              <el-form-item label="项目信息">
                <el-input
                  v-model="formData.projectInfo"
                  type="textarea"
                  :rows="3"
                  placeholder="请输入项目详细信息"
                  class="full-width"
                />
              </el-form-item>
            </div>

                         <!-- 计算输入参数 -->
             <div class="form-section">
               <h2><el-icon class="header-icon"><Connection /></el-icon> 计算输入参数</h2>
            
            <div class="schematic-diagram-container">
              <img src="@/assets/images/穿管工程简图.png" alt="穿管工程简图" class="schematic-diagram">
              </div>
              
              <!-- 管道与几何参数 -->
               <h4><el-icon><Odometer /></el-icon> 管道与几何参数</h4>
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="管道外径 D (m)">
                      <el-input-number v-model="formData.pipeOuterDiameter" :min="0" :precision="2" :step="0.1" class="full-width" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="管壁厚度 t (m)">
                      <el-input-number v-model="formData.pipeThickness" :min="0" :precision="3" :step="0.01" class="full-width" />
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="单段顶进长度 L (m)">
                      <el-input-number v-model="formData.pushLength" :min="0" :precision="1" :step="1" class="full-width" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="管顶覆土深度 H (m)">
                      <el-input-number v-model="formData.coverDepth" :min="0" :precision="2" :step="0.1" class="full-width" />
                    </el-form-item>
                  </el-col>
                </el-row>
                 <el-row :gutter="20">
                    <el-col :span="12">
                       <el-form-item label="工具管外径 Dt (m)">
                         <el-input-number v-model="formData.toolPipeOuterDiameter_Dt" :min="0" :precision="2" :step="0.1" class="full-width" />
                    </el-form-item>
                  </el-col>
                </el-row>
              </div>
              
              <!-- 材料与施工参数 -->
              <div class="form-section">
                <h3><el-icon><Box /></el-icon> 材料与施工参数</h3>
                 <el-row :gutter="20">
                    <el-col :span="12">
                <el-form-item label="管道材料">
                  <el-select v-model="formData.pipeMaterial" placeholder="选择管道材料" class="full-width">
                            <el-option label="钢筋混凝土管 (RCP)" value="concrete" />
                            <el-option label="高密度聚乙烯管 (HDPE)" value="hdpe" />
                  </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="单位面积摩阻力 f (kPa)">
                            <el-input-number v-model="formData.friction_f" :min="0" :precision="1" :step="1" class="full-width" />
                        </el-form-item>
                    </el-col>
                 </el-row>
                 <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="混凝土抗压强度 fc (MPa)">
                            <el-input-number v-model="formData.concreteCompressiveStrength_fc" :min="0" :precision="1" :step="1" class="full-width" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="稳定系数 φ">
                           <el-input-number v-model="formData.stabilityFactor_phi" :min="0" :max="1" :precision="2" :step="0.05" class="full-width" />
                        </el-form-item>
                    </el-col>
                 </el-row>
                <el-form-item label="工具管类型">
                  <el-radio-group v-model="formData.toolPipeType">
                    <el-radio-button label="closed">封闭式(泥水平衡)</el-radio-button>
                    <el-radio-button label="open">开放式</el-radio-button>
                  </el-radio-group>
                </el-form-item>
                <el-form-item label="是否考虑管道接口摩擦 F₃">
                   <el-switch v-model="formData.considerInterfaceFriction" />
                </el-form-item>

                <div v-if="formData.considerInterfaceFriction">
                  <el-row :gutter="20">
                    <el-col :span="12">
                      <el-form-item label="接口数量 n">
                        <el-input-number v-model="formData.interfaceCount" :min="0" :step="1" class="full-width" />
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="摩擦系数 μ (钢-混凝土)">
                        <el-input-number v-model="formData.interfaceFrictionCoefficient_mu" :min="0" :max="1" :precision="2" :step="0.01" class="full-width" />
                      </el-form-item>
                    </el-col>
                  </el-row>
                  <el-row :gutter="20">
                    <el-col :span="12">
                       <el-form-item label="接口压紧力 N (kN)">
                         <el-input-number v-model="formData.interfacePressure_N" :min="0" :precision="1" :step="1" class="full-width" />
                       </el-form-item>
                    </el-col>
                  </el-row>
                </div>

                <el-divider />

                <el-form-item label="安全系数 K">
                  <el-input-number v-model="formData.safetyFactor_K" :min="1.0" :max="2.0" :precision="2" :step="0.05" class="full-width" />
                </el-form-item>
              </div>
              
              <!-- 土质参数 -->
              <div class="form-section">
                <h3><el-icon><Files /></el-icon> 土质参数</h3>
                <el-row :gutter="20">
                   <el-col :span="12">
                      <el-form-item label="土体重度 γ (kN/m³)">
                        <el-input-number v-model="formData.soilUnitWeight" :min="0" :precision="1" :step="0.5" class="full-width" />
                </el-form-item>
                   </el-col>
                   <el-col :span="12">
                     <el-form-item label="土体反力模量 E' (MPa)">
                       <el-input-number v-model="formData.soilReactionModulus_E_prime" :min="0" :precision="1" :step="1" class="full-width" />
                </el-form-item>
                   </el-col>
                </el-row>
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="黏聚力 c (kPa)">
                      <el-input-number v-model="formData.cohesion_c" :min="0" :precision="1" :step="1" class="full-width" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="内摩擦角 φ (°)">
                      <el-input-number v-model="formData.internalFrictionAngle_phi" :min="0" :max="90" :precision="1" :step="1" class="full-width" />
                    </el-form-item>
                  </el-col>
                </el-row>
              </div>

              <!-- 后背墙稳定性参数 -->
              <div class="form-section">
                <h3><el-icon><OfficeBuilding /></el-icon> 后背墙稳定性参数</h3>
                <el-form-item label="后背墙类型">
                  <el-radio-group v-model="formData.backWallType" class="full-width">
                    <el-radio-button label="gravity">重力式混凝土后背墙</el-radio-button>
                    <el-radio-button label="pile">桩基加固后背墙</el-radio-button>
                    <el-radio-button label="sheet_pile">钢板桩后背墙</el-radio-button>
                  </el-radio-group>
                </el-form-item>

                <!-- 重力式 -->
                <div v-if="formData.backWallType === 'gravity'">
                    <el-row :gutter="20">
                        <el-col :span="12">
                             <el-form-item label="后背墙自重 W (kN)">
                               <el-input-number v-model="formData.gravity.W_selfWeight" :min="0" :precision="1" class="full-width" />
                             </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="墙后土体自重 Ws (kN)">
                                <el-input-number v-model="formData.gravity.Ws_soilWeight" :min="0" :precision="1" class="full-width" />
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-form-item label="墙底与地基摩擦系数 μ">
                        <el-input-number v-model="formData.gravity.mu_frictionCoeff" :min="0" :max="1" :precision="2" :step="0.05" class="full-width" />
                    </el-form-item>
                </div>
                <!-- 桩基 -->
                <div v-if="formData.backWallType === 'pile'">
                     <el-row :gutter="20">
                        <el-col :span="12">
                           <el-form-item label="抗滑桩数量 n">
                             <el-input-number v-model="formData.pile.n_pileCount" :min="0" :step="1" class="full-width" />
                           </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="单桩抗滑承载力 Pu (kN)">
                                <el-input-number v-model="formData.pile.Pu_singlePileCapacity" :min="0" :precision="1" class="full-width" />
                            </el-form-item>
                        </el-col>
                    </el-row>
                </div>
                <!-- 钢板桩 -->
                <div v-if="formData.backWallType === 'sheet_pile'">
                     <el-row :gutter="20">
                        <el-col :span="12">
                            <el-form-item label="钢板桩与土体摩擦角 δ (°)">
                               <el-input-number v-model="formData.sheet_pile.delta_frictionAngle" :min="0" :max="90" :precision="1" class="full-width" />
                           </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="钢板桩与土体接触面积 A (m²)">
                               <el-input-number v-model="formData.sheet_pile.A_contactArea" :min="0" :precision="2" class="full-width" />
                           </el-form-item>
                        </el-col>
                    </el-row>
                    <el-form-item label="界面抗剪强度 τ (kPa)">
                        <el-input-number v-model="formData.sheet_pile.tau_shearStrength" :min="0" :precision="1" class="full-width" />
                </el-form-item>
                </div>
              </div>
              
              <div class="form-actions">
                <el-button type="primary" @click="performCalculations" :loading="calculating" size="large">
                  <el-icon><Cpu /></el-icon> 全面计算
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
                <el-tag v-if="hasResults" type="success" effect="light" size="small">计算完成</el-tag>
              </div>
            </template>
            
            <el-tabs v-model="activeTab" class="result-tabs">
              <el-tab-pane label="顶进力分析" name="force">
                <div v-if="hasResults" class="result-content">
                  <el-descriptions title="顶推力计算详情" :column="2" border>
                    <el-descriptions-item label="F₁ 管道外壁摩擦阻力" label-align="left" :span="2">
                      <span class="highlight-value">{{ results.F1_frictionResistance }} kN</span>
                    </el-descriptions-item>
                     <el-descriptions-item label="F₂ 工具管正面阻力" label-align="left" :span="2">
                      <span class="highlight-value">{{ results.F2_frontResistance }} kN</span>
                    </el-descriptions-item>
                    <el-descriptions-item label="F₃ 管道接口摩擦阻力" label-align="left" :span="2">
                      <span class="numeric-value">{{ results.F3_interfaceFriction }} kN</span>
                    </el-descriptions-item>
                    <el-descriptions-item label="总顶推力 F = K(F₁+F₂+F₃)" label-align="left" :span="2">
                      <span class="highlight-value" style="color: var(--brand-accent);">{{ results.totalPushForce }} kN</span>
                    </el-descriptions-item>
                  </el-descriptions>
                </div>
                <div v-else class="empty-result">
                  <el-empty description="暂无数据，请先进行计算" />
                </div>
              </el-tab-pane>

              <el-tab-pane label="管道强度与变形" name="settlement">
                <div v-if="hasResults" class="result-content">
                  <!-- 可视化图片 -->
                  <div class="visualization-section">
                    <h4 class="section-title">
                      <el-icon><PieChart /></el-icon>
                      工程示意与验算结果可视化
                    </h4>
                    <PipelineStressVisualization
                      :pipeStrengthOk="results.pipeStrengthOk"
                      :pipeDeformationOk="results.pipeDeformationOk"
                      :strengthValue="results.sigma_hoopStress"
                      :deformationValue="results.S_pipeDeformation"
                    />
                  </div>

                  <el-descriptions title="荷载计算" :column="2" border class="result-descriptions">
                     <el-descriptions-item label="Pᵥ 垂直土压力" label-align="left">
                      <span class="numeric-value">{{ results.Pv_verticalSoilPressure }} kPa</span>
                    </el-descriptions-item>
                    <el-descriptions-item label="q 车辆活载" label-align="left">
                      <span class="numeric-value">{{ results.q_vehicleLoad }} kPa</span>
                    </el-descriptions-item>
                  </el-descriptions>
                  
                  <el-descriptions title="强度与变形验算" :column="2" border class="result-descriptions" style="margin-top: 20px;">
                    <el-descriptions-item label="σ 环向应力" label-align="left">
                       <span class="numeric-value">{{ results.sigma_hoopStress }} MPa</span>
                    </el-descriptions-item>
                    <el-descriptions-item label="[f] 管材抗拉强度" label-align="left">
                      <span class="numeric-value">{{ results.pipeTensileStrength }} MPa</span>
                    </el-descriptions-item>
                    <el-descriptions-item label="强度验算" label-align="left" :span="2">
                       <el-tag :type="results.pipeStrengthOk ? 'success' : 'danger'" effect="dark">
                        σ = {{ results.sigma_hoopStress }} MPa ≤ [f] = {{ results.pipeTensileStrength }} MPa
                        (结论: {{ results.pipeStrengthOk ? '通过' : '不通过' }})
                      </el-tag>
                    </el-descriptions-item>

                    <el-descriptions-item label="S 管体变形量" label-align="left">
                       <span class="numeric-value">{{ results.S_pipeDeformation }} mm</span>
                    </el-descriptions-item>
                     <el-descriptions-item label="[S] 容许变形量" label-align="left">
                      <span class="numeric-value">{{ results.allowableDeformation }} mm</span>
                    </el-descriptions-item>
                    <el-descriptions-item label="变形验算" label-align="left" :span="2">
                       <el-tag :type="results.pipeDeformationOk ? 'success' : 'danger'" effect="dark">
                        S = {{ results.S_pipeDeformation }} mm ≤ 0.05D = {{ results.allowableDeformation }} mm
                        (结论: {{ results.pipeDeformationOk ? '通过' : '不通过' }})
                      </el-tag>
                    </el-descriptions-item>
                  </el-descriptions>
                </div>
                <div v-else class="empty-result">
                  <el-empty description="暂无数据，请先进行计算" />
                </div>
              </el-tab-pane>

              <el-tab-pane label="稳定性综合验算" name="stability">
                <div v-if="hasResults" class="result-content">
                    <!-- 可视化图片 -->
                    <div class="visualization-section">
                      <h4 class="section-title">
                        <el-icon><PieChart /></el-icon>
                        稳定性综合验算可视化
                      </h4>
                      <PipelineStabilityVisualization
                        :pipePressureCheckOk="results.pipePressureCheckOk"
                        :backWallStabilityCheckOk="results.backWallStabilityCheckOk"
                        :totalPushForce="results.totalPushForce"
                        :pipeMaxPressureCapacity="results.pipeMaxPressureCapacity"
                        :backWallTotalResistance="results.backWallTotalResistance"
                      />
                    </div>

                    <!-- 管道承压能力 -->
                    <el-descriptions title="管道承压能力验算" :column="1" border class="result-descriptions">
                        <el-descriptions-item label="管道允许最大承压 F_allow">
                            <span class="numeric-value">{{ results.pipeMaxPressureCapacity }} kN</span>
                        </el-descriptions-item>
                        <el-descriptions-item label="验算结论">
                            <el-tag :type="results.pipePressureCheckOk ? 'success' : 'danger'" effect="dark">
                                F = {{ results.totalPushForce }} kN ≤ F_allow = {{ results.pipeMaxPressureCapacity }} kN (结论: {{ results.pipePressureCheckOk ? '通过' : '不通过' }})
                            </el-tag>
                        </el-descriptions-item>
                    </el-descriptions>
                    <!-- 后背墙稳定性 -->
                    <el-descriptions title="后背墙抗滑移稳定性验算" :column="1" border class="result-descriptions" style="margin-top: 20px;">
                         <el-descriptions-item label="被动土压力 Ep">
                            <span class="numeric-value">{{ results.passiveSoilPressure_Ep }} kN</span>
                        </el-descriptions-item>
                        <el-descriptions-item label="结构抗滑移阻力 R">
                            <span class="numeric-value">{{ results.structuralResistance_R }} kN</span>
                        </el-descriptions-item>
                        <el-descriptions-item label="后背墙总抗力 R_total = Ep + R">
                            <span class="highlight-value">{{ results.backWallTotalResistance }} kN</span>
                        </el-descriptions-item>
                        <el-descriptions-item label="验算结论">
                           <el-tag :type="results.backWallStabilityCheckOk ? 'success' : 'danger'" effect="dark">
                                F = {{ results.totalPushForce }} kN ≤ R_total = {{ results.backWallTotalResistance }} kN (结论: {{ results.backWallStabilityCheckOk ? '通过' : '不通过' }})
                            </el-tag>
                        </el-descriptions-item>
                    </el-descriptions>
                </div>
                <div v-else class="empty-result">
                  <el-empty description="暂无数据，请先进行计算" />
                </div>
              </el-tab-pane>

              <!-- 安全评估报告 -->
              <el-tab-pane label="安全评估报告" name="safety-report">
                <div v-if="hasResults" class="safety-report">
                  <div class="report-header">
                    <h3><el-icon><Document /></el-icon> 路基顶管施工安全评估报告</h3>
                    <div class="export-buttons">
                      <el-button type="primary" size="small" @click="exportPDFReport" :loading="exportingPDF">
                        <el-icon><Download /></el-icon> 导出PDF报告
                      </el-button>
                      <el-button type="info" size="small" @click="exportTXTReport">
                        <el-icon><Document /></el-icon> 导出TXT报告
                      </el-button>
                    </div>
                  </div>
                  
                  
                  <!-- 可见的报告内容 -->
                  <div class="report-content">
                    <div class="assessment-summary">
                      <h4>{{ getRoadbedOverallSafetyStatus().title }}</h4>
                      <p>{{ getRoadbedOverallSafetyStatus().description }}</p>
                    </div>
                    
                    <div class="verification-results">
                      <h4>验算结果汇总</h4>
                      <div class="verification-grid">
                        <div class="verification-item" :class="{ 'verification-pass': results.pipeStrengthOk, 'verification-fail': !results.pipeStrengthOk }">
                          <div class="verification-title">管道环向应力验算</div>
                          <div class="verification-result">{{ results.pipeStrengthOk ? '✓ 通过' : '✗ 不通过' }}</div>
                          <div class="verification-detail">σ = {{ results.sigma_hoopStress }} ≤ {{ results.pipeTensileStrength }} MPa</div>
                        </div>
                        
                        <div class="verification-item" :class="{ 'verification-pass': results.pipeDeformationOk, 'verification-fail': !results.pipeDeformationOk }">
                          <div class="verification-title">管体变形验算</div>
                          <div class="verification-result">{{ results.pipeDeformationOk ? '✓ 通过' : '✗ 不通过' }}</div>
                          <div class="verification-detail">S = {{ results.S_pipeDeformation }} ≤ {{ results.allowableDeformation }} mm</div>
                        </div>
                        
                        <div class="verification-item" :class="{ 'verification-pass': results.pipePressureCheckOk, 'verification-fail': !results.pipePressureCheckOk }">
                          <div class="verification-title">管道承压能力验算</div>
                          <div class="verification-result">{{ results.pipePressureCheckOk ? '✓ 通过' : '✗ 不通过' }}</div>
                          <div class="verification-detail">F = {{ results.totalPushForce }} ≤ {{ results.pipeMaxPressureCapacity }} kN</div>
                        </div>
                        
                        <div class="verification-item" :class="{ 'verification-pass': results.backWallStabilityCheckOk, 'verification-fail': !results.backWallStabilityCheckOk }">
                          <div class="verification-title">后背墙抗滑移验算</div>
                          <div class="verification-result">{{ results.backWallStabilityCheckOk ? '✓ 通过' : '✗ 不通过' }}</div>
                          <div class="verification-detail">F = {{ results.totalPushForce }} ≤ {{ results.backWallTotalResistance }} kN</div>
                        </div>
                      </div>
                    </div>
                    
                    <div class="recommendations">
                      <h4>技术建议</h4>
                      <div class="recommendation-list">
                        <div v-for="rec in getRoadbedRecommendations()" :key="rec.id" class="recommendation-item">
                          <div class="recommendation-title">{{ rec.title }}</div>
                          <div class="recommendation-content">{{ rec.content }}</div>
                        </div>
                      </div>
                    </div>
                    
                    <div class="conclusion">
                      <h4>评估结论</h4>
                      <div class="conclusion-content">
                        {{ getRoadbedConclusion() }}
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else class="empty-result">
                  <el-empty description="暂无数据，请先进行计算" />
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
// ShineBorder is no longer used
import { 
  Connection, 
  Document, 
  Odometer, 
  Box, 
  Files, 
  RefreshRight,
  QuestionFilled,
  TrendCharts,
  Cpu,
  OfficeBuilding,
  Download,
  PieChart
} from '@element-plus/icons-vue'
import { ElMessage, ElNotification } from 'element-plus'
import jsPDF from 'jspdf'
import html2pdf from 'html2pdf.js'
import html2canvas from 'html2canvas'
import PipelineStressVisualization from '@/components/PipelineStressVisualization.vue'
import PipelineStabilityVisualization from '@/components/PipelineStabilityVisualization.vue'
import PdfReportHeader from '@/components/PdfReportHeader.vue'
import PdfReportFooter from '@/components/PdfReportFooter.vue'
import logoImage from '@/assets/logo.png'

// --- 响应式状态定义 ---

const defaultFormData = {
  // 项目信息
  projectName: '',
  projectInfo: '',
  // 几何参数
  pipeOuterDiameter: 1.2,
  pipeThickness: 0.12,
  pushLength: 100.0,
  coverDepth: 3.0,
  toolPipeOuterDiameter_Dt: 1.22, // Dt 工具管外径
  // 材料与施工
  pipeMaterial: 'concrete',
  friction_f: 8.0,
  concreteCompressiveStrength_fc: 15.0,
  stabilityFactor_phi: 1.0,
  toolPipeType: 'closed',
  safetyFactor_K: 1.2,
  // 新增：接口摩擦
  considerInterfaceFriction: false,
  interfaceCount: 50, // n
  interfaceFrictionCoefficient_mu: 0.25, // μ
  interfacePressure_N: 10, // N: 接口压紧力(kN)
  // 土质参数
  soilUnitWeight: 18.0,
  soilReactionModulus_E_prime: 20.0,
  cohesion_c: 10.0,
  internalFrictionAngle_phi: 20.0,
  // 后背墙参数
  backWallType: 'gravity',
  gravity: {
      W_selfWeight: 500,
      Ws_soilWeight: 300,
      mu_frictionCoeff: 0.4,
  },
  pile: {
      n_pileCount: 4,
      Pu_singlePileCapacity: 400,
  },
  sheet_pile: {
      delta_frictionAngle: 15,
      A_contactArea: 20,
      tau_shearStrength: 15,
  }
};

const formData = reactive({ ...JSON.parse(JSON.stringify(defaultFormData)) });

const results = reactive({
  F1_frictionResistance: 0,
  F2_frontResistance: 0,
  F3_interfaceFriction: 0,
  totalPushForce: 0,

  Pv_verticalSoilPressure: 0,
  q_vehicleLoad: 0,
  sigma_hoopStress: 0,
  pipeTensileStrength: 0,
  pipeStrengthOk: false,
  S_pipeDeformation: 0,
  allowableDeformation: 0,
  pipeDeformationOk: false,

  pipeMaxPressureCapacity: 0,
  pipePressureCheckOk: false,
  passiveSoilPressure_Ep: 0,
  structuralResistance_R: 0,
  backWallTotalResistance: 0,
  backWallStabilityCheckOk: false,
});

const hasResults = ref(false);
const activeTab = ref('force');
const calculating = ref(false);
const exportingPDF = ref(false);

// --- 计算属性 ---

// 材料属性
const materialProperties = computed(() => {
  if (formData.pipeMaterial === 'concrete') {
    return {
      tensileStrength_f: 1.5, // MPa
      elasticModulus_E: 30000, // MPa (30 GPa)
      compressiveStrength_fc: formData.concreteCompressiveStrength_fc, // MPa
    };
  } else if (formData.pipeMaterial === 'hdpe') {
    return {
      tensileStrength_f: 8.0, // MPa
      elasticModulus_E: 800, // MPa (0.8 GPa)
      compressiveStrength_fc: 0, // HDPE不考虑抗压
    };
  }
  return { tensileStrength_f: 0, elasticModulus_E: 0, compressiveStrength_fc: 0 };
});

// --- 方法 ---

// 主计算函数
const performCalculations = () => {
  calculating.value = true;
  hasResults.value = false;

  // 模拟计算延迟
  setTimeout(() => {
    try {
      // 1. 顶推力计算
      calculatePushForce();
      
      // 2. 沉降与强度计算
      calculateSettlementAndStrength();

      // 3. 稳定性验算
      calculateStabilityChecks();

      hasResults.value = true;
      ElMessage({ message: '计算成功完成！', type: 'success' });

    } catch (error) {
      ElMessage({ message: `计算出错: ${error.message}`, type: 'error' });
    } finally {
      calculating.value = false;
    }
  }, 500);
};

// 顶推力计算
const calculatePushForce = () => {
    const { pipeOuterDiameter, pushLength, friction_f, soilUnitWeight, coverDepth, cohesion_c, internalFrictionAngle_phi, toolPipeType, safetyFactor_K, considerInterfaceFriction, interfaceCount, interfaceFrictionCoefficient_mu, interfacePressure_N, toolPipeOuterDiameter_Dt } = formData;
    
    // 1. 计算 F1 (管道外壁摩擦阻力)
    results.F1_frictionResistance = (Math.PI * pipeOuterDiameter * pushLength * friction_f).toFixed(2);

    // 2. 计算 F2 (工具管正面阻力)
    let P_frontal_pressure = 0; // kPa
    if (toolPipeType === 'closed') {
        const phi_rad = internalFrictionAngle_phi * (Math.PI / 180);
        const Ka = Math.pow(Math.tan(Math.PI / 4 - phi_rad / 2), 2);
        // 根据文档修正公式: P = γHKₐ + 2cKₐ
        P_frontal_pressure = soilUnitWeight * coverDepth * Ka + 2 * cohesion_c * Ka;
    } else { // open
        // 开放式取经验值 100~300 kPa, 取中间值 200 kPa
        P_frontal_pressure = 200;
    }
    results.F2_frontResistance = ((Math.PI * Math.pow(toolPipeOuterDiameter_Dt, 2) / 4) * P_frontal_pressure).toFixed(2);

    // 3. 计算 F3 (管道接口摩擦阻力)
    if (considerInterfaceFriction) {
        results.F3_interfaceFriction = (interfaceCount * interfaceFrictionCoefficient_mu * interfacePressure_N).toFixed(2);
    } else {
        results.F3_interfaceFriction = "0.00";
    }
    
    // 4. 计算总顶推力 F
    const F_total = safetyFactor_K * (parseFloat(results.F1_frictionResistance) + parseFloat(results.F2_frontResistance) + parseFloat(results.F3_interfaceFriction));
    results.totalPushForce = F_total.toFixed(2);
}

// 沉降与强度计算
const calculateSettlementAndStrength = () => {
    const { coverDepth, soilUnitWeight, pipeOuterDiameter, pipeThickness, soilReactionModulus_E_prime } = formData;
    const { tensileStrength_f, elasticModulus_E } = materialProperties.value;

    // 1. 垂直土压力 Pᵥ (kPa)
    const Pv = soilUnitWeight * coverDepth;
    results.Pv_verticalSoilPressure = Pv.toFixed(2);

    // 2. 车辆活载 q (kPa) - 依据文档 JTG D60-2015 修正
    const H = coverDepth;
    const tan30 = Math.tan(30 * Math.PI / 180);
    // 荷载分布面积 A = (0.2 + 2H * tan30) * (0.6 + 2H * tan30)
    const A_load_area = (0.2 + 2 * H * tan30) * (0.6 + 2 * H * tan30);
    // q = 260 / A
    const q = A_load_area > 0 ? 260 / A_load_area : 0;
    results.q_vehicleLoad = q.toFixed(2);
    
    const total_pressure_kPa = Pv + q; // 总压力 kPa
    
    // 3. 强度验算
    // σ = (Pᵥ + q) * D / (2t)
    // 压力单位从 kPa 转为 MPa (1 MPa = 1000 kPa)
    const sigma = (total_pressure_kPa / 1000) * pipeOuterDiameter / (2 * pipeThickness);
    results.sigma_hoopStress = sigma.toFixed(3);
    results.pipeTensileStrength = tensileStrength_f.toFixed(2);
    results.pipeStrengthOk = sigma <= tensileStrength_f;

    // 4. 变形验算
    // S = (Pᵥ+q)D⁴ / (3.67Et³ + 0.061E'D³)
    // 注意单位统一：压力(kPa), E/E'(MPa->kPa), 几何(m)
    const E_kPa = elasticModulus_E * 1000;
    const E_prime_kPa = soilReactionModulus_E_prime * 1000;
    const D = pipeOuterDiameter;
    const t = pipeThickness;
    
    const numerator = total_pressure_kPa * Math.pow(D, 4);
    const denominator = 3.67 * E_kPa * Math.pow(t, 3) + 0.061 * E_prime_kPa * Math.pow(D, 3);
    
    const S_m = numerator / denominator; // 变形量 (m)
    const S_mm = S_m * 1000; // 转换为 mm
    results.S_pipeDeformation = S_mm.toFixed(3);

    const allowableDeformation_mm = 0.05 * D * 1000;
    results.allowableDeformation = allowableDeformation_mm.toFixed(3);
    results.pipeDeformationOk = S_mm <= allowableDeformation_mm;
}

// 稳定性验算
const calculateStabilityChecks = () => {
    const { pipeOuterDiameter, pipeThickness, stabilityFactor_phi, soilUnitWeight, coverDepth, internalFrictionAngle_phi, cohesion_c, backWallType, gravity, pile, sheet_pile } = formData;
    const { compressiveStrength_fc } = materialProperties.value;
    const totalPushForceNum = parseFloat(results.totalPushForce);

    // 1. 管道承压能力验算 F ≤ ϕ⋅fc⋅Ap
    const Ap_pipeArea_mm2 = Math.PI * (Math.pow(pipeOuterDiameter * 1000, 2) - Math.pow((pipeOuterDiameter - 2 * pipeThickness) * 1000, 2)) / 4;
    // fc (MPa) * Ap (mm^2) = N, 转换为 kN
    const F_allow_kN = (stabilityFactor_phi * compressiveStrength_fc * Ap_pipeArea_mm2) / 1000;
    results.pipeMaxPressureCapacity = F_allow_kN.toFixed(2);
    results.pipePressureCheckOk = totalPushForceNum <= F_allow_kN;

    // 2. 后背墙抗滑移稳定性验算 F ≤ Ep + R
    const phi_rad = internalFrictionAngle_phi * (Math.PI / 180);
    const Kp = Math.pow(Math.tan(Math.PI / 4 + phi_rad / 2), 2);
    // 修正被动土压力 Ep 公式，去除多余的开方
    const Ep = 0.5 * soilUnitWeight * Math.pow(coverDepth, 2) * Kp + 2 * cohesion_c * coverDepth * Kp;
    results.passiveSoilPressure_Ep = Ep.toFixed(2);

    let R_resistance = 0;
    switch (backWallType) {
        case 'gravity':
            R_resistance = (gravity.W_selfWeight + gravity.Ws_soilWeight) * gravity.mu_frictionCoeff;
            break;
        case 'pile':
            R_resistance = pile.n_pileCount * pile.Pu_singlePileCapacity;
            break;
        case 'sheet_pile':
            const delta_rad = sheet_pile.delta_frictionAngle * (Math.PI / 180);
            R_resistance = Ep * Math.tan(delta_rad) + sheet_pile.A_contactArea * sheet_pile.tau_shearStrength;
            break;
    }
    results.structuralResistance_R = R_resistance.toFixed(2);

    const R_total = Ep + R_resistance;
    results.backWallTotalResistance = R_total.toFixed(2);
    results.backWallStabilityCheckOk = totalPushForceNum <= R_total;
}


// 重置表单
const resetForm = () => {
  Object.assign(formData, JSON.parse(JSON.stringify(defaultFormData)));
  Object.keys(results).forEach(key => {
    if (typeof results[key] === 'number') {
      results[key] = 0;
    } else if (typeof results[key] === 'boolean') {
      results[key] = false;
    }
  });
  hasResults.value = false;
  activeTab.value = 'force';
  ElMessage({ message: '所有参数已重置。', type: 'info' });
};

// --- 安全评估报告相关方法 ---

// 获取当前日期
const getCurrentDate = () => {
  return new Date().toLocaleDateString('zh-CN')
}

// 获取当前日期时间
const getCurrentDateTime = () => {
  return new Date().toLocaleString('zh-CN')
}

// 获取管道材料名称
const getPipeMaterialName = () => {
  const materialMap = {
    'concrete': '钢筋混凝土管 (RCP)',
    'hdpe': '高密度聚乙烯管 (HDPE)'
  }
  return materialMap[formData.pipeMaterial] || '未知材料'
}

// 获取工具管类型名称
const getToolPipeTypeName = () => {
  const typeMap = {
    'closed': '封闭式(泥水平衡)',
    'open': '开放式'
  }
  return typeMap[formData.toolPipeType] || '未知类型'
}

// 获取后背墙类型名称
const getBackWallTypeName = () => {
  const typeMap = {
    'gravity': '重力式挡墙',
    'pile': '桩基式挡墙',
    'sheet_pile': '钢板桩挡墙'
  }
  return typeMap[formData.backWallType] || '未知类型'
}

// 获取路基顶管整体安全状况
const getRoadbedOverallSafetyStatus = () => {
  const passedCount = [
    results.pipeStrengthOk,
    results.pipeDeformationOk,
    results.pipePressureCheckOk,
    results.backWallStabilityCheckOk
  ].filter(Boolean).length

  if (passedCount === 4) {
    return {
      title: '整体安全状况：优良',
      description: '所有验算项目均通过，顶管施工在当前参数条件下是安全的，可以按计划实施。'
    }
  } else if (passedCount >= 2) {
    return {
      title: '整体安全状况：一般',
      description: `有${4-passedCount}项验算未通过，建议优化相关参数或采取加强措施后再进行施工。`
    }
  } else {
    return {
      title: '整体安全状况：危险',
      description: '多项验算未通过，当前施工方案存在重大安全隐患，必须重新设计施工方案。'
    }
  }
}

// 获取路基顶管技术建议
const getRoadbedRecommendations = () => {
  const recommendations = []
  let recId = 1

  // 管道强度建议
  if (!results.pipeStrengthOk) {
    recommendations.push({
      id: recId++,
      title: '管道强度加强',
      content: '环向应力超标，建议增加管壁厚度或选择更高强度的管道材料。'
    })
  }

  // 变形控制建议
  if (!results.pipeDeformationOk) {
    recommendations.push({
      id: recId++,
      title: '变形控制措施',
      content: '管体变形过大，建议优化顶进施工工艺，控制顶进速度和压力。'
    })
  }

  // 承压能力建议
  if (!results.pipePressureCheckOk) {
    recommendations.push({
      id: recId++,
      title: '承压能力提升',
      content: '管道承压能力不足，建议分段施工降低单次顶推力，或加强管道结构。'
    })
  }

  // 后背墙稳定性建议
  if (!results.backWallStabilityCheckOk) {
    recommendations.push({
      id: recId++,
      title: '后背墙加固',
      content: '后背墙抗滑移能力不足，建议加强后背墙设计或采用更可靠的支撑结构。'
    })
  }

  // 通用建议
  recommendations.push({
    id: recId++,
    title: '施工监测',
    content: '建议在施工过程中加强变形监测，及时调整施工参数以确保安全。'
  })

  recommendations.push({
    id: recId++,
    title: '应急预案',
    content: '制定详细的应急预案，包括顶进困难、管道变形等突发情况的处理措施。'
  })

  return recommendations
}

// 获取路基顶管评估结论
const getRoadbedConclusion = () => {
  const passedCount = [
    results.pipeStrengthOk,
    results.pipeDeformationOk,
    results.pipePressureCheckOk,
    results.backWallStabilityCheckOk
  ].filter(Boolean).length

  if (passedCount === 4) {
    return '综合评估认为，当前顶管施工方案在技术上是可行的，各项安全验算均满足规范要求。建议按照设计参数进行施工，并在施工过程中严格控制质量，确保工程安全顺利完成。'
  } else if (passedCount >= 2) {
    return '综合评估认为，当前顶管施工方案需要进一步优化。建议根据技术建议调整相关参数，并采取相应的加强措施后方可施工。'
  } else {
    return '综合评估认为，当前顶管施工方案存在重大安全风险，不建议按现有方案施工。必须重新进行设计计算，确保所有安全验算均通过后方可实施。'
  }
}

// 导出TXT报告
const exportTXTReport = () => {
  if (!hasResults.value) {
    ElNotification({
      title: '导出失败',
      message: '请先进行计算再导出报告',
      type: 'warning',
      position: 'top-right'
    })
    return
  }

  const content = generateTXTReportContent()
  const blob = new Blob([content], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `路基顶管施工稳定性评估报告_${getCurrentDate().replace(/\//g, '')}.txt`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)

  ElNotification({
    title: '导出成功',
    message: 'TXT报告已导出到下载文件夹',
    type: 'success',
    position: 'top-right'
  })
}

// 生成TXT报告内容
const generateTXTReportContent = () => {
  return `
═══════════════════════════════════════════════════════════════
                     路基顶管施工稳定性评估报告
                     吉林省志安科技有限公司
═══════════════════════════════════════════════════════════════

【项目名称】${formData.projectName || '路基顶管施工项目'}
【项目类型】路基顶管施工稳定性计算
【计算日期】${getCurrentDate()}
【报告生成时间】${getCurrentDateTime()}

───────────────────────────────────────────────────────────────
                           计算条件
───────────────────────────────────────────────────────────────

【管道与几何参数】
管道外径 D：${formData.pipeOuterDiameter}m
工具管外径 Dt：${formData.toolPipeOuterDiameter_Dt}m
管壁厚度 t：${formData.pipeThickness}m
单段顶进长度 L：${formData.pushLength}m
管顶覆土深度 H：${formData.coverDepth}m

【材料与施工参数】
管道材料：${getPipeMaterialName()}
工具管类型：${getToolPipeTypeName()}
单位面积摩阻力 f：${formData.friction_f}kPa
混凝土抗压强度 fc：${formData.concreteCompressiveStrength_fc}MPa
稳定系数 φ：${formData.stabilityFactor_phi}

【土壤参数】
土壤重度 γ：${formData.soilUnitWeight}kN/m³
内摩擦角 φ：${formData.internalFrictionAngle_phi}°
粘聚力 c：${formData.cohesion_c}kPa

【后背墙参数】
后背墙类型：${getBackWallTypeName()}

───────────────────────────────────────────────────────────────
                           计算依据和公式
───────────────────────────────────────────────────────────────

【规范依据】
1. 《给水排水管道工程施工及验收规范》GB50268-2008
2. 《顶管施工技术及验收规范》CECS246:2008
3. 《混凝土结构设计规范》GB50010-2010
4. 《岩土工程勘察规范》GB50021-2001
5. 《建筑地基基础设计规范》GB50007-2011

【主要计算公式】
1. 总顶推力计算：
   F = F₁ + F₂ + F₃
   式中：F - 总顶推力；F₁ - 管道外壁摩擦阻力；F₂ - 工具管正面阻力；F₃ - 管道接口摩擦阻力

2. 管道外壁摩擦阻力：
   F₁ = π × D × L × f
   式中：D - 管道外径(m)；L - 顶进长度(m)；f - 单位面积摩阻力(kPa)

3. 工具管正面阻力：
   F₂ = π × (Dt²/4) × γ × H × K
   式中：Dt - 工具管外径(m)；γ - 土壤重度(kN/m³)；H - 覆土深度(m)；K - 侧向土压力系数

4. 管道接口摩擦阻力：
   F₃ = μ × F × n
   式中：μ - 接口摩擦系数；F - 轴向压力；n - 接口数量

5. 管道环向应力验算：
   σh = F/(π × D × t)
   式中：σh - 环向应力(MPa)；F - 顶推力(kN)；t - 管壁厚度(m)

6. 管体变形验算：
   S = F × L/(E × A)
   式中：S - 管体变形(mm)；E - 弹性模量(MPa)；A - 管道截面积(m²)

7. 后背墙抗滑移验算：
   K = (W × μ + c × A)/F
   式中：K - 抗滑移安全系数；W - 后背墙自重(kN)；μ - 摩擦系数；c - 粘聚力(kPa)；A - 接触面积(m²)

【计算步骤】
步骤1：根据管道几何参数和土壤条件计算各项阻力
步骤2：计算总顶推力F = F₁ + F₂ + F₃
步骤3：验算管道环向应力是否满足材料强度要求
步骤4：验算管体变形是否在允许范围内
步骤5：验算管道承压能力和后背墙稳定性
步骤6：综合评估施工安全性并提出技术建议

───────────────────────────────────────────────────────────────
                           计算结果
───────────────────────────────────────────────────────────────

【顶推力计算结果】
F₁ 管道外壁摩擦阻力：${results.F1_frictionResistance} kN
F₂ 工具管正面阻力：${results.F2_frontResistance} kN
F₃ 管道接口摩擦阻力：${results.F3_interfaceFriction} kN
总顶推力 F：${results.totalPushForce} kN

【管道强度与变形验算结果】
环向应力验算：${results.sigma_hoopStress} MPa ≤ ${results.pipeTensileStrength} MPa （${results.pipeStrengthOk ? '通过' : '不通过'}）
管体变形验算：${results.S_pipeDeformation} mm ≤ ${results.allowableDeformation} mm （${results.pipeDeformationOk ? '通过' : '不通过'}）

【稳定性综合验算结果】
管道承压能力验算：${results.totalPushForce} kN ≤ ${results.pipeMaxPressureCapacity} kN （${results.pipePressureCheckOk ? '通过' : '不通过'}）
后背墙抗滑移验算：${results.totalPushForce} kN ≤ ${results.backWallTotalResistance} kN （${results.backWallStabilityCheckOk ? '通过' : '不通过'}）

───────────────────────────────────────────────────────────────
                         安全评估报告
───────────────────────────────────────────────────────────────

【${getRoadbedOverallSafetyStatus().title}】
${getRoadbedOverallSafetyStatus().description}

【验算通过情况统计】
管道环向应力验算：${results.pipeStrengthOk ? '✓ 通过' : '✗ 不通过'}
管体变形验算：${results.pipeDeformationOk ? '✓ 通过' : '✗ 不通过'}
管道承压能力验算：${results.pipePressureCheckOk ? '✓ 通过' : '✗ 不通过'}
后背墙抗滑移验算：${results.backWallStabilityCheckOk ? '✓ 通过' : '✗ 不通过'}

【技术建议】
${getRoadbedRecommendations().map((rec, index) => `${index + 1}. ${rec.title}：${rec.content}`).join('\n')}

【评估结论】
${getRoadbedConclusion()}

───────────────────────────────────────────────────────────────
技术支持：吉林省志安科技有限公司
═══════════════════════════════════════════════════════════════
`
}

// 导出PDF报告 - 使用稳健的jsPDF + html2canvas方案
const exportPDFReport = async () => {
  if (!hasResults.value) {
    ElNotification({
      title: '导出失败',
      message: '请先进行计算再导出报告',
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
          <h1 style="font-size: 20px; color: #2c5aa0; margin: 0; font-family: 'Microsoft YaHei', 'SimSun', sans-serif;">路基顶管施工稳定性评估报告</h1>
        </div>
      `
      await addHtmlBlock(headerHtml)
    }

    // 页脚
    const addFooter = async () => {
      const footerHtml = `
        <div style="text-align: center; padding: 10px 0; font-size: 10px; color: #666; font-family: 'Microsoft YaHei', 'SimSun', sans-serif;">
          第 ${pageNumber} 页
        </div>
      `
      await addHtmlBlock(footerHtml)
    }

    // --- 开始构建PDF ---
    await addHeader()
    
    // 模块1: 项目基本信息
    const projectInfoHtml = `
      <h2 style="font-size: 18px; color: #2c5aa0; border-bottom: 1px solid #ddd; padding-bottom: 5px; margin-top: 10px;">项目基本信息</h2>
      <table style="width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 12px;">
        <tr>
          <td style="border: 1px solid #333; padding: 10px; background: #f8f8f8; font-weight: bold; width: 30%;">项目名称</td>
          <td style="border: 1px solid #333; padding: 10px;">${formData.projectName || '路基顶管施工项目'}</td>
        </tr>
        <tr>
          <td style="border: 1px solid #333; padding: 10px; background: #f8f8f8; font-weight: bold;">项目类型</td>
          <td style="border: 1px solid #333; padding: 10px;">路基顶管施工稳定性计算</td>
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
      <h3 style="font-size: 14px; margin: 15px 0 10px 0;">1. 管道与几何参数</h3>
      <table style="width: 100%; border-collapse: collapse; font-size: 12px;">
        <tr>
          <td style="border: 1px solid #333; padding: 8px; background: #f8f8f8;">管道外径 D</td><td style="border: 1px solid #333; padding: 8px;">${formData.pipeOuterDiameter} m</td>
          <td style="border: 1px solid #333; padding: 8px; background: #f8f8f8;">工具管外径 Dt</td><td style="border: 1px solid #333; padding: 8px;">${formData.toolPipeOuterDiameter_Dt} m</td>
        </tr>
        <tr>
          <td style="border: 1px solid #333; padding: 8px; background: #f8f8f8;">管壁厚度 t</td><td style="border: 1px solid #333; padding: 8px;">${formData.pipeThickness} m</td>
          <td style="border: 1px solid #333; padding: 8px; background: #f8f8f8;">单段顶进长度 L</td><td style="border: 1px solid #333; padding: 8px;">${formData.pushLength} m</td>
        </tr>
         <tr>
          <td style="border: 1px solid #333; padding: 8px; background: #f8f8f8;">管顶覆土深度 H</td><td style="border: 1px solid #333; padding: 8px;">${formData.coverDepth} m</td>
          <td style="border: 1px solid #333; padding: 8px; background: #f8f8f8;"></td><td style="border: 1px solid #333; padding: 8px;"></td>
        </tr>
      </table>
      <h3 style="font-size: 14px; margin: 15px 0 10px 0;">2. 土质参数</h3>
      <table style="width: 100%; border-collapse: collapse; font-size: 12px;">
        <tr>
          <td style="border: 1px solid #333; padding: 8px; background: #f8f8f8;">土体重度 γ</td><td style="border: 1px solid #333; padding: 8px;">${formData.soilUnitWeight} kN/m³</td>
          <td style="border: 1px solid #333; padding: 8px; background: #f8f8f8;">内摩擦角 φ</td><td style="border: 1px solid #333; padding: 8px;">${formData.internalFrictionAngle_phi}°</td>
        </tr>
        <tr>
          <td style="border: 1px solid #333; padding: 8px; background: #f8f8f8;">黏聚力 c</td><td style="border: 1px solid #333; padding: 8px;">${formData.cohesion_c} kPa</td>
          <td style="border: 1px solid #333; padding: 8px; background: #f8f8f8;"></td><td style="border: 1px solid #333; padding: 8px;"></td>
        </tr>
      </table>
    `
    await addHtmlBlock(conditionsHtml)

    // 模块3: 计算过程与公式 - 分解为多个子模块
    
    // 3.1 第二部分标题
    const formulasTitleHtml = `
      <h2 style="font-size: 18px; color: #2c5aa0; border-bottom: 1px solid #ddd; padding-bottom: 5px;">二、计算过程与公式</h2>
    `
    await addHtmlBlock(formulasTitleHtml)
    
    // 3.2 顶推力计算 - 总标题
    const pushForceMainTitleHtml = `
      <h3 style="font-size: 14px; margin: 15px 0 10px 0;">1. 顶推力计算</h3>
    `
    await addHtmlBlock(pushForceMainTitleHtml)
    
    // 3.3 管道外壁摩擦阻力 F₁
    const f1Html = `
      <div style="font-size: 12px;">
        <h4 style="font-size: 13px; margin: 10px 0 5px 0; color: #2c5aa0;">1.1 管道外壁摩擦阻力 F₁</h4>
        <p style="margin: 5px 0; padding: 8px; background: #f8f9fa; border-left: 3px solid #2c5aa0;">
          <strong>计算公式：</strong> F₁ = π × D × L × f<br>
          <strong>参数说明：</strong><br>
          • D = 管道外径 = ${formData.pipeOuterDiameter} m<br>
          • L = 单段顶进长度 = ${formData.pushLength} m<br>
          • f = 管道外壁与土体间摩擦系数 = ${formData.friction_f}<br>
          <strong>计算过程：</strong><br>
          F₁ = π × ${formData.pipeOuterDiameter} × ${formData.pushLength} × ${formData.friction_f}<br>
          F₁ = ${(Math.PI * formData.pipeOuterDiameter * formData.pushLength * formData.friction_f).toFixed(2)} kN<br>
          <strong>计算结果：</strong> F₁ = ${results.F1_frictionResistance} kN
        </p>
      </div>
    `
    await addHtmlBlock(f1Html)
    
    // 3.4 工具管正面阻力 F₂
    const f2Html = `
      <div style="font-size: 12px;">
        <h4 style="font-size: 13px; margin: 10px 0 5px 0; color: #2c5aa0;">1.2 工具管正面阻力 F₂</h4>
        <p style="margin: 5px 0; padding: 8px; background: #f8f9fa; border-left: 3px solid #2c5aa0;">
          <strong>计算公式：</strong> F₂ = π × (Dt²/4) × γ × H × K<br>
          <strong>参数说明：</strong><br>
          • Dt = 工具管外径 = ${formData.toolPipeOuterDiameter_Dt} m<br>
          • γ = 土体重度 = ${formData.soilUnitWeight} kN/m³<br>
          • H = 管顶覆土深度 = ${formData.coverDepth} m<br>
          • K = 安全系数 = ${formData.safetyFactor_K}<br>
          <strong>计算过程：</strong><br>
          F₂ = π × (${formData.toolPipeOuterDiameter_Dt}²/4) × ${formData.soilUnitWeight} × ${formData.coverDepth} × ${formData.safetyFactor_K}<br>
          F₂ = π × ${(Math.pow(formData.toolPipeOuterDiameter_Dt, 2)/4).toFixed(4)} × ${formData.soilUnitWeight} × ${formData.coverDepth} × ${formData.safetyFactor_K}<br>
          F₂ = ${(Math.PI * Math.pow(formData.toolPipeOuterDiameter_Dt, 2)/4 * formData.soilUnitWeight * formData.coverDepth * formData.safetyFactor_K).toFixed(2)} kN<br>
          <strong>计算结果：</strong> F₂ = ${results.F2_frontResistance} kN
        </p>
      </div>
    `
    await addHtmlBlock(f2Html)
    
    // 3.5 接口摩擦阻力 F₃
    const f3Html = `
      <div style="font-size: 12px;">
        <h4 style="font-size: 13px; margin: 10px 0 5px 0; color: #2c5aa0;">1.3 接口摩擦阻力 F₃</h4>
        <p style="margin: 5px 0; padding: 8px; background: #f8f9fa; border-left: 3px solid #2c5aa0;">
          <strong>计算公式：</strong> F₃ = π × D × t × f₃ × n<br>
          <strong>参数说明：</strong><br>
          • D = 管道外径 = ${formData.pipeOuterDiameter} m<br>
          • t = 接口厚度 = ${formData.interfaceThickness || 0.05} m<br>
          • f₃ = 接口摩擦系数 = ${formData.interfaceFriction_f3 || 0.3}<br>
          • n = 接口数量 = ${Math.ceil(formData.pushLength / 2) || 1} 个<br>
          <strong>计算结果：</strong> F₃ = ${results.F3_interfaceFriction} kN
        </p>
      </div>
    `
    await addHtmlBlock(f3Html)
    
    // 3.6 总顶推力计算
    const totalForceHtml = `
      <div style="font-size: 12px;">
        <h4 style="font-size: 13px; margin: 10px 0 5px 0; color: #007bff;">1.4 总顶推力计算</h4>
        <p style="margin: 5px 0; padding: 8px; background: #e7f3ff; border-left: 3px solid #007bff;">
          <strong>计算公式：</strong> F = F₁ + F₂ + F₃<br>
          <strong>计算过程：</strong><br>
          F = ${results.F1_frictionResistance} + ${results.F2_frontResistance} + ${results.F3_interfaceFriction}<br>
          <strong>最终结果：</strong> F = ${results.totalPushForce} kN
        </p>
      </div>
    `
    await addHtmlBlock(totalForceHtml)
    
    // 3.7 管道强度验算 - 总标题
    const strengthMainTitleHtml = `
      <h3 style="font-size: 14px; margin: 20px 0 10px 0;">2. 管道强度验算</h3>
    `
    await addHtmlBlock(strengthMainTitleHtml)
    
    // 3.8 环向应力验算
    const hoopStressHtml = `
      <div style="font-size: 12px;">
        <h4 style="font-size: 13px; margin: 10px 0 5px 0; color: #2c5aa0;">2.1 环向应力验算</h4>
        <p style="margin: 5px 0; padding: 8px; background: #f8f9fa; border-left: 3px solid #2c5aa0;">
          <strong>计算公式：</strong> σ = F / (π × D × t)<br>
          <strong>参数说明：</strong><br>
          • F = 总顶推力 = ${results.totalPushForce} kN<br>
          • D = 管道外径 = ${formData.pipeOuterDiameter} m<br>
          • t = 管壁厚度 = ${formData.pipeThickness} m<br>
          <strong>计算过程：</strong><br>
          σ = ${results.totalPushForce} / (π × ${formData.pipeOuterDiameter} × ${formData.pipeThickness})<br>
          σ = ${results.totalPushForce} / ${(Math.PI * formData.pipeOuterDiameter * formData.pipeThickness).toFixed(4)}<br>
          <strong>计算结果：</strong> σ = ${results.sigma_hoopStress} MPa<br>
          <strong>验算条件：</strong> σ ≤ [σ] = ${results.pipeTensileStrength} MPa<br>
          <strong>验算结论：</strong> ${results.pipeStrengthOk ? '满足要求' : '不满足要求'}
        </p>
      </div>
    `
    await addHtmlBlock(hoopStressHtml)
    
    // 3.9 管体变形验算
    const deformationHtml = `
      <div style="font-size: 12px;">
        <h4 style="font-size: 13px; margin: 10px 0 5px 0; color: #2c5aa0;">2.2 管体变形验算</h4>
        <p style="margin: 5px 0; padding: 8px; background: #f8f9fa; border-left: 3px solid #2c5aa0;">
          <strong>计算公式：</strong> S = (F × L) / (E × A)<br>
          <strong>参数说明：</strong><br>
          • F = 总顶推力 = ${results.totalPushForce} kN<br>
          • L = 顶进长度 = ${formData.pushLength} m<br>
          • E = 管材弹性模量 = ${formData.pipeElasticModulus_E || 200000} MPa<br>
          • A = 管道截面积 = π×(D²-(D-2t)²)/4 = ${(Math.PI * (Math.pow(formData.pipeOuterDiameter, 2) - Math.pow(formData.pipeOuterDiameter - 2*formData.pipeThickness, 2)) / 4).toFixed(6)} m²<br>
          <strong>计算结果：</strong> S = ${results.S_pipeDeformation} mm<br>
          <strong>验算条件：</strong> S ≤ [S] = ${results.allowableDeformation} mm<br>
          <strong>验算结论：</strong> ${results.pipeDeformationOk ? '满足要求' : '不满足要求'}
        </p>
      </div>
    `
    await addHtmlBlock(deformationHtml)
    
    // 3.10 稳定性综合验算 - 总标题
    const stabilityMainTitleHtml = `
      <h3 style="font-size: 14px; margin: 20px 0 10px 0;">3. 稳定性综合验算</h3>
    `
    await addHtmlBlock(stabilityMainTitleHtml)
    
    // 3.11 管道承压能力验算
    const pressureCapacityHtml = `
      <div style="font-size: 12px;">
        <h4 style="font-size: 13px; margin: 10px 0 5px 0; color: #2c5aa0;">3.1 管道承压能力验算</h4>
        <p style="margin: 5px 0; padding: 8px; background: #f8f9fa; border-left: 3px solid #2c5aa0;">
          <strong>验算条件：</strong> F ≤ F_max<br>
          <strong>计算值：</strong> F = ${results.totalPushForce} kN<br>
          <strong>允许值：</strong> F_max = ${results.pipeMaxPressureCapacity} kN<br>
          <strong>验算结论：</strong> ${results.pipePressureCheckOk ? '通过' : '不通过'}
        </p>
      </div>
    `
    await addHtmlBlock(pressureCapacityHtml)
    
    // 3.12 后背墙抗滑移验算
    const backWallStabilityHtml = `
      <div style="font-size: 12px;">
        <h4 style="font-size: 13px; margin: 10px 0 5px 0; color: #2c5aa0;">3.2 后背墙抗滑移验算</h4>
        <p style="margin: 5px 0; padding: 8px; background: #f8f9fa; border-left: 3px solid #2c5aa0;">
          <strong>验算条件：</strong> F ≤ R_total<br>
          <strong>顶推力：</strong> F = ${results.totalPushForce} kN<br>
          <strong>总阻力：</strong> R_total = ${results.backWallTotalResistance} kN<br>
          <strong>安全系数：</strong> K = R_total / F = ${(results.backWallTotalResistance / results.totalPushForce).toFixed(2)}<br>
          <strong>验算结论：</strong> ${results.backWallStabilityCheckOk ? '通过' : '不通过'}
        </p>
      </div>
    `
    await addHtmlBlock(backWallStabilityHtml)

    // 模块4: 验算结果
    const resultsHtml = `
      <h2 style="font-size: 18px; color: #2c5aa0; border-bottom: 1px solid #ddd; padding-bottom: 5px;">三、验算结果</h2>
      <table style="width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 12px;">
        <tr style="background: #f0f0f0;">
          <th style="border: 1px solid #333; padding: 10px; text-align: center;">验算项目</th>
          <th style="border: 1px solid #333; padding: 10px; text-align: center;">计算值</th>
          <th style="border: 1px solid #333; padding: 10px; text-align: center;">允许值</th>
          <th style="border: 1px solid #333; padding: 10px; text-align: center;">验算结果</th>
        </tr>
        <tr>
          <td style="border: 1px solid #333; padding: 10px;">环向应力验算</td><td style="border: 1px solid #333; padding: 10px;">${results.sigma_hoopStress} MPa</td><td style="border: 1px solid #333; padding: 10px;">${results.pipeTensileStrength} MPa</td><td style="border: 1px solid #333; padding: 10px; color: ${results.pipeStrengthOk ? '#198754' : '#dc3545'};">${results.pipeStrengthOk ? '通过' : '不通过'}</td>
        </tr>
        <tr>
          <td style="border: 1px solid #333; padding: 10px;">管体变形验算</td><td style="border: 1px solid #333; padding: 10px;">${results.S_pipeDeformation} mm</td><td style="border: 1px solid #333; padding: 10px;">${results.allowableDeformation} mm</td><td style="border: 1px solid #333; padding: 10px; color: ${results.pipeDeformationOk ? '#198754' : '#dc3545'};">${results.pipeDeformationOk ? '通过' : '不通过'}</td>
        </tr>
        <tr>
          <td style="border: 1px solid #333; padding: 10px;">管道承压能力验算</td><td style="border: 1px solid #333; padding: 10px;">${results.totalPushForce} kN</td><td style="border: 1px solid #333; padding: 10px;">${results.pipeMaxPressureCapacity} kN</td><td style="border: 1px solid #333; padding: 10px; color: ${results.pipePressureCheckOk ? '#198754' : '#dc3545'};">${results.pipePressureCheckOk ? '通过' : '不通过'}</td>
        </tr>
        <tr>
          <td style="border: 1px solid #333; padding: 10px;">后背墙抗滑移验算</td><td style="border: 1px solid #333; padding: 10px;">${results.totalPushForce} kN</td><td style="border: 1px solid #333; padding: 10px;">${results.backWallTotalResistance} kN</td><td style="border: 1px solid #333; padding: 10px; color: ${results.backWallStabilityCheckOk ? '#198754' : '#dc3545'};">${results.backWallStabilityCheckOk ? '通过' : '不通过'}</td>
        </tr>
      </table>
    `
    await addHtmlBlock(resultsHtml)

    // 模块5: 安全评估与建议
    const assessmentHtml = `
      <h2 style="font-size: 18px; color: #2c5aa0; border-bottom: 1px solid #ddd; padding-bottom: 5px;">四、安全评估与建议</h2>
      <div style="background: #f8f9fa; border-left: 4px solid #2c5aa0; padding: 15px; margin: 15px 0; font-size: 12px;">
        <h3 style="font-size: 14px; margin: 0 0 10px 0;">整体安全状况评估</h3>
        <p style="margin: 0;">${getRoadbedOverallSafetyStatus().description}</p>
      </div>
      <div style="background: #e7f3ff; border-left: 4px solid #007bff; padding: 15px; margin: 15px 0; font-size: 12px;">
        <h3 style="font-size: 14px; margin: 0 0 10px 0;">评估结论</h3>
        <p style="margin: 0;">${getRoadbedConclusion()}</p>
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
    
    // 保存PDF
    pdf.save(`路基顶管施工稳定性评估报告_${getCurrentDate().replace(/\//g, '')}.pdf`)
    
    ElNotification({
      title: '导出成功',
      message: 'PDF报告已成功导出，包含完整的计算过程和公式',
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

// 生成完整的HTML报告内容
const generateFullReportHTML = () => {
  const safetyStatus = getRoadbedOverallSafetyStatus()
  const recommendations = getRoadbedRecommendations()
  const conclusion = getRoadbedConclusion()
  
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
        <div class="report-title">路基顶管施工稳定性评估报告</div>
        <div class="company-name">吉林省志安科技有限公司</div>
      </div>
      
      <!-- 项目基本信息 -->
      <div class="section">
        <div class="section-title">项目基本信息</div>
        <table class="info-table">
          <tr>
            <td class="label-cell">项目名称</td>
            <td>${formData.projectName || '路基顶管施工项目'}</td>
          </tr>
          <tr>
            <td class="label-cell">项目类型</td>
            <td>路基顶管施工稳定性计算</td>
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
        
        <div class="subsection-title">1. 管道与几何参数</div>
        <table class="info-table">
          <tr><td class="label-cell">管道外径 D</td><td>${formData.pipeOuterDiameter} m</td></tr>
          <tr><td class="label-cell">工具管外径 Dt</td><td>${formData.toolPipeOuterDiameter_Dt} m</td></tr>
          <tr><td class="label-cell">管壁厚度 t</td><td>${formData.pipeThickness} m</td></tr>
          <tr><td class="label-cell">单段顶进长度 L</td><td>${formData.pushLength} m</td></tr>
          <tr><td class="label-cell">管顶覆土深度 H</td><td>${formData.coverDepth} m</td></tr>
        </table>
        
        <div class="subsection-title">2. 材料与施工参数</div>
        <table class="info-table">
          <tr><td class="label-cell">管道材料</td><td>${getPipeMaterialName()}</td></tr>
          <tr><td class="label-cell">工具管类型</td><td>${getToolPipeTypeName()}</td></tr>
          <tr><td class="label-cell">单位面积摩阻力 f</td><td>${formData.friction_f} kPa</td></tr>
          <tr><td class="label-cell">混凝土抗压强度 fc</td><td>${formData.concreteCompressiveStrength_fc} MPa</td></tr>
          <tr><td class="label-cell">稳定系数 φ</td><td>${formData.stabilityFactor_phi}</td></tr>
          <tr><td class="label-cell">安全系数 K</td><td>${formData.safetyFactor_K}</td></tr>
        </table>
        
        <div class="subsection-title">3. 土质参数</div>
        <table class="info-table">
          <tr><td class="label-cell">土体重度 γ</td><td>${formData.soilUnitWeight} kN/m³</td></tr>
          <tr><td class="label-cell">内摩擦角 φ</td><td>${formData.internalFrictionAngle_phi}°</td></tr>
          <tr><td class="label-cell">黏聚力 c</td><td>${formData.cohesion_c} kPa</td></tr>
          <tr><td class="label-cell">土体反力模量 E'</td><td>${formData.soilReactionModulus_E_prime} MPa</td></tr>
        </table>
        
        <div class="subsection-title">4. 后背墙参数</div>
        <table class="info-table">
          <tr><td class="label-cell">后背墙类型</td><td>${getBackWallTypeName()}</td></tr>
        </table>
      </div>
      
      <!-- 分页 -->
      <div class="page-break"></div>
      
      <!-- 计算结果 -->
      <div class="section">
        <div class="section-title">二、计算结果</div>
        
        <div class="subsection-title">1. 顶推力计算结果</div>
        <table class="info-table">
          <tr>
            <th>计算项目</th>
            <th>计算结果</th>
            <th>单位</th>
          </tr>
          <tr>
            <td>F₁ 管道外壁摩擦阻力</td>
            <td>${results.F1_frictionResistance}</td>
            <td>kN</td>
          </tr>
          <tr>
            <td>F₂ 工具管正面阻力</td>
            <td>${results.F2_frontResistance}</td>
            <td>kN</td>
          </tr>
          <tr>
            <td>F₃ 管道接口摩擦阻力</td>
            <td>${results.F3_interfaceFriction}</td>
            <td>kN</td>
          </tr>
          <tr style="background: #f0f9ff;">
            <td><strong>总顶推力 F</strong></td>
            <td><strong>${results.totalPushForce}</strong></td>
            <td><strong>kN</strong></td>
          </tr>
        </table>
        
        <div class="subsection-title">2. 管道强度与变形验算结果</div>
        <table class="info-table">
          <tr>
            <th>验算项目</th>
            <th>计算值</th>
            <th>允许值</th>
            <th>验算结果</th>
          </tr>
          <tr>
            <td>环向应力验算</td>
            <td>${results.sigma_hoopStress} MPa</td>
            <td>${results.pipeTensileStrength} MPa</td>
            <td class="${results.pipeStrengthOk ? 'result-pass' : 'result-fail'}">${results.pipeStrengthOk ? '通过' : '不通过'}</td>
          </tr>
          <tr>
            <td>管体变形验算</td>
            <td>${results.S_pipeDeformation} mm</td>
            <td>${results.allowableDeformation} mm</td>
            <td class="${results.pipeDeformationOk ? 'result-pass' : 'result-fail'}">${results.pipeDeformationOk ? '通过' : '不通过'}</td>
          </tr>
        </table>
        
        <div class="subsection-title">3. 稳定性综合验算结果</div>
        <table class="info-table">
          <tr>
            <th>验算项目</th>
            <th>作用力</th>
            <th>抗力</th>
            <th>验算结果</th>
          </tr>
          <tr>
            <td>管道承压能力验算</td>
            <td>${results.totalPushForce} kN</td>
            <td>${results.pipeMaxPressureCapacity} kN</td>
            <td class="${results.pipePressureCheckOk ? 'result-pass' : 'result-fail'}">${results.pipePressureCheckOk ? '通过' : '不通过'}</td>
          </tr>
          <tr>
            <td>后背墙抗滑移验算</td>
            <td>${results.totalPushForce} kN</td>
            <td>${results.backWallTotalResistance} kN</td>
            <td class="${results.backWallStabilityCheckOk ? 'result-pass' : 'result-fail'}">${results.backWallStabilityCheckOk ? '通过' : '不通过'}</td>
          </tr>
        </table>
      </div>
      
      <!-- 分页 -->
      <div class="page-break"></div>
      
      <!-- 安全评估报告 -->
      <div class="section">
        <div class="section-title">三、安全评估报告</div>
        
        <div class="assessment-box">
          <div class="subsection-title">${safetyStatus.title}</div>
          <p>${safetyStatus.description}</p>
        </div>
        
        <div class="subsection-title">验算通过情况统计</div>
        <ul>
          <li>管道环向应力验算：<span class="${results.pipeStrengthOk ? 'result-pass' : 'result-fail'}">${results.pipeStrengthOk ? '✓ 通过' : '✗ 不通过'}</span></li>
          <li>管体变形验算：<span class="${results.pipeDeformationOk ? 'result-pass' : 'result-fail'}">${results.pipeDeformationOk ? '✓ 通过' : '✗ 不通过'}</span></li>
          <li>管道承压能力验算：<span class="${results.pipePressureCheckOk ? 'result-pass' : 'result-fail'}">${results.pipePressureCheckOk ? '✓ 通过' : '✗ 不通过'}</span></li>
          <li>后背墙抗滑移验算：<span class="${results.backWallStabilityCheckOk ? 'result-pass' : 'result-fail'}">${results.backWallStabilityCheckOk ? '✓ 通过' : '✗ 不通过'}</span></li>
        </ul>
        
        <div class="subsection-title">技术建议</div>
        <ul>
          <li><strong>施工监测：</strong>建议在施工过程中加强变形监测，及时调整施工参数以确保安全。</li>
          <li><strong>应急预案：</strong>制定详细的应急预案，包括顶进困难、管道变形等突发情况的处理措施。</li>
        </ul>
        
        <div class="subsection-title">评估结论</div>
        <div class="assessment-box">
          <p>综合评估认为，当前顶管施工方案技术可行，建议按照设计参数进行施工，并在施工过程中严格控制质量，确保工程安全顺利完成。</p>
        </div>
      </div>
      
      <!-- 报告页脚 -->
      <div style="margin-top: 40px; border-top: 1px solid #ddd; padding-top: 20px; text-align: center; font-size: 10px; color: #666;">
        <p>技术支持：吉林省志安科技有限公司</p>
        <p style="margin: 5px 0;">报告生成日期：${getCurrentDateTime()}</p>
      </div>
    </body>
    </html>
  `
}

// 添加报告封面页
const addReportCoverPage = async (pdf, margin, contentWidth, contentHeight) => {
  const pageNumber = 1
  
  // 设置中文字体
  setupChineseFont(pdf)
  
  // 公司LOGO和标题区域
  pdf.setFontSize(18)
  pdf.setTextColor(44, 90, 160)
  const title = '路基顶管施工稳定性评估报告'
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
    ['项目名称', formData.projectName || '路基顶管施工项目'],
    ['项目类型', '路基顶管施工稳定性计算'],
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
    `管道外径：${formData.pipeOuterDiameter}m`,
    `管壁厚度：${formData.pipeThickness}m`,
    `顶进长度：${formData.pushLength}m`,
    `覆土深度：${formData.coverDepth}m`,
    `管道材料：${getPipeMaterialName()}`,
    `后背墙类型：${getBackWallTypeName()}`
  ]
  
  keyParams.forEach((param, index) => {
    if (index % 2 === 0) {
      pdf.text('• ' + param, margin, yPos + Math.floor(index / 2) * 8)
    } else {
      pdf.text('• ' + param, margin + contentWidth / 2, yPos + Math.floor(index / 2) * 8)
    }
  })
  
  // 添加页脚
  addPageFooter(pdf, pageNumber, 4)
}

// 添加计算条件和依据页
const addCalculationConditionsPage = async (pdf, margin, contentWidth, contentHeight) => {
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
    '《给水排水管道工程施工及验收规范》GB50268-2008',
    '《顶管施工技术及验收规范》CECS246:2008',
    '《混凝土结构设计规范》GB50010-2010',
    '《岩土工程勘察规范》GB50021-2001',
    '《建筑地基基础设计规范》GB50007-2011'
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
      title: '总顶推力计算',
      formula: 'F = K(F₁ + F₂ + F₃)',
      desc: 'F-总顶推力; F₁-管道外壁摩擦阻力; F₂-工具管正面阻力; F₃-管道接口摩擦阻力'
    },
    {
      title: '管道外壁摩擦阻力',
      formula: 'F₁ = π × D × L × f',
      desc: 'D-管道外径(m); L-顶进长度(m); f-单位面积摩阻力(kPa)'
    },
    {
      title: '工具管正面阻力',
      formula: 'F₂ = π × (Dt²/4) × P',
      desc: 'Dt-工具管外径(m); P-正面土压力(kPa)'
    },
    {
      title: '管道环向应力验算',
      formula: 'σ = (Pv + q) × D / (2t)',
      desc: 'σ-环向应力(MPa); Pv-垂直土压力; q-车辆活载; t-管壁厚度'
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
  if (yPos + 60 < contentHeight + margin) {
    pdf.setFont('helvetica', 'bold')
    pdf.setFontSize(12)
    pdf.text('3. 详细计算参数', margin, yPos)
    yPos += 10
    
    // 创建参数表格
    const paramData = [
      ['参数名称', '数值', '单位'],
      ['管道外径 D', formData.pipeOuterDiameter.toString(), 'm'],
      ['管壁厚度 t', formData.pipeThickness.toString(), 'm'],
      ['顶进长度 L', formData.pushLength.toString(), 'm'],
      ['覆土深度 H', formData.coverDepth.toString(), 'm'],
      ['土壤重度 γ', formData.soilUnitWeight.toString(), 'kN/m³'],
      ['内摩擦角 φ', formData.internalFrictionAngle_phi.toString(), '°'],
      ['粘聚力 c', formData.cohesion_c.toString(), 'kPa']
    ]
    
    drawTable(pdf, paramData, margin, yPos, contentWidth, 8)
  }
  
  addPageFooter(pdf, pageNumber, 4)
}

// 添加计算结果页
const addCalculationResultsPage = async (pdf, margin, contentWidth, contentHeight) => {
  const pageNumber = 3
  let yPos = margin + 10
  
  // 页面标题
  pdf.setFont('helvetica', 'bold')
  pdf.setFontSize(16)
  pdf.setTextColor(44, 90, 160)
  pdf.text('计算结果', margin, yPos)
  yPos += 15
  
  // 顶推力计算结果
  pdf.setFont('helvetica', 'bold')
  pdf.setFontSize(12)
  pdf.setTextColor(0, 0, 0)
  pdf.text('1. 顶推力计算结果', margin, yPos)
  yPos += 10
  
  const forceData = [
    ['计算项目', '计算结果', '单位'],
    ['F₁ 管道外壁摩擦阻力', results.F1_frictionResistance, 'kN'],
    ['F₂ 工具管正面阻力', results.F2_frontResistance, 'kN'],
    ['F₃ 管道接口摩擦阻力', results.F3_interfaceFriction, 'kN'],
    ['总顶推力 F', results.totalPushForce, 'kN']
  ]
  
  const tableHeight = drawTable(pdf, forceData, margin, yPos, contentWidth, 8)
  yPos += tableHeight + 15
  
  // 强度与变形验算结果
  pdf.setFont('helvetica', 'bold')
  pdf.setFontSize(12)
  pdf.text('2. 管道强度与变形验算结果', margin, yPos)
  yPos += 10
  
  const strengthData = [
    ['验算项目', '计算值', '允许值', '验算结果'],
    ['环向应力验算', `${results.sigma_hoopStress} MPa`, `${results.pipeTensileStrength} MPa`, results.pipeStrengthOk ? '通过' : '不通过'],
    ['管体变形验算', `${results.S_pipeDeformation} mm`, `${results.allowableDeformation} mm`, results.pipeDeformationOk ? '通过' : '不通过']
  ]
  
  const tableHeight2 = drawTable(pdf, strengthData, margin, yPos, contentWidth, 8)
  yPos += tableHeight2 + 15
  
  // 稳定性综合验算结果
  pdf.setFont('helvetica', 'bold')
  pdf.setFontSize(12)
  pdf.text('3. 稳定性综合验算结果', margin, yPos)
  yPos += 10
  
  const stabilityData = [
    ['验算项目', '作用力', '抗力', '验算结果'],
    ['管道承压能力验算', `${results.totalPushForce} kN`, `${results.pipeMaxPressureCapacity} kN`, results.pipePressureCheckOk ? '通过' : '不通过'],
    ['后背墙抗滑移验算', `${results.totalPushForce} kN`, `${results.backWallTotalResistance} kN`, results.backWallStabilityCheckOk ? '通过' : '不通过']
  ]
  
  drawTable(pdf, stabilityData, margin, yPos, contentWidth, 8)
  
  addPageFooter(pdf, pageNumber, 4)
}

// 添加安全评估报告页
const addSafetyAssessmentPage = async (pdf, margin, contentWidth, contentHeight) => {
  const pageNumber = 4
  let yPos = margin + 10
  
  // 页面标题
  pdf.setFont('helvetica', 'bold')
  pdf.setFontSize(16)
  pdf.setTextColor(44, 90, 160)
  pdf.text('安全评估报告', margin, yPos)
  yPos += 15
  
  // 整体安全状况
  const safetyStatus = getRoadbedOverallSafetyStatus()
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
    `• 管道环向应力验算：${results.pipeStrengthOk ? '✓ 通过' : '✗ 不通过'}`,
    `• 管体变形验算：${results.pipeDeformationOk ? '✓ 通过' : '✗ 不通过'}`,
    `• 管道承压能力验算：${results.pipePressureCheckOk ? '✓ 通过' : '✗ 不通过'}`,
    `• 后背墙抗滑移验算：${results.backWallStabilityCheckOk ? '✓ 通过' : '✗ 不通过'}`
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
  const recommendations = getRoadbedRecommendations()
  
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
    const conclusion = getRoadbedConclusion()
    const wrappedConclusion = pdf.splitTextToSize(conclusion, contentWidth)
    
    // 结论背景框
    pdf.setFillColor(248, 249, 250)
    pdf.rect(margin, yPos - 3, contentWidth, wrappedConclusion.length * 5 + 6, 'F')
    pdf.setDrawColor(44, 90, 160)
    pdf.rect(margin, yPos - 3, contentWidth, wrappedConclusion.length * 5 + 6)
    
    pdf.text(wrappedConclusion, margin + 3, yPos + 2)
  }
  
  addPageFooter(pdf, pageNumber, 4)
}

// 绘制表格的辅助函数
const drawTable = (pdf, data, x, y, width, rowHeight) => {
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

// 添加页脚的辅助函数
const addPageFooter = (pdf, pageNumber, totalPages) => {
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
</script>

<style scoped>
:root {
  --roadbed-primary: #409eff;
  --bg-card: rgba(17, 24, 39, 0.8);
  --bg-section: rgba(31, 41, 55, 0.6);
  --bg-input: rgba(31, 41, 55, 0.9);
  --vt-c-text-dark-1: #e5e7eb;
  --vt-c-text-dark-2: #9ca3af;
  --vt-c-text-numeric: #67e8f9;
}

.roadbed-calculation-view {
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
.calculation-form :deep(.el-input-number__input),
.calculation-form :deep(.el-select__text) {
  color: var(--text-primary) !important;
  font-weight: 500;
}

/* 确保下拉框内部的文字颜色也是正确的 */
.calculation-form :deep(.el-select .el-input__inner) {
    color: var(--text-primary) !important;
}

.calculation-form :deep(.el-input-group__append) {
  background-color: var(--bg-input);
  box-shadow: none;
}

.calculation-form :deep(.el-input__wrapper:hover),
.calculation-form :deep(.el-input-number:hover),
.calculation-form :deep(.el-select__wrapper:hover) {
  border-color: var(--brand-primary);
}

.calculation-form :deep(.el-input__wrapper.is-focus),
.calculation-form :deep(.el-input-number.is-focus),
.calculation-form :deep(.el-select__wrapper.is-focus) {
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
  margin-bottom: 20px;
}

.result-tabs :deep(.el-tabs__item) {
  color: var(--text-secondary);
  font-size: 1rem;
  padding: 0 24px;
  height: 48px;
  line-height: 48px;
  font-weight: 500;
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

.result-descriptions {
  margin-top: 20px;
}

.result-descriptions :deep(.el-descriptions__header) {
  margin-bottom: 16px;
}

.result-descriptions :deep(.el-descriptions__title) {
  color: var(--text-primary);
  font-size: 1.125rem;
}

.result-descriptions :deep(.el-descriptions__cell) {
  background-color: transparent !important;
  border-color: var(--el-border-color) !important;
}

.result-descriptions :deep(.el-descriptions__label) {
  color: var(--text-secondary) !important;
  font-weight: 500;
  background-color: var(--bg-section) !important;
}

.result-descriptions :deep(.el-descriptions__content) {
  color: var(--text-primary);
}

.highlight-value {
  color: var(--brand-primary);
  font-weight: 600;
  font-size: 1.125rem;
}

.numeric-value {
  color: var(--text-secondary);
  font-weight: 500;
}

.empty-result {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  color: var(--vt-c-text-dark-2);
}

.calculation-form :deep(.el-radio-button__inner) {
  background-color: var(--bg-input);
  color: var(--text-primary);
  border-color: var(--el-border-color);
}
.calculation-form :deep(.el-radio-button__original-radio:checked+.el-radio-button__inner) {
    background-color: var(--brand-primary);
    border-color: var(--brand-primary);
    color: var(--text-on-primary);
    box-shadow: -1px 0 0 0 var(--brand-primary);
  }

/* 安全评估报告专用样式 */
.safety-report {
  padding: 0;
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 16px 20px;
  background: linear-gradient(135deg, var(--brand-primary), var(--brand-accent));
  border-radius: 8px;
  color: white;
}

.report-header h3 {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  color: #ffffff !important;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.export-buttons {
  display: flex;
  gap: 8px;
}

.export-buttons .el-button {
  border-color: rgba(255, 255, 255, 0.3) !important;
  background-color: rgba(255, 255, 255, 0.1) !important;
  color: #ffffff !important;
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);
}

.export-buttons .el-button:hover {
  background-color: rgba(255, 255, 255, 0.2) !important;
  border-color: rgba(255, 255, 255, 0.5) !important;
}

.report-content {
  padding: 0 4px;
}

.assessment-summary {
  background: var(--bg-card);
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 24px;
  border: 1px solid var(--el-border-color-lighter);
}

.assessment-summary h4 {
  margin: 0 0 12px 0;
  color: var(--brand-primary);
  font-size: 1.1rem;
  font-weight: 600;
}

.assessment-summary p {
  margin: 0;
  line-height: 1.6;
  color: var(--text-secondary);
}

.verification-results {
  margin-bottom: 24px;
}

.verification-results h4 {
  margin: 0 0 16px 0;
  color: var(--text-primary);
  font-size: 1.1rem;
  font-weight: 600;
}

.verification-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
}

.verification-item {
  background: var(--bg-card);
  border: 2px solid var(--el-border-color-lighter);
  border-radius: 8px;
  padding: 16px;
  transition: all 0.2s ease;
}

.verification-item:hover {
  box-shadow: var(--el-box-shadow-light);
}

.verification-item.verification-pass {
  border-color: #67c23a;
  background: linear-gradient(135deg, #f0f9ff 0%, #ecfdf5 100%);
}

.verification-item.verification-fail {
  border-color: #f56c6c;
  background: linear-gradient(135deg, #fef2f2 0%, #fdf2f8 100%);
}

.verification-title {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
  font-size: 0.95rem;
}

.verification-result {
  font-weight: 700;
  margin-bottom: 6px;
  font-size: 1rem;
}

.verification-pass .verification-result {
  color: #67c23a;
}

.verification-fail .verification-result {
  color: #f56c6c;
}

.verification-detail {
  font-size: 0.85rem;
  color: var(--text-secondary);
  font-family: 'Courier New', monospace;
}

.recommendations {
  margin-bottom: 24px;
}

.recommendations h4 {
  margin: 0 0 16px 0;
  color: var(--text-primary);
  font-size: 1.1rem;
  font-weight: 600;
}

.recommendation-list {
  display: flex;
    flex-direction: column;
  gap: 12px;
}

.recommendation-item {
  background: var(--bg-card);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 8px;
  padding: 16px;
  border-left: 4px solid var(--brand-primary);
}

.recommendation-title {
  font-weight: 600;
  color: var(--brand-primary);
  margin-bottom: 6px;
  font-size: 0.95rem;
}

.recommendation-content {
  color: var(--text-secondary);
  line-height: 1.5;
  font-size: 0.9rem;
}

.conclusion {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 8px;
  padding: 20px;
  border-left: 4px solid var(--brand-accent);
}

.conclusion h4 {
  margin: 0 0 12px 0;
  color: var(--brand-accent);
  font-size: 1.1rem;
  font-weight: 600;
}

.conclusion-content {
  color: var(--text-primary);
  line-height: 1.7;
  font-style: italic;
  font-size: 0.95rem;
}

/* PDF模板专用样式 */
.pdf-report-container {
  font-family: 'SimSun', 'Microsoft YaHei', Arial, sans-serif;
  color: #000000;
  background-color: #ffffff;
  padding: 40px 30px;
  width: 734px; /* 794px - 60px padding */
  max-width: 734px;
  box-sizing: border-box;
  line-height: 1.5;
  font-size: 11px;
}

.pdf-header {
  text-align: center;
  margin-bottom: 20px;
  border-bottom: 2px solid #2c5aa0;
  padding-bottom: 15px;
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
  border-top: 1px solid #cccccc;
  margin: 15px 0;
}

.pdf-divider-thin {
  border-top: 1px solid #eeeeee;
  margin: 10px 0;
}

.pdf-section {
  margin-bottom: 20px;
  page-break-inside: avoid;
}

.pdf-section-title {
  font-size: 13px;
  font-weight: bold;
  color: #2c5aa0;
  margin: 15px 0 8px 0;
  padding: 6px 0;
  text-align: center;
  border-top: 1px solid #cccccc;
  border-bottom: 1px solid #cccccc;
}

.pdf-subsection-title {
  font-size: 12px;
  font-weight: bold;
  color: #333333;
  margin: 12px 0 6px 0;
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
  margin: 8px 0;
  font-size: 10px;
  page-break-inside: avoid;
}

.pdf-table td,
.pdf-table th {
  border: 1px solid #333333;
  padding: 4px 6px;
  text-align: left;
  vertical-align: top;
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

.pdf-highlight-row {
  background-color: #f0f9ff;
}

.pdf-safe-text {
  color: #198754;
  font-weight: bold;
}

.pdf-warning-text {
  color: #dc3545;
  font-weight: bold;
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

/* 可视化部分样式 */
.visualization-section {
  margin-bottom: 32px;
  background: #f8f9fa;
  border-radius: 12px;
  padding: 24px;
  border: 1px solid var(--el-border-color-light);
}

.section-title {
  margin: 0 0 20px 0;
  font-size: 1.125rem;
  color: var(--text-primary);
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-title .el-icon {
  color: var(--brand-primary);
}

/* PDF分页控制 */
.pdf-page-break {
  page-break-before: always;
  break-before: page;
  margin-top: 60px; /* 增加顶部间距以强制视觉分页 */
  padding-top: 20px;
}

</style> 