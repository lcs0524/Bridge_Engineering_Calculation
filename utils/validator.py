# -*- coding: utf-8 -*-
"""
输入验证器 - 验证用户输入参数的有效性
"""

import re
import math


class InputValidator:
    """输入验证器类"""
    
    def __init__(self):
        """初始化验证器"""
        pass
    
    def validate_numeric_input(self, value, min_value=None, max_value=None, allow_zero=False):
        """
        验证数值输入
        
        参数:
        value: 输入值
        min_value: 最小值
        max_value: 最大值
        allow_zero: 是否允许为零
        
        返回:
        is_valid: 是否有效
        error_msg: 错误信息
        parsed_value: 解析后的数值
        """
        try:
            # 尝试转换为浮点数
            parsed_value = float(value)
            
            # 检查是否为NaN或无穷大
            if math.isnan(parsed_value) or math.isinf(parsed_value):
                return False, "输入的数值无效", None
            
            # 检查零值
            if not allow_zero and parsed_value == 0:
                return False, "数值不能为零", None
            
            # 检查最小值
            if min_value is not None and parsed_value < min_value:
                return False, f"数值不能小于{min_value}", None
            
            # 检查最大值
            if max_value is not None and parsed_value > max_value:
                return False, f"数值不能大于{max_value}", None
            
            return True, "验证通过", parsed_value
            
        except ValueError:
            return False, "输入的不是有效数字", None
    
    def validate_pile_diameter(self, diameter_str):
        """验证桩径输入"""
        is_valid, error_msg, diameter = self.validate_numeric_input(
            diameter_str, min_value=0.1, max_value=10.0
        )
        
        if not is_valid:
            return False, f"桩径输入错误：{error_msg}"
        
        # 额外的桩径验证
        if diameter < 0.3:
            return False, "桩径过小，建议不小于0.3m"
        
        if diameter > 5.0:
            return False, "桩径过大，可能超出适用范围"
        
        return True, "桩径验证通过"
    
    def validate_pile_length(self, length_str):
        """验证桩长输入（土下层部分）"""
        is_valid, error_msg, length = self.validate_numeric_input(
            length_str, min_value=1.0, max_value=100.0
        )
        
        if not is_valid:
            return False, f"桩长（土下层）输入错误：{error_msg}"
        
        # 额外的桩长验证
        if length < 3.0:
            return False, "桩长（土下层）过短，建议不小于3.0m"
        
        if length > 80.0:
            return False, "桩长（土下层）过长，可能超出适用范围"
        
        return True, "桩长（土下层）验证通过"
    
    def validate_load(self, load_str):
        """验证荷载输入"""
        is_valid, error_msg, load = self.validate_numeric_input(
            load_str, min_value=1.0, max_value=50000.0
        )
        
        if not is_valid:
            return False, f"荷载输入错误：{error_msg}"
        
        # 额外的荷载验证
        if load < 100:
            return False, "荷载过小，建议不小于100kN"
        
        if load > 20000:
            return False, "荷载过大，可能超出适用范围"
        
        return True, "荷载验证通过"
    
    def validate_compression_modulus(self, modulus_str):
        """验证压缩模量输入"""
        is_valid, error_msg, modulus = self.validate_numeric_input(
            modulus_str, min_value=0.1, max_value=100.0
        )
        
        if not is_valid:
            return False, f"压缩模量输入错误：{error_msg}"
        
        # 额外的压缩模量验证
        if modulus < 1.0:
            return False, "压缩模量过小，可能不符合实际情况"
        
        if modulus > 50.0:
            return False, "压缩模量过大，请检查单位是否正确"
        
        return True, "压缩模量验证通过"
    
    def validate_poisson_ratio(self, ratio_str):
        """验证泊松比输入"""
        is_valid, error_msg, ratio = self.validate_numeric_input(
            ratio_str, min_value=-0.9, max_value=0.49
        )
        
        if not is_valid:
            return False, f"泊松比输入错误：{error_msg}"
        
        # 额外的泊松比验证
        if ratio < 0.1:
            return False, "泊松比过小，建议在0.1-0.45范围内"
        
        if ratio > 0.45:
            return False, "泊松比过大，建议在0.1-0.45范围内"
        
        return True, "泊松比验证通过"
    
    def validate_depth_range(self, depth_range_str):
        """验证深度范围输入"""
        # 检查深度范围格式 (如 "0-5" 或 "5-10")
        pattern = r'^\d+(\.\d+)?-\d+(\.\d+)?$'
        
        if not re.match(pattern, depth_range_str.strip()):
            return False, "深度范围格式错误，请使用'起始深度-结束深度'格式"
        
        try:
            parts = depth_range_str.strip().split('-')
            start_depth = float(parts[0])
            end_depth = float(parts[1])
            
            if start_depth >= end_depth:
                return False, "起始深度必须小于结束深度"
            
            if start_depth < 0:
                return False, "起始深度不能为负值"
            
            if end_depth > 100:
                return False, "结束深度过大，建议不超过100m"
            
            thickness = end_depth - start_depth
            if thickness < 0.5:
                return False, "土层厚度过小，建议不小于0.5m"
            
            return True, "深度范围验证通过"
            
        except ValueError:
            return False, "深度范围包含无效数字"
    
    def validate_soil_layer_name(self, name):
        """验证土层名称"""
        if not name or not name.strip():
            return False, "土层名称不能为空"
        
        name = name.strip()
        
        if len(name) > 20:
            return False, "土层名称过长，建议不超过20个字符"
        
        # 检查是否包含特殊字符
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
        for char in invalid_chars:
            if char in name:
                return False, f"土层名称不能包含特殊字符：{char}"
        
        return True, "土层名称验证通过"
    
    def validate_road_level(self, road_level):
        """验证路线等级"""
        valid_levels = ["一级公路", "二级公路"]
        
        if road_level not in valid_levels:
            return False, f"路线等级必须是以下之一：{', '.join(valid_levels)}"
        
        return True, "路线等级验证通过"
    
    def validate_pile_parameters_consistency(self, diameter, length):
        """验证桩径和桩长（土下层）的一致性"""
        try:
            d = float(diameter)
            l = float(length)
            
            # 长径比检查
            length_diameter_ratio = l / d
            
            if length_diameter_ratio < 5:
                return False, "桩长径比过小，可能影响承载力，建议增加桩长（土下层）或减小桩径"
            
            if length_diameter_ratio > 100:
                return False, "桩长径比过大，可能导致施工困难，建议调整参数"
            
            return True, "桩基参数一致性验证通过"
            
        except ValueError:
            return False, "参数格式错误，无法进行一致性检查"
    
    def validate_soil_layers_completeness(self, soil_layers):
        """验证土层数据的完整性"""
        if not soil_layers:
            return False, "至少需要定义一个土层"
        
        if len(soil_layers) > 10:
            return False, "土层数量过多，建议合并相似土层"
        
        # 检查深度连续性
        sorted_layers = []
        for layer in soil_layers:
            try:
                depth_range = layer['depth_range']
                parts = depth_range.split('-')
                start_depth = float(parts[0])
                end_depth = float(parts[1])
                sorted_layers.append((start_depth, end_depth, layer))
            except:
                return False, f"土层深度范围格式错误：{layer.get('depth_range', '未知')}"
        
        # 按起始深度排序
        sorted_layers.sort(key=lambda x: x[0])
        
        # 检查深度连续性
        expected_start = 0
        for start_depth, end_depth, layer in sorted_layers:
            if abs(start_depth - expected_start) > 0.1:  # 允许0.1m的误差
                return False, f"土层深度不连续，在{expected_start}m处缺少土层定义"
            expected_start = end_depth
        
        return True, "土层数据完整性验证通过"
    
    def validate_all_inputs(self, input_data):
        """
        验证所有输入数据
        
        参数:
        input_data: 包含所有输入的字典
        
        返回:
        is_valid: 是否全部有效
        error_messages: 错误信息列表
        """
        error_messages = []
        
        # 验证基本参数
        is_valid, msg = self.validate_pile_diameter(input_data.get('pile_diameter', ''))
        if not is_valid:
            error_messages.append(msg)
        
        is_valid, msg = self.validate_pile_length(input_data.get('pile_length', ''))
        if not is_valid:
            error_messages.append(msg)
        
        is_valid, msg = self.validate_load(input_data.get('load', ''))
        if not is_valid:
            error_messages.append(msg)
        
        is_valid, msg = self.validate_road_level(input_data.get('road_level', ''))
        if not is_valid:
            error_messages.append(msg)
        
        # 验证桩基参数一致性
        if 'pile_diameter' in input_data and 'pile_length' in input_data:
            is_valid, msg = self.validate_pile_parameters_consistency(
                input_data['pile_diameter'], input_data['pile_length']
            )
            if not is_valid:
                error_messages.append(msg)
        
        # 验证土层数据
        soil_layers = input_data.get('soil_layers', [])
        is_valid, msg = self.validate_soil_layers_completeness(soil_layers)
        if not is_valid:
            error_messages.append(msg)
        
        # 验证每个土层
        for i, layer in enumerate(soil_layers):
            # 验证深度范围
            is_valid, msg = self.validate_depth_range(layer.get('depth_range', ''))
            if not is_valid:
                error_messages.append(f"第{i+1}层土：{msg}")
            
            # 验证土层名称
            is_valid, msg = self.validate_soil_layer_name(layer.get('name', ''))
            if not is_valid:
                error_messages.append(f"第{i+1}层土：{msg}")
            
            # 验证压缩模量
            is_valid, msg = self.validate_compression_modulus(
                str(layer.get('compression_modulus', ''))
            )
            if not is_valid:
                error_messages.append(f"第{i+1}层土：{msg}")
            
            # 验证泊松比
            is_valid, msg = self.validate_poisson_ratio(
                str(layer.get('poisson_ratio', ''))
            )
            if not is_valid:
                error_messages.append(f"第{i+1}层土：{msg}")
        
        return len(error_messages) == 0, error_messages 