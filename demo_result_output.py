#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高架桥桩基沉降影响范围计算软件 - 结果输出演示
展示W_z1~W_z16沉降计算结果的完整输出功能

作者：金洪松
日期：2025.4.25
"""

import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from calculation.settlement import SettlementCalculator
from visualization.plotter import ResultPlotter
from utils.exporter import ResultExporter


def create_demo_calculation():
    """创建演示计算案例"""
    print("=" * 60)
    print("高架桥桩基沉降影响范围计算 - 结果输出演示")
    print("=" * 60)
    print()
    
    # 创建计算器
    calculator = SettlementCalculator()
    
    # 设置演示参数 - 模拟实际工程
    demo_params = {
        'pile_diameter': 1.5,        # 1.5m直径钻孔桩
        'pile_length': 30.0,         # 30m桩长
        'load': 3000.0,              # 3000kN单桩荷载
        'road_level': '一级公路',     # 一级公路标准
        'soil_layers': [
            {
                'depth_range': '0-2',
                'name': '素填土',
                'compression_modulus': 4.0,
                'poisson_ratio': 0.38
            },
            {
                'depth_range': '2-6',
                'name': '淤泥质粘土',
                'compression_modulus': 6.5,
                'poisson_ratio': 0.42
            },
            {
                'depth_range': '6-12',
                'name': '粘土',
                'compression_modulus': 11.0,
                'poisson_ratio': 0.35
            },
            {
                'depth_range': '12-20',
                'name': '粉质粘土',
                'compression_modulus': 15.5,
                'poisson_ratio': 0.32
            },
            {
                'depth_range': '20-30',
                'name': '中砂',
                'compression_modulus': 22.0,
                'poisson_ratio': 0.28
            }
        ]
    }
    
    print("输入参数:")
    print(f"  桩径: {demo_params['pile_diameter']} m")
    print(f"  桩长: {demo_params['pile_length']} m")
    print(f"  荷载: {demo_params['load']} kN")
    print(f"  路线等级: {demo_params['road_level']}")
    print(f"  土层数量: {len(demo_params['soil_layers'])} 层")
    print()
    
    # 执行计算
    print("正在进行沉降计算...")
    try:
        results = calculator.calculate_settlement(demo_params)
        print("✓ 计算完成")
        print()
        return results
    except Exception as e:
        print(f"✗ 计算失败: {e}")
        return None


def display_calculation_points(results):
    """显示W_z1~W_z16计算点结果"""
    print("W_z1 ~ W_z16 计算点沉降结果:")
    print("-" * 80)
    print(f"{'计算点':<8} {'X坐标(m)':<10} {'Y坐标(m)':<10} {'深度(m)':<8} {'沉降值(mm)':<12} {'影响系数':<10}")
    print("-" * 80)
    
    for point in results['points']:
        print(f"{point['point_id']:<8} {point['x']:<10.1f} {point['y']:<10.1f} "
              f"{point['z']:<8.1f} {point['settlement_mm']:<12.3f} {point['influence_factor']:<10.4f}")
    
    print("-" * 80)
    print()


def display_safety_assessment(results):
    """显示安全评估结果"""
    safety = results['safety_assessment']
    stats = results['statistics']
    
    print("安全评估结果:")
    print("-" * 50)
    print(f"安全等级: {safety['safety_level']}")
    print(f"最大沉降值: {safety['max_settlement_mm']:.3f} mm")
    print(f"最小沉降值: {stats['min_settlement_mm']:.3f} mm")
    print(f"平均沉降值: {stats['avg_settlement_mm']:.3f} mm")
    print()
    
    print("规范限值对比 (JTG D30-2015):")
    print(f"  一般路段限值: {safety['general_limit']} mm")
    print(f"  桥梁工程限值: {safety['bridge_limit']} mm")
    print(f"  桥头引道限值: {safety['approach_limit']} mm")
    print()
    
    print("超限情况:")
    print(f"  超出一般限值: {'是' if safety['exceed_general'] else '否'}")
    print(f"  超出桥梁限值: {'是' if safety['exceed_bridge'] else '否'}")
    print(f"  超出引道限值: {'是' if safety['exceed_approach'] else '否'}")
    print()
    
    print("影响范围统计:")
    print(f"  影响面积: {safety['influence_area']:.2f} m²")
    print(f"  影响点数量: {safety['influence_points_count']} 个")
    print(f"  警告点数量: {safety['warning_points_count']} 个")
    print(f"  危险点数量: {safety['danger_points_count']} 个")
    print()
    
    print("工程建议:")
    for i, rec in enumerate(safety['recommendations'], 1):
        print(f"  {i}. {rec}")
    print()


def create_all_plots(results):
    """创建所有类型的图表"""
    print("正在生成图表...")
    
    plotter = ResultPlotter()
    
    # 创建输出目录
    output_dir = "demo_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    plot_types = [
        ("沉降分析图", plotter.create_settlement_plot),
        ("等高线图", plotter.create_contour_plot),
        ("雷达图", plotter.create_radar_plot),
        ("瀑布图", plotter.create_waterfall_plot),
        ("影响区域图", plotter.create_influence_zone_plot),
        ("综合分析图", plotter.create_comprehensive_analysis)
    ]
    
    created_plots = []
    
    for plot_name, plot_func in plot_types:
        try:
            print(f"  正在生成{plot_name}...")
            fig = plot_func(results)
            
            # 保存图片
            filename = os.path.join(output_dir, f"{plot_name.replace('图', '')}.png")
            fig.savefig(filename, dpi=300, bbox_inches='tight')
            created_plots.append(filename)
            
            plt.close(fig)  # 关闭图形释放内存
            print(f"  ✓ {plot_name}已保存")
            
        except Exception as e:
            print(f"  ✗ {plot_name}生成失败: {e}")
    
    print(f"\n图表生成完成，共生成 {len(created_plots)} 个图表文件")
    return created_plots


def export_detailed_report(results):
    """导出详细报告"""
    print("正在导出详细报告...")
    
    exporter = ResultExporter()
    output_dir = "demo_output"
    
    # 导出Excel报告
    try:
        excel_file = os.path.join(output_dir, "沉降计算详细报告.xlsx")
        success, msg = exporter.export_to_excel(results, excel_file)
        if success:
            print(f"  ✓ Excel报告: {excel_file}")
        else:
            print(f"  ✗ Excel报告导出失败: {msg}")
    except Exception as e:
        print(f"  ✗ Excel报告导出失败: {e}")
    
    # 导出CSV数据
    try:
        success, msg = exporter.export_to_csv(results, output_dir)
        if success:
            print(f"  ✓ CSV数据: {output_dir}/计算结果.csv")
        else:
            print(f"  ✗ CSV数据导出失败: {msg}")
    except Exception as e:
        print(f"  ✗ CSV数据导出失败: {e}")
    
    # 导出JSON数据
    try:
        json_file = os.path.join(output_dir, "计算结果数据.json")
        success, msg = exporter.export_to_json(results, json_file)
        if success:
            print(f"  ✓ JSON数据: {json_file}")
        else:
            print(f"  ✗ JSON数据导出失败: {msg}")
    except Exception as e:
        print(f"  ✗ JSON数据导出失败: {e}")
    
    # 导出汇总报告
    try:
        report_file = os.path.join(output_dir, "工程汇总报告.txt")
        success, msg = exporter.export_summary_report(results, report_file)
        if success:
            print(f"  ✓ 汇总报告: {report_file}")
        else:
            print(f"  ✗ 汇总报告导出失败: {msg}")
    except Exception as e:
        print(f"  ✗ 汇总报告导出失败: {e}")
    
    print("报告导出完成")


def display_technical_summary(results):
    """显示技术总结"""
    print("技术总结:")
    print("-" * 50)
    print("计算理论: Boussinesq弹性理论")
    print("修正方法: 桩长和桩径参数修正")
    print("数值验证: 基于FLAC3D数值分析")
    print("技术规范: 《公路路基设计规范》JTG D30-2015")
    print()
    
    # 修正系数信息
    correction = results['correction_factors']
    print("应用的修正系数:")
    print(f"  桩长修正系数: {correction['length_correction']:.4f}")
    print(f"  桩径修正系数: {correction['diameter_correction']:.4f}")
    print(f"  综合修正系数: {correction['combined_correction']:.4f}")
    print()
    
    # 计算点分布信息
    points = results['points']
    depths = sorted(list(set([p['z'] for p in points])))
    distances = sorted(list(set([abs(p['x']) for p in points if p['x'] != 0])))
    
    print("计算点分布:")
    print(f"  深度层次: {depths} m")
    print(f"  水平距离: {distances} m")
    print(f"  总计算点: {len(points)} 个 (W1~W{len(points)})")
    print()


def main():
    """主演示函数"""
    try:
        # 1. 创建演示计算
        results = create_demo_calculation()
        if not results:
            print("演示计算失败，程序退出")
            return False
        
        # 2. 显示计算点结果
        display_calculation_points(results)
        
        # 3. 显示安全评估
        display_safety_assessment(results)
        
        # 4. 显示技术总结
        display_technical_summary(results)
        
        # 5. 创建所有图表
        created_plots = create_all_plots(results)
        
        # 6. 导出详细报告
        export_detailed_report(results)
        
        print("=" * 60)
        print("演示完成！")
        print("=" * 60)
        print(f"所有输出文件已保存到 'demo_output' 目录")
        print(f"包括：")
        print(f"  - 6种类型的分析图表")
        print(f"  - Excel详细报告")
        print(f"  - CSV数据文件")
        print(f"  - JSON结构化数据")
        print(f"  - 工程汇总报告")
        print()
        print("这些输出展示了W_z1~W_z16沉降计算结果的完整分析，")
        print("包括曲线图、等高线图、雷达图、瀑布图等多种可视化形式，")
        print("以及基于JTG D30-2015规范的安全评估和工程建议。")
        
        return True
        
    except Exception as e:
        print(f"演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 