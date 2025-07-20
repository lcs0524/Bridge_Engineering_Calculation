# -*- coding: utf-8 -*-
"""
路基顶管计算模块
实现顶推力计算和管道沉降验算功能
"""

import numpy as np
import math
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass


@dataclass
class PipelinePushCalculation:
    """顶管计算结果数据结构"""
    total_push_force: float  # 总顶推力 (kN)
    friction_resistance: float  # 管道外壁摩擦阻力 (kN)
    front_resistance: float  # 工具管正面阻力 (kN)
    interface_resistance: float  # 管道接口摩擦阻力 (kN)
    pipe_capacity: float  # 管道承压能力 (kN)
    work_well_capacity: float  # 工作井后背墙抗力 (kN)
    safety_factor: float  # 安全系数
    
    # 强度验算结果
    strength_check: bool  # 强度是否满足
    settlement_check: bool  # 沉降是否满足
    work_well_check: bool  # 工作井稳定性是否满足


@dataclass
class PipelineSettlementCalculation:
    """管道沉降计算结果数据结构"""
    vertical_soil_pressure: float  # 垂直土压力 (kPa)
    live_load_pressure: float  # 车辆活载压力 (kPa)
    total_pressure: float  # 总压力 (kPa)
    hoop_stress: float  # 环向应力 (kPa)
    pipe_deformation: float  # 管体变形 (mm)
    allowable_stress: float  # 允许应力 (kPa)
    allowable_deformation: float  # 允许变形 (mm)
    
    # 验算结果
    stress_check: bool  # 应力是否满足
    deformation_check: bool  # 变形是否满足


class PipelineCalculator:
    """路基顶管计算类"""
    
    def __init__(self):
        # 材料参数数据库
        self.material_properties = {
            '混凝土': {
                'elastic_modulus': 30000,  # MPa
                'tensile_strength': 2.01,  # MPa (C30混凝土)
                'density': 25.0  # kN/m³
            },
            '高密度聚乙烯': {
                'elastic_modulus': 800,  # MPa
                'tensile_strength': 20.0,  # MPa
                'density': 9.5  # kN/m³
            }
        }
        
        # 土质参数数据库
        self.soil_parameters = {
            '黏土': {
                'unit_weight': 18.0,  # kN/m³
                'cohesion': 25.0,  # kPa
                'friction_angle': 15.0,  # 度
                'friction_coefficient': 0.3
            },
            '砂土': {
                'unit_weight': 19.0,  # kN/m³
                'cohesion': 0.0,  # kPa
                'friction_angle': 30.0,  # 度
                'friction_coefficient': 0.4
            },
            '粉土': {
                'unit_weight': 18.5,  # kN/m³
                'cohesion': 15.0,  # kPa
                'friction_angle': 20.0,  # 度
                'friction_coefficient': 0.35
            }
        }
    
    def calculate_push_force(self, params: Dict[str, Any]) -> PipelinePushCalculation:
        """
        计算顶推力
        
        公式：
        F = K × (F₁ + F₂ + F₃)
        
        F₁ = π × D × L × f (管道外壁摩擦阻力)
        F₂ = (π × Dt² / 4) × P (工具管正面阻力)
        F₃ = n × μ × N (管道接口摩擦阻力，如适用)
        
        Args:
            params: 计算参数字典
            
        Returns:
            PipelinePushCalculation: 顶推计算结果
        """
        # 提取参数
        pipe_diameter = params.get('pipe_diameter', 1.0)  # m
        tool_diameter = params.get('tool_diameter', 1.2)  # m
        pipe_length = params.get('pipe_length', 100.0)  # m
        unit_friction = params.get('unit_friction', 5.0)  # kN/m²
        front_pressure = params.get('front_pressure', 100.0)  # kPa
        interface_count = params.get('interface_count', 0)
        interface_friction = params.get('interface_friction', 0.2)
        normal_force = params.get('normal_force', 100.0)  # kN
        safety_factor = params.get('safety_factor', 1.5)
        
        # 计算各项阻力
        # F₁ = π × D × L × f
        friction_resistance = math.pi * pipe_diameter * pipe_length * unit_friction
        
        # F₂ = (π × Dt² / 4) × P
        front_resistance = (math.pi * tool_diameter**2 / 4) * front_pressure
        
        # F₃ = n × μ × N (仅当有接口时计算)
        interface_resistance = interface_count * interface_friction * normal_force if interface_count > 0 else 0.0
        
        # 总顶推力 F = K × (F₁ + F₂ + F₃)
        total_push_force = safety_factor * (friction_resistance + front_resistance + interface_resistance)
        
        # 计算管道承压能力
        pipe_capacity = self.calculate_pipe_capacity(params)
        
        # 计算工作井后背墙抗力
        work_well_capacity = self.calculate_work_well_capacity(params)
        
        # 验算结果
        strength_check = total_push_force <= pipe_capacity
        work_well_check = total_push_force <= work_well_capacity
        
        return PipelinePushCalculation(
            total_push_force=total_push_force,
            friction_resistance=friction_resistance,
            front_resistance=front_resistance,
            interface_resistance=interface_resistance,
            pipe_capacity=pipe_capacity,
            work_well_capacity=work_well_capacity,
            safety_factor=safety_factor,
            strength_check=strength_check,
            settlement_check=True,  # 将在沉降计算中更新
            work_well_check=work_well_check
        )
    
    def calculate_pipe_capacity(self, params: Dict[str, Any]) -> float:
        """
        计算管道承压能力
        
        Args:
            params: 计算参数
            
        Returns:
            float: 管道承压能力 (kN)
        """
        pipe_diameter = params.get('pipe_diameter', 1.0)  # m
        wall_thickness = params.get('wall_thickness', 0.1)  # m
        material = params.get('material', '混凝土')
        reduction_factor = params.get('reduction_factor', 0.85)
        
        # 获取材料强度
        if material in self.material_properties:
            tensile_strength = self.material_properties[material]['tensile_strength']  # MPa
        else:
            tensile_strength = 2.01  # 默认C30混凝土
        
        # 计算截面积
        outer_radius = pipe_diameter / 2
        inner_radius = outer_radius - wall_thickness
        
        if inner_radius <= 0:
            return 0.0
        
        # 环形截面积
        area = math.pi * (outer_radius**2 - inner_radius**2)  # m²
        
        # 转换为kN
        capacity = tensile_strength * area * 1000 * reduction_factor  # kN
        
        return capacity
    
    def calculate_work_well_capacity(self, params: Dict[str, Any]) -> float:
        """
        计算工作井后背墙抗力
        
        Args:
            params: 计算参数
            
        Returns:
            float: 工作井后背墙抗力 (kN)
        """
        work_well_type = params.get('work_well_type', 'gravity')
        
        if work_well_type == 'gravity':
            return self.calculate_gravity_wall_capacity(params)
        elif work_well_type == 'pile':
            return self.calculate_pile_wall_capacity(params)
        elif work_well_type == 'sheet_pile':
            return self.calculate_sheet_pile_capacity(params)
        else:
            return 1000.0  # 默认值
    
    def calculate_gravity_wall_capacity(self, params: Dict[str, Any]) -> float:
        """计算重力式后背墙抗力"""
        wall_height = params.get('wall_height', 3.0)  # m
        wall_width = params.get('wall_width', 2.0)  # m
        wall_length = params.get('wall_length', 4.0)  # m
        soil_unit_weight = params.get('soil_unit_weight', 18.0)  # kN/m³
        friction_angle = params.get('friction_angle', 30.0)  # 度
        
        # 计算被动土压力
        ka = math.tan(math.radians(45 - friction_angle/2))**2
        kp = math.tan(math.radians(45 + friction_angle/2))**2
        
        # 土压力系数差
        pressure_diff = 0.5 * soil_unit_weight * wall_height**2 * (kp - ka)
        
        # 总抗力
        total_resistance = pressure_diff * wall_width  # kN
        
        return total_resistance
    
    def calculate_pile_wall_capacity(self, params: Dict[str, Any]) -> float:
        """计算桩基后背墙抗力"""
        pile_count = params.get('pile_count', 4)
        pile_diameter = params.get('pile_diameter', 0.8)  # m
        pile_length = params.get('pile_length', 15.0)  # m
        skin_friction = params.get('skin_friction', 50.0)  # kPa
        
        # 计算单桩承载力
        single_pile_capacity = math.pi * pile_diameter * pile_length * skin_friction
        
        # 总抗力
        total_capacity = single_pile_capacity * pile_count  # kN
        
        return total_capacity
    
    def calculate_sheet_pile_capacity(self, params: Dict[str, Any]) -> float:
        """计算钢板桩后背墙抗力"""
        pile_length = params.get('pile_length', 8.0)  # m
        embedment_depth = params.get('embedment_depth', 4.0)  # m
        soil_unit_weight = params.get('soil_unit_weight', 18.0)  # kN/m³
        friction_angle = params.get('friction_angle', 30.0)  # 度
        
        # 计算被动土压力
        kp = math.tan(math.radians(45 + friction_angle/2))**2
        
        # 被动土压力
        passive_pressure = 0.5 * soil_unit_weight * embedment_depth**2 * kp
        
        # 总抗力
        total_resistance = passive_pressure * pile_length  # kN
        
        return total_resistance
    
    def calculate_pipeline_settlement(self, params: Dict[str, Any]) -> PipelineSettlementCalculation:
        """
        计算管道沉降
        
        公式：
        垂直土压力：Pv = γ × H
        车辆活载：q = 260/A (按JTGD60-2015)
        环向应力：σ = (Pv + q) × D / (2t)
        管体变形：S = (Pv + q) × D⁴ / (3.67Et³ + 0.061E'D³)
        
        Args:
            params: 计算参数
            
        Returns:
            PipelineSettlementCalculation: 沉降计算结果
        """
        # 提取参数
        pipe_diameter = params.get('pipe_diameter', 1.0)  # m
        wall_thickness = params.get('wall_thickness', 0.1)  # m
        cover_depth = params.get('cover_depth', 2.0)  # m
        material = params.get('material', '混凝土')
        soil_modulus = params.get('soil_modulus', 10.0)  # MPa
        
        # 获取材料参数
        if material in self.material_properties:
            elastic_modulus = self.material_properties[material]['elastic_modulus']  # MPa
            tensile_strength = self.material_properties[material]['tensile_strength']  # MPa
            unit_weight = self.material_properties[material]['density']  # kN/m³
        else:
            elastic_modulus = 30000  # 默认混凝土
            tensile_strength = 2.01
            unit_weight = 25.0
        
        # 计算土压力
        vertical_soil_pressure = unit_weight * cover_depth  # kPa
        
        # 车辆活载 (按JTGD60-2015)
        contact_area = 0.2 * 0.6  # m² (标准车辆荷载接触面积)
        live_load_pressure = 260.0 / contact_area  # kPa
        
        # 总压力
        total_pressure = vertical_soil_pressure + live_load_pressure
        
        # 环向应力
        hoop_stress = total_pressure * pipe_diameter / (2 * wall_thickness)
        
        # 管体变形
        # S = (Pv + q) × D⁴ / (3.67Et³ + 0.061E'D³)
        numerator = total_pressure * (pipe_diameter * 1000)**4  # 转换为mm
        denominator = (3.67 * elastic_modulus * (wall_thickness * 1000)**3 + 
                      0.061 * soil_modulus * (pipe_diameter * 1000)**3)
        
        if denominator > 0:
            pipe_deformation = numerator / denominator  # mm
        else:
            pipe_deformation = 0.0
        
        # 允许应力 (材料强度乘以折减系数)
        allowable_stress = tensile_strength * 1000  # kPa
        
        # 允许变形 (不超过管径的5%)
        allowable_deformation = 0.05 * pipe_diameter * 1000  # mm
        
        # 验算结果
        stress_check = hoop_stress <= allowable_stress
        deformation_check = pipe_deformation <= allowable_deformation
        
        return PipelineSettlementCalculation(
            vertical_soil_pressure=vertical_soil_pressure,
            live_load_pressure=live_load_pressure,
            total_pressure=total_pressure,
            hoop_stress=hoop_stress,
            pipe_deformation=pipe_deformation,
            allowable_stress=allowable_stress,
            allowable_deformation=allowable_deformation,
            stress_check=stress_check,
            deformation_check=deformation_check
        )
    
    def calculate_pipeline_stability(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        计算管道整体稳定性
        
        Args:
            params: 计算参数
            
        Returns:
            Dict: 包含顶推力和沉降计算结果的综合字典
        """
        # 计算顶推力
        push_calculation = self.calculate_push_force(params)
        
        # 计算沉降
        settlement_calculation = self.calculate_pipeline_settlement(params)
        
        # 创建综合结果
        result = {
            'push_calculation': push_calculation,
            'settlement_calculation': settlement_calculation,
            'safety_assessment': {
                'overall_safe': (push_calculation.strength_check and 
                               push_calculation.work_well_check and 
                               settlement_calculation.stress_check and 
                               settlement_calculation.deformation_check),
                'strength_ratio': push_calculation.total_push_force / push_calculation.pipe_capacity,
                'deformation_ratio': settlement_calculation.pipe_deformation / settlement_calculation.allowable_deformation,
                'recommendations': self.generate_recommendations(push_calculation, settlement_calculation)
            }
        }
        
        return result
    
    def generate_recommendations(self, push_calc: PipelinePushCalculation, 
                               settlement_calc: PipelineSettlementCalculation) -> List[str]:
        """生成工程建议"""
        recommendations = []
        
        # 强度验算建议
        if not push_calc.strength_check:
            recommendations.append("管道强度不足，建议增加管壁厚度或改用高强度材料")
        
        # 工作井稳定性建议
        if not push_calc.work_well_check:
            recommendations.append("工作井后背墙抗力不足，建议加强后背墙结构")
        
        # 应力验算建议
        if not settlement_calc.stress_check:
            recommendations.append("环向应力超限，建议增加覆土深度或改用高强度管道")
        
        # 变形验算建议
        if not settlement_calc.deformation_check:
            recommendations.append("管道变形超限，建议减小管径或增加管壁厚度")
        
        # 一般建议
        if len(recommendations) == 0:
            recommendations.append("所有验算均满足要求，可按设计参数施工")
            recommendations.append("建议施工过程中加强监测，确保施工安全")
        
        return recommendations
    
    def get_material_list(self) -> List[str]:
        """获取可用材料列表"""
        return list(self.material_properties.keys())
    
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
        required_params = ['pipe_diameter', 'pipe_length', 'cover_depth']
        for param in required_params:
            if param not in params or params[param] is None:
                errors.append(f"缺少必填参数: {param}")
                continue
            
            if not isinstance(params[param], (int, float)) or params[param] <= 0:
                errors.append(f"参数 {param} 必须是正数")
        
        # 检查数值范围
        if 'pipe_diameter' in params and params['pipe_diameter'] > 5.0:
            errors.append("管径不应超过5.0米")
        
        if 'cover_depth' in params and params['cover_depth'] < 1.0:
            errors.append("覆土深度不应小于1.0米")
        
        if 'safety_factor' in params and not 1.1 <= params['safety_factor'] <= 2.0:
            errors.append("安全系数应在1.1-2.0之间")
        
        return len(errors) == 0, errors