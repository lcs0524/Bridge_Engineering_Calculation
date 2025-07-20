# -*- coding: utf-8 -*-
"""
参数修正模块
实现桩基参数修正系数的计算
"""

import math


class CorrectionCalculator:
    """参数修正计算器"""
    
    def __init__(self):
        """初始化修正计算器"""
        pass
    
    def calculate_length_correction(self, pile_length):
        """
        计算桩长修正系数
        
        根据文档：a = 0.985 - 0.00051 × (桩长)
        
        参数:
        pile_length: 桩长 (m)
        
        返回:
        a: 桩长修正系数
        """
        a = 0.985 - (0.00051 * pile_length)

        return a
    
    def calculate_diameter_correction(self, pile_diameter):
        """
        计算桩径修正系数
        
        根据文档：
        b = 0.038 × (桩径)² - 0.206 × (桩径) + 1.159 (桩径小于2.5m时)
        
        参数:
        pile_diameter: 桩径 (m)
        
        返回:
        b: 桩径修正系数
        """
        b = (0.038 * pile_diameter**2) - (0.206 * pile_diameter) + 1.159
        
        return b
    
    def calculate_combined_correction(self, pile_length, pile_diameter):
        """
        计算综合修正系数 (a * b)
        
        参数:
        pile_length: 桩长 (m)
        pile_diameter: 桩径 (m)
        
        返回:
        combined: 综合修正系数 (a × b)
        """
        a = self.calculate_length_correction(pile_length)
        b = self.calculate_diameter_correction(pile_diameter)
        combined = a * b
        
        return combined

 