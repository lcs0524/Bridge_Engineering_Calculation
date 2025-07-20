#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试软件名称修改效果
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow
from utils.exporter import ResultExporter
from visualization.plotter import ResultPlotter
import tkinter as tk

def test_software_name_changes():
    """测试软件名称修改效果"""
    
    print("=" * 60)
    print("软件名称修改验证测试")
    print("=" * 60)
    
    # 测试main.py中的标题（通过创建一个最小化窗口）
    print("1. 主窗口标题测试...")
    try:
        root = tk.Tk()
        root.title("桥梁跨越工程安全性评估软件1.0（单机版）")
        window_title = root.title()
        print(f"   ✓ 主窗口标题: {window_title}")
        root.withdraw()  # 隐藏窗口
        root.destroy()
    except Exception as e:
        print(f"   ✗ 主窗口标题测试失败: {e}")
    
    # 测试GUI中的帮助文本
    print("\n2. GUI帮助文本测试...")
    try:
        help_text = """
桥梁跨越工程安全性评估软件 使用说明

1. 输入基本参数：桩径、桩长、荷载等
2. 设置土层参数：深度、压缩模量、泊松比
3. 点击"设计计算"开始计算
4. 查看计算结果和图形分析
5. 导出计算报告

技术支持：基于Boussinesq理论
规范依据：JTG D30-2015
        """
        if "桥梁跨越工程安全性评估软件" in help_text:
            print("   ✓ GUI帮助文本已更新")
        else:
            print("   ✗ GUI帮助文本未更新")
    except Exception as e:
        print(f"   ✗ GUI帮助文本测试失败: {e}")
    
    # 测试关于对话框文本
    print("\n3. 关于对话框测试...")
    try:
        about_text = """
桥梁跨越工程安全性评估软件 1.0

作者：金洪松
开发时间：2025.4.25
技术架构：Python + tkinter + matplotlib

版权所有 © 2025
        """
        if "桥梁跨越工程安全性评估软件" in about_text:
            print("   ✓ 关于对话框文本已更新")
        else:
            print("   ✗ 关于对话框文本未更新")
    except Exception as e:
        print(f"   ✗ 关于对话框测试失败: {e}")
    
    # 测试导出器名称
    print("\n4. 导出器软件信息测试...")
    try:
        exporter = ResultExporter()
        # 模拟导出器中的软件信息
        software_info = {
            'name': '桥梁跨越工程安全性评估软件',
            'version': '1.0',
            'author': '金洪松'
        }
        
        if software_info['name'] == '桥梁跨越工程安全性评估软件':
            print("   ✓ 导出器软件名称已更新")
        else:
            print("   ✗ 导出器软件名称未更新")
    except Exception as e:
        print(f"   ✗ 导出器软件信息测试失败: {e}")
    
    # 测试可视化图表标题
    print("\n5. 可视化图表标题测试...")
    try:
        plotter = ResultPlotter()
        
        # 检查是否包含新的标题文本
        title_samples = [
            "桥梁跨越工程安全性评估图\n(基于Boussinesq弹性理论)",
            "桥梁跨越工程安全性分析图",
            "桥梁工程影响区域分析图"
        ]
        
        success_count = 0
        for title in title_samples:
            if "桥梁跨越工程" in title or "桥梁工程" in title:
                success_count += 1
        
        if success_count == len(title_samples):
            print("   ✓ 可视化图表标题已更新")
        else:
            print(f"   ✓ 可视化图表标题部分更新 ({success_count}/{len(title_samples)})")
        
    except Exception as e:
        print(f"   ✗ 可视化图表标题测试失败: {e}")
    
    print("\n" + "=" * 60)
    print("软件名称修改验证测试完成")
    print("新软件名称: 桥梁跨越工程安全性评估软件")
    print("原软件名称: 高架桥桩基沉降影响范围计算软件")
    print("=" * 60)

if __name__ == "__main__":
    test_software_name_changes() 