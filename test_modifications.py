#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修改后的双桩计算功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from calculation.settlement import SettlementCalculator
from visualization.plotter import ResultPlotter

def test_dual_pile_calculation():
    """测试双桩计算功能"""
    
    # 创建计算器
    calculator = SettlementCalculator()
    plotter = ResultPlotter()
    
    # 设置测试参数
    test_params = {
        'project_name': '测试项目 - 高架桥双桩沉降分析',
        'project_type': '桥梁工程',
        'road_level': '一级公路',
        'lane_count': 4,
        
        # 桩1参数
        'pile1': {
            'diameter': 1.0,
            'length': 20.0,
            'load': 1000.0
        },
        
        # 桩2参数
        'pile2': {
            'diameter': 1.2,
            'length': 25.0,
            'load': 1200.0
        },
        
        # 被跨越公路参数
        'road_params': {
            'width': 12.0,
            'pile1_distance': 5.0,
            'pile2_distance': 8.0
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
    
    try:
        print("开始双桩沉降计算测试...")
        
        # 执行计算
        results = calculator.calculate_settlement(test_params)
        
        print(f"✅ 计算成功完成")
        print(f"项目名称: {results['input_parameters']['project_name']}")
        print(f"公路类型: {results['input_parameters']['road_level']}")
        print(f"计算点数: {len(results['points'])} 个")
        print(f"最大沉降: {results['statistics']['max_settlement_mm']:.3f} mm")
        print(f"最小沉降: {results['statistics']['min_settlement_mm']:.3f} mm")
        print(f"平均沉降: {results['statistics']['avg_settlement_mm']:.3f} mm")
        print(f"安全等级: {results['safety_assessment']['safety_level']}")
        
        # 测试颜色分布图
        print("\n开始颜色分布图测试...")
        fig = plotter.settlement_distribution_plot(results, test_params)
        print("✅ 颜色分布图创建成功")
        
        # 测试沉降分析图
        print("\n开始沉降分析图测试...")
        fig2 = plotter.create_settlement_plot(results)
        print("✅ 沉降分析图创建成功")
        
        # 显示前5个计算点的详细结果
        print("\n前5个计算点的结果:")
        print("点号\tX坐标\tY坐标\t深度\t桩1沉降\t桩2沉降\t总沉降")
        for i, point in enumerate(results['points'][:5]):
            print(f"{point['point_id']}\t{point['x']:.1f}\t{point['y']:.1f}\t{point['z']:.1f}\t"
                  f"{point['pile1_settlement']*1000:.2f}\t{point['pile2_settlement']*1000:.2f}\t"
                  f"{point['settlement_mm']:.2f}")
        
        print("\n✅ 所有测试通过！双桩计算系统工作正常。")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_dual_pile_calculation() 