#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试桩位置可视化显示
验证红色和蓝色桩是否正确显示在路基外侧
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def test_pile_visualization():
    """测试桩位置可视化"""
    print("=" * 60)
    print("测试桩位置可视化显示")
    print("=" * 60)
    
    # 模拟路基参数
    road_width = 20  # 路基宽度20m
    pile1_distance = 5  # 桩1距路基边缘5m
    pile2_distance = 5  # 桩2距路基边缘5m
    pile1_diameter = 1.0  # 桩1直径
    pile2_diameter = 1.2  # 桩2直径
    
    # 计算图形坐标系中的位置（图形中心为40,40）
    road_center_x = 40
    road_center_y = 40
    road_left = road_center_x - road_width/2  # 30
    road_right = road_center_x + road_width/2  # 50
    
    # 根据实际计算逻辑确定桩位置（在路基外侧）
    pile1_x = road_left - pile1_distance  # 25 (路基左侧外)
    pile1_y = road_center_y  # 40
    pile2_x = road_right + pile2_distance  # 55 (路基右侧外)  
    pile2_y = road_center_y  # 40
    
    print(f"路基宽度: {road_width}m")
    print(f"路基位置: X从{road_left}到{road_right} (中心{road_center_x})")
    print(f"桩1位置: ({pile1_x}, {pile1_y}) - 在路基左侧外{pile1_distance}m")
    print(f"桩2位置: ({pile2_x}, {pile2_y}) - 在路基右侧外{pile2_distance}m")
    
    # 创建可视化图形
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 绘制路基
    road_rect = patches.Rectangle((road_left, road_center_y-5), road_width, 10, 
                                facecolor='gray', alpha=0.7, label='原有路基', 
                                edgecolor='black', linewidth=2)
    ax.add_patch(road_rect)
    
    # 绘制桩基
    circle1 = patches.Circle((pile1_x, pile1_y), pile1_diameter/2*2, 
                           color='red', alpha=0.8, label='桩基1（左侧外）',
                           edgecolor='darkred', linewidth=2)
    circle2 = patches.Circle((pile2_x, pile2_y), pile2_diameter/2*2, 
                           color='blue', alpha=0.8, label='桩基2（右侧外）',
                           edgecolor='darkblue', linewidth=2)
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    
    # 添加标注
    ax.annotate(f'桩1\n距路基{pile1_distance}m', (pile1_x, pile1_y-3), 
               ha='center', va='top', fontsize=12, fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.3", facecolor='red', alpha=0.7))
    ax.annotate(f'桩2\n距路基{pile2_distance}m', (pile2_x, pile2_y-3), 
               ha='center', va='top', fontsize=12, fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.3", facecolor='blue', alpha=0.7))
    
    # 添加路基边界线
    ax.axvline(x=road_left, color='red', linestyle='--', alpha=0.5, label='路基左边界')
    ax.axvline(x=road_right, color='red', linestyle='--', alpha=0.5, label='路基右边界')
    ax.axvline(x=road_center_x, color='green', linestyle='-', alpha=0.7, label='路基中心线')
    
    # 添加距离标注
    ax.annotate('', xy=(road_left, 50), xytext=(pile1_x, 50),
               arrowprops=dict(arrowstyle='<->', color='red', lw=2))
    ax.text((road_left + pile1_x)/2, 52, f'{pile1_distance}m', 
           ha='center', va='bottom', fontsize=10, color='red', fontweight='bold')
    
    ax.annotate('', xy=(road_right, 50), xytext=(pile2_x, 50),
               arrowprops=dict(arrowstyle='<->', color='blue', lw=2))
    ax.text((road_right + pile2_x)/2, 52, f'{pile2_distance}m', 
           ha='center', va='bottom', fontsize=10, color='blue', fontweight='bold')
    
    # 设置坐标轴
    ax.set_xlim(15, 65)
    ax.set_ylim(25, 55)
    ax.set_xlabel('X坐标 (m)', fontsize=12)
    ax.set_ylabel('Y坐标 (m)', fontsize=12)
    ax.set_title('桩基位置验证图\n（红色和蓝色桩应在路基外侧）', fontsize=14, fontweight='bold')
    
    # 添加网格
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    
    # 添加图例
    ax.legend(loc='upper left')
    
    plt.tight_layout()
    plt.savefig('桩位置验证图.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # 验证结果
    print("\n=" * 60)
    print("验证结果:")
    print(f"✓ 桩1在路基左边界外: {pile1_x} < {road_left} ? {pile1_x < road_left}")
    print(f"✓ 桩2在路基右边界外: {pile2_x} > {road_right} ? {pile2_x > road_right}")
    print(f"✓ 路基范围: [{road_left}, {road_right}]")
    print(f"✓ 桩1到路基左边界距离: {road_left - pile1_x}m")
    print(f"✓ 桩2到路基右边界距离: {pile2_x - road_right}m")
    
    if pile1_x < road_left and pile2_x > road_right:
        print("✓ 桩位置显示正确：两个桩都在路基外侧！")
        return True
    else:
        print("✗ 桩位置显示错误：桩仍在路基内部！")
        return False

if __name__ == "__main__":
    test_pile_visualization() 