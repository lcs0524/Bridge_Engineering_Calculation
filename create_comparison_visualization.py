#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建可视化对比：展示新的4x4网格矩形区域效果
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from calculation.settlement import SettlementCalculator
from visualization.plotter import ResultPlotter
import matplotlib.pyplot as plt

def create_new_visualization():
    """创建新的4x4网格矩形区域可视化效果"""
    
    # 创建计算器
    calculator = SettlementCalculator()
    plotter = ResultPlotter()
    
    # 设置测试参数（符合实际沉降示意图的效果）
    test_params = {
        'project_name': '高架桥桩基沉降影响范围计算示例',
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
            'pile1_distance': 6.0,
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
        print("开始计算沉降...")
        
        # 执行计算
        results = calculator.calculate_settlement(test_params)
        
        print(f"计算完成！")
        print(f"项目名称: {results['input_parameters']['project_name']}")
        print(f"计算点数: {len(results['points'])} 个")
        print(f"最大沉降: {results['statistics']['max_settlement_mm']:.3f} mm")
        print(f"安全等级: {results['safety_assessment']['safety_level']}")
        
        # 创建新的4x4网格矩形区域可视化
        print("\n创建新的4x4网格矩形区域可视化...")
        fig = plotter.settlement_distribution_plot(results, test_params)
        
        # 保存图片
        output_file = "新的4x4网格矩形区域可视化效果.png"
        fig.savefig(output_file, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        print(f"✅ 新可视化效果已保存为: {output_file}")
        
        # 显示图片（可选）
        plt.show()
        
        # 显示16个计算点的详细结果
        print("\n16个计算点的沉降结果:")
        print("点号\tX坐标\tY坐标\t深度\t沉降值(mm)\t颜色等级")
        print("-" * 60)
        
        allowable = results['safety_assessment']['bridge_limit']
        for i, point in enumerate(results['points']):
            settlement = point['settlement_mm']
            percentage = (settlement / allowable) * 100 if allowable > 0 else 0
            
            if percentage > 100:
                color_level = "红色(超限)"
            elif percentage >= 40:
                color_level = "橙色(警告)"
            elif percentage >= 10:
                color_level = "黄色(注意)"
            else:
                color_level = "绿色(安全)"
            
            print(f"{point['point_id']}\t{point['x']:.1f}\t{point['y']:.1f}\t{point['z']:.1f}\t"
                  f"{settlement:.2f}\t\t{color_level}")
        
        print(f"\n容许沉降限值: {allowable:.0f} mm")
        print(f"颜色等级说明:")
        print(f"  绿色: < 10% 容许值 (< {allowable*0.1:.0f} mm)")
        print(f"  黄色: 10%-40% 容许值 ({allowable*0.1:.0f}-{allowable*0.4:.0f} mm)")
        print(f"  橙色: 40%-100% 容许值 ({allowable*0.4:.0f}-{allowable:.0f} mm)")
        print(f"  红色: > 100% 容许值 (> {allowable:.0f} mm)")
        
        print("\n✅ 新的4x4网格矩形区域可视化创建完成！")
        print("这种可视化效果符合实际沉降示意图的要求：")
        print("1. 16个计算点清晰分开")
        print("2. 每个点占据一个明确的矩形区域")
        print("3. 形成4x4网格布局")
        print("4. 根据沉降值大小用不同颜色显示")
        print("5. 显示桩基参数和位置")
        print("6. 包含计算公式说明")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_new_visualization() 