#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查计算结果中每个点的实际数据结构
"""

import os
import sys
import json

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from calculation.settlement import SettlementCalculator

def check_data_structure():
    """检查计算结果的数据结构"""
    print("=== 检查计算结果数据结构 ===")
    
    try:
        # 创建计算器
        calculator = SettlementCalculator()
        
        # 设置输入参数
        input_params = {
            'pile1': {
                'diameter': 1.2,
                'length': 30.0,
                'load': 8000.0
            },
            'pile2': {
                'diameter': 1.0,
                'length': 25.0,
                'load': 6000.0
            },
            'road_level': '高速公路',
            'road_params': {
                'width': 12.0,
                'pile1_distance': 5.0,
                'pile2_distance': 5.0
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
                }
            ]
        }
        
        print("✓ 输入参数设置完成")
        
        # 执行计算
        print("正在执行计算...")
        results = calculator.calculate_settlement(input_params)
        print(f"✓ 计算完成")
        
        # 检查顶级结构
        print(f"\n顶级键: {list(results.keys())}")
        
        # 检查第一个计算点的结构
        if results['points']:
            first_point = results['points'][0]
            print(f"\n第一个计算点的键: {list(first_point.keys())}")
            print(f"第一个计算点内容:")
            for key, value in first_point.items():
                if isinstance(value, dict):
                    print(f"  {key}: {list(value.keys())}")
                else:
                    print(f"  {key}: {value} ({type(value)})")
        
        # 检查所有计算点是否有相同的结构
        print(f"\n所有计算点的键一致性检查:")
        if results['points']:
            first_keys = set(results['points'][0].keys())
            for i, point in enumerate(results['points']):
                point_keys = set(point.keys())
                if point_keys != first_keys:
                    print(f"  点 {i+1} 键不一致: 缺少 {first_keys - point_keys}, 多余 {point_keys - first_keys}")
                else:
                    print(f"  点 {i+1} ✓")
        
        # 检查exporter期望的键
        expected_keys = ['point_id', 'x', 'y', 'z', 'distance', 'settlement_mm', 
                        'influence_factor', 'sigma_z', 'tau_xz', 'tau_yz', 'soil_properties']
        
        print(f"\nExporter期望的键检查:")
        if results['points']:
            actual_keys = set(results['points'][0].keys())
            for key in expected_keys:
                if key in actual_keys:
                    print(f"  {key}: ✓")
                else:
                    print(f"  {key}: ✗ 缺失")
            
            print(f"\n实际有但exporter不期望的键:")
            for key in actual_keys - set(expected_keys):
                print(f"  {key}: (额外)")
        
        # 保存详细结构到文件以供检查
        output_file = "data_structure_check.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2, default=str)
        print(f"\n完整数据结构已保存到: {output_file}")
        
        return results
        
    except Exception as e:
        print(f"✗ 检查失败: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    check_data_structure() 