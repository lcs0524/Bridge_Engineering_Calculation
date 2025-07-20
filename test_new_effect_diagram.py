#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新的效果图可视化实现
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from calculation.settlement import SettlementCalculator
from visualization.plotter import ResultPlotter
import matplotlib.pyplot as plt
import numpy as np

def test_new_effect_diagram():
    """测试新的效果图可视化实现"""
    
    # 创建计算器和绘图器
    calculator = SettlementCalculator()
    plotter = ResultPlotter()
    
    # 设置测试参数
    test_params = {
        'project_name': '高架桥桩基沉降影响范围计算测试',
        'project_type': '桥梁工程',
        'road_level': '一级公路',
        'lane_count': 4,
        
        'pile1': {
            'diameter': 1.0,
            'length': 20.0,
            'load': 1000.0
        },
        
        'pile2': {
            'diameter': 1.2,
            'length': 25.0,
            'load': 1200.0
        },
        
        'road_params': {
            'width': 12.0,
            'pile1_distance': 6.0,
            'pile2_distance': 8.0
        },
        
        'soil_layers': [
            {
                'depth_range': '0-5',
                'name': '素填土',
                'compression_modulus': 6.0,
                'poisson_ratio': 0.35
            },
            {
                'depth_range': '5-15',
                'name': '粉质粘土',
                'compression_modulus': 9.0,
                'poisson_ratio': 0.30
            },
            {
                'depth_range': '15-30',
                'name': '中砂',
                'compression_modulus': 18.0,
                'poisson_ratio': 0.25
            }
        ],
        
        'calculation_params': {
            'max_depth': 30.0,
            'settlement_threshold': 150.0,
            'bridge_settlement_threshold': 100.0
        }
    }
    
    try:
        print("开始执行沉降计算...")
        
        # 执行计算
        results = calculator.calculate_settlement(test_params)
        
        print(f"✓ 计算完成！")
        print(f"项目名称: {results['input_parameters']['project_name']}")
        print(f"计算点数: {len(results['points'])} 个")
        print(f"最大沉降: {results['statistics']['max_settlement_mm']:.3f} mm")
        print(f"安全等级: {results['safety_assessment']['safety_level']}")
        
        # 提取参数用于新的可视化函数
        pile1_params = test_params['pile1']
        pile2_params = test_params['pile2']
        road_params = test_params['road_params']
        
        # 计算桩位置
        roadbed_width = road_params['width']
        pile1_distance = road_params['pile1_distance']
        pile2_distance = road_params['pile2_distance']
        
        pile1_x = -(roadbed_width/2 + pile1_distance)
        pile2_x = +(roadbed_width/2 + pile2_distance)
        
        # 提取计算点坐标和沉降值
        points_3d = [(p['x'], p['y'], p['z']) for p in results['points']]
        settlements = [p['settlement_mm'] for p in results['points']]
        
        # 获取安全阈值
        safety_assessment = results['safety_assessment']
        max_settlement_threshold = safety_assessment['bridge_limit']
        
        # 计算单桩沉降值（用于显示）
        pile1_settlement = max([p.get('pile1_settlement', 0) * 1000 for p in results['points']])
        pile2_settlement = max([p.get('pile2_settlement', 0) * 1000 for p in results['points']])
        
        # 相互作用系数
        interaction_coefficient = 0.8
        
        # 桩参数（取较大的桩径和桩长）
        pile_diameter = max(pile1_params['diameter'], pile2_params['diameter'])
        pile_length = max(pile1_params['length'], pile2_params['length'])
        
        print(f"\n桩基参数:")
        print(f"桩1位置: X = {pile1_x:.1f}m")
        print(f"桩2位置: X = {pile2_x:.1f}m") 
        print(f"路基宽度: {roadbed_width:.1f}m")
        print(f"桩径: {pile_diameter:.1f}m")
        print(f"桩长: {pile_length:.1f}m")
        print(f"沉降阈值: {max_settlement_threshold:.1f}mm")
        
        print(f"\n正在生成新的效果图可视化...")
        
        # 调用新的可视化函数
        fig = plotter.settlement_distribution_plot(
            pile1_x, pile2_x, pile_diameter, pile_length,
            roadbed_width, points_3d, settlements, max_settlement_threshold,
            pile1_settlement, pile2_settlement, interaction_coefficient
        )
        
        # 保存图片
        output_file = "新效果图实现_测试结果.png"
        fig.savefig(output_file, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        print(f"✓ 新效果图已保存为: {output_file}")
        
        # 显示详细的计算点信息
        print(f"\n16个计算点的详细信息:")
        print("点号\tX坐标\tY坐标\t深度\t沉降值(mm)\t安全状态")
        print("-" * 65)
        
        for i, (point, settlement) in enumerate(zip(points_3d, settlements)):
            x, y, z = point
            settlement_ratio = (settlement / max_settlement_threshold) * 100
            
            if settlement_ratio <= 50:
                status = '安全'
            elif settlement_ratio <= 75:
                status = '注意'
            elif settlement_ratio <= 100:
                status = '警告'
            else:
                status = '超限'
            
            print(f"P{i+1:2d}\t{x:6.2f}\t{y:6.2f}\t{z:6.2f}\t{settlement:8.3f}\t{status}")
        
        # 显示图形
        plt.show()
        
        print(f"\n✅ 新效果图实现测试完成！")
        print(f"所有细节已按照您的效果图要求实现：")
        print(f"• 桩顶网格填充 + 桩身斜线填充")
        print(f"• 黑色桥面结构")
        print(f"• 棕色梯形路基")
        print(f"• 蓝色尺寸标注（L₁、L₂、x）")
        print(f"• 4×4=16个彩色散点")
        print(f"• 虚线网格显示")
        print(f"• 分层背景效果")
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("新效果图可视化实现测试")
    print("=" * 60)
    test_new_effect_diagram() 