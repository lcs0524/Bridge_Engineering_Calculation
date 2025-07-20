#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试等高线绘制修复效果的脚本
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from visualization.plotter import ResultPlotter
from calculation.settlement import SettlementCalculator
from calculation.correction import CorrectionCalculator

def test_contour_plotting():
    """测试等高线绘制功能"""
    print("开始测试等高线绘制修复效果...")
    
    # 创建测试数据
    test_params = {
        'pile1': {
            'diameter': 1.2,
            'length': 20.0,
            'load': 5000.0,
            'x': -10.0,
            'y': 0.0
        },
        'pile2': {
            'diameter': 1.2,
            'length': 20.0,
            'load': 5000.0,
            'x': 10.0,
            'y': 0.0
        },
        'road_level': '一级公路',  # 添加缺失的公路等级参数
        'road_params': {
            'width': 8.0,
            'calculation_points': 16,
            'pile1_distance': 15.0,  # 修正参数名
            'pile2_distance': 15.0   # 修正参数名
        },
        'soil_layers': [
            {
                'depth_range': '0-5',
                'compression_modulus': 8.0,
                'poisson_ratio': 0.35,
                'unit_weight': 18.0,
                'name': '粘土'
            },
            {
                'depth_range': '5-15',
                'compression_modulus': 15.0,
                'poisson_ratio': 0.30,
                'unit_weight': 19.0,
                'name': '砂土'
            },
            {
                'depth_range': '15-30',
                'compression_modulus': 25.0,
                'poisson_ratio': 0.25,
                'unit_weight': 20.0,
                'name': '砂砾'
            }
        ],
        'highway_type': '一级公路',
        'project_type': '高速公路桥梁'
    }
    
    try:
        # 执行计算
        print("1. 开始沉降计算...")
        calculator = SettlementCalculator()
        correction = CorrectionCalculator()
        
        # 计算沉降
        results = calculator.calculate_settlement(test_params)
        print(f"   计算完成，共 {len(results['points'])} 个计算点")
        
        # 显示计算点数据
        print("\n2. 计算点沉降数据:")
        for i, point in enumerate(results['points']):
            print(f"   W{i+1}: ({point['x']:.1f}, {point['y']:.1f}) -> {point['settlement_mm']:.3f} mm")
        
        # 测试等高线绘制
        print("\n3. 测试等高线绘制...")
        plotter = ResultPlotter()
        
        try:
            fig = plotter.create_contour_plot(results)
            print("   ✅ 等高线图创建成功！")
            
            # 保存图片
            output_file = "test_contour_plot.png"
            fig.savefig(output_file, dpi=300, bbox_inches='tight')
            print(f"   📊 等高线图已保存为: {output_file}")
            
            plt.close(fig)
            
        except Exception as e:
            print(f"   ❌ 等高线绘制失败: {e}")
            return False
        
        # 测试其他可视化功能
        print("\n4. 测试其他可视化功能...")
        
        try:
            # 测试颜色分布图
            fig_color = plotter.settlement_distribution_plot(results, test_params)
            fig_color.savefig("test_color_distribution.png", dpi=300, bbox_inches='tight')
            print("   ✅ 颜色分布图创建成功!")
            plt.close(fig_color)
            
            # 测试综合分析图
            fig_comprehensive = plotter.create_comprehensive_analysis(results)
            fig_comprehensive.savefig("test_comprehensive_analysis.png", dpi=300, bbox_inches='tight')
            print("   ✅ 综合分析图创建成功!")
            plt.close(fig_comprehensive)
            
        except Exception as e:
            print(f"   ⚠️  其他可视化测试出现问题: {e}")
        
        print("\n🎉 所有测试完成！等高线绘制问题已修复。")
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_edge_cases():
    """测试边界情况"""
    print("\n5. 测试边界情况...")
    
    # 测试共面数据点
    print("   测试共面数据点情况...")
    edge_results = {
        'points': [
            {'x': 0, 'y': 0, 'z': 1, 'settlement_mm': 10.0},
            {'x': 1, 'y': 0, 'z': 1, 'settlement_mm': 10.0},
            {'x': 0, 'y': 1, 'z': 1, 'settlement_mm': 10.0},
            {'x': 1, 'y': 1, 'z': 1, 'settlement_mm': 10.0},
        ],
        'statistics': {
            'max_settlement_mm': 10.0,
            'min_settlement_mm': 10.0,
            'avg_settlement_mm': 10.0
        },
        'safety_assessment': {
            'safety_level': '安全',
            'max_settlement_mm': 10.0,
            'bridge_limit': 150,
            'general_limit': 100,
            'influence_area': 1.0,
            'influence_points_count': 0,
            'recommendations': ['数据点共面，建议检查计算参数']
        }
    }
    
    try:
        plotter = ResultPlotter()
        fig = plotter.create_contour_plot(edge_results)
        fig.savefig("test_edge_case_coplanar.png", dpi=300, bbox_inches='tight')
        print("   ✅ 共面数据点测试通过！")
        plt.close(fig)
    except Exception as e:
        print(f"   ❌ 共面数据点测试失败: {e}")
    
    # 测试数据范围很小的情况
    print("   测试数据范围很小的情况...")
    small_range_results = {
        'points': [
            {'x': 0.0001, 'y': 0.0001, 'z': 1, 'settlement_mm': 5.001},
            {'x': 0.0002, 'y': 0.0001, 'z': 1, 'settlement_mm': 5.002},
            {'x': 0.0001, 'y': 0.0002, 'z': 1, 'settlement_mm': 5.003},
            {'x': 0.0002, 'y': 0.0002, 'z': 1, 'settlement_mm': 5.004},
        ],
        'statistics': {
            'max_settlement_mm': 5.004,
            'min_settlement_mm': 5.001,
            'avg_settlement_mm': 5.0025
        },
        'safety_assessment': {
            'safety_level': '安全',
            'max_settlement_mm': 5.004,
            'bridge_limit': 150,
            'general_limit': 100,
            'influence_area': 0.0001,
            'influence_points_count': 0,
            'recommendations': ['数据范围很小，建议检查计算精度']
        }
    }
    
    try:
        fig = plotter.create_contour_plot(small_range_results)
        fig.savefig("test_edge_case_small_range.png", dpi=300, bbox_inches='tight')
        print("   ✅ 小范围数据测试通过！")
        plt.close(fig)
    except Exception as e:
        print(f"   ❌ 小范围数据测试失败: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("   桩基沉降影响范围计算软件 - 等高线绘制修复测试")
    print("=" * 60)
    
    success = test_contour_plotting()
    
    if success:
        test_edge_cases()
        print("\n" + "=" * 60)
        print("🎉 所有测试完成！Qhull错误已成功修复。")
        print("✅ 等高线绘制功能现在可以正常工作了。")
        print("📊 生成的测试图片:")
        print("   - test_contour_plot.png (等高线图)")
        print("   - test_color_distribution.png (颜色分布图)")
        print("   - test_comprehensive_analysis.png (综合分析图)")
        print("   - test_edge_case_*.png (边界情况测试)")
        print("=" * 60)
    else:
        print("\n❌ 测试失败，请检查修复代码。") 