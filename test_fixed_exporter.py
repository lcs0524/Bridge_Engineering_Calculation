#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试修复后的原版ResultExporter
"""

import os
import sys
import traceback

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from utils.exporter import ResultExporter
from calculation.settlement import SettlementCalculator

def test_fixed_exporter():
    """测试修复后的原版exporter"""
    print("=== 测试修复后的原版ResultExporter ===")
    
    try:
        # 创建计算器
        calculator = SettlementCalculator()
        
        # 设置输入参数
        input_params = {
            'pile1': {
                'diameter': 1.2,
                'length': 30.0,
                'load': 8000.0
            },
            'pile2': {
                'diameter': 1.0,
                'length': 25.0,
                'load': 6000.0
            },
            'road_level': '高速公路',
            'road_params': {
                'width': 12.0,
                'pile1_distance': 5.0,
                'pile2_distance': 5.0
            },
            'soil_layers': [
                {
                    'depth_range': '0-5',
                    'name': '粉质粘土',
                    'compression_modulus': 8.5,
                    'poisson_ratio': 0.35
                },
                {
                    'depth_range': '5-10',
                    'name': '砂土',
                    'compression_modulus': 15.0,
                    'poisson_ratio': 0.30
                }
            ]
        }
        
        print("✓ 输入参数设置完成")
        
        # 执行计算
        print("正在执行计算...")
        results = calculator.calculate_settlement(input_params)
        print(f"✓ 计算完成，包含 {len(results['points'])} 个计算点")
        
        # 创建原版导出器
        exporter = ResultExporter()
        print("✓ 原版ResultExporter创建成功")
        
        # 测试导出
        output_file = "fixed_export_report.xlsx"
        print(f"正在导出到文件: {output_file}")
        
        success, message = exporter.export_to_excel(results, output_file)
        
        if success:
            print(f"✓ Excel导出成功: {message}")
            
            # 检查文件
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                print(f"✓ 文件大小: {file_size} 字节")
                
                # 验证文件完整性
                try:
                    import pandas as pd
                    excel_file = pd.ExcelFile(output_file)
                    sheet_names = excel_file.sheet_names
                    print(f"✓ Excel工作表: {sheet_names}")
                    
                    # 验证每个工作表
                    for sheet_name in sheet_names:
                        df = pd.read_excel(output_file, sheet_name=sheet_name)
                        print(f"✓ {sheet_name}: {len(df)} 行数据")
                    
                    print("前3行计算结果预览:")
                    df_results = pd.read_excel(output_file, sheet_name='计算结果')
                    print(df_results.head(3))
                    
                except Exception as e:
                    print(f"✗ Excel文件验证失败: {e}")
                    return False
            else:
                print("✗ 文件未创建")
                return False
        else:
            print(f"✗ Excel导出失败: {message}")
            return False
        
        print(f"\n✓ 测试完成，文件保存在: {os.path.abspath(output_file)}")
        print("请尝试用Excel打开此文件验证是否正常")
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_fixed_exporter() 