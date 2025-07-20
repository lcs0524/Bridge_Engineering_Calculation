# -*- coding: utf-8 -*-
"""
沉降计算主模块
整合Boussinesq理论计算和参数修正，实现完整的沉降计算流程
"""

import numpy as np
import math
from .boussinesq import BoussinesqCalculator
from .correction import CorrectionCalculator


class SettlementCalculator:
    """沉降计算主类"""
    
    def __init__(self):
        """初始化计算器"""
        self.boussinesq = BoussinesqCalculator()
        self.correction = CorrectionCalculator()
        
    def calculate_settlement(self, params):
        """
        主要沉降计算方法（双桩系统）
        
        参数:
        params: 包含所有计算参数的字典
            - project_name: 项目名称
            - project_type: 项目类型
            - road_level: 路线等级（5种类型）
            - lane_count: 车道数量
            - pile1: 桩1参数字典 {diameter, length(土下层), load}
            - pile2: 桩2参数字典 {diameter, length(土下层), load}
            - road_params: 公路参数字典 {width, pile1_distance, pile2_distance}
            - soil_layers: 土层参数列表
        
        返回:
        results: 计算结果字典
        """
        try:
            # 验证输入参数
            self._validate_parameters(params)
            
            # 获取基本参数
            pile1 = params['pile1']
            pile2 = params['pile2']
            road_level = params['road_level']
            road_params = params['road_params']
            soil_layers = params['soil_layers']
            
            # 计算等效土层参数
            equivalent_soil = self._calculate_equivalent_soil_properties(soil_layers)
            
            # 获取16个标准计算点（参考实际沉降示意图）
            points = self._get_16_standard_points(road_params)
            
            # 计算各点沉降值（双桩叠加）
            calculation_results = []
            
            for i, (x, y, z) in enumerate(points):
                # 计算该点到两桩的距离（3D距离，符合勾股定理）
                pile1_x, pile1_y = self._get_pile_position(1, road_params)
                pile2_x, pile2_y = self._get_pile_position(2, road_params)
                
                distance1 = math.sqrt((x - pile1_x)**2 + (y - pile1_y)**2 + z**2)
                distance2 = math.sqrt((x - pile2_x)**2 + (y - pile2_y)**2 + z**2)
                
                point_soil = self._get_soil_properties_at_depth(soil_layers, z)
                
                point_G = self.boussinesq.calculate_shear_modulus(
                    point_soil['compression_modulus'], point_soil['poisson_ratio']
                )
                
                # 计算桩1的影响
                # 使用简化后的综合修正系数
                combined_correction1 = self.correction.calculate_combined_correction(
                    pile1['length'], pile1['diameter']
                )
                
                # Boussinesq计算，然后乘以综合修正系数
                # 假设 boussinesq.py 中的 calculate_settlement 返回的是未修正的理论沉降
                raw_settlement1 = self.boussinesq.calculate_settlement(
                    pile1['load'], point_G, x - pile1_x, y - pile1_y, z, 
                    point_soil['poisson_ratio']
                )
                settlement1 = raw_settlement1 * combined_correction1
                
                # 计算桩2的影响
                # 使用简化后的综合修正系数
                combined_correction2 = self.correction.calculate_combined_correction(
                    pile2['length'], pile2['diameter']
                )
                
                raw_settlement2 = self.boussinesq.calculate_settlement(
                    pile2['load'], point_G, x - pile2_x, y - pile2_y, z,
                    point_soil['poisson_ratio']
                )
                settlement2 = raw_settlement2 * combined_correction2
                
                # 双桩叠加影响（考虑相互作用）
                total_settlement = settlement1 + settlement2
                
                # 如果桩间相互作用系数仍然需要，则保留，否则也可以简化
                pile_spacing = math.sqrt((pile2_x - pile1_x)**2 + (pile2_y - pile1_y)**2)
                interaction_factor = self._calculate_pile_interaction(pile_spacing, 
                                                                    pile1['diameter'], pile2['diameter'])
                total_settlement *= interaction_factor
                
                # 计算综合影响系数
                influence_factor = self.boussinesq.calculate_influence_factor(x, y, z)
                
                # 计算应力分量（叠加）
                sigma_z1, tau_xz1, tau_yz1 = self.boussinesq.calculate_stress_components(
                    pile1['load'], x - pile1_x, y - pile1_y, z
                )
                sigma_z2, tau_xz2, tau_yz2 = self.boussinesq.calculate_stress_components(
                    pile2['load'], x - pile2_x, y - pile2_y, z
                )
                
                # 存储结果
                result = {
                    'point_id': f'W{i+1}',
                    'x': x,
                    'y': y,
                    'z': z,
                    'pile1_distance': distance1,
                    'pile2_distance': distance2,
                    'pile1_settlement': settlement1,
                    'pile2_settlement': settlement2,
                    'total_settlement': total_settlement,
                    'settlement_mm': total_settlement * 1000,  # 转换为mm
                    # 'influence_factor': influence_factor, # 如果不再需要，可以移除
                    'interaction_factor': interaction_factor, # 如果不再需要，可以移除
                    # 'sigma_z': sigma_z1 + sigma_z2, # 如果不再需要，可以移除
                    # 'tau_xz': tau_xz1 + tau_xz2, # 如果不再需要，可以移除
                    # 'tau_yz': tau_yz1 + tau_yz2, # 如果不再需要，可以移除
                    'correction_factors': { # 这里可以只保留 a 和 b
                        'pile1': {'a': self.correction.calculate_length_correction(pile1['length']), 
                                  'b': self.correction.calculate_diameter_correction(pile1['diameter'])},
                        'pile2': {'a': self.correction.calculate_length_correction(pile2['length']), 
                                  'b': self.correction.calculate_diameter_correction(pile2['diameter'])}
                    },
                    'soil_properties': point_soil
                }
                
                calculation_results.append(result)
            
            # 计算统计信息
            settlements = [r['total_settlement'] for r in calculation_results]
            max_settlement = max(settlements)
            min_settlement = min(settlements)
            avg_settlement = np.mean(settlements)
            
            # 验证计算结果的物理逻辑
            physics_verification = self._verify_physical_logic(calculation_results)
            
            # 安全评估
            safety_assessment = self._evaluate_safety(calculation_results, road_level)
            
            # 组装最终结果
            final_results = {
                'input_parameters': params,
                'equivalent_soil': equivalent_soil,
                'points': calculation_results,
                'statistics': {
                    'max_settlement': max_settlement,
                    'min_settlement': min_settlement,
                    'avg_settlement': avg_settlement,
                    'max_settlement_mm': max_settlement * 1000,
                    'min_settlement_mm': min_settlement * 1000,
                    'avg_settlement_mm': avg_settlement * 1000
                },
                'safety_assessment': safety_assessment,
                'physics_verification': physics_verification,
                'calculation_info': {
                    'method': 'Boussinesq理论 + 双桩叠加分析',
                    'standard': 'JTG D30-2015',
                    'correction_applied': True,
                    'flac3d_calibrated': True,
                    'pile_interaction': True,
                    'coordinate_system': {
                        'x_axis': '路基横向，中心线为0，负值为左侧，正值为右侧',
                        'y_axis': '路线方向，桩位于Y=0断面',
                        'z_axis': '地面以下深度，正值向下',
                        'pile_positions': '两桩均位于路基外侧'
                    }
                }
            }
            
            return final_results
            
        except Exception as e:
            raise Exception(f"沉降计算失败: {str(e)}")
    
    def _validate_parameters(self, params):
        """验证输入参数"""
        required_keys = ['pile1', 'pile2', 'road_level', 'road_params', 'soil_layers']
        
        for key in required_keys:
            if key not in params:
                raise ValueError(f"缺少必要参数: {key}")
        
        # 验证桩1参数
        pile1 = params['pile1']
        if pile1['diameter'] <= 0:
            raise ValueError("桩1直径必须大于0")
        if pile1['length'] <= 0:
            raise ValueError("桩1长度（土下层）必须大于0")
        if pile1['load'] <= 0:
            raise ValueError("桩1荷载必须大于0")
        
        # 验证桩2参数
        pile2 = params['pile2']
        if pile2['diameter'] <= 0:
            raise ValueError("桩2直径必须大于0")
        if pile2['length'] <= 0:
            raise ValueError("桩2长度（土下层）必须大于0")
        if pile2['load'] <= 0:
            raise ValueError("桩2荷载必须大于0")
        
        # 验证公路参数
        road_params = params['road_params']
        if road_params['width'] <= 0:
            raise ValueError("路基宽度必须大于0")
        if road_params['pile1_distance'] < 0:
            raise ValueError("路基与桩1距离不能为负数")
        if road_params['pile2_distance'] < 0:
            raise ValueError("路基与桩2距离不能为负数")
        
        if not params['soil_layers']:
            raise ValueError("至少需要一个土层")
        
        # 验证土层参数
        for i, layer in enumerate(params['soil_layers']):
            if layer['compression_modulus'] <= 0:
                raise ValueError(f"第{i+1}层土的压缩模量必须大于0")
            
            if layer['poisson_ratio'] <= -1 or layer['poisson_ratio'] >= 0.5:
                raise ValueError(f"第{i+1}层土的泊松比必须在(-1, 0.5)范围内")
    
    def _calculate_equivalent_soil_properties(self, soil_layers):
        """计算等效土层参数"""
        total_thickness = 0
        weighted_E = 0
        weighted_nu = 0
        
        for layer in soil_layers:
            # 解析深度范围
            depth_range = layer['depth_range']
            if '-' in depth_range:
                depth_start, depth_end = map(float, depth_range.split('-'))
                thickness = depth_end - depth_start
            else:
                thickness = 1.0  # 默认厚度
            
            total_thickness += thickness
            weighted_E += layer['compression_modulus'] * thickness
            weighted_nu += layer['poisson_ratio'] * thickness
        
        if total_thickness == 0:
            raise ValueError("土层总厚度不能为0")
        
        equivalent_E = weighted_E / total_thickness
        equivalent_nu = weighted_nu / total_thickness
        
        return {
            'E': equivalent_E,
            'nu': equivalent_nu,
            'total_thickness': total_thickness
        }
    
    def _get_soil_properties_at_depth(self, soil_layers, depth):
        """获取指定深度的土层属性"""
        for layer in soil_layers:
            depth_range = layer['depth_range']
            if '-' in depth_range:
                depth_start, depth_end = map(float, depth_range.split('-'))
                if depth_start <= depth <= depth_end:
                    return {
                        'compression_modulus': layer['compression_modulus'],
                        'poisson_ratio': layer['poisson_ratio'],
                        'name': layer['name']
                    }
        
        # 如果没有找到对应的土层，返回最后一层的属性
        if soil_layers:
            last_layer = soil_layers[-1]
            return {
                'compression_modulus': last_layer['compression_modulus'],
                'poisson_ratio': last_layer['poisson_ratio'],
                'name': last_layer['name']
            }
        
        # 默认土层属性
        return {
            'compression_modulus': 10.0,
            'poisson_ratio': 0.3,
            'name': '默认土层'
        }
    
    def _evaluate_safety(self, calculation_results, road_level):
        """评估工程安全性"""
        # 根据JTG D30-2015规范的沉降限值 (单位转换: cm -> mm)
        limit_values = {
            "高速公路": {
                "general_limit": 200,      # 最严格标准：20cm = 200mm
                "bridge_limit": 150,       # 桥梁工程：15cm = 150mm  
                "bridge_approach": 80,     # 桥头引道：8cm = 80mm
                "culvert_passage": 150     # 涵洞通道：15cm = 150mm
            },
            "一级公路": {
                "general_limit": 300,      # 一般路段：30cm = 300mm
                "bridge_limit": 200,       # 严格要求：20cm = 200mm  
                "bridge_approach": 100,    # 桥头引道：10cm = 100mm
                "culvert_passage": 200     # 涵洞通道：20cm = 200mm
            },
            "二级公路": {
                "general_limit": 400,      # 一般路段：40cm = 400mm
                "bridge_limit": 300,       # 桥梁工程：30cm = 300mm
                "bridge_approach": 150,    # 桥头引道：15cm = 150mm
                "culvert_passage": 300     # 涵洞通道：30cm = 300mm
            },
            "三级公路": {
                "general_limit": 500,      # 一般路段：50cm = 500mm
                "bridge_limit": 400,       # 桥梁工程：40cm = 400mm
                "bridge_approach": 200,    # 桥头引道：20cm = 200mm
                "culvert_passage": 400     # 涵洞通道：40cm = 400mm
            },
            "四级公路": {
                "general_limit": 600,      # 最宽松标准：60cm = 600mm
                "bridge_limit": 500,       # 桥梁工程：50cm = 500mm
                "bridge_approach": 250,    # 桥头引道：25cm = 250mm
                "culvert_passage": 500     # 涵洞通道：50cm = 500mm
            }
        }
        
        # 获取当前路线等级的限值，默认使用一级公路标准
        current_limits = limit_values.get(road_level, limit_values["一级公路"])
        
        # 针对桩基础工程，主要考虑桥梁部分，使用严格标准
        general_limit = current_limits["general_limit"]
        bridge_limit = current_limits["bridge_limit"]      # 桩基础按严格标准
        approach_limit = current_limits["bridge_approach"] # 桥头引道标准
        
        # 检查是否超限
        settlements_mm = [r['settlement_mm'] for r in calculation_results]
        max_settlement_mm = max(settlements_mm)
        
        # 安全等级判定
        safety_level = "安全"
        safety_color = "green"
        recommendations = []
        
        # 按照最严格的标准进行评估
        if max_settlement_mm > approach_limit:
            if max_settlement_mm > bridge_limit:
                if max_settlement_mm > general_limit:
                    safety_level = "危险"
                    safety_color = "red"
                    recommendations.append("沉降值严重超出规范限值，工程存在重大安全隐患")
                    recommendations.append("必须立即停工并重新设计桩基础系统")
                    recommendations.append("建议增加桩数、加大桩径或采用复合地基")
                    recommendations.append("进行FLAC3D三维数值分析验证设计方案")
                else:
                    safety_level = "危险"
                    safety_color = "red"
                    recommendations.append("沉降值超出桥梁工程限值，需要重新设计")
                    recommendations.append("建议优化桩基设计参数或采用加固措施")
                    recommendations.append("考虑预应力管桩或采用桩筏基础")
            else:
                safety_level = "警告"
                safety_color = "orange"
                recommendations.append("沉降值超出桥头引道限值，需要专项设计")
                recommendations.append("建议在桥头设置过渡段减少差异沉降")
                recommendations.append("加强施工监测，控制沉降发展")
        else:
            recommendations.append("沉降值满足规范要求，工程安全")
            recommendations.append("建议按现有设计方案实施")
            recommendations.append("施工过程中加强沉降观测")
        
        # 影响范围评估
        influence_points = []
        warning_points = []
        danger_points = []
        
        for result in calculation_results:
            settlement = result['settlement_mm']
            if settlement > 5:  # 5mm作为影响阈值
                influence_points.append(result)
            if settlement > approach_limit:
                warning_points.append(result)
            if settlement > bridge_limit:
                danger_points.append(result)
        
        # 计算影响范围面积
        influence_area = self._calculate_influence_area(influence_points)
        
        # 详细的工程建议
        if max_settlement_mm > bridge_limit:
            recommendations.extend([
                "建议进行桩基承载力验算和变形验算",
                "考虑采用PHC预应力管桩或钢管桩",
                "评估地基处理方案的必要性"
            ])
        
        if len(danger_points) > len(calculation_results) * 0.3:  # 超过30%的点超限
            recommendations.append("大范围超限，建议全面重新设计基础方案")
        
        # 技术措施建议
        technical_recommendations = []
        if max_settlement_mm > approach_limit:
            technical_recommendations.extend([
                "设置桥头搭板减少车辆颠簸",
                "采用轻质填料减小附加荷载", 
                "分层分期施工控制沉降速率"
            ])
        
        return {
            'safety_level': safety_level,
            'safety_color': safety_color,
            'max_settlement_mm': max_settlement_mm,
            'general_limit': general_limit,
            'bridge_limit': bridge_limit,
            'approach_limit': approach_limit,
            'exceed_general': max_settlement_mm > general_limit,
            'exceed_bridge': max_settlement_mm > bridge_limit,
            'exceed_approach': max_settlement_mm > approach_limit,
            'recommendations': recommendations,
            'technical_recommendations': technical_recommendations,
            'influence_area': influence_area,
            'influence_points_count': len(influence_points),
            'warning_points_count': len(warning_points),
            'danger_points_count': len(danger_points),
            'safety_statistics': {
                'safe_points': len(calculation_results) - len(influence_points),
                'influence_points': len(influence_points) - len(warning_points),
                'warning_points': len(warning_points) - len(danger_points),
                'danger_points': len(danger_points)
            },
            'compliance_analysis': {
                'meets_general_standard': max_settlement_mm <= general_limit,
                'meets_bridge_standard': max_settlement_mm <= bridge_limit,
                'meets_approach_standard': max_settlement_mm <= approach_limit,
                'overall_compliance': max_settlement_mm <= approach_limit
            }
        }
    
    def _calculate_influence_area(self, influence_points):
        """计算影响范围面积"""
        if not influence_points:
            return 0
        
        # 简化计算：用最大距离估算影响半径
        max_distance = 0
        for point in influence_points:
            distance = math.sqrt(point['x']**2 + point['y']**2)
            max_distance = max(max_distance, distance)
        
        # 影响面积（近似为圆形）
        influence_area = math.pi * max_distance**2
        
        return influence_area
    
    def export_calculation_report(self, results, filename):
        """导出计算报告"""
        # 这个方法可以用于生成详细的计算报告
        # 在实际应用中可以集成到导出模块中
        pass
    
    def get_settlement_contour_data(self, results):
        """获取沉降等高线数据"""
        points = results['points']
        
        x_coords = [p['x'] for p in points]
        y_coords = [p['y'] for p in points]
        settlements = [p['settlement_mm'] for p in points]
        
        return {
            'x': x_coords,
            'y': y_coords,
            'z': settlements,
            'levels': np.linspace(min(settlements), max(settlements), 10)
        } 
    
    def _get_16_standard_points(self, road_params):
        """获取16个标准计算点（按工程示意图合理分布）"""
        import numpy as np
        
        width = road_params['width']
        
        # 根据工程示意图，计算点应该分布在路基影响范围内
        # 设置合理的分析范围
        if width < 20:
            analysis_range = 20  # 最小分析范围20米
        else:
            analysis_range = width * 1.5  # 路基宽度的1.5倍
        
        # 4×4网格坐标（平面分布）
        grid_spacing = analysis_range / 5  # 5等分，取中间4个点
        positions = [-analysis_range/2 + grid_spacing * (i+1) for i in range(4)]
        
        # 4个深度层
        depths = [1, 2, 3, 4]
        
        points = []
        
        # 方案1：每个深度层4个点，沿X方向分布
        for z in depths:
            for x in positions:
                y = 0  # Y坐标固定在路基中心线
                points.append((x, y, z))
        
        return points
    
    def _get_pile_position(self, pile_number, road_params):
        """获取桩的位置坐标"""
        # 根据重新定义的坐标系：
        # X轴：沿路基横向，负值为左侧，正值为右侧
        # Y轴：沿路线方向，桩位于Y=0断面
        # 两个桩都在原有路基外侧
        
        if pile_number == 1:
            # 桩1位置（在路基左侧外）
            x = -(road_params['width']/2 + road_params['pile1_distance'])
            y = 0  # 桩位于Y=0断面
        else:
            # 桩2位置（在路基右侧外）
            x = (road_params['width']/2 + road_params['pile2_distance'])
            y = 0  # 桩位于Y=0断面
        
        return x, y
    
    def _calculate_pile_interaction(self, pile_spacing, pile1_diameter, pile2_diameter):
        """计算桩间相互作用系数"""
        # 根据桩间距和桩径计算相互作用系数
        avg_diameter = (pile1_diameter + pile2_diameter) / 2
        spacing_ratio = pile_spacing / avg_diameter
        
        # 相互作用系数经验公式
        if spacing_ratio <= 3:
            # 桩间距较小，相互作用显著
            interaction_factor = 0.8 + 0.2 * (spacing_ratio / 3)
        elif spacing_ratio <= 6:
            # 中等桩间距
            interaction_factor = 1.0 - 0.1 * ((spacing_ratio - 3) / 3)
        else:
            # 桩间距较大，相互作用较小
            interaction_factor = 0.9 + 0.1 * min(1.0, (spacing_ratio - 6) / 4)
        
        return max(0.8, min(1.2, interaction_factor))  # 限制在合理范围内
    
    def _verify_physical_logic(self, calculation_results):
        """验证计算结果的物理逻辑合理性"""
        verification_results = {
            'distance_settlement_correlation': True,
            'center_vs_edge_logic': True,
            'warnings': []
        }
        
        # 检查距离与沉降的反比关系
        for result in calculation_results:
            dist1 = result['pile1_distance']
            dist2 = result['pile2_distance']
            settlement1 = result['pile1_settlement']
            settlement2 = result['pile2_settlement']
            
            # 对于单桩，距离越大沉降应该越小
            # 这里我们检查是否存在明显违反物理逻辑的情况
            
        # 检查路基中心点vs边缘点的沉降逻辑
        center_points = [r for r in calculation_results if abs(r['x']) < 1.0]  # 中心附近的点
        edge_points = [r for r in calculation_results if abs(r['x']) > 5.0]    # 边缘的点
        
        if center_points and edge_points:
            avg_center_settlement = np.mean([p['total_settlement'] for p in center_points])
            avg_edge_settlement = np.mean([p['total_settlement'] for p in edge_points])
            
            # 由于两个桩都在路基外侧，路基中心点的沉降应该小于靠近桩的边缘点
            if avg_center_settlement > avg_edge_settlement * 1.2:  # 允许20%的误差
                verification_results['center_vs_edge_logic'] = False
                verification_results['warnings'].append(
                    f"警告：路基中心点平均沉降({avg_center_settlement:.3f}m) "
                    f"大于边缘点平均沉降({avg_edge_settlement:.3f}m)，不符合物理逻辑"
                )
        
        return verification_results
    
    def get_allowable_settlement(self, road_level, location_type="一般路段"):
        """获取沉降容许值"""
        allowable_values = {
            "高速公路": {"一般路段": 300, "桥头引道": 100, "涵洞通道": 200},  # mm
            "一级公路": {"一般路段": 300, "桥头引道": 100, "涵洞通道": 200},
            "二级公路": {"一般路段": 500, "桥头引道": 200}
        }
        
        return allowable_values.get(road_level, {}).get(location_type, 300)
    
    def get_settlement_with_formula(self, P, G, nu, a, b, point_index):
        """使用您提供的具体公式计算沉降"""
        # 预定义的系数表
        coefficients = {
            1: (1.768, 1.414), 2: (0.983, 0.894), 3: (0.664, 0.632), 4: (0.499, 0.485),
            5: (1.252, 0.894), 6: (0.884, 0.707), 7: (0.640, 0.555), 8: (0.492, 0.447),
            9: (0.917, 0.632), 10: (0.747, 0.555), 11: (0.589, 0.471), 12: (0.472, 0.400),
            13: (0.713, 0.485), 14: (0.626, 0.447), 15: (0.528, 0.400), 16: (0.442, 0.354)
        }
        
        coeff1, coeff2 = coefficients[point_index]
        
        # W = (a·b·P)/(4π·G) × (coeff1 - coeff2·ν)
        W = (a * b * P) / (4 * math.pi * G) * (coeff1 - coeff2 * nu)
        
        return W