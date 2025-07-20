#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
最终测试：验证main.py中调用的Excel导出功能
"""

import os
import sys
import traceback

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 模拟main.py中的导入和调用
from calculation.settlement import SettlementCalculator
from utils.exporter import ResultExporter

def simulate_main_export():
    """模拟main.py中的导出流程"""
    print("=== 模拟main.py中的Excel导出流程 ===")
    
    try:
        # 模拟从GUI获取的参数（与main.py中MainWindow.get_input_parameters一致）
        params = {
            # 项目信息
            'project_name': '高架桥桩基沉降分析项目',
            'project_type': '桥梁工程',
            'road_level': '高速公路',
            'lane_count': 4,
            
            # 桩1参数
            'pile1': {
                'diameter': 1.2,
                'length': 30.0,
                'load': 8000.0
            },
            
            # 桩2参数  
            'pile2': {
                'diameter': 1.0,
                'length': 25.0,
                'load': 6000.0
            },
            
            # 被跨越公路参数
            'road_params': {
                'width': 12.0,
                'pile1_distance': 5.0,
                'pile2_distance': 5.0
            },
            
            # 土层参数
            'soil_layers': [
                {
                    'depth_range': '0-5',
                    'name': '粘土',
                    'compression_modulus': 10.0,
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
        
        print("✓ 输入参数准备完成（模拟GUI输入）")
        
        # 步骤1: 执行计算（模拟MainWindow.run_calculation）
        print("1. 执行沉降计算...")
        calculator = SettlementCalculator()
        calculation_results = calculator.calculate_settlement(params)
        print(f"   ✓ 计算完成，获得 {len(calculation_results['points'])} 个计算点")
        
        # 步骤2: 执行导出（模拟MainWindow.export_report）
        print("2. 执行Excel导出...")
        exporter = ResultExporter()
        
        # 模拟用户选择文件名
        filename = "main_export_test.xlsx"
        print(f"   导出文件: {filename}")
        
        # 调用导出方法（与main.py中完全一致）
        success, message = exporter.export_to_excel(calculation_results, filename)
        
        if success:
            print(f"   ✓ 导出成功: {message}")
            
            # 验证文件
            if os.path.exists(filename):
                file_size = os.path.getsize(filename)
                print(f"   ✓ 文件大小: {file_size} 字节")
                
                # 详细验证
                try:
                    import pandas as pd
                    excel_file = pd.ExcelFile(filename)
                    sheet_names = excel_file.sheet_names
                    print(f"   ✓ 工作表: {sheet_names}")
                    
                    # 验证每个工作表
                    for sheet_name in sheet_names:
                        df = pd.read_excel(filename, sheet_name=sheet_name)
                        print(f"   ✓ {sheet_name}: {len(df)} 行")
                    
                    print(f"\n3. 验证数据内容:")
                    df_results = pd.read_excel(filename, sheet_name='计算结果')
                    print(f"   计算结果表: {len(df_results)} 行 × {len(df_results.columns)} 列")
                    print(f"   列名: {list(df_results.columns)}")
                    print(f"   沉降值范围: {df_results['沉降值(mm)'].min():.2f} ~ {df_results['沉降值(mm)'].max():.2f} mm")
                    
                    # 显示前3行
                    print("\n   前3行数据:")
                    print(df_results[['计算点', 'X坐标(m)', 'Y坐标(m)', '沉降值(mm)', '对应土层']].head(3))
                    
                except Exception as e:
                    print(f"   ✗ 文件验证失败: {e}")
                    return False
            else:
                print("   ✗ 文件未创建")
                return False
        else:
            print(f"   ✗ 导出失败: {message}")
            return False
        
        print(f"\n=== 测试完成 ===")
        print(f"✅ main.py中的Excel导出功能现在可以正常工作")
        print(f"📁 测试文件: {os.path.abspath(filename)}")
        print(f"💡 用户可以正常使用main.py中的'导出报告'功能")
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        traceback.print_exc()
        return False

def check_export_workflow():
    """检查完整的导出工作流"""
    print("\n=== 导出工作流检查 ===")
    
    # 检查关键组件
    components = [
        ('calculation.settlement', 'SettlementCalculator'),
        ('utils.exporter', 'ResultExporter'),
        ('gui.main_window', 'MainWindow')
    ]
    
    for module_name, class_name in components:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"✓ {module_name}.{class_name} - 可用")
        except Exception as e:
            print(f"✗ {module_name}.{class_name} - 错误: {e}")
    
    print("✓ 所有组件检查完成")

if __name__ == "__main__":
    # 检查组件
    check_export_workflow()
    
    # 执行主测试
    simulate_main_export() 