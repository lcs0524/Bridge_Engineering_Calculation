#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试主程序 - 直接启动桥梁模块
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import traceback

# 添加模块路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.multi_module_window import MultiModuleWindow


def main():
    """测试主程序入口"""
    try:
        print("启动测试程序...")
        
        # 创建主窗口
        root = tk.Tk()
        root.title("桥梁跨越工程综合安全性评估软件 v2.0 - 测试版")
        root.geometry("1400x900")
        
        # 设置窗口属性
        root.resizable(True, True)
        root.minsize(1200, 800)
        
        print("创建MultiModuleWindow...")
        
        # 直接创建主应用程序
        app = MultiModuleWindow(root)
        
        print("启动主循环...")
        
        # 运行主循环
        root.mainloop()
        
    except Exception as e:
        # 错误处理
        error_msg = f"软件启动失败：\n{str(e)}\n\n详细错误信息：\n{traceback.format_exc()}"
        print(error_msg)
        messagebox.showerror("启动错误", error_msg)
        sys.exit(1)


if __name__ == "__main__":
    main() 