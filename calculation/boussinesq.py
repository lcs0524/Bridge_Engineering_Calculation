# -*- coding: utf-8 -*-
"""
Boussinesq理论计算模块
实现半无限空间弹性体表面作用集中力的应力和位移计算
"""

import numpy as np
import math


class BoussinesqCalculator:
    """Boussinesq理论计算器"""
    
    def __init__(self):
        """初始化计算器"""
        pass
    
    def calculate_settlement(self, P, G, x, y, z, nu):
        """
        计算Boussinesq理论下的垂直位移
        
        参数:
        P: 集中力 (kN)
        G: 剪切模量 (MPa)
        x, y, z: 计算点坐标 (m)
        nu: 泊松比
        
        返回:
        omega: 垂直位移 (m)
        """
        # 计算距离
        R = math.sqrt(x**2 + y**2 + z**2)
        
        if R == 0:
            # 避免除零错误
            return 0
        
        # Boussinesq公式: ω = P/(4πG) × [z²/R³ + 2(1-ν)/R]
        term1 = z**2 / (R**3)
        term2 = 2 * (1 - nu) / R
        
        # 转换单位：P(kN) -> N, G(MPa) -> Pa
        P_N = P * 1000  # kN转N
        G_Pa = G * 1e6  # MPa转Pa
        
        omega = (P_N / (4 * math.pi * G_Pa)) * (term1 + term2)
        
        return omega
    
    def calculate_shear_modulus(self, E, nu):
        """
        计算剪切模量
        
        参数:
        E: 弹性模量 (MPa)
        nu: 泊松比
        
        返回:
        G: 剪切模量 (MPa)
        """
        G = E / (2 * (1 + nu))
        return G
    
    def calculate_stress_components(self, P, x, y, z):
        """
        计算Boussinesq理论下的应力分量
        
        参数:
        P: 集中力 (kN)
        x, y, z: 计算点坐标 (m)
        
        返回:
        sigma_z: 垂直应力 (kPa)
        tau_xz: 剪应力xz (kPa)
        tau_yz: 剪应力yz (kPa)
        """
        R = math.sqrt(x**2 + y**2 + z**2)
        
        if R == 0:
            return 0, 0, 0
        
        # 转换单位：P(kN) -> N
        P_N = P * 1000
        
        # 垂直应力 σz = 3Pz³/(2πR⁵)
        sigma_z = (3 * P_N * z**3) / (2 * math.pi * R**5)
        
        # 剪应力 τxz = 3Pxz²/(2πR⁵)
        tau_xz = (3 * P_N * x * z**2) / (2 * math.pi * R**5)
        
        # 剪应力 τyz = 3Pyz²/(2πR⁵)
        tau_yz = (3 * P_N * y * z**2) / (2 * math.pi * R**5)
        
        # 转换为kPa
        sigma_z /= 1000
        tau_xz /= 1000
        tau_yz /= 1000
        
        return sigma_z, tau_xz, tau_yz
    
    def calculate_influence_factor(self, x, y, z):
        """
        计算影响系数
        
        参数:
        x, y, z: 计算点坐标 (m)
        
        返回:
        I: 影响系数
        """
        R = math.sqrt(x**2 + y**2 + z**2)
        
        if R == 0:
            return 0
        
        # 影响系数 I = 1/(2π) × [z/R³ × (1 + z/R)]
        I = (1 / (2 * math.pi)) * (z / R**3) * (1 + z / R)
        
        return I
    
    def calculate_settlement_with_correction(self, P, G, x, y, z, nu, correction_a=1.0, correction_b=1.0):
        """
        使用工程参数修正的Boussinesq公式计算沉降
        W = (a·b·P)/(4π·G) × [z²/R³ + 2(1-ν)/R]
        """
        # 计算距离
        R = math.sqrt(x**2 + y**2 + z**2)
        
        if R == 0:
            return 0
        
        # 工程参数修正的Boussinesq公式
        term1 = z**2 / (R**3)
        term2 = 2 * (1 - nu) / R
        
        # 转换单位：P(kN) -> N, G(MPa) -> Pa
        P_N = P * 1000
        G_Pa = G * 1e6
        
        # W = (a·b·P)/(4π·G) × [z²/R³ + 2(1-ν)/R]
        omega = (correction_a * correction_b * P_N) / (4 * math.pi * G_Pa) * (term1 + term2)
        
        return omega
    
    def calculate_multiple_points(self, P, G, nu, points, correction_a=1.0, correction_b=1.0):
        """
        计算多个点的沉降值
        
        参数:
        P: 集中力 (kN)
        G: 剪切模量 (MPa)
        nu: 泊松比
        points: 计算点列表 [(x1, y1, z1), (x2, y2, z2), ...]
        correction_a: 桩长修正系数
        correction_b: 桩径修正系数
        
        返回:
        results: 结果列表 [{'x': x, 'y': y, 'z': z, 'settlement': w, 'influence_factor': I}, ...]
        """
        results = []
        
        for x, y, z in points:
            # 计算沉降
            settlement = self.calculate_settlement_with_correction(
                P, G, x, y, z, nu, correction_a, correction_b
            )
            
            # 计算影响系数
            influence_factor = self.calculate_influence_factor(x, y, z)
            
            # 计算应力分量
            sigma_z, tau_xz, tau_yz = self.calculate_stress_components(P, x, y, z)
            
            result = {
                'x': x,
                'y': y,
                'z': z,
                'settlement': settlement,
                'influence_factor': influence_factor,
                'sigma_z': sigma_z,
                'tau_xz': tau_xz,
                'tau_yz': tau_yz
            }
            
            results.append(result)
        
        return results
    
    def validate_parameters(self, P, E, nu):
        """
        验证输入参数的有效性
        
        参数:
        P: 集中力 (kN)
        E: 弹性模量 (MPa)
        nu: 泊松比
        
        返回:
        is_valid: 是否有效
        error_msg: 错误信息
        """
        if P <= 0:
            return False, "集中力P必须大于0"
        
        if E <= 0:
            return False, "弹性模量E必须大于0"
        
        if nu <= -1 or nu >= 0.5:
            return False, "泊松比ν必须在(-1, 0.5)范围内"
        
        return True, "参数验证通过"
    
    def get_standard_calculation_points(self, pile_diameter):
        """
        获取标准16个计算点的坐标
        
        参数:
        pile_diameter: 桩径 (m)
        
        返回:
        points: 16个计算点的坐标列表
        """
        points = []
        
        # 根据文档图片，设置16个计算点
        # 4行4列的网格布局，距离基于桩径的倍数
        distances = [1.1, 2.2, 3.3, 4.4]  # 距离倍数
        depths = [1.0, 2.0, 3.0, 4.0]     # 深度
        
        point_index = 1
        for depth in depths:
            for distance in distances:
                x = distance * pile_diameter
                y = 0  # 简化为线性分布
                z = depth
                points.append((x, y, z))
                point_index += 1
        
        return points