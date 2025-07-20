# -*- coding: utf-8 -*-
"""
结果绘图器 - 实现图表绘制功能
"""

import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.patches import Circle
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
try:
    from scipy.interpolate import griddata
    from scipy.spatial import ConvexHull
except ImportError:
    griddata = None
    ConvexHull = None

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class ResultPlotter:
    """结果绘图器类"""
    
    def __init__(self):
        """初始化绘图器"""
        pass
        
    def get_settlement_color(self, settlement_mm, allowable_limit):
        """根据沉降值和容许值确定颜色
        颜色分布规则：
        - 沉降数值大于容许值时为红色
        - 小于容许值且大于容许值40%时为橙色
        - 小于容许值40%且大于容许值10%时为黄色
        - 小于容许值10%时为绿色
        """
        if settlement_mm > allowable_limit:  # 大于容许值
            return 'red'
        elif settlement_mm > allowable_limit * 0.4:  # 小于容许值且大于容许值40%
            return 'orange'
        elif settlement_mm > allowable_limit * 0.1:  # 小于容许值40%且大于容许值10%
            return 'yellow'
        else:  # 小于容许值10%
            return 'green'
    
    def settlement_distribution_plot(self, pile1_x, pile2_x, pile_diameter, pile_length, 
                                   roadbed_width, points_3d, settlements, max_settlement_threshold,
                                   pile1_settlement, pile2_settlement, interaction_coefficient,
                                   l1_distance_val, l2_distance_val):
        """
        根据效果图绘制沉降分布图，包含详细的桩体样式和尺寸标注
        """
        fig, ax = plt.subplots(figsize=(16, 12))
        
        # 设置坐标范围
        x_range = max(abs(pile1_x), abs(pile2_x)) * 1.3
        y_range = pile_length * 1.2
        ax.set_xlim(-x_range, x_range)
        ax.set_ylim(-y_range, y_range * 0.3)
        
        # === 1. 背景分层 ===
        # 上部灰色背景
        upper_bg = patches.Rectangle((-x_range, 0), 2*x_range, y_range*0.3, 
                                    facecolor='lightgray', alpha=0.3, zorder=0)
        ax.add_patch(upper_bg)
        
        # 下部点状填充背景
        xx, yy = np.meshgrid(np.linspace(-x_range, x_range, 100), 
                            np.linspace(-y_range, 0, 80))
        ax.scatter(xx.flatten(), yy.flatten(), s=0.5, c='gray', alpha=0.1, zorder=0)
        
        # === 2. 顶部黑色桥面结构 ===
        # 计算桩顶位置：pile_body_start + pile_top_height = -2.0 + 3.0 = 1.0
        pile_top_level = 1.0  # 桩的上沿位置
        bridge_height = pile_top_level  # 桥面下沿与桩上沿对齐
        bridge_rect = patches.Rectangle((-x_range*0.9, bridge_height), x_range*1.8, 3.0,
                                       facecolor='black', alpha=0.8, zorder=2)
        ax.add_patch(bridge_rect)
        
        # 桥面网格填充效果
        for i in range(int(x_range*1.8/2)):
            for j in range(2):
                x_grid = -x_range*0.9 + i*2
                y_grid = bridge_height + j*1.5
                if x_grid < x_range*0.9:
                    grid_rect = patches.Rectangle((x_grid, y_grid), 1.8, 1.2,
                                                facecolor='none', edgecolor='white', 
                                                linewidth=0.5, alpha=0.6, zorder=3)
                    ax.add_patch(grid_rect)
        
        # === 3. 棕色梯形路基 ===
        roadbed_height = 1.5
        roadbed_top_width = roadbed_width
        roadbed_bottom_width = roadbed_width * 1.2
        
        # 修正：让路基上沿与桥面下沿贴合
        roadbed_top_level = bridge_height  # 路基上沿与桥面下沿对齐
        
        roadbed_points = [
            [-roadbed_top_width/2, roadbed_top_level],  # 修改：使用bridge_height而不是0
            [roadbed_top_width/2, roadbed_top_level],   # 修改：使用bridge_height而不是0
            [roadbed_bottom_width/2, roadbed_top_level - roadbed_height],  # 修改：相对于新的上沿位置
            [-roadbed_bottom_width/2, roadbed_top_level - roadbed_height]  # 修改：相对于新的上沿位置
        ]
        roadbed = patches.Polygon(roadbed_points, facecolor='#A0522D', edgecolor='black', 
                                 linewidth=1.5, alpha=0.8, zorder=4)
        ax.add_patch(roadbed)
        
        # === 4. 桩体设计（白色背景+黑色交叉线条） ===
        def draw_pile(pile_x, pile_name):
            # 桩体参数
            pile_width = pile_diameter
            pile_top_height = 3.0  # 网格填充部分高度
            
            # 修正：桩的中间分界线与路基下沿齐平
            roadbed_bottom_level = roadbed_top_level - roadbed_height  # 路基下沿位置
            pile_middle_line = roadbed_bottom_level  # 桩的中间分界线与路基下沿对齐
            
            # 重新定义桩体各部分位置
            pile_top_start = pile_middle_line  # 桩顶部开始位置（中间分界线）
            pile_top_end = pile_top_start + pile_top_height  # 桩顶部结束位置
            pile_bottom = pile_middle_line - pile_length  # 桩底位置（桩长从中间线算起）
            
            # 桩顶部 - 白色背景矩形（网格填充区域）
            pile_top = patches.Rectangle((pile_x - pile_width/2, pile_top_start), 
                                       pile_width, pile_top_height,
                                       facecolor='white', edgecolor='black', 
                                       linewidth=2, alpha=1.0, zorder=5)
            ax.add_patch(pile_top)
            
            # 桩顶黑色网格交叉线条
            grid_spacing = 0.4
            # 垂直线条
            for i in range(1, int(pile_width/grid_spacing)):
                x_line = pile_x - pile_width/2 + i*grid_spacing
                ax.plot([x_line, x_line], [pile_top_start, pile_top_end], 
                       'black', linewidth=1.0, alpha=0.8, zorder=6)
            
            # 水平线条
            for j in range(1, int(pile_top_height/grid_spacing)):
                y_line = pile_top_start + j*grid_spacing
                ax.plot([pile_x - pile_width/2, pile_x + pile_width/2], [y_line, y_line], 
                       'black', linewidth=1.0, alpha=0.8, zorder=6)
            
            # 桩身 - 白色背景矩形（斜线填充区域）
            pile_body_height = pile_length  # 桩身高度就是桩长
            pile_body = patches.Rectangle((pile_x - pile_width/2, pile_bottom), 
                                        pile_width, pile_body_height,
                                        facecolor='white', edgecolor='black', 
                                        linewidth=2, alpha=1.0, zorder=5)
            ax.add_patch(pile_body)
            
            # 桩身黑色斜线填充效果
            diagonal_spacing = 0.6
            for i in range(int(pile_length/diagonal_spacing) + 1):
                y_start = pile_top_start - i*diagonal_spacing
                if y_start > pile_bottom:
                    # 左上到右下的斜线
                    ax.plot([pile_x - pile_width/2, pile_x + pile_width/2], 
                           [y_start, y_start - pile_width], 'black', linewidth=1.0, alpha=0.8, zorder=6)
                    # 右上到左下的斜线
                    ax.plot([pile_x - pile_width/2, pile_x + pile_width/2], 
                           [y_start - pile_width, y_start], 'black', linewidth=1.0, alpha=0.8, zorder=6)
            
            # 桩名称标注
            ax.text(pile_x, pile_bottom - 1.5, pile_name, 
                   ha='center', va='top', fontsize=10, fontweight='bold', 
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8), zorder=8)
            
            return pile_top_height
        
        # 绘制左右桩
        draw_pile(pile1_x, '桩1')
        draw_pile(pile2_x, '桩2')
        
        # === 5. 4×4=16个计算点 ===
        # 绘制带颜色的计算点圆圈，根据沉降值确定颜色
        for i, (point_data, settlement_val) in enumerate(zip(points_3d, settlements)):
            orig_x, orig_y, orig_z = point_data
            
            # 确定点的颜色 - 根据沉降值与阈值的比例
            # 确定点的颜色 - 使用更敏感的分级
            point_color = '#2E8B57'  # 默认深海绿
            if max_settlement_threshold > 0:
                settlement_ratio = settlement_val / max_settlement_threshold
                if settlement_ratio < 0.1:          # 0-10%
                    point_color = '#2E8B57'      # 极低沉降 - 深海绿
                elif settlement_ratio < 0.3:        # 10%-30%
                    point_color = '#32CD32'      # 低沉降 - 酸橙绿
                elif settlement_ratio < 0.6:        # 30%-60%
                    point_color = '#FFD700'      # 中等沉降 - 金色
                elif settlement_ratio < 0.9:        # 60%-90%
                    point_color = '#FF8C00'      # 高沉降 - 深橙色
                else:                               # >90%
                    point_color = '#DC143C'      # 最高沉降 - 深红色
            
            # 绘制计算点（圆圈）
            circle = patches.Circle((orig_x, -orig_z), 0.4, color=point_color, alpha=0.9, zorder=7)
            ax.add_patch(circle)
            
            # 保留点编号标注 - 使用原始位置标注，避免沉降后位置变化导致编号重叠或混乱
            ax.text(orig_x + 0.5, -orig_z + 0.5, f'P{i+1}', ha='center', va='center', 
                   fontsize=9, fontweight='bold', color='black', zorder=8,
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='white', 
                            edgecolor='black', alpha=0.7))
            
            # 计算剖面距离R的逻辑可以保留，如果其他地方需要用，但这里不再直接标注
            # r1_2d = math.sqrt((orig_x - pile1_x)**2 + orig_z**2)
            # r2_2d = math.sqrt((orig_x - pile2_x)**2 + orig_z**2)
            # min_r = min(r1_2d, r2_2d)
            
        # === 6. 浅蓝色尺寸标注 ===
        annotation_y = -0.5  # 向下平移，避免被路面遮挡
        arrow_props = dict(arrowstyle='<->', color='deepskyblue', lw=2)
        
        # L1 距离标注
        # l1_distance = abs(pile1_x + roadbed_width/2) # Removed old calculation
        ax.annotate('', xy=(pile1_x, annotation_y), xytext=(-roadbed_width/2, annotation_y),
                   arrowprops=arrow_props, zorder=10)
        ax.text((pile1_x - roadbed_width/2)/2, annotation_y + 0.5, f'L1 = {l1_distance_val:.1f}m', # Used l1_distance_val
               ha='center', va='bottom', fontsize=12, color='deepskyblue', fontweight='bold', zorder=10)
        
        # L2 距离标注  
        # l2_distance = abs(pile2_x - roadbed_width/2) # Removed old calculation
        ax.annotate('', xy=(pile2_x, annotation_y), xytext=(roadbed_width/2, annotation_y),
                   arrowprops=arrow_props, zorder=10)
        ax.text((pile2_x + roadbed_width/2)/2, annotation_y + 0.5, f'L2 = {l2_distance_val:.1f}m', # Used l2_distance_val
               ha='center', va='bottom', fontsize=12, color='deepskyblue', fontweight='bold', zorder=10)
        
        # x 路基宽度标注 (与L1、L2齐平)
        ax.annotate('', xy=(roadbed_width/2, annotation_y), xytext=(-roadbed_width/2, annotation_y),
                   arrowprops=arrow_props, zorder=10)
        ax.text(0, annotation_y + 0.5, f'x = {roadbed_width:.1f}m', 
               ha='center', va='bottom', fontsize=12, color='deepskyblue', fontweight='bold', zorder=10)
        
        # === 7. 网格虚线 ===
        # 绘制4×4网格的虚线
        unique_x = sorted(list(set([point[0] for point in points_3d])))
        unique_z = sorted(list(set([point[2] for point in points_3d])))
        
        for x in unique_x:
            ax.axvline(x, color='gray', linestyle='--', alpha=0.5, zorder=1)
        for z in unique_z:
            ax.axhline(-z, color='gray', linestyle='--', alpha=0.5, zorder=1)
        
        # === 8. 图例和信息 ===
        # legend_elements = [
        #     patches.Patch(facecolor='forestgreen', label='安全 (≤50%)'),
        #     patches.Patch(facecolor='gold', label='注意 (50-75%)'),
        #     patches.Patch(facecolor='darkorange', label='警告 (75-100%)'),
        #     patches.Patch(facecolor='crimson', label='超限 (>100%)'),
        # ]
        
        # ax.legend(handles=legend_elements, loc='upper right', 
        #          title='沉降安全评估', fontsize=10, title_fontsize=11) # 注释掉安全评估图例
        
        
        # === 10. 图形设置 ===
        # 设置坐标轴
        ax.set_xlabel('横向距离 X (m)', fontsize=12, fontweight='bold')
        ax.set_ylabel('深度 Z (m)', fontsize=12, fontweight='bold')
        ax.set_title('工程示意简图', fontsize=14, fontweight='bold', pad=20)
        
        # 设置网格
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal', adjustable='box')
        
        # 调整子图参数，确保标题和标签完全可见
        plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.15, hspace=0.4, wspace=0.3)
        return fig
        
    def create_settlement_plot(self, results):
        """创建沉降分析图表 - 基于工程示意简图显示沉降等级分布"""
        calc_points = results.get('points', [])
        if not calc_points:
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.text(0.5, 0.5, '无数据可用于生成沉降分析图', horizontalalignment='center',
                   verticalalignment='center', transform=ax.transAxes, fontsize=16, color='red')
            ax.set_title('沉降分析图', fontsize=16, fontweight='bold')
            ax.set_xticks([])
            ax.set_yticks([])
            return fig
            
        # 从 results 中分离输入参数和计算结果
        input_params = results.get('input_parameters', {})
        calc_safety_assessment = results.get('safety_assessment', {})
    
        # 从 input_params 提取路基和桩的原始参数
        gui_pile1_params = input_params.get('pile1', {})
        gui_pile2_params = input_params.get('pile2', {})
        gui_road_params = input_params.get('road_params', {})
    
        # 计算绘图所需的各项参数
        roadbed_width = gui_road_params.get('width', 20.0)
        l1_distance_val = gui_road_params.get('pile1_distance', 0.0)
        l2_distance_val = gui_road_params.get('pile2_distance', 0.0)
    
        pile1_x = -(roadbed_width / 2 + l1_distance_val)
        pile2_x = +(roadbed_width / 2 + l2_distance_val)
    
        pile_diameter = max(gui_pile1_params.get('diameter', 1.0), gui_pile2_params.get('diameter', 1.0))
        pile_length = max(gui_pile1_params.get('length', 20.0), gui_pile2_params.get('length', 20.0)) # 桩长（土下层）
    
        # 从计算结果中提取
        points_3d = [(p.get('x', 0), p.get('y', 0), p.get('z', 0)) for p in calc_points]
        settlements = [p.get('settlement_mm', 0) for p in calc_points]
        
        max_settlement_threshold = calc_safety_assessment.get('bridge_limit', 150.0)
        
        # 定义沉降等级区间（调整为更敏感的分级）
        levels = [
            (0, 0.1, '极低沉降', '#2E8B57'),      # 0-10% - 深海绿
            (0.1, 0.3, '低沉降', '#32CD32'),      # 10%-30% - 酸橙绿
            (0.3, 0.6, '中等沉降', '#FFD700'),    # 30%-60% - 金色
            (0.6, 0.9, '高沉降', '#FF8C00'),      # 60%-90% - 深橙色
            (0.9, float('inf'), '最高沉降', '#DC143C')  # >90% - 深红色
        ]
        
        pile1_settlement = 0
        if calc_points:
            pile1_settlement = max([p.get('pile1_settlement', 0) * 1000 for p in calc_points])
        
        pile2_settlement = 0
        if calc_points:
            pile2_settlement = max([p.get('pile2_settlement', 0) * 1000 for p in calc_points])
            
        interaction_coefficient = 0.8 # 与gui/main_window.py中一致
    
        # 首先绘制工程示意简图作为基础
        fig = self.settlement_distribution_plot(
            pile1_x, pile2_x, pile_diameter, pile_length, 
            roadbed_width, points_3d, settlements, max_settlement_threshold,
            pile1_settlement, pile2_settlement, interaction_coefficient,
            l1_distance_val, l2_distance_val # 确保传递了正确的L1, L2
        )
        
        # 获取当前的坐标轴
        ax = fig.gca()
        
        # 重新设置标题
        ax.set_title('沉降分析图 - 基于工程示意简图', 
                    fontsize=14, fontweight='bold', pad=25) # 增加 pad 值

        # 确保 settlements 列表不为空，否则无法计算 min/max
        if not settlements:
            # 如果没有沉降数据，可以提前返回或绘制一个提示信息
            ax.text(0.5, 0.5, '无沉降数据可供分析', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
            plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.15, hspace=0.4, wspace=0.3)
            return fig

        # 计算沉降值的统计信息（移到循环之前）
        min_settlement = min(settlements)
        max_settlement = max(settlements)
        settlement_range = max_settlement - min_settlement
        
        # 基于实际沉降值范围的动态分级（移到循环之前）
        if max_settlement_threshold <= 0: # 增加对 max_settlement_threshold 的检查，防止除零
            # 如果阈值为0或负数，使用默认的绝对沉降值分级
            levels = [
                (0, 10, '极低沉降', '#2E8B57'), # 假设单位mm
                (10, 30, '低沉降', '#32CD32'),
                (30, 60, '中等沉降', '#FFD700'),
                (60, 90, '高沉降', '#FF8C00'),
                (90, float('inf'), '最高沉降', '#DC143C')
            ]
        elif settlement_range > 0:
            # 使用四分位数进行分级，并确保 qN/max_settlement_threshold 不会导致问题
            q1 = min_settlement + settlement_range * 0.2
            q2 = min_settlement + settlement_range * 0.4
            q3 = min_settlement + settlement_range * 0.6
            q4 = min_settlement + settlement_range * 0.8
            
            levels = [
                (0, q1/max_settlement_threshold if max_settlement_threshold else 0.2, '极低沉降', '#2E8B57'),
                (q1/max_settlement_threshold if max_settlement_threshold else 0.2, q2/max_settlement_threshold if max_settlement_threshold else 0.4, '低沉降', '#32CD32'),
                (q2/max_settlement_threshold if max_settlement_threshold else 0.4, q3/max_settlement_threshold if max_settlement_threshold else 0.6, '中等沉降', '#FFD700'),
                (q3/max_settlement_threshold if max_settlement_threshold else 0.6, q4/max_settlement_threshold if max_settlement_threshold else 0.8, '高沉降', '#FF8C00'),
                (q4/max_settlement_threshold if max_settlement_threshold else 0.8, float('inf'), '最高沉降', '#DC143C')
            ]
        else:
            # 如果所有点沉降值相同，或者 max_settlement_threshold 有问题，使用基于阈值的默认比例分级
            levels = [
                (0, 0.1, '极低沉降', '#2E8B57'),
                (0.1, 0.3, '低沉降', '#32CD32'),
                (0.3, 0.6, '中等沉降', '#FFD700'),
                (0.6, 0.9, '高沉降', '#FF8C00'),
                (0.9, float('inf'), '最高沉降', '#DC143C')
            ]
        
        # 在基础图上绘制沉降后的、带颜色的计算点
        # 使用 calc_points 进行迭代，因为它包含 settlement_mm
        for i, p_data in enumerate(calc_points):
            orig_x = p_data.get('x', 0)
            orig_z = p_data.get('z', 0) # 原始深度（正值）
            s_mm = p_data.get('settlement_mm', 0)
    
            # 计算沉降后的Z坐标（单位：米），沉降使深度增加
            adjusted_z_m = orig_z + (s_mm / 1000.0)
    
            # 确定点的颜色
            point_color = 'gray' # 默认颜色
            if max_settlement_threshold > 0: # 避免除零
                settlement_ratio = s_mm / max_settlement_threshold
                # 确保 levels 在这里是正确定义的
                for r_min, r_max, _, color_val in levels: # 现在levels应该已经定义了
                    if r_min <= settlement_ratio < r_max:
                        point_color = color_val
                        break
                # 处理超出最后一个区间的情况 (例如 ratio >= 1.0 for '最高沉降')
                # 同样要确保 levels 存在且不为空
                if levels and settlement_ratio >= levels[-1][0]: 
                     point_color = levels[-1][3] 
            elif s_mm > 0: # 如果没有阈值，但有沉降，根据绝对值给一个颜色
                # 这里的逻辑可以根据需要调整，例如使用上面定义的绝对值levels
                for r_min_abs, r_max_abs, _, color_val_abs in levels: # 假设levels此时是绝对值分级
                    if r_min_abs <= s_mm < r_max_abs:
                        point_color = color_val_abs
                        break
                if levels and s_mm >= levels[-1][0]:
                    point_color = levels[-1][3]
            
            # 绘制计算点（圆圈）在沉降后的位置
            # 注意Y轴镜像是 -z
            circle = patches.Circle((orig_x, -adjusted_z_m), 0.4, color=point_color, alpha=0.9, zorder=7)
            ax.add_patch(circle)
            
            # 可以在此处添加沉降数值标注，如果需要
            # ax.text(orig_x, -adjusted_z_m - 0.6, f'{s_mm:.2f}mm', 
            #        ha='center', va='top', fontsize=8, color=point_color,
            #        bbox=dict(boxstyle='round,pad=0.1', facecolor='white', alpha=0.7))
        
        # 创建渐近变化的颜色条图例
        from matplotlib.colors import LinearSegmentedColormap
        import matplotlib.patches as mpatches
        
        # 定义颜色映射 - 从绿色(低沉降)到红色(高沉降)
        colors = ['#2E8B57', '#32CD32', '#FFD700', '#FF8C00', '#DC143C']
        n_bins = 100
        cmap = LinearSegmentedColormap.from_list('settlement', colors, N=n_bins)
        
        # 在右侧添加颜色条图例 - 增加间距给标签留空间
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="3%", pad=0.15)  # 增加pad值
        
        # 创建颜色条数据
        settlement_normalized = np.linspace(min_settlement, max_settlement, n_bins)
        settlement_2d = settlement_normalized.reshape(-1, 1)
        
        # 绘制颜色条 - 确保方向正确
        im = cax.imshow(settlement_2d, aspect='auto', cmap=cmap, 
                       extent=[0, 1, min_settlement, max_settlement],
                       origin='lower')  # 底部是最小值(绿色)，顶部是最大值(红色)
        cax.set_ylabel('沉降值 (mm)', fontsize=12, fontweight='bold')
        
        # 设置颜色条的刻度
        cax.set_yticks(np.linspace(min_settlement, max_settlement, 6))
        cax.tick_params(labelsize=8)
        
        # 添加等级标签到颜色条 - 直接使用原始levels顺序
        label_positions = np.linspace(min_settlement, max_settlement, len(levels))
        
        # 直接使用levels，不再反转
        for i, (start_ratio, end_ratio, label, color) in enumerate(levels):
            y_pos = label_positions[i]
            
            cax.text(1.1, y_pos, label, fontsize=9, 
                    verticalalignment='center', fontweight='bold',
                    color='black')
        
        # 添加阈值线
        threshold_y = max_settlement_threshold
        if threshold_y <= max_settlement:
            cax.axhline(y=threshold_y, color='red', linestyle='--', linewidth=2)
            cax.text(1.1, threshold_y, f'阈值\n{threshold_y}mm', 
                    fontsize=8, verticalalignment='center', 
                    color='red', fontweight='bold')
        
        # 移除颜色条的x轴刻度
        cax.set_xticks([])
        
        # 调整子图参数，确保标题和标签完全可见
        plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.15, hspace=0.4, wspace=0.3)
        return fig
        
    def create_contour_plot(self, results):
        """创建等高线图 - 真正的等高线图而不是散点图"""
        if griddata is None:
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.text(0.5, 0.5, '绘制等高线图需要安装scipy库\n请运行: pip install scipy',
                   horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
                   fontsize=14, color='red', bbox=dict(facecolor='white', alpha=0.8))
            ax.set_title('等高线图 - 依赖缺失', fontsize=14, fontweight='bold')
            ax.set_xticks([])
            ax.set_yticks([])
            return fig

        calc_points = results.get('points', [])
        if not calc_points or len(calc_points) < 3:
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.text(0.5, 0.5, '数据不足，无法生成等高线图\n(至少需要3个计算点)',
                   horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
                   fontsize=14, color='red')
            ax.set_title('等高线分析图 - 数据不足', fontsize=14, fontweight='bold')
            ax.set_xticks([])
            ax.set_yticks([])
            return fig
        
        # 从 results 中分离输入参数和计算结果
        input_params = results.get('input_parameters', {})
        calc_safety_assessment = results.get('safety_assessment', {})

        # 从 input_params 提取路基和桩的原始参数
        gui_pile1_params = input_params.get('pile1', {})
        gui_pile2_params = input_params.get('pile2', {})
        gui_road_params = input_params.get('road_params', {})

        # 计算绘图所需的各项参数
        roadbed_width = gui_road_params.get('width', 20.0)
        l1_distance_val = gui_road_params.get('pile1_distance', 0.0)
        l2_distance_val = gui_road_params.get('pile2_distance', 0.0)

        pile1_x = -(roadbed_width / 2 + l1_distance_val)
        pile2_x = +(roadbed_width / 2 + l2_distance_val)

        pile_diameter = max(gui_pile1_params.get('diameter', 1.0), gui_pile2_params.get('diameter', 1.0))
        pile_length = max(gui_pile1_params.get('length', 20.0), gui_pile2_params.get('length', 20.0))

        # 从计算结果中提取数据
        if not calc_points:
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.text(0.5, 0.5, '无沉降数据可供分析', horizontalalignment='center', 
                   verticalalignment='center', transform=ax.transAxes, fontsize=14)
            ax.set_title('等高线分析图', fontsize=14, fontweight='bold')
            return fig

        # 提取坐标和沉降数据
        x_coords = [p.get('x', 0) for p in calc_points]
        z_coords = [p.get('z', 0) for p in calc_points]  # 深度坐标
        settlements = [p.get('settlement_mm', 0) for p in calc_points]
        
        max_settlement_threshold = calc_safety_assessment.get('bridge_limit', 150.0)
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # 设置绘图范围
        x_min, x_max = min(x_coords) - 5, max(x_coords) + 5
        z_min, z_max = min(z_coords) - 5, max(z_coords) + 5
        
        # 创建网格用于插值
        xi = np.linspace(x_min, x_max, 100)
        zi = np.linspace(z_min, z_max, 100)
        Xi, Zi = np.meshgrid(xi, zi)
        
        # 使用scipy的griddata进行插值
        points = np.array(list(zip(x_coords, z_coords)))
        values = np.array(settlements)
        
        # 插值生成等高线数据
        Yi = griddata(points, values, (Xi, Zi), method='cubic', fill_value=0)
        
        # 绘制基础结构（路基和桩）
        # 绘制路基（地面）
        roadbed_x = [-roadbed_width/2, roadbed_width/2, roadbed_width/2, -roadbed_width/2, -roadbed_width/2]
        roadbed_z = [0, 0, -2, -2, 0]
        ax.fill(roadbed_x, roadbed_z, color='lightgray', alpha=0.7, label='路基')
        ax.plot(roadbed_x, roadbed_z, 'k-', linewidth=2)
        
        # 绘制桩1
        pile1_width = pile_diameter / 2
        pile1_rect_x = [pile1_x - pile1_width, pile1_x + pile1_width, 
                       pile1_x + pile1_width, pile1_x - pile1_width, pile1_x - pile1_width]
        pile1_rect_z = [0, 0, -pile_length, -pile_length, 0]
        ax.fill(pile1_rect_x, pile1_rect_z, color='black', alpha=0.8)
        ax.plot(pile1_rect_x, pile1_rect_z, 'k-', linewidth=2)
        
        # 绘制桩2
        pile2_width = pile_diameter / 2
        pile2_rect_x = [pile2_x - pile2_width, pile2_x + pile2_width, 
                       pile2_x + pile2_width, pile2_x - pile2_width, pile2_x - pile2_width]
        pile2_rect_z = [0, 0, -pile_length, -pile_length, 0]
        ax.fill(pile2_rect_x, pile2_rect_z, color='black', alpha=0.8)
        ax.plot(pile2_rect_x, pile2_rect_z, 'k-', linewidth=2)
        
        # 绘制等高线
        min_settlement = min(settlements)
        max_settlement = max(settlements)
        
        # 定义等高线级别
        if max_settlement > min_settlement:
            levels_contour = np.linspace(min_settlement, max_settlement, 15)
        else:
            levels_contour = [min_settlement]
        
        # 绘制填充等高线
        contourf = ax.contourf(Xi, -Zi, Yi, levels=levels_contour, cmap='RdYlGn_r', alpha=0.6)
        
        # 绘制等高线线条
        contour_lines = ax.contour(Xi, -Zi, Yi, levels=levels_contour, colors='black', linewidths=0.5, alpha=0.8)
        
        # 添加等高线标签
        ax.clabel(contour_lines, inline=True, fontsize=8, fmt='%.1f')
        
        # 绘制计算点
        for i, p_data in enumerate(calc_points):
            x = p_data.get('x', 0)
            z = -p_data.get('z', 0)  # 注意Y轴镜像
            settlement = p_data.get('settlement_mm', 0)
            
            # 根据沉降值确定点的颜色
            if settlement < max_settlement_threshold * 0.2:
                color = '#2E8B57'  # 极低沉降
            elif settlement < max_settlement_threshold * 0.4:
                color = '#32CD32'  # 低沉降
            elif settlement < max_settlement_threshold * 0.6:
                color = '#FFD700'  # 中等沉降
            elif settlement < max_settlement_threshold * 0.8:
                color = '#FF8C00'  # 高沉降
            else:
                color = '#DC143C'  # 最高沉降
            
            ax.scatter(x, z, c=color, s=50, edgecolors='black', linewidth=1, zorder=10)
            
            # 添加点标签
            point_name = p_data.get('name', f'P{i+1}')
            ax.annotate(f'{point_name}\n{settlement:.1f}mm', 
                       (x, z), xytext=(5, 5), textcoords='offset points',
                       fontsize=8, ha='left', va='bottom',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        
        # 添加颜色条
        cbar = plt.colorbar(contourf, ax=ax, shrink=0.8, aspect=20)
        cbar.set_label('沉降值 (mm)', fontsize=12, fontweight='bold')
        
        # 添加阈值线到颜色条
        if max_settlement_threshold <= max_settlement:
            cbar.ax.axhline(y=max_settlement_threshold, color='red', linestyle='--', linewidth=2)
            cbar.ax.text(0.5, max_settlement_threshold, f'阈值 {max_settlement_threshold}mm', 
                        transform=cbar.ax.get_yaxis_transform(), 
                        ha='left', va='center', color='red', fontweight='bold')
        
        # 设置坐标轴
        ax.set_xlabel('横向距离 X (m)', fontsize=12, fontweight='bold')
        ax.set_ylabel('深度 Z (m)', fontsize=12, fontweight='bold')
        ax.set_title('沉降等高线分析图', fontsize=14, fontweight='bold', pad=20)
        
        # 设置网格
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # 设置坐标轴范围
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(-z_max, -z_min)
        
        # 添加图例
        legend_elements = [
            plt.Rectangle((0, 0), 1, 1, facecolor='lightgray', alpha=0.7, label='路基'),
            plt.Rectangle((0, 0), 1, 1, facecolor='black', alpha=0.8, label='桩基'),
            plt.Line2D([0], [0], color='black', linewidth=0.5, label='等高线'),
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        # 调整布局 - 设置更大的边距确保标签完整显示
        plt.subplots_adjust(left=0.12, right=0.88, top=0.90, bottom=0.12, hspace=0.3, wspace=0.3)
        return fig
        
    def create_radar_plot(self, results):
        """创建雷达图"""
        points = results.get('points', [])
        if not points:
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.text(0.5, 0.5, '无数据可用于生成雷达图', horizontalalignment='center',
                   verticalalignment='center', transform=ax.transAxes, fontsize=16, color='red')
            ax.set_title('沉降雷达分析图', fontsize=16, fontweight='bold')
            ax.set_xticks([])
            ax.set_yticks([])
            return fig
            
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), 
                                      subplot_kw=dict(projection='polar'))
        fig.suptitle('沉降雷达分析图', fontsize=16, fontweight='bold')
        
        # 1. 按深度分层的雷达图
        ax1.set_title('分层沉降雷达图', pad=20, fontweight='bold')
        
        # 按深度分组
        depth_groups = {}
        for point in points:
            depth = point.get('z', 0)
            if depth not in depth_groups:
                depth_groups[depth] = []
            depth_groups[depth].append(point)
        
        angles = np.linspace(0, 2*np.pi, len(points)//len(depth_groups), endpoint=False)
        angles = np.concatenate((angles, [angles[0]]))  # 闭合图形
        
        colors = ['red', 'blue', 'green', 'orange', 'purple']
        for i, (depth, group) in enumerate(sorted(depth_groups.items())):
            settlements = [p.get('settlement_mm', 0) for p in group]
            settlements.append(settlements[0])  # 闭合图形
            
            ax1.plot(angles, settlements, 'o-', linewidth=2, 
                    label=f'深度 {depth}m', color=colors[i % len(colors)])
            ax1.fill(angles, settlements, alpha=0.25, color=colors[i % len(colors)])
        
        ax1.set_rlabel_position(0)
        ax1.legend(loc='upper right', bbox_to_anchor=(1.2, 1.0))
        
        # 2. 距离-沉降雷达图
        ax2.set_title('距离-沉降雷达图', pad=20, fontweight='bold')
        
        # 计算角度（基于计算点位置）
        angles_2 = []
        distances = []
        settlements_2 = []
        
        for point in points:
            angle = math.atan2(point['y'], point['x']) if point['x'] != 0 else math.pi/2
            if angle < 0:
                angle += 2*math.pi
            angles_2.append(angle)
            distances.append(math.sqrt(point['x']**2 + point['y']**2))
            settlements_2.append(point['settlement_mm'])
        
        # 按角度排序
        sorted_indices = np.argsort(angles_2)
        angles_2 = [angles_2[i] for i in sorted_indices]
        settlements_2 = [settlements_2[i] for i in sorted_indices]
        distances = [distances[i] for i in sorted_indices]
        
        # 绘制雷达图
        ax2.scatter(angles_2, settlements_2, c=distances, cmap='viridis', s=100, alpha=0.8)
        
        # 连接线
        angles_2.append(angles_2[0])
        settlements_2.append(settlements_2[0])
        ax2.plot(angles_2, settlements_2, 'b-', alpha=0.5)
        
        ax2.set_rlabel_position(45)
        
        # 调整子图参数，确保标题和标签完全可见
        plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.15, hspace=0.4, wspace=0.3)
        return fig
    
    def create_waterfall_plot(self, results):
        """创建瀑布图"""
        points = results.get('points', [])
        if not points:
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.text(0.5, 0.5, '无数据可用于生成瀑布图', horizontalalignment='center',
                   verticalalignment='center', transform=ax.transAxes, fontsize=16, color='red')
            ax.set_title('沉降瀑布分析图', fontsize=16, fontweight='bold')
            ax.set_xticks([])
            ax.set_yticks([])
            return fig
            
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        fig.suptitle('沉降瀑布分析图', fontsize=16, fontweight='bold')
        
        # 1. 按计算点顺序的瀑布图
        settlements = [p['settlement_mm'] for p in points]
        point_names = [f"W{i+1}" for i in range(len(points))]
        
        # 计算累积值
        cumulative = np.cumsum([0] + settlements)
        
        # 绘制瀑布图
        for i in range(len(settlements)):
            height = settlements[i]
            bottom = cumulative[i]
            color = 'green' if height < 10 else 'orange' if height < 20 else 'red'
            
            bar = ax1.bar(i, height, bottom=bottom, color=color, alpha=0.7, 
                         edgecolor='black', linewidth=1)
            
            # 添加连接线
            if i < len(settlements) - 1:
                ax1.plot([i+0.4, i+1-0.4], [cumulative[i+1], cumulative[i+1]], 
                        'k--', alpha=0.5)
            
            # 添加数值标签
            ax1.text(i, bottom + height/2, f'{height:.2f}', 
                    ha='center', va='center', fontweight='bold', fontsize=8)
        
        ax1.set_title('计算点沉降瀑布图', fontweight='bold')
        ax1.set_xlabel('计算点')
        ax1.set_ylabel('沉降值 (mm)')
        ax1.set_xticks(range(len(point_names)))
        ax1.set_xticklabels(point_names, rotation=45)
        ax1.grid(True, alpha=0.3)
        
        # 2. 按深度分层的瀑布图
        depth_groups = {}
        for point in points:
            depth = point['z']
            if depth not in depth_groups:
                depth_groups[depth] = []
            depth_groups[depth].append(point['settlement_mm'])
        
        depths = sorted(depth_groups.keys())
        avg_settlements = [np.mean(depth_groups[d]) for d in depths]
        
        # 计算累积平均值
        cumulative_avg = np.cumsum([0] + avg_settlements)
        
        for i, depth in enumerate(depths):
            height = avg_settlements[i]
            bottom = cumulative_avg[i]
            
            # 颜色基于深度
            color = plt.cm.viridis(i / len(depths))
            
            bar = ax2.bar(i, height, bottom=bottom, color=color, alpha=0.7, 
                         edgecolor='black', linewidth=1)
            
            # 添加连接线
            if i < len(depths) - 1:
                ax2.plot([i+0.4, i+1-0.4], [cumulative_avg[i+1], cumulative_avg[i+1]], 
                        'k--', alpha=0.5)
            
            # 添加数值标签
            ax2.text(i, bottom + height/2, f'{height:.2f}', 
                    ha='center', va='center', fontweight='bold', fontsize=9)
        
        ax2.set_title('深度分层平均沉降瀑布图', fontweight='bold')
        ax2.set_xlabel('深度 (m)')
        ax2.set_ylabel('平均沉降值 (mm)')
        ax2.set_xticks(range(len(depths)))
        ax2.set_xticklabels([f'{d}m' for d in depths])
        ax2.grid(True, alpha=0.3)
        
        # 调整子图参数，确保标题和标签完全可见
        plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.15, hspace=0.4, wspace=0.3)
        return fig
    
    def create_influence_zone_plot(self, results):
        """创建影响区域分析图"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        fig.suptitle('桥梁工程影响区域分析图', fontsize=16, fontweight='bold')
        
        points = results['points']
        safety = results['safety_assessment']
        
        # 1. 影响区域平面图
        x = [p['x'] for p in points]
        y = [p['y'] for p in points]
        settlements = [p['settlement_mm'] for p in points]
        
        # 根据沉降值设置颜色和大小
        colors = []
        sizes = []
        for settlement in settlements:
            if settlement > safety['bridge_limit']:
                colors.append('red')
                sizes.append(200)
            elif settlement > 10:  # 10mm作为影响阈值
                colors.append('orange')
                sizes.append(150)
            else:
                colors.append('green')
                sizes.append(100)
        
        scatter = ax1.scatter(x, y, c=colors, s=sizes, alpha=0.7, edgecolors='black')
        
        # 绘制影响区域边界
        if len(x) > 3:
            try:
                # 找到超过影响阈值的点
                influence_points = [(x[i], y[i]) for i, s in enumerate(settlements) if s > 5]
                if len(influence_points) > 2:
                    influence_points = np.array(influence_points)
                    if ConvexHull is not None:
                        hull = ConvexHull(influence_points)
                        for simplex in hull.simplices:
                            ax1.plot(influence_points[simplex, 0], influence_points[simplex, 1], 'r-', alpha=0.5)
            except:
                pass
        
        # 添加桩基位置
        ax1.plot(0, 0, 'ks', markersize=15, label='桩基中心')
        
        # 添加图例
        legend_elements = [
            plt.scatter([], [], c='green', s=100, label='安全区域 (<10mm)'),
            plt.scatter([], [], c='orange', s=150, label='影响区域 (10-20mm)'),
            plt.scatter([], [], c='red', s=200, label=f'超限区域 (>{safety["bridge_limit"]}mm)'),
            plt.scatter([], [], c='black', s=200, marker='s', label='桩基中心')
        ]
        ax1.legend(handles=legend_elements, loc='upper right')
        
        ax1.set_title('影响区域分布图', fontweight='bold')
        ax1.set_xlabel('X坐标 (m)')
        ax1.set_ylabel('Y坐标 (m)')
        ax1.grid(True, alpha=0.3)
        ax1.set_aspect('equal')
        
        # 2. 安全性分析柱状图
        safety_categories = ['安全点位', '影响点位', '超限点位']
        safe_count = sum(1 for s in settlements if s <= 10)
        influence_count = sum(1 for s in settlements if 10 < s <= safety['bridge_limit'])
        exceed_count = sum(1 for s in settlements if s > safety['bridge_limit'])
        
        counts = [safe_count, influence_count, exceed_count]
        colors_bar = ['green', 'orange', 'red']
        
        bars = ax2.bar(safety_categories, counts, color=colors_bar, alpha=0.7, edgecolor='black')
        
        # 添加百分比标签
        total_points = len(settlements)
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            percentage = (count / total_points) * 100
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{count}\n({percentage:.1f}%)', ha='center', va='bottom', fontweight='bold')
        
        ax2.set_title('安全性统计分析', fontweight='bold')
        ax2.set_ylabel('计算点数量')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # 调整子图参数，确保标题和标签完全可见
        plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.15, hspace=0.4, wspace=0.3)
        return fig
    
    def create_comprehensive_analysis(self, results):
        """创建综合分析图表"""
        fig = plt.figure(figsize=(20, 12))
        fig.suptitle('桩基沉降影响范围综合分析报告', fontsize=18, fontweight='bold')
        
        # 创建子图布局
        gs = fig.add_gridspec(3, 4, hspace=0.4, wspace=0.3, 
                             top=0.92, bottom=0.12, left=0.06, right=0.96)
        
        points = results['points']
        x = [p['x'] for p in points]
        y = [p['y'] for p in points]
        z = [p['settlement_mm'] for p in points]
        depths = [p['z'] for p in points]
        
        # 1. 主要沉降分布图
        ax1 = fig.add_subplot(gs[0, :2])
        scatter = ax1.scatter(x, y, c=z, cmap='RdYlBu_r', s=120, alpha=0.8, edgecolors='black')
        plt.colorbar(scatter, ax=ax1, label='沉降值 (mm)')
        ax1.set_title('沉降空间分布图', fontweight='bold', fontsize=14)
        ax1.set_xlabel('X坐标 (m)')
        ax1.set_ylabel('Y坐标 (m)')
        ax1.grid(True, alpha=0.3)
        
        # 2. 安全评估饼图
        ax2 = fig.add_subplot(gs[0, 2])
        safety = results['safety_assessment']
        safe_count = sum(1 for s in z if s <= 10)
        influence_count = sum(1 for s in z if 10 < s <= safety['bridge_limit'])
        exceed_count = sum(1 for s in z if s > safety['bridge_limit'])
        
        sizes = [safe_count, influence_count, exceed_count]
        labels = ['安全', '影响', '超限']
        colors = ['green', 'orange', 'red']
        
        wedges, texts, autotexts = ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                          startangle=90, textprops={'fontweight': 'bold'})
        ax2.set_title('安全性分布', fontweight='bold', fontsize=12)
        
        # 4. 深度-沉降关系
        ax4 = fig.add_subplot(gs[1, :2])
        depth_settlements = list(zip(depths, z))
        depth_settlements.sort()
        depths_sorted, z_sorted = zip(*depth_settlements)
        
        ax4.plot(depths_sorted, z_sorted, 'bo-', linewidth=2, markersize=8, alpha=0.7)
        ax4.axhline(y=safety['bridge_limit'], color='red', linestyle='--', linewidth=2, 
                   label=f'桥梁限值 ({safety["bridge_limit"]}mm)')
        ax4.axhline(y=safety['general_limit'], color='orange', linestyle='--', linewidth=2,
                   label=f'一般限值 ({safety["general_limit"]}mm)')
        
        ax4.set_title('深度-沉降关系曲线', fontweight='bold', fontsize=14)
        ax4.set_xlabel('深度 (m)')
        ax4.set_ylabel('沉降值 (mm)')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # 5. 距离影响分析
        ax5 = fig.add_subplot(gs[1, 2:])
        distances = [math.sqrt(xi**2 + yi**2) for xi, yi in zip(x, y)]
        
        ax5.scatter(distances, z, c=depths, cmap='viridis', s=100, alpha=0.8, edgecolors='black')
        plt.colorbar(ax5.collections[0], ax=ax5, label='深度 (m)')
        
        # 拟合趋势线
        if len(distances) > 1:
            z_fit = np.polyfit(distances, z, 2)
            p = np.poly1d(z_fit)
            x_trend = np.linspace(min(distances), max(distances), 100)
            ax5.plot(x_trend, p(x_trend), 'r-', linewidth=2, alpha=0.7, label='趋势线')
            ax5.legend()
        
        ax5.set_title('距离-沉降关系分析', fontweight='bold', fontsize=14)
        ax5.set_xlabel('距离 (m)')
        ax5.set_ylabel('沉降值 (mm)')
        ax5.grid(True, alpha=0.3)
        
        return fig
    
    def save_all_plots(self, results, output_dir="output"):
        """保存所有图表到指定目录"""
        import os
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 保存各种图表（删除影响区域图和综合分析图）
        plots = {
            'settlement_analysis': self.create_settlement_plot(results),
            'contour_analysis': self.create_contour_plot(results),
            'radar_analysis': self.create_radar_plot(results),
            'waterfall_analysis': self.create_waterfall_plot(results)
        }
        
        saved_files = []
        for name, fig in plots.items():
            filename = os.path.join(output_dir, f"{name}.png")
            fig.savefig(filename, dpi=300, bbox_inches='tight')
            saved_files.append(filename)
            plt.close(fig)
        
        return saved_files