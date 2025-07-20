#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试Excel导出功能修复 - 模拟真实数据
"""

import os
import sys
import traceback

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from utils.exporter import ResultExporter

def create_mock_calculation_results():
    """创建模拟的计算结果数据"""
    # 模拟计算结果结构，确保包含所有必要的键
    results = {
        'points': [],
        'safety_assessment': {
            'safety_level': '安全',
            'max_settlement_mm': 15.23,
            'general_limit': 100,
            'bridge_limit': 150,
            'approach_limit': 50,
            'exceed_general': False,
            'exceed_bridge': False,
            'exceed_approach': False,
            'influence_area': 2500.0,
            'influence_points_count': 8,
            'warning_points_count': 0,
            'danger_points_count': 0,
            'safety_statistics': {
                'safe_points': 16,
                'influence_points': 8,
                'warning_points': 0,
                'danger_points': 0
            },
            'recommendations': [
                '加强施工监测',
                '控制施工荷载'
            ],
            'compliance_analysis': {
                'meets_general_standard': True,
                'meets_bridge_standard': True,
                'meets_approach_standard': True,
                'overall_compliance': True
            }
        },
        'statistics': {
            'max_settlement_mm': 15.23,
            'min_settlement_mm': 1.12,
            'avg_settlement_mm': 8.45
        },
        'input_parameters': {
            'project_name': '测试项目',
            'project_type': '桥梁工程',
            'road_level': '高速公路',
            'pile_diameter': 1.2,
            'pile_length': 30.0,
            'load': 8000.0,
            'road_params': {
                'width': 12.0,
                'pile1_distance': 5.0,
                'pile2_distance': 5.0
            },
            'soil_layers': [
                {
                    'depth_range': '0-5m',
                    'name': '粉质粘土',
                    'compression_modulus': 8.5,
                    'poisson_ratio': 0.35
                },
                {
                    'depth_range': '5-10m',
                    'name': '砂土',
                    'compression_modulus': 15.0,
                    'poisson_ratio': 0.30
                }
            ]
        }
    }
    
    # 生成16个计算点的数据
    for i in range(16):
        x = (i % 4) * 5.0  # X坐标: 0, 5, 10, 15
        y = (i // 4) * 5.0  # Y坐标: 0, 5, 10, 15
        z = 2.0 + i * 0.5   # 深度递增
        
        point = {
            'point_id': f'P{i+1:02d}',
            'x': x,
            'y': y,
            'z': z,
            'distance': ((x-10)**2 + (y-10)**2)**0.5,  # 距离中心的距离
            'settlement_mm': 15.23 - i * 0.8,  # 沉降值递减
            'influence_factor': 0.95 - i * 0.05,
            'sigma_z': 120.0 - i * 5.0,
            'tau_xz': 15.0 - i * 0.8,
            'tau_yz': 12.0 - i * 0.6,
            'pile1_settlement': (15.23 - i * 0.8) * 0.6 / 1000,  # 转换为m
            'pile2_settlement': (15.23 - i * 0.8) * 0.4 / 1000,  # 转换为m
            'interaction_factor': 0.85 - i * 0.02,
            'soil_properties': {
                'name': '粉质粘土' if i < 8 else '砂土',
                'depth_range': '0-5m' if i < 8 else '5-10m'
            }
        }
        results['points'].append(point)
    
    return results

def test_excel_export():
    """测试Excel导出功能"""
    print("=== Excel导出功能测试 ===")
    
    try:
        # 创建导出器
        exporter = ResultExporter()
        print("✓ ResultExporter 创建成功")
        
        # 创建模拟数据
        results = create_mock_calculation_results()
        print(f"✓ 模拟计算结果创建成功，包含 {len(results['points'])} 个计算点")
        
        # 测试导出
        output_file = "test_export_report.xlsx"
        print(f"正在导出到文件: {output_file}")
        
        exporter.export_to_excel(results, output_file)
        print("✓ Excel文件导出成功")
        
        # 检查文件是否存在
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"✓ 文件创建成功，大小: {file_size} 字节")
            
            # 尝试用pandas读取验证文件完整性
            try:
                import pandas as pd
                df = pd.read_excel(output_file, sheet_name='计算结果')
                print(f"✓ Excel文件验证成功，包含 {len(df)} 行数据")
                print("  前几行数据预览:")
                print(df.head(3))
                
            except Exception as e:
                print(f"✗ Excel文件验证失败: {e}")
                return False
                
        else:
            print("✗ 文件未创建")
            return False
            
        print("\n=== 测试完成 ===")
        print(f"测试文件保存在: {os.path.abspath(output_file)}")
        return True
        
    except Exception as e:
        print(f"✗ Excel导出测试失败: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_excel_export() 