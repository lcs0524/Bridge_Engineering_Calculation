# -*- coding: utf-8 -*-
"""
调试版本的结果导出器 - 添加详细的错误检查和日志输出
"""

import pandas as pd
import os
from datetime import datetime
import json
import traceback


class ResultExporterDebug:
    """调试版本的结果导出器类"""
    
    def __init__(self):
        """初始化导出器"""
        pass
    
    def export_to_excel(self, results, filename):
        """
        导出结果到Excel文件 - 调试版本
        
        参数:
        results: 计算结果字典
        filename: 输出文件名
        """
        print(f"[DEBUG] 开始导出Excel文件: {filename}")
        
        try:
            # 检查输入数据结构
            print("[DEBUG] 检查输入数据结构...")
            self._validate_results_structure(results)
            
            # 创建Excel写入器
            print("[DEBUG] 创建Excel写入器...")
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                
                print("[DEBUG] 1. 写入输入参数表...")
                self._write_input_parameters(writer, results)
                
                print("[DEBUG] 2. 写入计算结果表...")
                self._write_calculation_results(writer, results)
                
                print("[DEBUG] 3. 写入统计分析表...")
                self._write_statistics(writer, results)
                
                print("[DEBUG] 4. 写入安全评估表...")
                self._write_safety_assessment(writer, results)
                
                print("[DEBUG] 5. 写入修正系数表...")
                self._write_correction_factors(writer, results)
            
            print(f"[DEBUG] Excel文件导出成功: {filename}")
            return True, "Excel导出成功"
            
        except Exception as e:
            error_msg = f"Excel导出失败：{str(e)}"
            print(f"[ERROR] {error_msg}")
            traceback.print_exc()
            return False, error_msg
    
    def _validate_results_structure(self, results):
        """验证结果数据结构"""
        print("[DEBUG] 验证数据结构...")
        
        # 检查顶级键
        required_keys = ['points', 'input_parameters', 'statistics', 'safety_assessment']
        for key in required_keys:
            if key not in results:
                raise KeyError(f"缺少必需的键: {key}")
            print(f"[DEBUG] ✓ 找到键: {key}")
        
        # 检查points结构
        if not results['points']:
            raise ValueError("计算点数据为空")
        
        print(f"[DEBUG] 计算点数量: {len(results['points'])}")
        
        # 检查第一个点的结构
        first_point = results['points'][0]
        point_keys = ['point_id', 'x', 'y', 'z', 'settlement_mm', 'soil_properties']
        for key in point_keys:
            if key not in first_point:
                print(f"[WARNING] 计算点缺少键: {key}")
            else:
                print(f"[DEBUG] ✓ 计算点包含键: {key}")
        
        # 检查correction_factors
        if 'correction_factors' not in results:
            print("[WARNING] 缺少correction_factors，将创建默认值")
            results['correction_factors'] = {
                'length_correction': 1.0,
                'diameter_correction': 1.0,
                'combined_correction': 1.0
            }
        
        print("[DEBUG] 数据结构验证完成")
    
    def _write_input_parameters(self, writer, results):
        """写入输入参数表"""
        try:
            input_params = results['input_parameters']
            print(f"[DEBUG] 输入参数键: {list(input_params.keys())}")
            
            # 基本参数
            basic_data = [
                ['参数名称', '数值', '单位'],
                ['桩径', input_params.get('pile_diameter', 'N/A'), 'm'],
                ['桩长', input_params.get('pile_length', 'N/A'), 'm'],
                ['荷载', input_params.get('load', 'N/A'), 'kN'],
                ['路线等级', input_params.get('road_level', 'N/A'), '-'],
            ]
            
            basic_df = pd.DataFrame(basic_data[1:], columns=basic_data[0])
            basic_df.to_excel(writer, sheet_name='输入参数', index=False, startrow=0)
            
            # 土层参数
            if 'soil_layers' in input_params and input_params['soil_layers']:
                soil_data = []
                for i, layer in enumerate(input_params['soil_layers']):
                    soil_data.append([
                        f"土层{i+1}",
                        layer.get('depth_range', 'N/A'),
                        layer.get('name', 'N/A'),
                        layer.get('compression_modulus', 'N/A'),
                        layer.get('poisson_ratio', 'N/A')
                    ])
                
                soil_df = pd.DataFrame(soil_data, 
                                     columns=['序号', '深度范围(m)', '土层名称', '压缩模量(MPa)', '泊松比'])
                soil_df.to_excel(writer, sheet_name='输入参数', index=False, startrow=len(basic_data)+2)
            
            print("[DEBUG] 输入参数表写入完成")
            
        except Exception as e:
            print(f"[ERROR] 写入输入参数表失败: {e}")
            raise
    
    def _write_calculation_results(self, writer, results):
        """写入计算结果表"""
        try:
            points = results['points']
            print(f"[DEBUG] 处理 {len(points)} 个计算点")
            
            calc_data = []
            for i, point in enumerate(points):
                print(f"[DEBUG] 处理点 {i+1}: {point.get('point_id', f'P{i+1}')}")
                
                # 检查每个点的键
                required_point_keys = ['point_id', 'x', 'y', 'z', 'distance', 
                                     'settlement_mm', 'influence_factor', 'sigma_z', 
                                     'tau_xz', 'tau_yz', 'soil_properties']
                
                row_data = []
                for key in required_point_keys:
                    if key == 'soil_properties':
                        if key in point and 'name' in point[key]:
                            row_data.append(point[key]['name'])
                        else:
                            row_data.append('未知土层')
                    else:
                        value = point.get(key, 0 if key in ['settlement_mm', 'x', 'y', 'z', 'distance', 
                                                          'influence_factor', 'sigma_z', 'tau_xz', 'tau_yz'] 
                                         else f'P{i+1}')
                        row_data.append(value)
                
                calc_data.append(row_data)
            
            calc_df = pd.DataFrame(calc_data, columns=[
                '计算点', 'X坐标(m)', 'Y坐标(m)', '深度(m)', '距离(m)',
                '沉降值(mm)', '影响系数', '垂直应力(kPa)', '剪应力τxz(kPa)', 
                '剪应力τyz(kPa)', '对应土层'
            ])
            
            calc_df.to_excel(writer, sheet_name='计算结果', index=False)
            print("[DEBUG] 计算结果表写入完成")
            
        except Exception as e:
            print(f"[ERROR] 写入计算结果表失败: {e}")
            raise
    
    def _write_statistics(self, writer, results):
        """写入统计分析表"""
        try:
            stats = results['statistics']
            print(f"[DEBUG] 统计数据键: {list(stats.keys())}")
            
            stats_data = [
                ['统计项目', '数值', '单位'],
                ['最大沉降值', f"{stats.get('max_settlement_mm', 0):.3f}", 'mm'],
                ['最小沉降值', f"{stats.get('min_settlement_mm', 0):.3f}", 'mm'],
                ['平均沉降值', f"{stats.get('avg_settlement_mm', 0):.3f}", 'mm'],
                ['沉降值范围', f"{stats.get('max_settlement_mm', 0) - stats.get('min_settlement_mm', 0):.3f}", 'mm'],
            ]
            
            stats_df = pd.DataFrame(stats_data[1:], columns=stats_data[0])
            stats_df.to_excel(writer, sheet_name='统计分析', index=False)
            print("[DEBUG] 统计分析表写入完成")
            
        except Exception as e:
            print(f"[ERROR] 写入统计分析表失败: {e}")
            raise
    
    def _write_safety_assessment(self, writer, results):
        """写入安全评估表"""
        try:
            safety = results['safety_assessment']
            print(f"[DEBUG] 安全评估数据键: {list(safety.keys())}")
            
            safety_data = [
                ['评估项目', '结果', '说明'],
                ['安全等级', safety.get('safety_level', '未知'), ''],
                ['最大沉降值', f"{safety.get('max_settlement_mm', 0):.3f} mm", ''],
                ['一般限值', f"{safety.get('general_limit', 100)} mm", ''],
                ['桥梁限值', f"{safety.get('bridge_limit', 150)} mm", ''],
                ['是否超过一般限值', '是' if safety.get('exceed_general', False) else '否', ''],
                ['是否超过桥梁限值', '是' if safety.get('exceed_bridge', False) else '否', ''],
                ['影响范围面积', f"{safety.get('influence_area', 0):.2f} m²", ''],
                ['影响点数量', f"{safety.get('influence_points_count', 0)}", '个'],
            ]
            
            safety_df = pd.DataFrame(safety_data[1:], columns=safety_data[0])
            safety_df.to_excel(writer, sheet_name='安全评估', index=False, startrow=0)
            
            # 建议事项
            recommendations = safety.get('recommendations', [])
            if recommendations:
                recommendations_data = [['序号', '建议事项']]
                for i, rec in enumerate(recommendations, 1):
                    recommendations_data.append([i, rec])
                
                rec_df = pd.DataFrame(recommendations_data[1:], columns=recommendations_data[0])
                rec_df.to_excel(writer, sheet_name='安全评估', index=False, 
                              startrow=len(safety_data)+2)
            
            print("[DEBUG] 安全评估表写入完成")
            
        except Exception as e:
            print(f"[ERROR] 写入安全评估表失败: {e}")
            raise
    
    def _write_correction_factors(self, writer, results):
        """写入修正系数表"""
        try:
            correction = results.get('correction_factors', {
                'length_correction': 1.0,
                'diameter_correction': 1.0,
                'combined_correction': 1.0
            })
            
            input_params = results['input_parameters']
            pile_length = input_params.get('pile_length', 20.0)
            pile_diameter = input_params.get('pile_diameter', 1.0)
            
            correction_data = [
                ['修正系数', '数值', '说明'],
                ['桩长修正系数a', f"{correction.get('length_correction', 1.0):.4f}", 
                 f"a = 0.985 - 0.00051 × {pile_length}"],
                ['桩径修正系数b', f"{correction.get('diameter_correction', 1.0):.4f}", 
                 f"b = 0.038 × {pile_diameter}² - 0.206 × {pile_diameter} + 1.159"],
                ['综合修正系数', f"{correction.get('combined_correction', 1.0):.4f}", 'a × b'],
            ]
            
            correction_df = pd.DataFrame(correction_data[1:], columns=correction_data[0])
            correction_df.to_excel(writer, sheet_name='修正系数', index=False)
            print("[DEBUG] 修正系数表写入完成")
            
        except Exception as e:
            print(f"[ERROR] 写入修正系数表失败: {e}")
            raise 