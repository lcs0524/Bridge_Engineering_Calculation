#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
桥梁跨越工程安全性评估软件 1.0
作者：金洪松
日期：2025.4.25
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox, ttk
import traceback
import time
import threading
from tkinter import font
from PIL import Image, ImageTk

# 添加模块路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.multi_module_window import MultiModuleWindow


class SplashScreen:
    """高端启动画面类"""
    
    def __init__(self, parent_root, on_complete_callback=None):
        self.parent_root = parent_root
        self.on_complete_callback = on_complete_callback
        self.parent_root.withdraw()  # 先隐藏主窗口
        
        # 创建启动窗口（作为主窗口的子窗口）
        self.splash = tk.Toplevel(self.parent_root)
        self.splash.title("桥梁跨越工程安全性评估软件")
        
        # 设置窗口属性（增加宽度和高度以容纳更大的卡片）
        width, height = 900, 600
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.splash.geometry(f"{width}x{height}+{x}+{y}")
        self.splash.overrideredirect(True)  # 去掉窗口边框
        self.splash.attributes('-topmost', True)  # 置顶显示
        
        # 设置窗口样式 - 现代化渐变背景
        self.splash.configure(bg='#f8fafc')
        
        self.create_widgets()
        self.start_animation()
        
    def create_default_icon(self, parent_frame):
        """创建默认桥梁图标（备用方案）"""
        icon_canvas = tk.Canvas(parent_frame, width=80, height=80, bg='#f1f5f9', highlightthickness=0)
        icon_canvas.pack()
        
        # 绘制简化的桥梁图标
        # 桥墩
        icon_canvas.create_rectangle(15, 45, 25, 70, fill='#64748b', outline='')
        icon_canvas.create_rectangle(55, 45, 65, 70, fill='#64748b', outline='')
        
        # 桥面
        icon_canvas.create_rectangle(10, 40, 70, 48, fill='#475569', outline='')
        
        # 拉索
        for i in range(3):
            x = 20 + i * 15
            icon_canvas.create_line(40, 25, x, 45, fill='#94a3b8', width=2)
            icon_canvas.create_line(40, 25, x + 20, 45, fill='#94a3b8', width=2)
        
        # 主塔
        icon_canvas.create_rectangle(38, 15, 42, 45, fill='#374151', outline='')
        
    def create_widgets(self):
        """创建界面元素"""
        # 先创建装饰背景
        self.create_gradient_background()
        
        # 创建主容器阴影（增加宽度和高度）
        shadow_container = tk.Frame(self.splash, bg='#cbd5e1', bd=0)
        shadow_container.place(x=63, y=63, width=780, height=480)
        
        # 创建主容器 - 半透明玻璃效果（增加宽度和高度）
        main_frame = tk.Frame(self.splash, bg='#f8faff', relief='flat', bd=1)
        main_frame.place(x=60, y=60, width=780, height=480)
        
        # 创建内容区域 - 使用渐变融合的背景
        content_frame = tk.Frame(main_frame, bg='#f0f4ff')
        content_frame.pack(fill='both', expand=True, padx=1, pady=1)
        
        # 顶部区域 - Logo和标题
        header_frame = tk.Frame(content_frame, bg='#f0f4ff')
        header_frame.pack(fill='x', pady=(25, 20))
        
        # 软件图标区域 - 添加圆形背景
        icon_container = tk.Frame(header_frame, bg='#f0f4ff')
        icon_container.pack()
        
        # 创建圆形图标背景
        icon_bg_canvas = tk.Canvas(icon_container, width=100, height=100, bg='#f0f4ff', highlightthickness=0)
        icon_bg_canvas.pack()
        
        # 绘制圆形背景和阴影效果
        icon_bg_canvas.create_oval(10, 12, 90, 92, fill='#e2e8f0', outline='', width=0)  # 阴影
        icon_bg_canvas.create_oval(8, 10, 88, 90, fill='#ffffff', outline='#e2e8f0', width=1)  # 主背景
        
        # 图标框架
        icon_frame = tk.Frame(icon_container, bg='#ffffff')
        icon_frame.place(x=18, y=20, width=64, height=60)
        
        # 加载并显示桥梁图标
        try:
            # 加载桥梁图标图片
            icon_path = os.path.join(os.path.dirname(__file__), 'images', '高架桥桩.png')
            if os.path.exists(icon_path):
                # 打开并调整图片大小
                pil_image = Image.open(icon_path)
                pil_image = pil_image.resize((60, 56), Image.Resampling.LANCZOS)
                self.bridge_icon = ImageTk.PhotoImage(pil_image)
                
                # 显示图标
                icon_label = tk.Label(
                    icon_frame,
                    image=self.bridge_icon,
                    bg='#ffffff',
                    bd=0
                )
                icon_label.pack(expand=True)
            else:
                # 如果图片不存在，创建默认图标
                self.create_default_icon(icon_frame)
        except Exception as e:
            print(f"加载图标失败: {e}")
            # 创建默认图标
            self.create_default_icon(icon_frame)
        
        # 主标题
        title_label = tk.Label(
            header_frame, 
            text="桥梁跨越工程安全性评估软件",
            font=("SimHei", 20, "bold"),
            fg='#1e293b',  # 更深的颜色
            bg='#f0f4ff'
        )
        title_label.pack(pady=(15, 5))
        
        # 副标题
        subtitle_label = tk.Label(
            header_frame,
            text="Bridge Span Engineering Safety Assessment Software",
            font=("Arial", 10),
            fg='#64748b',
            bg='#f0f4ff'
        )
        subtitle_label.pack()
        
        # 版本信息
        version_label = tk.Label(
            header_frame,
            text="Version 1.0  |  专业版",
            font=("SimHei", 9),
            fg='#3b82f6',
            bg='#f0f4ff'
        )
        version_label.pack(pady=(6, 0))
        
        # 中间区域 - 特性展示（增加空间）
        features_frame = tk.Frame(content_frame, bg='#f0f4ff')
        features_frame.pack(fill='x', pady=(5, 10))
        
        # 特性卡片容器
        cards_container = tk.Frame(features_frame, bg='#f0f4ff')
        cards_container.pack()
        
        features_data = [
            ("基于经典力学理论的精确计算", "#3b82f6", "#dbeafe"),
            ("FLAC3D数值模拟标定修正", "#10b981", "#d1fae5"), 
            ("标准计算点叠加效应全面分析", "#f59e0b", "#fef3c7"),
            ("图形化结果智能展示", "#8b5cf6", "#e9d5ff")
        ]
        
        # 创建现代化卡片布局
        for i, (title, color, bg_color) in enumerate(features_data):
            row = i // 2
            col = i % 2
            
            # 卡片容器（大幅增加尺寸）
            card_container = tk.Frame(cards_container, bg='#f0f4ff')
            card_container.grid(row=row, column=col, padx=10, pady=8, sticky='nsew')
            
            # 配置网格权重，使卡片能够平均分布
            cards_container.grid_columnconfigure(0, weight=1)
            cards_container.grid_columnconfigure(1, weight=1)
            cards_container.grid_rowconfigure(0, weight=1)
            cards_container.grid_rowconfigure(1, weight=1)
            
            # 卡片阴影层（进一步增加宽度）
            shadow_frame = tk.Frame(card_container, bg='#e2e8f0', bd=0, width=260, height=120)
            shadow_frame.pack_propagate(False)
            shadow_frame.pack(padx=(0, 2), pady=(0, 2))
            
            # 主卡片层（进一步增加宽度）
            card_frame = tk.Frame(shadow_frame, bg=bg_color, bd=0)
            card_frame.place(x=0, y=0, width=258, height=118)
            
            # 卡片顶部色彩条
            color_bar = tk.Frame(card_frame, bg=color, height=3, bd=0)
            color_bar.pack(fill='x')
            
            # 卡片内容区域（调整内边距）
            content_area = tk.Frame(card_frame, bg=bg_color)
            content_area.pack(fill='both', expand=True, padx=25, pady=15)
            
            # 特性标题（增加wraplength避免不必要换行）
            title_label = tk.Label(
                content_area,
                text=title,
                font=("SimHei", 10, "bold"),
                fg='#1e293b',
                bg=bg_color,
                anchor='center',
                justify='center',
                wraplength=200  # 增加wraplength到200避免过早换行
            )
            title_label.pack(fill='both', expand=True)
            
            # 添加小图标装饰（右上角位置调整）
            icon_canvas = tk.Canvas(card_frame, width=16, height=16, bg=bg_color, highlightthickness=0)
            icon_canvas.place(x=230, y=8)
            
            # 根据不同功能绘制不同的小图标
            if i == 0:  # 理论计算
                icon_canvas.create_oval(3, 3, 13, 13, fill=color, outline='')
                icon_canvas.create_text(8, 8, text="∑", fill='white', font=("Arial", 6, "bold"))
            elif i == 1:  # 数值模拟
                icon_canvas.create_rectangle(2, 4, 14, 12, fill=color, outline='')
                icon_canvas.create_line(4, 6, 12, 6, fill='white', width=1)
                icon_canvas.create_line(4, 10, 12, 10, fill='white', width=1)
            elif i == 2:  # 叠加分析
                for j in range(3):
                    icon_canvas.create_rectangle(3+j*1.5, 4+j, 9+j*1.5, 8+j, fill=color, outline='')
            else:  # 图形展示
                icon_canvas.create_polygon([3, 12, 8, 4, 13, 12], fill=color, outline='')
        
        # 底部区域 - 进度条和状态
        footer_frame = tk.Frame(content_frame, bg='#f0f4ff')
        footer_frame.pack(fill='x', side='bottom', pady=(15, 20))
        
        # 状态显示区域 - 现代化设计
        status_outer = tk.Frame(footer_frame, bg='#e6edff', bd=0)
        status_outer.pack(fill='x', padx=40, pady=(0, 12))
        
        status_container = tk.Frame(status_outer, bg='#f8faff', bd=0)
        status_container.pack(fill='x', padx=1, pady=1)
        
        # 状态标签
        self.status_label = tk.Label(
            status_container,
            text="正在初始化系统组件...",
            font=("SimHei", 10),
            fg='#475569',
            bg='#f8faff'
        )
        self.status_label.pack(pady=8)
        
        # 进度条容器 - 现代化设计
        progress_outer = tk.Frame(footer_frame, bg='#d1d9ff', height=12, bd=0)
        progress_outer.pack(fill='x', padx=40)
        progress_outer.pack_propagate(False)
        
        # 现代化进度条
        self.progress_canvas = tk.Canvas(
            progress_outer, 
            height=10, 
            bg='#d1d9ff', 
            highlightthickness=0
        )
        self.progress_canvas.pack(fill='x', padx=1, pady=1)
        
        # 作者信息
        author_label = tk.Label(
            footer_frame,
            text="© 2025 金洪松  |  技术支持",
            font=("SimHei", 8),
            fg='#6b7daa',
            bg='#f0f4ff'
        )
        author_label.pack(pady=(12, 0))
        
        self.progress = 0
        
    def create_gradient_background(self):
        """创建桥梁跨越主题的炫酷背景效果"""
        # 创建背景画布（增加宽度和高度）
        bg_canvas = tk.Canvas(
            self.splash, 
            width=900, 
            height=600, 
            highlightthickness=0
        )
        bg_canvas.place(x=0, y=0)
        
        # 创建深蓝到浅蓝的渐变背景（更科技感）
        for i in range(600):
            # 渐变色计算 - 从深蓝到浅蓝
            progress = i / 600
            
            # 从深蓝色 #1e3a8a 渐变到浅蓝色 #e0f2fe
            r = int(30 + (224 - 30) * progress * 0.8)
            g = int(58 + (242 - 58) * progress * 0.9)  
            b = int(138 + (254 - 138) * progress * 0.6)
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            bg_canvas.create_line(0, i, 900, i, fill=color, width=1)
        
        # 绘制炫酷的桥梁轮廓（左侧）
        # 主塔1
        bg_canvas.create_line(100, 150, 100, 450, fill='#64748b', width=8)
        bg_canvas.create_line(95, 150, 105, 150, fill='#475569', width=6)
        
        # 主塔2  
        bg_canvas.create_line(300, 120, 300, 450, fill='#64748b', width=8)
        bg_canvas.create_line(295, 120, 305, 120, fill='#475569', width=6)
        
        # 桥面
        bg_canvas.create_line(50, 350, 350, 320, fill='#475569', width=6)
        
        # 拉索系统（左侧桥塔）
        for i in range(5):
            x_start = 100
            y_start = 160 + i * 30
            x_end = 80 + i * 20
            y_end = 350
            bg_canvas.create_line(x_start, y_start, x_end, y_end, fill='#94a3b8', width=2)
            
            x_end = 120 + i * 20
            bg_canvas.create_line(x_start, y_start, x_end, y_end, fill='#94a3b8', width=2)
        
        # 拉索系统（右侧桥塔）
        for i in range(6):
            x_start = 300
            y_start = 140 + i * 25
            x_end = 270 + i * 15
            y_end = 325
            bg_canvas.create_line(x_start, y_start, x_end, y_end, fill='#94a3b8', width=2)
            
            x_end = 330 + i * 15
            bg_canvas.create_line(x_start, y_start, x_end, y_end, fill='#94a3b8', width=2)
        
        # 右侧科技线条装饰
        for i in range(8):
            x = 650 + i * 30
            y1 = 100 + i * 15
            y2 = y1 + 80
            opacity = max(0.3, 1 - (i * 0.1))
            
            # 计算半透明颜色
            r, g, b = 147, 197, 253  # #93c5fd
            alpha = int(255 * opacity)
            color_alpha = f"#{r:02x}{g:02x}{b:02x}"
            
            bg_canvas.create_line(x, y1, x, y2, fill=color_alpha, width=3)
            bg_canvas.create_oval(x-3, y1-3, x+3, y1+3, fill=color_alpha, outline='')
        
        # 添加科技网格效果（右下角）
        for i in range(0, 200, 25):
            for j in range(0, 150, 25):
                x = 700 + i
                y = 400 + j
                if (i + j) % 50 == 0:
                    # 网格节点
                    bg_canvas.create_oval(x-2, y-2, x+2, y+2, fill='#60a5fa', outline='')
                    # 连接线
                    if i < 175:
                        bg_canvas.create_line(x, y, x+25, y, fill='#93c5fd', width=1)
                    if j < 125:
                        bg_canvas.create_line(x, y, x, y+25, fill='#93c5fd', width=1)
        
        # 添加粒子效果（动态感）
        import random
        for _ in range(20):
            x = random.randint(400, 850)
            y = random.randint(50, 250)
            size = random.randint(1, 3)
            
            bg_canvas.create_oval(
                x, y, x+size, y+size, 
                fill='#dbeafe', outline='', 
                width=0
            )
        
        # 左上角光效装饰
        for i in range(6):
            radius = 40 + i * 15
            opacity = (6 - i) / 6.0
            
            # 计算光效颜色
            r, g, b = 59, 130, 246  # #3b82f6
            r = int(224 + (r - 224) * opacity * 0.3)
            g = int(242 + (g - 242) * opacity * 0.3)
            b = int(254 + (b - 254) * opacity * 0.3)
            glow_color = f"#{r:02x}{g:02x}{b:02x}"
            
            bg_canvas.create_oval(
                -radius, -radius, radius, radius,
                fill='', outline=glow_color, width=2
            )
        
        # 底部装饰线条
        for i in range(5):
            y = 550 + i * 8
            opacity = (5 - i) / 5.0
            
            r, g, b = 148, 163, 184
            r = int(30 + (r - 30) * opacity)
            g = int(58 + (g - 58) * opacity)
            b = int(138 + (b - 138) * opacity)
            line_color = f"#{r:02x}{g:02x}{b:02x}"
            
            bg_canvas.create_line(0, y, 900, y, fill=line_color, width=1)
        
    def update_progress(self, value, status):
        """更新进度条和状态"""
        self.progress = value
        self.status_label.config(text=status)
        
        # 更新进度条
        self.progress_canvas.delete("progress")
        canvas_width = self.progress_canvas.winfo_width()
        if canvas_width > 1:
            progress_width = (canvas_width * self.progress) / 100
            
            # 绘制进度条背景
            self.progress_canvas.create_rectangle(
                0, 0, canvas_width, 10, 
                fill='#d1d9ff', outline='', tags="progress"
            )
            
            # 绘制现代化进度条
            if progress_width > 0:
                # 创建圆角进度条效果
                self.progress_canvas.create_rectangle(
                    3, 3, progress_width-3, 7, 
                    fill='#3b82f6', outline='', tags="progress"
                )
                
                # 添加渐变高光效果
                if progress_width > 6:
                    # 顶部高光
                    self.progress_canvas.create_rectangle(
                        3, 3, progress_width-3, 4.5, 
                        fill='#60a5fa', outline='', tags="progress"
                    )
                    
                    # 进度条动态光点效果
                    if progress_width > 20:
                        light_pos = max(10, progress_width - 15)
                        self.progress_canvas.create_oval(
                            light_pos, 2, light_pos + 6, 8,
                            fill='#93c5fd', outline='', tags="progress"
                        )
        
        self.splash.update()
        
    def start_animation(self):
        """启动加载动画"""
        def loading_animation():
            steps = [
                (15, "正在加载系统核心模块..."),
                (35, "正在初始化计算引擎..."),
                (55, "正在加载界面组件..."),
                (75, "正在配置系统参数..."),
                (90, "正在准备启动界面..."),
                (100, "系统启动完成!")
            ]
            
            for progress, status in steps:
                self.update_progress(progress, status)
                time.sleep(0.9)  # 模拟加载时间
                
            time.sleep(0.8)
            self.finish_loading()
            
        # 在新线程中运行动画
        animation_thread = threading.Thread(target=loading_animation)
        animation_thread.daemon = True
        animation_thread.start()
        
    def finish_loading(self):
        """完成加载，启动主程序"""
        # 先调用回调函数初始化主程序
        if self.on_complete_callback:
            self.on_complete_callback()
        
        # 关闭启动界面
        self.splash.destroy()
        
        # 显示主窗口
        self.parent_root.deiconify()


def main():
    """主程序入口"""
    try:
        # 创建主窗口
        root = tk.Tk()
        root.title("桥梁跨越工程综合安全性评估软件 v2.0")
        root.state('zoomed')  # 最大化窗口
        
        # 设置窗口图标和基本属性
        root.resizable(True, True)
        root.minsize(1200, 800)
        
        # 初始化主应用程序的回调函数
        def init_main_app():
            try:
                app = MultiModuleWindow(root)
            except Exception as e:
                root.deiconify()
                print(e)
                raise e
        
        # 显示启动画面，传递回调函数
        splash = SplashScreen(root, init_main_app)
        
        # 运行主循环（只调用一次）
        root.mainloop()
        
    except Exception as e:
        # 错误处理
        error_msg = f"软件启动失败：\n{str(e)}\n\n详细错误信息：\n{traceback.format_exc()}"
        messagebox.showerror("启动错误", error_msg)
        sys.exit(1)


if __name__ == "__main__":
    main() 