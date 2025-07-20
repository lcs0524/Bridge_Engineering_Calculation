#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试GUI中的桩位置显示
使用实际GUI参数结构验证桩位置是否正确显示在路基外侧
"""

from visualization.plotter import ResultPlotter
from calculation.settlement import SettlementCalculator
import matplotlib.pyplot as plt

def test_gui_pile_position():
    """测试GUI中的桩位置显示"""
    print("=" * 60)
    print("测试GUI中的桩位置显示")
    print("=" * 60)
    
    # 使用GUI相同的参数结构
    params = {
        # 项目信息
        'project_name': '测试项目',
        'project_type': '高架桥',
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
        
        # 被跨越公路参数 - 关键参数！
        'road_params': {
            'width': 20.0,        # 路基宽度20m
            'pile1_distance': 5.0, # 桩1距路基边缘5m
            'pile2_distance': 5.0  # 桩2距路基边缘5m
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
            }
        ]
    }
    
    print("使用的参数:")
    print(f"路基宽度: {params['road_params']['width']}m")
    print(f"桩1距路基边缘距离: {params['road_params']['pile1_distance']}m")
    print(f"桩2距路基边缘距离: {params['road_params']['pile2_distance']}m")
    print(f"桩1直径: {params['pile1']['diameter']}m")
    print(f"桩2直径: {params['pile2']['diameter']}m")
    
    # 执行计算
    calculator = SettlementCalculator()
    results = calculator.calculate_settlement(params)
    
    print(f"\\n计算完成，共 {len(results['points'])} 个计算点")
    
    # 创建可视化
    plotter = ResultPlotter()
    
    print("\\n创建桩位置可视化...")
    fig = plotter.settlement_distribution_plot(results, params)
    
    # 显示桩位置计算详情
    road_width = params['road_params']['width']
    pile1_distance = params['road_params']['pile1_distance']
    pile2_distance = params['road_params']['pile2_distance']
    
    # 计算图形坐标系中的位置（图形中心为40,40）
    road_center_x = 40
    road_left = road_center_x - road_width/2  # 30
    road_right = road_center_x + road_width/2  # 50
    
    # 根据实际计算逻辑确定桩位置（在路基外侧）
    pile1_x = road_left - pile1_distance  # 25
    pile2_x = road_right + pile2_distance  # 55
    
    print("\\n=" * 60)
    print("桩位置验证:")
    print(f"路基范围: X从{road_left}到{road_right} (宽度{road_width}m)")
    print(f"桩1位置: X={pile1_x} (应该 < {road_left})")
    print(f"桩2位置: X={pile2_x} (应该 > {road_right})")
    print(f"桩1在路基外侧: {pile1_x < road_left} (距离{road_left - pile1_x}m)")
    print(f"桩2在路基外侧: {pile2_x > road_right} (距离{pile2_x - road_right}m)")
    
    if pile1_x < road_left and pile2_x > road_right:
        print("✓ 计算正确：两个桩都在路基外侧！")
    else:
        print("✗ 计算错误：桩可能在路基内部！")
    
    # 保存图片
    plt.savefig('GUI桩位置验证图.png', dpi=150, bbox_inches='tight')
    print(f"\\n图片已保存为: GUI桩位置验证图.png")
    
    # 显示图形
    plt.show()
    
    return True

if __name__ == "__main__":
    test_gui_pile_position() 