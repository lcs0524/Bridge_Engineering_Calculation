#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
使用调试版本的exporter测试真实计算结果的Excel导出
"""

import os
import sys
import traceback

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from utils.exporter_debug import ResultExporterDebug
from calculation.settlement import SettlementCalculator

def create_real_calculation():
    """创建真实的计算结果"""
    print("=== 创建真实计算结果 ===")
    
    try:
        # 创建计算器
        calculator = SettlementCalculator()
        
        # 设置输入参数（按照SettlementCalculator的要求）
        input_params = {
            'pile1': {
                'diameter': 1.2,  # 桩径(m)
                'length': 30.0,   # 桩长(m)
                'load': 8000.0    # 荷载(kN)
            },
            'pile2': {
                'diameter': 1.0,  # 桩径(m)
                'length': 25.0,   # 桩长(m)
                'load': 6000.0    # 荷载(kN)
            },
            'road_level': '高速公路',
            'road_params': {
                'width': 12.0,           # 路基宽度(m)
                'pile1_distance': 5.0,   # 路基与桩1距离(m)
                'pile2_distance': 5.0    # 路基与桩2距离(m)
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
                },
                {
                    'depth_range': '10-15',
                    'name': '粘土',
                    'compression_modulus': 12.0,
                    'poisson_ratio': 0.35
                },
                {
                    'depth_range': '15-20',
                    'name': '砂土',
                    'compression_modulus': 18.0,
                    'poisson_ratio': 0.28
                }
            ]
        }
        
        print(f"✓ 输入参数设置完成")
        print(f"  - 桩1: 直径{input_params['pile1']['diameter']}m, 长度{input_params['pile1']['length']}m, 荷载{input_params['pile1']['load']}kN")
        print(f"  - 桩2: 直径{input_params['pile2']['diameter']}m, 长度{input_params['pile2']['length']}m, 荷载{input_params['pile2']['load']}kN")
        print(f"  - 路基宽度: {input_params['road_params']['width']} m")
        print(f"  - 土层数量: {len(input_params['soil_layers'])}")
        
        # 执行计算
        print("正在执行计算...")
        results = calculator.calculate_settlement(input_params)
        
        print(f"✓ 计算完成")
        print(f"  - 计算点数量: {len(results.get('points', []))}")
        print(f"  - 结果数据键: {list(results.keys())}")
        
        return results
        
    except Exception as e:
        print(f"✗ 创建真实计算结果失败: {e}")
        traceback.print_exc()
        return None

def test_real_excel_export():
    """测试真实计算结果的Excel导出"""
    print("\n=== 测试真实Excel导出 ===")
    
    try:
        # 创建真实计算结果
        results = create_real_calculation()
        if not results:
            print("✗ 无法获取计算结果，测试终止")
            return False
        
        # 创建调试版本导出器
        exporter = ResultExporterDebug()
        print("✓ 调试版导出器创建成功")
        
        # 测试导出
        output_file = "debug_export_report.xlsx"
        print(f"\n正在导出到文件: {output_file}")
        print("-" * 50)
        
        success, message = exporter.export_to_excel(results, output_file)
        
        print("-" * 50)
        
        if success:
            print(f"✓ Excel导出成功: {message}")
            
            # 检查文件
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                print(f"✓ 文件大小: {file_size} 字节")
                
                # 尝试用pandas验证
                try:
                    import pandas as pd
                    
                    # 读取所有工作表
                    excel_file = pd.ExcelFile(output_file)
                    sheet_names = excel_file.sheet_names
                    print(f"✓ Excel工作表: {sheet_names}")
                    
                    # 验证计算结果表
                    df_results = pd.read_excel(output_file, sheet_name='计算结果')
                    print(f"✓ 计算结果表: {len(df_results)} 行数据")
                    
                    # 显示前几行
                    print("前3行数据预览:")
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
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_real_excel_export() 