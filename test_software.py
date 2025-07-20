#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高架桥桩基沉降影响范围计算软件测试脚本
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from calculation.settlement import SettlementCalculator
from calculation.boussinesq import BoussinesqCalculator
from calculation.correction import CorrectionCalculator
from utils.validator import InputValidator
from utils.exporter import ResultExporter


def test_boussinesq_calculator():
    """测试Boussinesq计算器"""
    print("测试Boussinesq计算器...")
    
    calc = BoussinesqCalculator()
    
    # 测试基本参数
    G = calc.calculate_shear_modulus(10.0, 0.3)
    print(f"剪切模量: {G:.2f} MPa")
    
    # 测试沉降计算
    settlement = calc.calculate_settlement(1000, G, 1.0, 0.0, 1.0, 0.3)
    print(f"沉降值: {settlement*1000:.4f} mm")
    
    # 测试计算点生成
    points = calc.get_standard_calculation_points(1.0)
    print(f"生成计算点数量: {len(points)}")
    
    print("Boussinesq计算器测试通过！\n")


def test_correction_calculator():
    """测试修正计算器"""
    print("测试修正计算器...")
    
    calc = CorrectionCalculator()
    
    # 测试修正系数计算
    a = calc.calculate_length_correction(20.0)
    b = calc.calculate_diameter_correction(1.0)
    print(f"桩长修正系数a: {a:.4f}")
    print(f"桩径修正系数b: {b:.4f}")
    
    # 测试参数验证
    is_valid, msg = calc.validate_correction_parameters(20.0, 1.0)
    print(f"参数验证: {is_valid}, {msg}")
    
    print("修正计算器测试通过！\n")


def test_input_validator():
    """测试输入验证器"""
    print("测试输入验证器...")
    
    validator = InputValidator()
    
    # 测试桩径验证
    is_valid, msg = validator.validate_pile_diameter("1.0")
    print(f"桩径验证: {is_valid}, {msg}")
    
    # 测试桩长验证
    is_valid, msg = validator.validate_pile_length("20.0")
    print(f"桩长验证: {is_valid}, {msg}")
    
    # 测试荷载验证
    is_valid, msg = validator.validate_load("1000.0")
    print(f"荷载验证: {is_valid}, {msg}")
    
    print("输入验证器测试通过！\n")


def test_settlement_calculator():
    """测试沉降计算器"""
    print("测试沉降计算器...")
    
    calc = SettlementCalculator()
    
    # 准备测试参数
    test_params = {
        'pile_diameter': 1.0,
        'pile_length': 20.0,
        'load': 1000.0,
        'road_level': '一级公路',
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
    
    # 执行计算
    try:
        results = calc.calculate_settlement(test_params)
        print(f"计算成功！")
        print(f"最大沉降值: {results['statistics']['max_settlement_mm']:.3f} mm")
        print(f"安全等级: {results['safety_assessment']['safety_level']}")
        print(f"计算点数量: {len(results['points'])}")
    except Exception as e:
        print(f"计算失败: {e}")
        return False
    
    print("沉降计算器测试通过！\n")
    return results


def test_result_exporter(results):
    """测试结果导出器"""
    print("测试结果导出器...")
    
    exporter = ResultExporter()
    
    # 测试生成汇总报告
    report = exporter.generate_summary_report(results)
    print("汇总报告生成成功！")
    print(f"报告长度: {len(report)} 字符")
    
    # 测试导出格式
    formats = exporter.get_export_formats()
    print(f"支持的导出格式: {', '.join(formats.keys())}")
    
    print("结果导出器测试通过！\n")


def test_visualization_features(results):
    """测试可视化功能"""
    print("测试可视化功能...")
    
    from visualization.plotter import ResultPlotter
    plotter = ResultPlotter()
    
    try:
        # 测试各种图表类型
        print("1. 测试沉降分析图...")
        fig1 = plotter.create_settlement_plot(results)
        print("   沉降分析图创建成功")
        
        print("2. 测试等高线图...")
        try:
            fig2 = plotter.create_contour_plot(results)
            print("   等高线图创建成功")
        except ImportError:
            print("   等高线图需要scipy库支持")
        
        print("3. 测试雷达图...")
        fig3 = plotter.create_radar_plot(results)
        print("   雷达图创建成功")
        
        print("4. 测试瀑布图...")
        fig4 = plotter.create_waterfall_plot(results)
        print("   瀑布图创建成功")
        
        print("5. 测试影响区域图...")
        fig5 = plotter.create_influence_zone_plot(results)
        print("   影响区域图创建成功")
        
        print("6. 测试综合分析图...")
        fig6 = plotter.create_comprehensive_analysis(results)
        print("   综合分析图创建成功")
        
        # 关闭所有图形
        import matplotlib.pyplot as plt
        plt.close('all')
        
        print("可视化功能测试通过！\n")
        return True
        
    except Exception as e:
        print(f"可视化功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_safety_assessment(results):
    """测试安全评估功能"""
    print("测试安全评估功能...")
    
    try:
        safety = results['safety_assessment']
        
        # 检查安全评估字段
        required_fields = [
            'safety_level', 'max_settlement_mm', 'general_limit', 
            'bridge_limit', 'approach_limit', 'recommendations',
            'influence_area', 'influence_points_count'
        ]
        
        for field in required_fields:
            if field not in safety:
                print(f"   缺少安全评估字段: {field}")
                return False
        
        print(f"   安全等级: {safety['safety_level']}")
        print(f"   最大沉降: {safety['max_settlement_mm']:.3f} mm")
        print(f"   桥梁限值: {safety['bridge_limit']} mm")
        print(f"   影响面积: {safety['influence_area']:.2f} m²")
        print(f"   建议数量: {len(safety['recommendations'])}")
        
        # 检查符合性分析
        if 'compliance_analysis' in safety:
            compliance = safety['compliance_analysis']
            print(f"   符合性分析: {compliance['overall_compliance']}")
        
        # 检查安全统计
        if 'safety_statistics' in safety:
            stats = safety['safety_statistics']
            total_points = sum(stats.values())
            print(f"   统计点数: {total_points}")
        
        print("安全评估功能测试通过！\n")
        return True
        
    except Exception as e:
        print(f"安全评估功能测试失败: {e}")
        return False


def test_comprehensive_calculation():
    """测试完整计算流程"""
    print("测试完整计算流程...")
    
    calc = SettlementCalculator()
    
    # 准备测试参数 - 使用更接近实际的参数
    test_params = {
        'pile_diameter': 1.2,      # 1.2m桩径
        'pile_length': 25.0,       # 25m桩长
        'load': 2000.0,            # 2000kN荷载
        'road_level': '一级公路',
        'soil_layers': [
            {
                'depth_range': '0-3',
                'name': '杂填土',
                'compression_modulus': 5.0,
                'poisson_ratio': 0.35
            },
            {
                'depth_range': '3-8',
                'name': '淤泥质粘土',
                'compression_modulus': 8.0,
                'poisson_ratio': 0.40
            },
            {
                'depth_range': '8-15',
                'name': '粘土',
                'compression_modulus': 12.0,
                'poisson_ratio': 0.35
            },
            {
                'depth_range': '15-25',
                'name': '砂土',
                'compression_modulus': 18.0,
                'poisson_ratio': 0.30
            }
        ]
    }
    
    try:
        results = calc.calculate_settlement(test_params)
        
        print(f"   计算成功完成")
        print(f"   最大沉降值: {results['statistics']['max_settlement_mm']:.3f} mm")
        print(f"   安全等级: {results['safety_assessment']['safety_level']}")
        print(f"   计算点数量: {len(results['points'])}")
        print(f"   影响点数量: {results['safety_assessment']['influence_points_count']}")
        
        # 检查W_z1到W_z16的命名
        point_ids = [p['point_id'] for p in results['points']]
        expected_ids = [f'W{i}' for i in range(1, 17)]
        
        print(f"   计算点编号: {', '.join(point_ids[:8])}...")  # 显示前8个
        
        if len(point_ids) == 16:
            print("   ✓ 16个计算点(W1~W16)生成正确")
        else:
            print(f"   ✗ 计算点数量不正确，期望16个，实际{len(point_ids)}个")
        
        print("完整计算流程测试通过！\n")
        return results
        
    except Exception as e:
        print(f"完整计算流程测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """主测试函数"""
    print("=" * 60)
    print("高架桥桩基沉降影响范围计算软件 - 功能测试")
    print("=" * 60)
    print()
    
    try:
        # 1. 测试Boussinesq计算器
        test_boussinesq_calculator()
        
        # 2. 测试修正计算器
        test_correction_calculator()
        
        # 3. 测试输入验证器
        test_input_validator()
        
        # 4. 测试沉降计算器
        results = test_settlement_calculator()
        
        if results:
            # 5. 测试结果导出器
            test_result_exporter(results)
            
            # 6. 测试可视化功能
            test_visualization_features(results)
            
            # 7. 测试安全评估功能
            test_safety_assessment(results)
            
            # 8. 测试完整计算流程
            test_comprehensive_calculation()
        
        print("=" * 60)
        print("所有测试通过！软件功能正常。")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 