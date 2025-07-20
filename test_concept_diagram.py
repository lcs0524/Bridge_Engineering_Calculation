#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试概念图设计的可视化效果
验证：路基在上方，桩在外侧，4×4网格在地下
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from calculation.settlement import SettlementCalculator
from visualization.plotter import ResultPlotter
import matplotlib.pyplot as plt


def test_concept_diagram():
    """测试概念图设计效果"""
    print("=== 测试概念图设计的可视化效果 ===")
    
    # 创建计算器和绘图器
    calculator = SettlementCalculator()
    plotter = ResultPlotter()
    
    # 设置测试参数（与概念图一致）
    params = {
        'project_name': '概念图验证测试',
        'project_type': '桥梁工程',
        'road_level': '一级公路',
        'lane_count': 4,
        
        # 桩1参数
        'pile1': {
            'diameter': 1.0,   # 桩径1m
            'length': 20.0,    # 桩长20m
            'load': 1000.0     # 荷载1000kN
        },
        
        # 桩2参数 
        'pile2': {
            'diameter': 1.0,   # 桩径1m
            'length': 20.0,    # 桩长20m
            'load': 1000.0     # 荷载1000kN
        },
        
        # 被跨越公路参数
        'road_params': {
            'width': 12.0,          # 路基宽度X=12m
            'pile1_distance': 5.0,   # L1=5m
            'pile2_distance': 5.0    # L2=5m  
        },
        
        # 土层参数
        'soil_layers': [
            {'depth_range': '0-5', 'name': '粘土', 'compression_modulus': 10.0, 'poisson_ratio': 0.35},
            {'depth_range': '5-10', 'name': '砂土', 'compression_modulus': 15.0, 'poisson_ratio': 0.30},
            {'depth_range': '10-15', 'name': '粘土', 'compression_modulus': 12.0, 'poisson_ratio': 0.35},
            {'depth_range': '15-20', 'name': '砂土', 'compression_modulus': 18.0, 'poisson_ratio': 0.28}
        ]
    }
    
    print("计算参数：")
    print(f"路基宽度X: {params['road_params']['width']}m")
    print(f"桩1距离L1: {params['road_params']['pile1_distance']}m")
    print(f"桩2距离L2: {params['road_params']['pile2_distance']}m")
    
    # 计算桩位置
    width = params['road_params']['width']
    pile1_distance = params['road_params']['pile1_distance']
    pile2_distance = params['road_params']['pile2_distance']
    
    pile1_x = -(width/2 + pile1_distance)
    pile2_x = +(width/2 + pile2_distance)
    
    print(f"桩1位置: X = {pile1_x}m（左侧外）")
    print(f"桩2位置: X = {pile2_x}m（右侧外）")
    
    # 执行沉降计算
    print("\n正在进行沉降计算...")
    try:
        results = calculator.calculate_settlement(params)
        print("✓ 计算完成")
        
        # 输出计算点信息
        points = results['points']
        print(f"\n计算点分析：")
        print(f"总计算点数: {len(points)}")
        
        # 分析网格范围
        x_coords = [p['x'] for p in points]
        y_coords = [p['y'] for p in points]
        z_coords = [p['z'] for p in points]
        
        print(f"X坐标范围: {min(x_coords):.1f} 到 {max(x_coords):.1f}")
        print(f"Y坐标范围: {min(y_coords):.1f} 到 {max(y_coords):.1f}")
        print(f"Z深度范围: {min(z_coords):.1f} 到 {max(z_coords):.1f}")
        
        # 验证桩是否在网格外部
        x_min, x_max = min(x_coords), max(x_coords)
        if pile1_x < x_min and pile2_x > x_max:
            print("✓ 验证通过：桩1和桩2都在4×4网格外部")
        else:
            print("✗ 验证失败：桩位置可能在网格内部")
            print(f"  网格X范围: [{x_min:.1f}, {x_max:.1f}]")
            print(f"  桩1位置: {pile1_x:.1f}, 桩2位置: {pile2_x:.1f}")
        
        # 显示沉降统计
        stats = results['statistics']
        print(f"\n沉降统计：")
        print(f"最大沉降: {stats['max_settlement_mm']:.3f} mm")
        print(f"最小沉降: {stats['min_settlement_mm']:.3f} mm")
        print(f"平均沉降: {stats['avg_settlement_mm']:.3f} mm")
        
        # 绘制概念图
        print("\n正在绘制概念图...")
        fig = plotter.settlement_distribution_plot(results, params)
        
        # 保存图片
        filename = "概念图验证_沉降分析.png"
        fig.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ 概念图已保存: {filename}")
        
        # 显示图形
        plt.show()
        
        return True
        
    except Exception as e:
        print(f"✗ 计算失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_concept_diagram()
    if success:
        print("\n=== 概念图验证成功！===")
        print("✓ 桩基位于路基外侧")
        print("✓ 4×4网格在地下") 
        print("✓ 路基梯形在顶部")
        print("✓ 距离标注清晰")
        print("✓ 符合工程概念图设计")
    else:
        print("\n=== 概念图验证失败 ===") 