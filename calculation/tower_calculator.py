# -*- coding: utf-8 -*-
"""
电线塔基础稳定性计算模块
实现地基承载力、抗倾覆、抗滑移三大稳定性验算功能
"""

import numpy as np
import math
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass


@dataclass
class TowerFoundationCalculation:
    """电线塔基础计算结果数据结构"""
    
    # 地基承载力计算结果
    corrected_bearing_capacity: float  # 修正后的地基承载力 (kPa)
    max_base_pressure: float          # 最大基底压力 (kPa)
    min_base_pressure: float          # 最小基底压力 (kPa)
    average_base_pressure: float      # 平均基底压力 (kPa)
    
    # 抗倾覆计算结果
    overturning_resistance_moment: float  # 抗倾覆力矩 (kN·m)
    overturning_moment: float             # 倾覆力矩 (kN·m)
    overturning_safety_factor: float      # 抗倾覆安全系数
    
    # 抗滑移计算结果
    sliding_resistance_force: float   # 抗滑移力 (kN)
    sliding_force: float              # 滑移力 (kN)
    sliding_safety_factor: float      # 抗滑移安全系数
    
    # 验算结果
    bearing_check: bool               # 地基承载力是否满足
    overturning_check: bool           # 抗倾覆是否满足
    sliding_check: bool               # 抗滑移是否满足


class TowerCalculator:
    """电线塔基础稳定性计算类"""
    
    def __init__(self):
        # 规范要求的安全系数
        self.safety_factors = {
            'bearing_normal': 1.0,      # 地基承载力正常使用状态
            'bearing_extreme': 1.2,     # 地基承载力极端状态
            'overturning_normal': 1.5,  # 抗倾覆正常使用状态
            'overturning_extreme': 1.2, # 抗倾覆极端状态
            'sliding_normal': 1.3,      # 抗滑移正常使用状态
            'sliding_extreme': 1.1      # 抗滑移极端状态
        }
        
        # 土质参数数据库
        self.soil_parameters = {
            '黏土': {
                'bearing_capacity': 150,    # kPa
                'unit_weight': 18.0,        # kN/m³
                'friction_coefficient': 0.25,
                'cohesion': 25.0,           # kPa
                'friction_angle': 15.0      # 度
            },
            '砂土': {
                'bearing_capacity': 200,    # kPa
                'unit_weight': 19.0,        # kN/m³
                'friction_coefficient': 0.4,
                'cohesion': 0.0,            # kPa
                'friction_angle': 30.0      # 度
            },
            '粉土': {
                'bearing_capacity': 180,    # kPa
                'unit_weight': 18.5,        # kN/m³
                'friction_coefficient': 0.3,
                'cohesion': 15.0,           # kPa
                'friction_angle': 20.0      # 度
            },
            '岩石': {
                'bearing_capacity': 500,    # kPa
                'unit_weight': 25.0,        # kN/m³
                'friction_coefficient': 0.6,
                'cohesion': 50.0,           # kPa
                'friction_angle': 40.0      # 度
            }
        }
    
    def calculate_bearing_capacity(self, params: Dict[str, Any]) -> float:
        """
        计算修正后的地基承载力
        
        公式：fa = fak + ηb×γ×(b-3) + ηd×γm×(d-0.5)
        
        Args:
            params: 计算参数
            
        Returns:
            float: 修正后的地基承载力 (kPa)
        """
        # 提取参数
        soil_type = params.get('soil_type', '黏土')
        base_width = params.get('base_width', 2.0)      # m
        base_length = params.get('base_length', 3.0)    # m
        embedment_depth = params.get('embedment_depth', 1.5)  # m
        
        # 获取土体参数
        if soil_type in self.soil_parameters:
            soil_data = self.soil_parameters[soil_type]
            fak = soil_data['bearing_capacity']  # kPa
            gamma = soil_data['unit_weight']     # kN/m³
        else:
            fak = 150  # 默认粘土
            gamma = 18.0
        
        # 修正系数 (按GB50007-2011)
        width_correction_factor = self.get_width_correction_factor(soil_type, base_width)
        depth_correction_factor = self.get_depth_correction_factor(soil_type, embedment_depth)
        
        # 计算修正后的地基承载力
        fa = fak + width_correction_factor * gamma * max(0, base_width - 3) + \
             depth_correction_factor * gamma * max(0, embedment_depth - 0.5)
        
        return fa
    
    def get_width_correction_factor(self, soil_type: str, base_width: float) -> float:
        """获取宽度修正系数"""
        # 按GB50007-2011表5.2.4
        if soil_type == '黏土':
            return 0.0  # 粘性土宽度修正系数为0
        elif soil_type in ['砂土', '粉土']:
            return 2.0  # 砂土和粉土宽度修正系数
        elif soil_type == '岩石':
            return 0.5  # 岩石宽度修正系数
        else:
            return 0.0
    
    def get_depth_correction_factor(self, soil_type: str, embedment_depth: float) -> float:
        """获取深度修正系数"""
        # 按GB50007-2011表5.2.4
        if soil_type == '黏土':
            return 1.0  # 粘性土深度修正系数
        elif soil_type == '砂土':
            return 3.0  # 砂土深度修正系数
        elif soil_type == '粉土':
            return 2.0  # 粉土深度修正系数
        elif soil_type == '岩石':
            return 4.4  # 岩石深度修正系数
        else:
            return 1.0
    
    def calculate_base_pressure(self, params: Dict[str, Any]) -> Tuple[float, float, float]:
        """
        计算基底压力
        
        公式：Pmax,min = (N+G)/A ± M/W
        
        Args:
            params: 计算参数
            
        Returns:
            Tuple[float, float, float]: (最大压力, 最小压力, 平均压力)
        """
        # 提取参数
        tower_load = params.get('tower_load', 500.0)      # kN
        horizontal_force = params.get('horizontal_force', 50.0)  # kN
        force_height = params.get('force_height', 15.0)   # m
        base_weight = params.get('base_weight', 200.0)    # kN
        base_width = params.get('base_width', 2.0)        # m
        base_length = params.get('base_length', 3.0)      # m
        
        # 计算基础面积和截面模量
        base_area = base_width * base_length  # m²
        section_modulus = (base_length * base_width**2) / 6  # m³
        
        # 计算总竖向力
        total_vertical_force = tower_load + base_weight  # kN
        
        # 计算弯矩
        moment = horizontal_force * force_height  # kN·m
        
        # 计算基底压力
        average_pressure = total_vertical_force / base_area  # kPa
        
        # 最大和最小基底压力
        max_pressure = average_pressure + moment / section_modulus  # kPa
        min_pressure = average_pressure - moment / section_modulus  # kPa
        
        # 确保最小压力不小于0
        min_pressure = max(0, min_pressure)
        
        return max_pressure, min_pressure, average_pressure
    
    def calculate_overturning_stability(self, params: Dict[str, Any]) -> Tuple[float, float, float]:
        """
        计算抗倾覆稳定性
        
        公式：K = M抗 / M倾 ≥ 1.5(正常) / 1.2(极端)
        
        Args:
            params: 计算参数
            
        Returns:
            Tuple[float, float, float]: (抗倾覆力矩, 倾覆力矩, 安全系数)
        """
        # 提取参数
        tower_load = params.get('tower_load', 500.0)       # kN
        horizontal_force = params.get('horizontal_force', 50.0)  # kN
        force_height = params.get('force_height', 15.0)    # m
        base_weight = params.get('base_weight', 200.0)     # kN
        base_width = params.get('base_width', 2.0)         # m
        
        # 计算抗倾覆力矩 (竖向力 × 基础宽度/2)
        total_vertical_force = tower_load + base_weight  # kN
        overturning_resistance_moment = total_vertical_force * (base_width / 2)  # kN·m
        
        # 计算倾覆力矩 (水平力 × 作用高度)
        overturning_moment = horizontal_force * force_height  # kN·m
        
        # 计算安全系数
        if overturning_moment > 0:
            overturning_safety_factor = overturning_resistance_moment / overturning_moment
        else:
            overturning_safety_factor = float('inf')
        
        return overturning_resistance_moment, overturning_moment, overturning_safety_factor
    
    def calculate_sliding_stability(self, params: Dict[str, Any]) -> Tuple[float, float, float]:
        """
        计算抗滑移稳定性
        
        公式：Kh = Fh / Fv ≥ 1.3
        
        Args:
            params: 计算参数
            
        Returns:
            Tuple[float, float, float]: (抗滑移力, 滑移力, 安全系数)
        """
        # 提取参数
        tower_load = params.get('tower_load', 500.0)      # kN
        horizontal_force = params.get('horizontal_force', 50.0)  # kN
        base_weight = params.get('base_weight', 200.0)    # kN
        soil_type = params.get('soil_type', '黏土')
        
        # 获取摩擦系数
        if soil_type in self.soil_parameters:
            friction_coefficient = self.soil_parameters[soil_type]['friction_coefficient']
        else:
            friction_coefficient = 0.25  # 默认粘土
        
        # 计算抗滑移力 (竖向力 × 摩擦系数)
        total_vertical_force = tower_load + base_weight  # kN
        sliding_resistance_force = total_vertical_force * friction_coefficient  # kN
        
        # 滑移力 (水平力)
        sliding_force = horizontal_force  # kN
        
        # 计算安全系数
        if sliding_force > 0:
            sliding_safety_factor = sliding_resistance_force / sliding_force
        else:
            sliding_safety_factor = float('inf')
        
        return sliding_resistance_force, sliding_force, sliding_safety_factor
    
    def calculate_tower_stability(self, params: Dict[str, Any], load_case: str = 'normal') -> TowerFoundationCalculation:
        """
        计算电线塔基础整体稳定性
        
        Args:
            params: 计算参数
            load_case: 荷载工况 ('normal' 或 'extreme')
            
        Returns:
            TowerFoundationCalculation: 基础稳定性计算结果
        """
        # 计算各项稳定性
        corrected_bearing_capacity = self.calculate_bearing_capacity(params)
        max_pressure, min_pressure, avg_pressure = self.calculate_base_pressure(params)
        resistance_moment, overturning_moment, overturning_factor = self.calculate_overturning_stability(params)
        resistance_force, sliding_force, sliding_factor = self.calculate_sliding_stability(params)
        
        # 确定安全系数要求
        if load_case == 'extreme':
            bearing_required = self.safety_factors['bearing_extreme']
            overturning_required = self.safety_factors['overturning_extreme']
            sliding_required = self.safety_factors['sliding_extreme']
        else:
            bearing_required = self.safety_factors['bearing_normal']
            overturning_required = self.safety_factors['overturning_normal']
            sliding_required = self.safety_factors['sliding_normal']
        
        # 验算结果
        bearing_check = max_pressure <= corrected_bearing_capacity and min_pressure >= 0
        overturning_check = overturning_factor >= overturning_required
        sliding_check = sliding_factor >= sliding_required
        
        return TowerFoundationCalculation(
            corrected_bearing_capacity=corrected_bearing_capacity,
            max_base_pressure=max_pressure,
            min_base_pressure=min_pressure,
            average_base_pressure=avg_pressure,
            overturning_resistance_moment=resistance_moment,
            overturning_moment=overturning_moment,
            overturning_safety_factor=overturning_factor,
            sliding_resistance_force=resistance_force,
            sliding_force=sliding_force,
            sliding_safety_factor=sliding_factor,
            bearing_check=bearing_check,
            overturning_check=overturning_check,
            sliding_check=sliding_check
        )
    
    def calculate_comprehensive_stability(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        计算电线塔基础综合稳定性
        
        Args:
            params: 计算参数
            
        Returns:
            Dict: 包含正常使用和极端工况的综合结果
        """
        # 计算正常使用工况
        normal_calculation = self.calculate_tower_stability(params, 'normal')
        
        # 计算极端工况
        extreme_params = params.copy()
        # 极端工况下荷载放大1.2倍
        extreme_params['tower_load'] = params.get('tower_load', 500.0) * 1.2
        extreme_params['horizontal_force'] = params.get('horizontal_force', 50.0) * 1.2
        extreme_calculation = self.calculate_tower_stability(extreme_params, 'extreme')
        
        # 创建综合结果
        result = {
            'normal_condition': normal_calculation,
            'extreme_condition': extreme_calculation,
            'safety_assessment': {
                'overall_safe': (normal_calculation.bearing_check and 
                               normal_calculation.overturning_check and 
                               normal_calculation.sliding_check),
                'critical_condition': 'normal' if (normal_calculation.bearing_check and 
                                                normal_calculation.overturning_check and 
                                                normal_calculation.sliding_check) else 'extreme',
                'recommendations': self.generate_tower_recommendations(normal_calculation, extreme_calculation)
            }
        }
        
        return result
    
    def generate_tower_recommendations(self, normal_calc: TowerFoundationCalculation, 
                                   extreme_calc: TowerFoundationCalculation) -> List[str]:
        """生成电线塔基础工程建议"""
        recommendations = []
        
        # 地基承载力建议
        if not normal_calc.bearing_check:
            if normal_calc.max_base_pressure > normal_calc.corrected_bearing_capacity:
                recommendations.append("最大基底压力超限，建议增大基础尺寸或提高地基承载力")
            if normal_calc.min_base_pressure < 0:
                recommendations.append("最小基底压力为负，基础出现拉应力，建议扩大基础面积")
        
        # 抗倾覆建议
        if not normal_calc.overturning_check:
            recommendations.append(f"抗倾覆安全系数{normal_calc.overturning_safety_factor:.2f}不足，建议扩大基础尺寸")
        
        # 抗滑移建议
        if not normal_calc.sliding_check:
            recommendations.append(f"抗滑移安全系数{normal_calc.sliding_safety_factor:.2f}不足，建议增加基础埋深或设置防滑措施")
        
        # 极端工况建议
        if not extreme_calc.bearing_check or not extreme_calc.overturning_check or not extreme_calc.sliding_check:
            recommendations.append("极端工况下稳定性不足，建议加强基础设计或采取减载措施")
        
        # 一般建议
        if len(recommendations) == 0:
            recommendations.append("所有稳定性验算均满足要求，可按设计参数施工")
            recommendations.append("建议施工过程中加强监测，确保基础稳定性")
        
        return recommendations
    
    def get_soil_types(self) -> List[str]:
        """获取可用土质类型列表"""
        return list(self.soil_parameters.keys())
    
    def validate_parameters(self, params: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        验证输入参数
        
        Args:
            params: 待验证的参数
            
        Returns:
            Tuple[bool, List[str]]: (是否有效, 错误信息列表)
        """
        errors = []
        
        # 检查必填参数
        required_params = ['tower_load', 'horizontal_force', 'base_width', 'base_length']
        for param in required_params:
            if param not in params or params[param] is None:
                errors.append(f"缺少必填参数: {param}")
                continue
            
            if not isinstance(params[param], (int, float)) or params[param] <= 0:
                errors.append(f"参数 {param} 必须是正数")
        
        # 检查数值范围
        if 'base_width' in params and params['base_width'] < 1.0:
            errors.append("基础宽度不应小于1.0米")
        
        if 'base_length' in params and params['base_length'] < 1.0:
            errors.append("基础长度不应小于1.0米")
        
        if 'embedment_depth' in params and params['embedment_depth'] < 0.5:
            errors.append("基础埋深不应小于0.5米")
        
        if 'force_height' in params and params['force_height'] < 5.0:
            errors.append("水平力作用高度不应小于5.0米")
        
        return len(errors) == 0, errors
    
    def calculate_economic_recommendation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        计算经济优化建议
        
        Args:
            params: 计算参数
            
        Returns:
            Dict: 经济优化建议
        """
        # 获取当前计算结果
        result = self.calculate_comprehensive_stability(params)
        normal_calc = result['normal_condition']
        
        # 计算各项安全系数裕度
        bearing_margin = normal_calc.corrected_bearing_capacity - normal_calc.max_base_pressure
        overturning_margin = normal_calc.overturning_safety_factor - self.safety_factors['overturning_normal']
        sliding_margin = normal_calc.sliding_safety_factor - self.safety_factors['sliding_normal']
        
        # 生成优化建议
        optimization = {
            'current_dimensions': {
                'base_width': params.get('base_width', 2.0),
                'base_length': params.get('base_length', 3.0),
                'embedment_depth': params.get('embedment_depth', 1.5)
            },
            'safety_margins': {
                'bearing_margin': bearing_margin,
                'overturning_margin': overturning_margin,
                'sliding_margin': sliding_margin
            },
            'optimization_suggestions': []
        }
        
        # 根据裕度提供优化建议
        if bearing_margin > 100:  # 地基承载力裕度较大
            optimization['optimization_suggestions'].append(
                "地基承载力裕度较大，可考虑减小基础尺寸以节约材料"
            )
        
        if overturning_margin > 0.5:  # 抗倾覆安全系数裕度较大
            optimization['optimization_suggestions'].append(
                "抗倾覆安全系数裕度较大，可考虑减小基础宽度"
            )
        
        if sliding_margin > 0.3:  # 抗滑移安全系数裕度较大
            optimization['optimization_suggestions'].append(
                "抗滑移安全系数裕度较大，可考虑减小基础埋深"
            )
        
        return optimization