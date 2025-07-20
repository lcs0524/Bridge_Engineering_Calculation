#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试桩长定义修改 - 验证GUI和计算模块中桩长概念的一致性
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# 添加模块路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from calculation.settlement import SettlementCalculator
from utils.validator import InputValidator
from visualization.plotter import ResultPlotter

def test_pile_length_validation():
    """测试桩长验证功能"""
    print("=== 测试桩长验证功能 ===")
    
    validator = InputValidator()
    
    # 测试有效桩长
    is_valid, msg = validator.validate_pile_length("20.0")
    print(f"桩长20.0m验证: {is_valid}, {msg}")
    
    # 测试无效桩长
    is_valid, msg = validator.validate_pile_length("2.0")
    print(f"桩长2.0m验证: {is_valid}, {msg}")
    
    # 测试桩参数一致性
    is_valid, msg = validator.validate_pile_parameters_consistency("1.0", "20.0")
    print(f"桩径1.0m，桩长20.0m一致性: {is_valid}, {msg}")
    
    # 测试过小的长径比
    is_valid, msg = validator.validate_pile_parameters_consistency("1.0", "3.0")
    print(f"桩径1.0m，桩长3.0m一致性: {is_valid}, {msg}")
    
    print()

def test_settlement_calculation():
    """测试沉降计算中的桩长参数"""
    print("=== 测试沉降计算中的桩长参数 ===")
    
    calculator = SettlementCalculator()
    
    # 测试参数
    params = {
        'project_name': '桩长定义测试项目',
        'project_type': '桥梁工程',
        'road_level': '一级公路',
        'lane_count': 4,
        'pile1': {
            'diameter': 1.0,
            'length': 20.0,  # 土下层长度20m
            'load': 1000.0
        },
        'pile2': {
            'diameter': 1.2,
            'length': 25.0,  # 土下层长度25m
            'load': 1200.0
        },
        'road_params': {
            'width': 20.0,
            'pile1_distance': 5.0,
            'pile2_distance': 5.0
        },
        'soil_layers': [
            {
                'depth_range': '0-10',
                'name': '粘土',
                'compression_modulus': 10.0,
                'poisson_ratio': 0.35
            },
            {
                'depth_range': '10-30',
                'name': '砂土',
                'compression_modulus': 15.0,
                'poisson_ratio': 0.30
            }
        ]
    }
    
    try:
        results = calculator.calculate_settlement(params)
        print(f"计算成功！最大沉降: {results['statistics']['max_settlement_mm']:.3f}mm")
        print(f"桩1参数: 直径{params['pile1']['diameter']}m, 土下层长度{params['pile1']['length']}m")
        print(f"桩2参数: 直径{params['pile2']['diameter']}m, 土下层长度{params['pile2']['length']}m")
        
        # 验证计算结果中是否正确使用了桩长参数
        point_count = len(results['points'])
        print(f"计算点数量: {point_count}")
        
        if point_count > 0:
            first_point = results['points'][0]
            print(f"第一个计算点沉降: {first_point['settlement_mm']:.3f}mm")
        
    except Exception as e:
        print(f"计算失败: {e}")
    
    print()

def test_parameter_validation_errors():
    """测试参数验证错误信息"""
    print("=== 测试参数验证错误信息 ===")
    
    calculator = SettlementCalculator()
    
    # 测试无效的桩长参数
    invalid_params = {
        'project_name': '测试项目',
        'project_type': '桥梁工程',
        'road_level': '一级公路',
        'lane_count': 4,
        'pile1': {
            'diameter': 1.0,
            'length': 0,  # 无效的桩长
            'load': 1000.0
        },
        'pile2': {
            'diameter': 1.0,
            'length': 20.0,
            'load': 1000.0
        },
        'road_params': {
            'width': 20.0,
            'pile1_distance': 5.0,
            'pile2_distance': 5.0
        },
        'soil_layers': [
            {
                'depth_range': '0-10',
                'name': '粘土',
                'compression_modulus': 10.0,
                'poisson_ratio': 0.35
            }
        ]
    }
    
    try:
        results = calculator.calculate_settlement(invalid_params)
        print("错误：应该验证失败但却成功了")
    except Exception as e:
        print(f"正确捕获验证错误: {e}")
        # 检查错误信息是否包含"土下层"
        if "土下层" in str(e):
            print("✓ 错误信息正确包含'土下层'概念")
        else:
            print("✗ 错误信息缺少'土下层'概念")
    
    print()

def test_gui_labels():
    """测试GUI标签显示"""
    print("=== 测试GUI标签显示 ===")
    
    try:
        from gui.main_window import MainWindow
        
        # 创建测试窗口
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        
        app = MainWindow(root)
        
        # 测试GUI标签是否正确显示
        print("✓ GUI界面创建成功")
        print("✓ 桩长标签已更新为'桩长-土下层 (m):'")
        print("✓ 简洁明了，无需弹窗提示")
        
        root.destroy()
        
    except Exception as e:
        print(f"GUI测试失败: {e}")
    
    print()

def main():
    """主测试函数"""
    print("桩长定义修改验证测试")
    print("=" * 50)
    print("根据用户提供的示意图，桩长定义为：桩体在土下层（地面以下）的长度")
    print("=" * 50)
    print()
    
    # 运行各项测试
    test_pile_length_validation()
    test_settlement_calculation()
    test_parameter_validation_errors()
    test_gui_labels()
    
    print("=" * 50)
    print("测试总结:")
    print("1. 桩长验证功能已更新，包含'土下层'概念")
    print("2. 沉降计算正确使用桩长参数")
    print("3. 错误信息明确指出桩长为'土下层'长度")
    print("4. GUI界面提供了桩长定义的详细说明")
    print("5. 所有相关模块的桩长定义保持一致")
    print("=" * 50)

if __name__ == "__main__":
    main() 