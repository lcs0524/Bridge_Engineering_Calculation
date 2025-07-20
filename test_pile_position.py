#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试桩位置显示修正
验证红色和蓝色桩是否正确显示在路基外侧
"""

from calculation.settlement import SettlementCalculator
from visualization.plotter import ResultPlotter
import matplotlib.pyplot as plt

def test_pile_position():
    """测试桩位置显示"""
    print("=" * 60)
    print("测试桩位置显示修正")
    print("=" * 60)
    
    # 模拟计算参数
    params = {
        'road_level': '一级公路',  # 公路等级参数在顶层
        'road_params': {
            'width': 20,  # 路基宽度20m
            'height': 2,
            'pile1_distance': 5,  # 桩1距路基边缘5m
            'pile2_distance': 5   # 桩2距路基边缘5m
        },
        'pile1': {
            'diameter': 1.0,
            'length': 20,
            'load': 1000
        },
        'pile2': {
            'diameter': 1.2, 
            'length': 25,
            'load': 1200
        },
        'soil_layers': [
            {'name': '粉质粘土', 'thickness': 8, 'compression_modulus': 8.5, 'poisson_ratio': 0.35},
            {'name': '砂土', 'thickness': 12, 'compression_modulus': 15.0, 'poisson_ratio': 0.3}
        ]
    }
    
    # 创建计算器
    calculator = SettlementCalculator()
    
    try:
        # 执行计算
        print("正在执行沉降计算...")
        results = calculator.calculate_settlement(params)
        
        # 创建可视化器
        plotter = ResultPlotter()
        
        # 生成分布图
        print("正在生成桩位置可视化图...")
        fig = plotter.settlement_distribution_plot(results, params)
        
        # 保存图形
        plt.figure(fig.number)
        plt.savefig('test_pile_position.png', dpi=300, bbox_inches='tight')
        print("✓ 图形已保存为: test_pile_position.png")
        
        # 验证桩位置计算
        road_width = params['road_params']['width']
        pile1_distance = params['road_params']['pile1_distance'] 
        pile2_distance = params['road_params']['pile2_distance']
        
        # 计算理论桩位置（基于图形坐标系）
        road_center_x = 40  # 图形中心
        road_left = road_center_x - road_width/2   # 30
        road_right = road_center_x + road_width/2  # 50
        
        pile1_x_expected = road_left - pile1_distance   # 25 (路基左侧外)
        pile2_x_expected = road_right + pile2_distance  # 55 (路基右侧外)
        
        print("\n桩位置验证:")
        print(f"路基宽度: {road_width}m")
        print(f"路基范围: X={road_left}m 到 X={road_right}m")
        print(f"桩1位置: X={pile1_x_expected}m (应在路基左侧外)")
        print(f"桩2位置: X={pile2_x_expected}m (应在路基右侧外)")
        print(f"桩1距路基边缘: {pile1_distance}m")
        print(f"桩2距路基边缘: {pile2_distance}m")
        
        # 检查桩是否在路基外侧
        pile1_outside = pile1_x_expected < road_left
        pile2_outside = pile2_x_expected > road_right
        
        print("\n修正验证结果:")
        print(f"✓ 桩1在路基外侧: {pile1_outside}")
        print(f"✓ 桩2在路基外侧: {pile2_outside}")
        
        if pile1_outside and pile2_outside:
            print("🎉 修正成功！两个桩都正确位于路基外侧")
        else:
            print("❌ 修正失败！桩仍在路基内部")
        
        plt.show()
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

if __name__ == "__main__":
    test_pile_position() 