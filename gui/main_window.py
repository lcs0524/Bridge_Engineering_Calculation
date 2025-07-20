# -*- coding: utf-8 -*-
"""
主窗口模块 - 实现软件的主要用户界面
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
matplotlib.rcParams['axes.unicode_minus'] = False

from calculation.settlement import SettlementCalculator
from visualization.plotter import ResultPlotter
from utils.validator import InputValidator
from utils.exporter import ResultExporter


class MainWindow:
    """主窗口类"""
    
    def __init__(self, root):
        self.root = root
        self.calculator = SettlementCalculator()
        self.plotter = ResultPlotter()
        self.validator = InputValidator()
        self.exporter = ResultExporter()
        
        # 计算结果存储
        self.calculation_results = None
        self.soil_layers = []
        
        # 视图状态管理
        self.view_state = {
            'original_xlim': None,
            'original_ylim': None,
            'current_xlim': None,
            'current_ylim': None,
            'zoom_factor': 1.0,
            'pan_start': None,
            'is_panning': False
        }
        
        # 初始化缩放相关变量（已在__init__中定义）
        self.figure = None
        self.axes = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 创建主菜单
        self.create_menu()
        
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
        
        # 配置root的网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)  # 主框架区域
        self.root.rowconfigure(1, weight=0)  # 状态栏区域
        
        # 创建 PanedWindow 用于左右布局
        self.paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        self.paned_window.grid(row=0, column=0, sticky="nsew")
        
        # 左侧输入区域
        self.input_main_frame = self.create_input_area_frame(self.paned_window)
        self.paned_window.add(self.input_main_frame, weight=1)
        
        # 中间结果显示区域
        self.result_main_frame = self.create_result_area_frame(self.paned_window)
        self.paned_window.add(self.result_main_frame, weight=3) # 结果区分配更大权重
        
        # 右侧功能按钮区域 和 主框架布局配置
        self.create_button_area_and_configure_main_layout(main_frame)
        
        # 底部状态栏
        self.create_status_bar()
        
    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="新建项目", command=self.new_project)
        file_menu.add_command(label="打开项目", command=self.open_project)
        file_menu.add_command(label="保存项目", command=self.save_project)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        
        # 计算菜单
        calc_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="计算", menu=calc_menu)
        calc_menu.add_command(label="设计计算", command=self.run_calculation)
        calc_menu.add_command(label="参数修正", command=self.show_correction_dialog)
        
        # 结果菜单
        result_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="结果", menu=result_menu)
        result_menu.add_command(label="结果查询", command=self.show_results)
        result_menu.add_command(label="导出报告", command=self.export_report)
        result_menu.add_command(label="绘制图形", command=self.plot_results)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="使用说明", command=self.show_help)
        help_menu.add_command(label="关于软件", command=self.show_about)
        
    def create_input_area_frame(self, parent_for_labelframe):
        """创建并返回输入区域的LabelFrame"""
        input_frame = ttk.LabelFrame(parent_for_labelframe, text="输入参数", padding="10")
        # input_frame 将由 PanedWindow 管理其大小和位置，所以这里不需要 grid 或 pack 到 parent_for_labelframe
        
        # 项目信息输入
        project_frame = ttk.LabelFrame(input_frame, text="项目信息", padding="5")
        project_frame.pack(fill="x", pady=(0, 10))
        
        # 项目名称
        ttk.Label(project_frame, text="项目名称:").grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.project_name_var = tk.StringVar(value="高架桥桩基沉降分析项目")
        ttk.Entry(project_frame, textvariable=self.project_name_var, width=30).grid(row=0, column=1, columnspan=2, padx=(0, 10))
        
        # 项目类型
        ttk.Label(project_frame, text="项目类型:").grid(row=0, column=3, sticky="w", padx=(0, 5))
        self.project_type_var = tk.StringVar(value="桥梁工程")
        project_type_combo = ttk.Combobox(project_frame, textvariable=self.project_type_var,
                                         values=["桥梁工程", "道路工程", "市政工程", "其他"], state="readonly", width=12)
        project_type_combo.grid(row=0, column=4)
        
        # 基本参数输入
        basic_frame = ttk.LabelFrame(input_frame, text="计算条件", padding="5")
        basic_frame.pack(fill="x", pady=(0, 10))
        
        # 公路类型选择（5种）
        ttk.Label(basic_frame, text="公路类型:").grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.road_level_var = tk.StringVar(value="一级公路")
        road_combo = ttk.Combobox(basic_frame, textvariable=self.road_level_var, 
                                 values=["高速公路", "一级公路", "二级公路", "三级公路", "四级公路"], 
                                 state="readonly", width=12)
        road_combo.grid(row=0, column=1, padx=(0, 10))
        
        # 车道数量
        ttk.Label(basic_frame, text="车道数量:").grid(row=0, column=2, sticky="w", padx=(0, 5))
        self.lane_count_var = tk.StringVar(value="4")
        lane_combo = ttk.Combobox(basic_frame, textvariable=self.lane_count_var,
                                 values=["2", "4", "6", "8"], state="readonly", width=8)
        lane_combo.grid(row=0, column=3, padx=(0, 10))
        
        # 桩1参数
        pile1_frame = ttk.LabelFrame(input_frame, text="桩1参数", padding="5")
        pile1_frame.pack(fill="x", pady=(0, 10))

        # 调整列配置，为每个控件分配更合理的空间
        pile1_frame.columnconfigure(1, weight=1)
        pile1_frame.columnconfigure(3, weight=1)
        pile1_frame.columnconfigure(5, weight=1)

        # 桩1直径
        ttk.Label(pile1_frame, text="桩径 (m):").grid(row=0, column=0, sticky="w", padx=(0, 2))
        self.pile1_diameter_var = tk.StringVar(value="1.0")
        ttk.Entry(pile1_frame, textvariable=self.pile1_diameter_var, width=10).grid(row=0, column=1, padx=(0, 5), sticky="ew")
        
        # 桩1长度（土下层部分）
        ttk.Label(pile1_frame, text="桩长-土下层 (m):").grid(row=0, column=2, sticky="w", padx=(5, 2))
        self.pile1_length_var = tk.StringVar(value="20.0")
        ttk.Entry(pile1_frame, textvariable=self.pile1_length_var, width=10).grid(row=0, column=3, padx=(0, 5), sticky="ew")
        
        # 桩1荷载
        ttk.Label(pile1_frame, text="荷载 P1 (kN):").grid(row=0, column=4, sticky="w", padx=(5, 2))
        self.pile1_load_var = tk.StringVar(value="1000.0")
        ttk.Entry(pile1_frame, textvariable=self.pile1_load_var, width=10).grid(row=0, column=5, sticky="ew")
        
        # 桩2参数
        pile2_frame = ttk.LabelFrame(input_frame, text="桩2参数", padding="5")
        pile2_frame.pack(fill="x", pady=(0, 10))

        # 调整列配置
        pile2_frame.columnconfigure(1, weight=1)
        pile2_frame.columnconfigure(3, weight=1)
        pile2_frame.columnconfigure(5, weight=1)

        # 桩2直径
        ttk.Label(pile2_frame, text="桩径 (m):").grid(row=0, column=0, sticky="w", padx=(0, 2))
        self.pile2_diameter_var = tk.StringVar(value="1.0")
        ttk.Entry(pile2_frame, textvariable=self.pile2_diameter_var, width=10).grid(row=0, column=1, padx=(0, 5), sticky="ew")
        
        # 桩2长度（土下层部分）
        ttk.Label(pile2_frame, text="桩长-土下层 (m):").grid(row=0, column=2, sticky="w", padx=(5, 2))
        self.pile2_length_var = tk.StringVar(value="20.0")
        ttk.Entry(pile2_frame, textvariable=self.pile2_length_var, width=10).grid(row=0, column=3, padx=(0, 5), sticky="ew")
        
        # 桩2荷载
        ttk.Label(pile2_frame, text="荷载 P2 (kN):").grid(row=0, column=4, sticky="w", padx=(5, 2))
        self.pile2_load_var = tk.StringVar(value="1000.0")
        ttk.Entry(pile2_frame, textvariable=self.pile2_load_var, width=10).grid(row=0, column=5, sticky="ew")
        
        # 被跨越公路参数
        road_frame = ttk.LabelFrame(input_frame, text="被跨越公路参数", padding="5")
        road_frame.pack(fill="x", pady=(0, 10))
        
        # 第一行：路基宽度
        ttk.Label(road_frame, text="路基宽度 (m):").grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.road_width_var = tk.StringVar(value="12.0")
        ttk.Entry(road_frame, textvariable=self.road_width_var, width=15).grid(row=0, column=1, padx=(0, 10), sticky="w")
        
        # 第二行：路基与桩的距离
        ttk.Label(road_frame, text="路基与桩1距离 (m):").grid(row=1, column=0, sticky="w", padx=(0, 5), pady=(5, 0))
        self.road_pile1_distance_var = tk.StringVar(value="5.0")
        ttk.Entry(road_frame, textvariable=self.road_pile1_distance_var, width=15).grid(row=1, column=1, padx=(0, 10), pady=(5, 0), sticky="w")
        
        ttk.Label(road_frame, text="路基与桩2距离 (m):").grid(row=1, column=2, sticky="w", padx=(20, 5), pady=(5, 0))
        self.road_pile2_distance_var = tk.StringVar(value="5.0")
        ttk.Entry(road_frame, textvariable=self.road_pile2_distance_var, width=15).grid(row=1, column=3, padx=(0, 10), pady=(5, 0), sticky="w")
        
        # 土层参数表格
        soil_frame = ttk.LabelFrame(input_frame, text="土层参数", padding="5")
        soil_frame.pack(fill="both", expand=True)
        
        # 创建表格
        columns = ("深度 (m)", "土层名称", "压缩模量 (MPa)", "泊松比ν")
        self.soil_tree = ttk.Treeview(soil_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.soil_tree.heading(col, text=col)
            self.soil_tree.column(col, width=120)
        
        # 滚动条
        soil_scrollbar = ttk.Scrollbar(soil_frame, orient="vertical", command=self.soil_tree.yview)
        self.soil_tree.configure(yscrollcommand=soil_scrollbar.set)
        
        self.soil_tree.pack(side="left", fill="both", expand=True)
        soil_scrollbar.pack(side="right", fill="y")
        
        # 添加默认土层数据
        self.add_default_soil_layers()
        
        # 土层操作按钮
        soil_button_frame = ttk.Frame(input_frame)
        soil_button_frame.pack(fill="x", pady=(5, 0))
        
        ttk.Button(soil_button_frame, text="添加土层", command=self.add_soil_layer).pack(side="left", padx=(0, 5))
        ttk.Button(soil_button_frame, text="删除土层", command=self.delete_soil_layer).pack(side="left", padx=(0, 5))
        ttk.Button(soil_button_frame, text="编辑土层", command=self.edit_soil_layer).pack(side="left")
        
        return input_frame # 返回创建的LabelFrame

    def create_result_area_frame(self, parent_for_labelframe):
        """创建并返回结果显示区域的LabelFrame"""
        result_frame = ttk.LabelFrame(parent_for_labelframe, text="计算结果", padding="10")
        # result_frame 将由 PanedWindow 管理其大小和位置
        
        # 创建Notebook用于分页显示
        self.notebook = ttk.Notebook(result_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # 数值结果页
        self.result_table_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.result_table_frame, text="数值结果")
        
        # 创建结果表格
        result_columns = ("计算点", "X坐标", "Y坐标", "深度", "桩1沉降", "桩2沉降", "总沉降值 (mm)", "相互作用系数")
        self.result_tree = ttk.Treeview(self.result_table_frame, columns=result_columns, show="headings")
        
        for col in result_columns:
            self.result_tree.heading(col, text=col)
            self.result_tree.column(col, width=80)
        
        result_scrollbar = ttk.Scrollbar(self.result_table_frame, orient="vertical", command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=result_scrollbar.set)
        
        self.result_tree.pack(side="left", fill="both", expand=True)
        result_scrollbar.pack(side="right", fill="y")
        
        # 图形结果页 - 创建支持缩放的图形显示区域
        self.create_zoomable_plot_area()
        
        # 安全评估页
        self.safety_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.safety_frame, text="安全评估")
        
        # 创建安全评估显示区域
        self.create_safety_assessment_area()
        
        return result_frame # 返回创建的LabelFrame

    def create_safety_assessment_area(self):
        """创建安全评估显示区域"""
        # 总体安全状态
        status_frame = ttk.LabelFrame(self.safety_frame, text="总体安全状态", padding="10")
        status_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        self.safety_status_frame = ttk.Frame(status_frame)
        self.safety_status_frame.pack(fill="x")
        
        # 详细评估信息
        detail_frame = ttk.LabelFrame(self.safety_frame, text="详细评估信息", padding="10")
        detail_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # 创建文本区域显示详细信息
        self.safety_text = tk.Text(detail_frame, wrap=tk.WORD, height=15)
        safety_scrollbar = ttk.Scrollbar(detail_frame, orient="vertical", command=self.safety_text.yview)
        self.safety_text.configure(yscrollcommand=safety_scrollbar.set)
        
        self.safety_text.pack(side="left", fill="both", expand=True)
        safety_scrollbar.pack(side="right", fill="y")
    
    def create_zoomable_plot_area(self):
        """创建支持缩放的图形显示区域"""
        self.plot_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.plot_frame, text="图形分析")
        
        # 图形控制面板
        plot_control_frame = ttk.Frame(self.plot_frame)
        plot_control_frame.pack(fill="x", padx=5, pady=5)
        
        # 第一行控制
        control_row1 = ttk.Frame(plot_control_frame)
        control_row1.pack(fill="x", pady=(0, 5))
        
        ttk.Label(control_row1, text="图表类型:").pack(side="left", padx=(0, 5))
        
        self.plot_type_var = tk.StringVar(value="工程示意简图")
        plot_type_combo = ttk.Combobox(
            control_row1, textvariable=self.plot_type_var,
            values=["工程示意简图", "沉降分析图", "等高线图", "雷达图", "瀑布图"],
            state="readonly", width=15
        )
        plot_type_combo.pack(side="left", padx=(0, 10))
        plot_type_combo.bind("<<ComboboxSelected>>", self.on_plot_type_changed)
        
        ttk.Button(control_row1, text="重新绘制", command=self.plot_results).pack(side="left", padx=(0, 5))
        ttk.Button(control_row1, text="保存图片", command=self.save_current_plot).pack(side="left", padx=(0, 5))
        ttk.Button(control_row1, text="保存所有图表", command=self.save_all_plots).pack(side="left")
        
        # 第二行控制 - 缩放和视图控制
        control_row2 = ttk.Frame(plot_control_frame)
        control_row2.pack(fill="x")
        
        ttk.Label(control_row2, text="视图控制:").pack(side="left", padx=(0, 5))
        
        # 缩放控制按钮
        ttk.Button(control_row2, text="放大", command=self.zoom_in).pack(side="left", padx=(0, 2))
        ttk.Button(control_row2, text="缩小", command=self.zoom_out).pack(side="left", padx=(0, 2))
        ttk.Button(control_row2, text="适应窗口", command=self.fit_to_window).pack(side="left", padx=(0, 2))
        ttk.Button(control_row2, text="重置视图", command=self.reset_view).pack(side="left", padx=(0, 10))
        
        # 缩放比例显示
        self.zoom_var = tk.StringVar(value="100%")
        ttk.Label(control_row2, text="缩放:").pack(side="left", padx=(10, 2))
        ttk.Label(control_row2, textvariable=self.zoom_var).pack(side="left")
        
        # 图形显示容器
        self.plot_display_frame = ttk.Frame(self.plot_frame)
        self.plot_display_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        
        # 初始化缩放相关变量（已在__init__中定义）
    
    def on_plot_type_changed(self, event=None):
        """图表类型改变时的处理"""
        if self.calculation_results:
            self.plot_results()
    
    def save_current_plot(self):
        """保存当前图表"""
        if not self.calculation_results:
            messagebox.showwarning("提示", "请先进行计算")
            return
        
        plot_type = self.plot_type_var.get()
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG图片", "*.png"), ("PDF文件", "*.pdf"), ("所有文件", "*.*")],
            initialname=f"{plot_type.replace('图', '')}_分析图"
        )
        
        if filename:
            try:
                # 获取当前显示的图形
                current_fig = self.get_current_figure()
                if current_fig:
                    current_fig.savefig(filename, dpi=300, bbox_inches='tight')
                    messagebox.showinfo("图表已保存到：\n{filename}")
                else:
                    messagebox.showerror("保存失败", "没有找到可保存的图表")
            except Exception as e:
                messagebox.showerror("保存失败", f"保存图表时发生错误：\n{str(e)}")
    
    def save_all_plots(self):
        """保存所有图表"""
        if not self.calculation_results:
            messagebox.showwarning("提示", "请先进行计算")
            return
        
        output_dir = filedialog.askdirectory(title="选择保存目录")
        if output_dir:
            try:
                saved_files = self.plotter.save_all_plots(self.calculation_results, output_dir)
                messagebox.showinfo("保存成功", 
                                  f"已保存 {len(saved_files)} 个图表到：\n{output_dir}")
            except Exception as e:
                messagebox.showerror("保存失败", f"保存图表时发生错误：\n{str(e)}")
    
    def get_current_figure(self):
        """获取当前显示的matplotlib图形"""
        for widget in self.plot_display_frame.winfo_children():
            if hasattr(widget, 'figure'):
                return widget.figure
        return None
    
    def create_button_area_and_configure_main_layout(self, main_frame_parent):
        """创建功能按钮区域并配置main_frame的布局"""
        # 创建自适应按钮区域
        self.create_adaptive_button_area(main_frame_parent)
        
        # 配置main_frame_parent的网格权重
        main_frame_parent.columnconfigure(0, weight=1)  # PanedWindow 区域
        main_frame_parent.rowconfigure(0, weight=1)     # PanedWindow 区域
        main_frame_parent.rowconfigure(1, weight=0)     # Button 区域
        
    def create_adaptive_button_area(self, parent):
        """创建自适应功能按钮区域"""
        button_main_frame = ttk.Frame(parent)
        button_main_frame.grid(row=1, column=0, sticky="ew", pady=(5, 0))
        
        # 配置网格权重
        parent.grid_rowconfigure(1, weight=0)  # 按钮区域不扩展
        
        # 主要功能按钮组
        main_buttons_frame = ttk.LabelFrame(button_main_frame, text="主要功能", padding="5")
        main_buttons_frame.pack(side="left", fill="y", padx=(0, 5))
        
        # 使用网格布局，支持按钮自适应
        ttk.Button(main_buttons_frame, text="设计计算", command=self.run_calculation, width=12).grid(row=0, column=0, padx=2, pady=2)
        ttk.Button(main_buttons_frame, text="结果查询", command=self.show_results, width=12).grid(row=0, column=1, padx=2, pady=2)
        ttk.Button(main_buttons_frame, text="绘制图形", command=self.plot_results, width=12).grid(row=0, column=2, padx=2, pady=2)
        
        # 导出功能按钮组
        export_buttons_frame = ttk.LabelFrame(button_main_frame, text="导出功能", padding="5")
        export_buttons_frame.pack(side="left", fill="y", padx=(0, 5))
        
        ttk.Button(export_buttons_frame, text="导出报告", command=self.export_report, width=12).grid(row=0, column=0, padx=2, pady=2)
        ttk.Button(export_buttons_frame, text="保存图片", command=self.save_current_plot, width=12).grid(row=0, column=1, padx=2, pady=2)
        
        # 工具功能按钮组
        tool_buttons_frame = ttk.LabelFrame(button_main_frame, text="工具", padding="5")
        tool_buttons_frame.pack(side="left", fill="y")
        
        ttk.Button(tool_buttons_frame, text="参数修正", command=self.show_correction_dialog, width=12).grid(row=0, column=0, padx=2, pady=2)
        ttk.Button(tool_buttons_frame, text="工作记录", command=self.show_work_record, width=12).grid(row=0, column=1, padx=2, pady=2)
        
    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 5))
        
        self.status_label = ttk.Label(self.status_bar, text="准备就绪")
        self.status_label.pack(side="left", padx=10, pady=2)
        
        # 规范连接
        spec_label = ttk.Label(self.status_bar, text="规范连接：《公路路基设计规范》JTG D30-2015")
        spec_label.pack(side="right", padx=10, pady=2)
        
    def add_default_soil_layers(self):
        """添加默认土层数据"""
        default_layers = [
            ("0-5", "粘土", "10.0", "0.35"),
            ("5-10", "砂土", "15.0", "0.30"),
            ("10-15", "粘土", "12.0", "0.35"),
            ("15-20", "砂土", "18.0", "0.28"),
        ]
        
        for layer in default_layers:
            self.soil_tree.insert("", "end", values=layer)
            
    def update_status(self, message):
        """更新状态栏信息"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
        
    def run_calculation(self):
        """运行沉降计算"""
        try:
            self.update_status("正在进行计算...")
            
            # 验证输入参数
            if not self.validate_inputs():
                return
                
            # 获取输入参数
            params = self.get_input_parameters()
            
            # 执行计算
            self.calculation_results = self.calculator.calculate_settlement(params)
            
            # 显示结果
            self.display_results()
            
            self.update_status("计算完成")
            messagebox.showinfo("计算完成", "沉降计算已完成，请查看结果。")
            
        except Exception as e:
            self.update_status("计算失败")
            messagebox.showerror("计算错误", f"计算过程中发生错误：\n{str(e)}")
    
    def validate_inputs(self):
        """验证输入参数"""
        try:
            # 验证项目信息
            if not self.project_name_var.get().strip():
                messagebox.showerror("输入错误", "请输入项目名称")
                return False
            
            # 验证桩1参数
            pile1_diameter = float(self.pile1_diameter_var.get())
            pile1_length = float(self.pile1_length_var.get())
            pile1_load = float(self.pile1_load_var.get())
            
            if pile1_diameter <= 0 or pile1_length <= 0 or pile1_load <= 0:
                messagebox.showerror("输入错误", "桩1的桩径、桩长（土下层）和荷载必须大于0")
                return False
            
            # 验证桩2参数
            pile2_diameter = float(self.pile2_diameter_var.get())
            pile2_length = float(self.pile2_length_var.get())
            pile2_load = float(self.pile2_load_var.get())
            
            if pile2_diameter <= 0 or pile2_length <= 0 or pile2_load <= 0:
                messagebox.showerror("输入错误", "桩2的桩径、桩长（土下层）和荷载必须大于0")
                return False
            
            # 验证被跨越公路参数
            road_width = float(self.road_width_var.get())
            road_pile1_dist = float(self.road_pile1_distance_var.get())
            road_pile2_dist = float(self.road_pile2_distance_var.get())
            
            if road_width <= 0 or road_pile1_dist < 0 or road_pile2_dist < 0:
                messagebox.showerror("输入错误", "路基宽度必须大于0，距离不能为负数")
                return False
                
            # 验证土层参数
            if len(self.soil_tree.get_children()) == 0:
                messagebox.showerror("输入错误", "请至少添加一个土层")
                return False
                
            return True
            
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数值")
            return False
    
    def get_input_parameters(self):
        """获取输入参数"""
        params = {
            # 项目信息
            'project_name': self.project_name_var.get(),
            'project_type': self.project_type_var.get(),
            'road_level': self.road_level_var.get(),
            'lane_count': int(self.lane_count_var.get()),
            
            # 桩1参数
            'pile1': {
                'diameter': float(self.pile1_diameter_var.get()),
                'length': float(self.pile1_length_var.get()),
                'load': float(self.pile1_load_var.get())
            },
            
            # 桩2参数
            'pile2': {
                'diameter': float(self.pile2_diameter_var.get()),
                'length': float(self.pile2_length_var.get()),
                'load': float(self.pile2_load_var.get())
            },
            
            # 被跨越公路参数
            'road_params': {
                'width': float(self.road_width_var.get()),
                'pile1_distance': float(self.road_pile1_distance_var.get()),
                'pile2_distance': float(self.road_pile2_distance_var.get())
            },
            
            # 土层参数
            'soil_layers': []
        }
        
        # 获取土层参数
        for item in self.soil_tree.get_children():
            values = self.soil_tree.item(item)['values']
            layer = {
                'depth_range': values[0],
                'name': values[1],
                'compression_modulus': float(values[2]),
                'poisson_ratio': float(values[3])
            }
            params['soil_layers'].append(layer)
            
        return params
    
    def display_results(self):
        """显示计算结果"""
        if not self.calculation_results:
            return
            
        # 清空现有结果
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
            
        # 添加计算结果到表格
        for result in self.calculation_results['points']:
            self.result_tree.insert("", "end", values=(
                result['point_id'],
                f"{result['x']:.1f}",
                f"{result['y']:.1f}",
                f"{result['z']:.1f}",
                f"{result['pile1_settlement']*1000:.3f}",  # 桩1沉降mm
                f"{result['pile2_settlement']*1000:.3f}",  # 桩2沉降mm
                f"{result['settlement_mm']:.3f}",          # 总沉降mm
                f"{result['interaction_factor']:.4f}"      # 相互作用系数
            ))
        
        # 显示安全评估信息
        self.display_safety_assessment()
        
        # 自动切换到图形分析页并绘制默认图表
        self.notebook.select(1)  # 切换到图形分析页
        self.plot_results()
    
    def display_safety_assessment(self):
        """显示安全评估信息"""
        if not self.calculation_results:
            return
        
        safety = self.calculation_results['safety_assessment']
        stats = self.calculation_results['statistics']
        
        # 清空现有显示
        for widget in self.safety_status_frame.winfo_children():
            widget.destroy()
        
        # 显示安全等级状态指示器
        status_label = ttk.Label(self.safety_status_frame, 
                                text=f"安全等级: {safety['safety_level']}", 
                                font=("Arial", 14, "bold"))
        status_label.pack(side="left", padx=(0, 20))
        
        # 根据安全等级设置颜色指示
        level_colors = {'安全': 'green', '警告': 'orange', '危险': 'red'}
        level_color = level_colors.get(safety['safety_level'], 'gray')
        
        status_indicator = tk.Label(self.safety_status_frame, 
                                   text="●", font=("Arial", 20), 
                                   fg=level_color)
        status_indicator.pack(side="left", padx=(0, 20))
        
        # 最大沉降值显示
        max_settlement_label = ttk.Label(self.safety_status_frame,
                                        text=f"最大沉降: {safety['max_settlement_mm']:.3f} mm",
                                        font=("Arial", 12, "bold"))
        max_settlement_label.pack(side="left")
        
        # 详细评估信息文本
        self.safety_text.delete(1.0, tk.END)
        
        safety_report = f"""
=== 桩基沉降影响范围安全评估报告 ===

一、计算结果概况
最大沉降值：{safety['max_settlement_mm']:.3f} mm
最小沉降值：{stats['min_settlement_mm']:.3f} mm
平均沉降值：{stats['avg_settlement_mm']:.3f} mm
标准差：{np.std([p['settlement_mm'] for p in self.calculation_results['points']]):.3f} mm

二、规范限值对比（JTG D30-2015）
一般路段限值：{safety['general_limit']} mm
桥梁工程限值：{safety['bridge_limit']} mm
桥头引道限值：{safety['approach_limit']} mm

三、超限情况分析
超出一般限值：{'是' if safety['exceed_general'] else '否'}
超出桥梁限值：{'是' if safety['exceed_bridge'] else '否'}
超出引道限值：{'是' if safety['exceed_approach'] else '否'}

四、影响范围统计
影响范围面积：{safety['influence_area']:.2f} m²
总计算点数：{len(self.calculation_results['points'])} 个
影响点数量：{safety['influence_points_count']} 个
警告点数量：{safety['warning_points_count']} 个
危险点数量：{safety['danger_points_count']} 个

五、安全性分布
安全点位：{safety['safety_statistics']['safe_points']} 个
影响点位：{safety['safety_statistics']['influence_points']} 个
警告点位：{safety['safety_statistics']['warning_points']} 个
危险点位：{safety['safety_statistics']['danger_points']} 个

六、工程建议
"""
        
        for i, rec in enumerate(safety['recommendations'], 1):
            safety_report += f"{i}. {rec}\n"
        
        if 'technical_recommendations' in safety and safety['technical_recommendations']:
            safety_report += "\n七、技术措施建议\n"
            for i, tech_rec in enumerate(safety['technical_recommendations'], 1):
                safety_report += f"{i}. {tech_rec}\n"
        
        safety_report += f"""
八、符合性分析
满足一般标准：{'是' if safety['compliance_analysis']['meets_general_standard'] else '否'}
满足桥梁标准：{'是' if safety['compliance_analysis']['meets_bridge_standard'] else '否'}
满足引道标准：{'是' if safety['compliance_analysis']['meets_approach_standard'] else '否'}
整体符合性：{'是' if safety['compliance_analysis']['overall_compliance'] else '否'}

九、技术依据
计算理论：Boussinesq弹性理论
修正方法：桩长和桩径参数修正
数值验证：基于FLAC3D数值分析
技术规范：《公路路基设计规范》JTG D30-2015

=== 报告结束 ===
        """
        
        self.safety_text.insert(tk.END, safety_report)
    
    def create_plot_by_type(self, plot_type, updated_results):
        """根据类型创建图形"""
        current_params = updated_results['input_parameters']
        
        if plot_type == "工程示意简图":
            # 提取桩基参数
            pile1_params = current_params.get('pile1', {})
            pile2_params = current_params.get('pile2', {})
            road_params = current_params.get('road_params', {})
            
            # 计算桩位置
            roadbed_width = road_params.get('width', 20)
            pile1_distance_val = road_params.get('pile1_distance', 5)
            pile2_distance_val = road_params.get('pile2_distance', 5)
            
            pile1_x = -(roadbed_width/2 + pile1_distance_val)
            pile2_x = +(roadbed_width/2 + pile2_distance_val)
            
            # 提取计算点坐标和沉降值
            points_3d = [(p['x'], p['y'], p['z']) for p in self.calculation_results['points']]
            settlements = [p['settlement_mm'] for p in self.calculation_results['points']]
            
            # 获取安全阈值
            safety_assessment = self.calculation_results.get('safety_assessment', {})
            max_settlement_threshold = safety_assessment.get('bridge_limit', 150)
            
            # 计算单桩沉降值（用于显示）
            pile1_settlement = max([p.get('pile1_settlement', 0) * 1000 for p in self.calculation_results['points']])
            pile2_settlement = max([p.get('pile2_settlement', 0) * 1000 for p in self.calculation_results['points']])
            
            # 相互作用系数（假设为0.8）
            interaction_coefficient = 0.8
            
            # 桩参数（取较大的桩径和桩长）
            pile_diameter = max(pile1_params.get('diameter', 1.0), pile2_params.get('diameter', 1.0))
            pile_length = max(pile1_params.get('length', 20.0), pile2_params.get('length', 20.0))
            
            return self.plotter.settlement_distribution_plot(
                pile1_x, pile2_x, pile_diameter, pile_length,
                roadbed_width, points_3d, settlements, max_settlement_threshold,
                pile1_settlement, pile2_settlement, interaction_coefficient,
                pile1_distance_val, pile2_distance_val
            )
        elif plot_type == "沉降分析图":
            return self.plotter.create_settlement_plot(updated_results)
        elif plot_type == "等高线图":
            return self.plotter.create_contour_plot(updated_results)
        elif plot_type == "雷达图":
            return self.plotter.create_radar_plot(updated_results)
        elif plot_type == "瀑布图":
            return self.plotter.create_waterfall_plot(updated_results)
        else:
            return self.plotter.create_settlement_distribution_plot(updated_results)
    
    def plot_results_with_zoom(self):
        """绘制支持完整交互功能的结果图形"""
        if not self.calculation_results:
            messagebox.showwarning("提示", "请先进行计算")
            return
        
        try:
            # 清除之前的图形
            for widget in self.plot_display_frame.winfo_children():
                widget.destroy()
            
            # 获取当前输入参数
            current_params = self.get_input_parameters()
            updated_results = self.calculation_results.copy()
            updated_results['input_parameters'] = current_params
            
            # 根据选择的图表类型创建图形
            plot_type = self.plot_type_var.get()
            self.figure = self.create_plot_by_type(plot_type, updated_results)
            
            # 获取主要的axes对象
            self.axes = self.figure.get_axes()[0] if self.figure.get_axes() else None
            
            # 保存原始视图状态
            if self.axes:
                self.view_state['original_xlim'] = self.axes.get_xlim()
                self.view_state['original_ylim'] = self.axes.get_ylim()
                self.view_state['current_xlim'] = self.axes.get_xlim()
                self.view_state['current_ylim'] = self.axes.get_ylim()
            
            # 创建主容器
            main_container = ttk.Frame(self.plot_display_frame)
            main_container.pack(fill="both", expand=True, padx=5, pady=5)
            
            # 创建工具栏容器
            toolbar_frame = ttk.Frame(main_container)
            toolbar_frame.pack(fill="x", pady=(0, 5))
            
            # 创建图形容器
            plot_frame = ttk.Frame(main_container)
            plot_frame.pack(fill="both", expand=True)
            
            # 创建画布
            self.canvas = FigureCanvasTkAgg(self.figure, plot_frame)
            self.canvas.draw()
            
            # 获取画布widget
            canvas_widget = self.canvas.get_tk_widget()
            canvas_widget.pack(fill="both", expand=True)
            
            # 创建增强的工具栏
            from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
            self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
            self.toolbar.update()
            
            # 绑定完整的交互事件
            self.bind_canvas_events(canvas_widget)
            
            # 重置缩放状态
            self.current_zoom = 1.0
            self.view_state['zoom_factor'] = 1.0
            self.zoom_var.set("100%")
            
            self.update_status(f"已绘制{plot_type} - 支持完整交互操作")
            
        except Exception as e:
            self.update_status("绘图失败")
            messagebox.showerror("绘图错误", f"绘制{plot_type}时发生错误：\n{str(e)}")
            import traceback
            traceback.print_exc()
    
    def bind_canvas_events(self, canvas_widget):
        """绑定画布交互事件"""
        # 鼠标事件
        canvas_widget.bind("<Button-1>", self.on_canvas_click)
        canvas_widget.bind("<B1-Motion>", self.on_canvas_drag)
        canvas_widget.bind("<ButtonRelease-1>", self.on_canvas_release)
        canvas_widget.bind("<Button-3>", self.on_right_click)
        canvas_widget.bind("<MouseWheel>", self.on_mouse_wheel)
        canvas_widget.bind("<Double-Button-1>", self.on_double_click)
        
        # 键盘快捷键
        canvas_widget.bind("<Control-plus>", lambda e: self.zoom_in())
        canvas_widget.bind("<Control-equal>", lambda e: self.zoom_in())  # 兼容不同键盘
        canvas_widget.bind("<Control-minus>", lambda e: self.zoom_out())
        canvas_widget.bind("<Control-0>", lambda e: self.reset_view())
        canvas_widget.bind("<Control-r>", lambda e: self.reset_view())
        canvas_widget.bind("<Control-f>", lambda e: self.fit_to_window())
        
        # 设置焦点
        canvas_widget.focus_set()
        canvas_widget.bind("<FocusIn>", lambda e: None)  # 确保能接收键盘事件
    
    def zoom_in(self, factor=1.2):
        """智能放大功能"""
        if not self.axes:
            return
        
        try:
            # 获取当前视图中心
            current_xlim = self.axes.get_xlim()
            current_ylim = self.axes.get_ylim()
            
            center_x = (current_xlim[0] + current_xlim[1]) / 2
            center_y = (current_ylim[0] + current_ylim[1]) / 2
            
            # 计算新的视图范围
            width = (current_xlim[1] - current_xlim[0]) / factor
            height = (current_ylim[1] - current_ylim[0]) / factor
            
            new_xlim = (center_x - width/2, center_x + width/2)
            new_ylim = (center_y - height/2, center_y + height/2)
            
            # 应用新的视图范围
            self.axes.set_xlim(new_xlim)
            self.axes.set_ylim(new_ylim)
            
            # 更新状态
            self.view_state['current_xlim'] = new_xlim
            self.view_state['current_ylim'] = new_ylim
            self.view_state['zoom_factor'] *= factor
            
            # 重绘
            self.canvas.draw()
            
            # 更新缩放显示
            self.zoom_var.set(f"{int(self.view_state['zoom_factor'] * 100)}%")
            
        except Exception as e:
            print(f"放大操作失败: {e}")
    
    def zoom_out(self, factor=1.2):
        """智能缩小功能"""
        self.zoom_in(1/factor)
    
    def fit_to_window(self):
        """智能适应窗口大小"""
        if not self.axes or not self.canvas:
            return
        
        try:
            # 获取画布尺寸
            canvas_widget = self.canvas.get_tk_widget()
            canvas_width = canvas_widget.winfo_width()
            canvas_height = canvas_widget.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:
                # 如果画布尺寸无效，使用默认尺寸
                canvas_width = 800
                canvas_height = 600
            
            # 获取数据范围
            if (self.view_state['original_xlim'] and 
                self.view_state['original_ylim']):
                data_xlim = self.view_state['original_xlim']
                data_ylim = self.view_state['original_ylim']
            else:
                # 重新计算数据范围
                self.axes.relim()
                self.axes.autoscale_view()
                data_xlim = self.axes.get_xlim()
                data_ylim = self.axes.get_ylim()
            
            # 计算数据的宽高比
            data_width = data_xlim[1] - data_xlim[0]
            data_height = data_ylim[1] - data_ylim[0]
            data_aspect = data_width / data_height if data_height != 0 else 1
            
            # 计算画布的宽高比（考虑边距）
            canvas_aspect = canvas_width / canvas_height if canvas_height != 0 else 1
            
            # 根据宽高比调整视图
            if data_aspect > canvas_aspect:
                # 数据更宽，以宽度为准
                center_y = (data_ylim[0] + data_ylim[1]) / 2
                new_height = data_width / canvas_aspect
                new_ylim = (center_y - new_height/2, center_y + new_height/2)
                self.axes.set_xlim(data_xlim)
                self.axes.set_ylim(new_ylim)
            else:
                # 数据更高，以高度为准
                center_x = (data_xlim[0] + data_xlim[1]) / 2
                new_width = data_height * canvas_aspect
                new_xlim = (center_x - new_width/2, center_x + new_width/2)
                self.axes.set_xlim(new_xlim)
                self.axes.set_ylim(data_ylim)
            
            # 更新状态
            self.view_state['current_xlim'] = self.axes.get_xlim()
            self.view_state['current_ylim'] = self.axes.get_ylim()
            self.view_state['zoom_factor'] = 1.0
            
            # 重绘
            self.canvas.draw()
            
            # 更新显示
            self.zoom_var.set("适应窗口")
            
        except Exception as e:
            print(f"适应窗口操作失败: {e}")
            # 降级到简单的自动缩放
            if self.toolbar:
                self.toolbar.home()
    
    def reset_view(self):
        """重置到原始视图"""
        if not self.axes:
            return
        
        try:
            if (self.view_state['original_xlim'] and 
                self.view_state['original_ylim']):
                # 恢复到原始视图
                self.axes.set_xlim(self.view_state['original_xlim'])
                self.axes.set_ylim(self.view_state['original_ylim'])
                
                # 更新状态
                self.view_state['current_xlim'] = self.view_state['original_xlim']
                self.view_state['current_ylim'] = self.view_state['original_ylim']
                self.view_state['zoom_factor'] = 1.0
                
                # 重绘
                self.canvas.draw()
                
                # 更新显示
                self.zoom_var.set("100%")
            else:
                # 降级到工具栏的home功能
                if self.toolbar:
                    self.toolbar.home()
                    self.view_state['zoom_factor'] = 1.0
                    self.zoom_var.set("100%")
                    
        except Exception as e:
            print(f"重置视图操作失败: {e}")
    
    def on_mouse_wheel(self, event):
        """鼠标滚轮缩放"""
        if not self.axes:
            return
        
        # 检查Ctrl键
        if event.state & 0x4:  # Ctrl键按下
            try:
                # 获取鼠标在axes中的位置
                if event.x and event.y:
                    # 转换鼠标坐标到数据坐标
                    canvas_widget = self.canvas.get_tk_widget()
                    
                    # 获取鼠标相对于画布的位置
                    x_canvas = canvas_widget.canvasx(event.x)
                    y_canvas = canvas_widget.canvasy(event.y)
                    
                    # 转换为matplotlib坐标
                    try:
                        inv = self.axes.transData.inverted()
                        x_data, y_data = inv.transform((x_canvas, y_canvas))
                        
                        # 以鼠标位置为中心进行缩放
                        self.zoom_at_point(x_data, y_data, 1.2 if event.delta > 0 else 1/1.2)
                    except:
                        # 如果坐标转换失败，使用中心缩放
                        if event.delta > 0:
                            self.zoom_in()
                        else:
                            self.zoom_out()
                else:
                    # 使用中心缩放
                    if event.delta > 0:
                        self.zoom_in()
                    else:
                        self.zoom_out()
                        
            except Exception as e:
                print(f"滚轮缩放失败: {e}")
            
            return "break"
    
    def zoom_at_point(self, x_center, y_center, factor):
        """在指定点进行缩放"""
        if not self.axes:
            return
        
        try:
            current_xlim = self.axes.get_xlim()
            current_ylim = self.axes.get_ylim()
            
            # 计算新的视图范围
            width = (current_xlim[1] - current_xlim[0]) / factor
            height = (current_ylim[1] - current_ylim[0]) / factor
            
            # 以指定点为中心
            new_xlim = (x_center - width/2, x_center + width/2)
            new_ylim = (y_center - height/2, y_center + height/2)
            
            # 应用新的视图范围
            self.axes.set_xlim(new_xlim)
            self.axes.set_ylim(new_ylim)
            
            # 更新状态
            self.view_state['current_xlim'] = new_xlim
            self.view_state['current_ylim'] = new_ylim
            self.view_state['zoom_factor'] *= factor
            
            # 重绘
            self.canvas.draw()
            
            # 更新显示
            self.zoom_var.set(f"{int(self.view_state['zoom_factor'] * 100)}%")
            
        except Exception as e:
            print(f"定点缩放失败: {e}")
    
    def on_canvas_click(self, event):
        """画布点击事件"""
        if self.canvas:
            canvas_widget = self.canvas.get_tk_widget()
            canvas_widget.focus_set()
            
            # 记录拖拽起始点
            self.view_state['pan_start'] = (event.x, event.y)
            self.view_state['is_panning'] = False
    
    def on_canvas_drag(self, event):
        """画布拖拽事件 - 实现平移功能"""
        if (not self.axes or 
            not self.view_state['pan_start'] or 
            not event.state & 0x100):  # 检查是否按下鼠标左键
            return
        
        try:
            # 标记为正在拖拽
            self.view_state['is_panning'] = True
            
            # 计算拖拽距离
            start_x, start_y = self.view_state['pan_start']
            dx = event.x - start_x
            dy = event.y - start_y
            
            # 转换为数据坐标的偏移
            current_xlim = self.axes.get_xlim()
            current_ylim = self.axes.get_ylim()
            
            # 获取画布尺寸
            canvas_widget = self.canvas.get_tk_widget()
            canvas_width = canvas_widget.winfo_width()
            canvas_height = canvas_widget.winfo_height()
            
            if canvas_width > 0 and canvas_height > 0:
                # 计算数据坐标的偏移量
                data_width = current_xlim[1] - current_xlim[0]
                data_height = current_ylim[1] - current_ylim[0]
                
                dx_data = -dx * data_width / canvas_width
                dy_data = dy * data_height / canvas_height
                
                # 应用平移
                new_xlim = (current_xlim[0] + dx_data, current_xlim[1] + dx_data)
                new_ylim = (current_ylim[0] + dy_data, current_ylim[1] + dy_data)
                
                self.axes.set_xlim(new_xlim)
                self.axes.set_ylim(new_ylim)
                
                # 更新状态
                self.view_state['current_xlim'] = new_xlim
                self.view_state['current_ylim'] = new_ylim
                
                # 重绘
                self.canvas.draw_idle()  # 使用draw_idle提高性能
                
                # 更新起始点
                self.view_state['pan_start'] = (event.x, event.y)
                
        except Exception as e:
            print(f"拖拽平移失败: {e}")
    
    def on_canvas_release(self, event):
        """画布释放事件"""
        self.view_state['is_panning'] = False
        self.view_state['pan_start'] = None
    
    def on_double_click(self, event):
        """双击事件 - 智能缩放到点击区域"""
        if not self.axes:
            return
        
        try:
            # 转换鼠标坐标到数据坐标
            canvas_widget = self.canvas.get_tk_widget()
            x_canvas = canvas_widget.canvasx(event.x)
            y_canvas = canvas_widget.canvasy(event.y)
            
            inv = self.axes.transData.inverted()
            x_data, y_data = inv.transform((x_canvas, y_canvas))
            
            # 以双击点为中心放大
            self.zoom_at_point(x_data, y_data, 2.0)
            
        except Exception as e:
            print(f"双击缩放失败: {e}")
    
    def on_right_click(self, event):
        """增强的右键菜单"""
        try:
            # 创建右键菜单
            context_menu = tk.Menu(self.root, tearoff=0)
            
            # 缩放选项
            context_menu.add_command(label="🔍 放大 (Ctrl++)", command=self.zoom_in)
            context_menu.add_command(label="🔍 缩小 (Ctrl+-)", command=self.zoom_out)
            context_menu.add_separator()
            
            # 视图选项
            context_menu.add_command(label="📐 适应窗口 (Ctrl+F)", command=self.fit_to_window)
            context_menu.add_command(label="🔄 重置视图 (Ctrl+0)", command=self.reset_view)
            context_menu.add_separator()
            
            # 功能选项
            context_menu.add_command(label="💾 保存图片", command=self.save_current_plot)
            context_menu.add_command(label="🔄 重新绘制", command=self.plot_results)
            
            # 显示菜单
            context_menu.tk_popup(event.x_root, event.y_root)
            
        except Exception as e:
            print(f"右键菜单失败: {e}")
        finally:
            try:
                context_menu.grab_release()
            except:
                pass
    
    def on_window_resize(self, event):
        """窗口大小调整事件处理"""
        if event.widget == self.root and self.canvas:
            # 延迟执行适应窗口，避免频繁调整
            self.root.after(100, self._delayed_fit_to_window)
    
    def _delayed_fit_to_window(self):
        """延迟执行的适应窗口功能"""
        try:
            if hasattr(self, '_resize_timer'):
                self.root.after_cancel(self._resize_timer)
            
            # 如果当前是适应窗口模式，重新适应
            if self.zoom_var.get() == "适应窗口":
                self._resize_timer = self.root.after(200, self.fit_to_window)
        except:
            pass
    
    def plot_results(self):
        """绘制结果图形 - 调用支持缩放的版本"""
        self.plot_results_with_zoom()
    
    def new_project(self):
        """新建项目"""
        # 清空所有输入和结果
        self.pile_diameter_var.set("1.0")
        self.pile_length_var.set("20.0")
        self.load_var.set("1000.0")
        self.road_level_var.set("一级公路")
        
        # 清空土层表格
        for item in self.soil_tree.get_children():
            self.soil_tree.delete(item)
        self.add_default_soil_layers()
        
        # 清空结果
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        
        self.calculation_results = None
        self.update_status("新建项目完成")
    
    def open_project(self):
        """打开项目文件"""
        messagebox.showinfo("功能提示", "项目文件导入功能正在开发中...")
    
    def save_project(self):
        """保存项目文件"""
        messagebox.showinfo("功能提示", "项目文件保存功能正在开发中...")
    
    def show_correction_dialog(self):
        """显示参数修正对话框"""
        # 创建参数修正窗口
        correction_window = tk.Toplevel(self.root)
        correction_window.title("参数修正计算")
        correction_window.geometry("500x400")
        correction_window.resizable(False, False)
        
        # 主框架
        main_frame = ttk.Frame(correction_window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 输入参数框架
        input_frame = ttk.LabelFrame(main_frame, text="输入参数", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 桩长输入
        ttk.Label(input_frame, text="桩长 (m):").grid(row=0, column=0, sticky=tk.W, pady=2)
        pile_length_var = tk.StringVar(value="20.0")
        ttk.Entry(input_frame, textvariable=pile_length_var, width=15).grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # 桩径输入
        ttk.Label(input_frame, text="桩径 (m):").grid(row=1, column=0, sticky=tk.W, pady=2)
        pile_diameter_var = tk.StringVar(value="1.0")
        ttk.Entry(input_frame, textvariable=pile_diameter_var, width=15).grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # 结果显示框架
        result_frame = ttk.LabelFrame(main_frame, text="修正系数计算结果", padding="10")
        result_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 结果显示文本框
        result_text = tk.Text(result_frame, height=12, width=50, wrap=tk.WORD)
        result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 滚动条
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=result_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        result_text.configure(yscrollcommand=scrollbar.set)
        
        def calculate_corrections():
            """计算参数修正系数"""
            try:
                pile_length = float(pile_length_var.get())
                pile_diameter = float(pile_diameter_var.get())
                
                # 导入修正计算器
                from calculation.correction import CorrectionCalculator
                calculator = CorrectionCalculator()
                
                # 计算修正系数
                a = calculator.calculate_length_correction(pile_length)
                b = calculator.calculate_diameter_correction(pile_diameter)
                combined = a * b
                
                # 显示结果
                result_text.delete(1.0, tk.END)
                result_content = f"""参数修正系数计算结果
{'='*40}

输入参数：
  桩长：{pile_length:.2f} m
  桩径：{pile_diameter:.2f} m

修正系数计算：
  a = 0.985 - 0.00051 × (桩长)
  a = 0.985 - 0.00051 × {pile_length:.2f}
  a = {a:.6f}

  b = 0.038 × (桩径)² - 0.206 × (桩径) + 1.159
  {'  (适用于桩径 < 2.5m)' if pile_diameter < 2.5 else '  (桩径 ≥ 2.5m，使用默认值 1.0)'}
  {'b = 0.038 × {:.2f}² - 0.206 × {:.2f} + 1.159'.format(pile_diameter, pile_diameter) if pile_diameter < 2.5 else 'b = 1.0 (默认值)'}
  b = {b:.6f}

综合修正系数：
  综合系数 = a × b = {a:.6f} × {b:.6f} = {combined:.6f}

说明：
• 桩长修正系数 a：考虑桩长对沉降的影响
• 桩径修正系数 b：考虑桩径对沉降的影响  
• 综合修正系数：用于最终沉降计算的修正
"""
                result_text.insert(1.0, result_content)
                
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数值")
            except Exception as e:
                messagebox.showerror("错误", f"计算出错：{str(e)}")
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        # 计算按钮
        ttk.Button(button_frame, text="计算修正系数", command=calculate_corrections).grid(row=0, column=0, padx=(0, 10))
        
        # 关闭按钮
        ttk.Button(button_frame, text="关闭", command=correction_window.destroy).grid(row=0, column=1)
        
        # 初始计算
        calculate_corrections()
        
        # 窗口居中
        correction_window.transient(self.root)
        correction_window.grab_set()
    
    def show_results(self):
        """显示详细结果"""
        if not self.calculation_results:
            messagebox.showwarning("提示", "请先进行计算")
            return
        
        # 切换到结果页
        self.notebook.select(0)
    
    def export_report(self):
        """导出计算报告"""
        if not self.calculation_results:
            messagebox.showwarning("提示", "请先进行计算")
            return
            
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")]
            )
            
            if filename:
                self.exporter.export_to_excel(self.calculation_results, filename)
                messagebox.showinfo("导出成功", f"报告已导出到：\n{filename}")
                
        except Exception as e:
            messagebox.showerror("导出失败", f"导出报告时发生错误：\n{str(e)}")
    
    def show_work_record(self):
        """显示工作记录"""
        messagebox.showinfo("功能提示", "工作记录功能正在开发中...")
    
    def add_soil_layer(self):
        """添加土层"""
        # 创建土层添加对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("添加土层")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # 创建输入框架
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # 深度范围输入
        ttk.Label(main_frame, text="深度范围 (m):").grid(row=0, column=0, sticky="w", pady=(0, 10))
        depth_frame = ttk.Frame(main_frame)
        depth_frame.grid(row=0, column=1, sticky="ew", pady=(0, 10))
        
        depth_start_var = tk.StringVar()
        depth_end_var = tk.StringVar()
        
        ttk.Entry(depth_frame, textvariable=depth_start_var, width=8).pack(side="left")
        ttk.Label(depth_frame, text=" - ").pack(side="left", padx=5)
        ttk.Entry(depth_frame, textvariable=depth_end_var, width=8).pack(side="left")
        
        # 土层名称输入
        ttk.Label(main_frame, text="土层名称:").grid(row=1, column=0, sticky="w", pady=(0, 10))
        name_var = tk.StringVar()
        name_combo = ttk.Combobox(main_frame, textvariable=name_var, width=20,
                                 values=["粘土", "砂土", "粉土", "淤泥", "砂砾", "岩石", "其他"])
        name_combo.grid(row=1, column=1, sticky="ew", pady=(0, 10))
        
        # 压缩模量输入
        ttk.Label(main_frame, text="压缩模量 (MPa):").grid(row=2, column=0, sticky="w", pady=(0, 10))
        modulus_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=modulus_var, width=20).grid(row=2, column=1, sticky="ew", pady=(0, 10))
        
        # 泊松比输入
        ttk.Label(main_frame, text="泊松比 ν:").grid(row=3, column=0, sticky="w", pady=(0, 10))
        poisson_var = tk.StringVar()
        poisson_combo = ttk.Combobox(main_frame, textvariable=poisson_var, width=20,
                                    values=["0.20", "0.25", "0.28", "0.30", "0.35", "0.40", "0.45"])
        poisson_combo.grid(row=3, column=1, sticky="ew", pady=(0, 10))
        
        # 配置列权重
        main_frame.columnconfigure(1, weight=1)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(20, 0))
        
        def validate_and_add():
            """验证输入并添加土层"""
            try:
                # 验证输入
                depth_start = float(depth_start_var.get())
                depth_end = float(depth_end_var.get())
                name = name_var.get().strip()
                modulus = float(modulus_var.get())
                poisson = float(poisson_var.get())
                
                # 验证数据有效性
                if depth_start >= depth_end:
                    messagebox.showerror("输入错误", "起始深度必须小于结束深度")
                    return
                
                if depth_start < 0 or depth_end < 0:
                    messagebox.showerror("输入错误", "深度不能为负数")
                    return
                    
                if not name:
                    messagebox.showerror("输入错误", "请输入土层名称")
                    return
                    
                if modulus <= 0:
                    messagebox.showerror("输入错误", "压缩模量必须大于0")
                    return
                    
                if poisson <= 0 or poisson >= 0.5:
                    messagebox.showerror("输入错误", "泊松比必须在0到0.5之间")
                    return
                
                # 检查深度范围是否与现有土层重叠
                for item in self.soil_tree.get_children():
                    values = self.soil_tree.item(item)['values']
                    existing_range = values[0]
                    if '-' in existing_range:
                        existing_start, existing_end = map(float, existing_range.split('-'))
                        if not (depth_end <= existing_start or depth_start >= existing_end):
                            messagebox.showerror("输入错误", f"深度范围与现有土层 '{existing_range}' 重叠")
                            return
                
                # 添加到表格
                depth_range = f"{depth_start}-{depth_end}"
                self.soil_tree.insert("", "end", values=(depth_range, name, f"{modulus:.1f}", f"{poisson:.2f}"))
                
                # 清除旧的计算结果，提示用户重新计算
                self.calculation_results = None
                self.clear_results_display()
                
                # 关闭对话框
                dialog.destroy()
                messagebox.showinfo("成功", "土层添加成功，请重新进行设计计算")
                
            except ValueError:
                messagebox.showerror("输入错误", "请输入有效的数值")
            except Exception as e:
                messagebox.showerror("错误", f"添加土层时发生错误：{str(e)}")
        
        def cancel():
            """取消添加"""
            dialog.destroy()
        
        # 添加按钮
        ttk.Button(button_frame, text="确定", command=validate_and_add).pack(side="left", padx=(0, 10))
        ttk.Button(button_frame, text="取消", command=cancel).pack(side="left")
        
        # 设置默认值
        name_var.set("粘土")
        modulus_var.set("10.0")
        poisson_var.set("0.35")
        
        # 焦点设置到第一个输入框
        depth_frame.winfo_children()[0].focus_set()

    def delete_soil_layer(self):
        """删除土层"""
        selected = self.soil_tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请先选择要删除的土层")
            return
        
        # 确认删除
        if messagebox.askyesno("确认删除", "确定要删除选中的土层吗？"):
            for item in selected:
                self.soil_tree.delete(item)
            
            # 清除旧的计算结果，提示用户重新计算
            self.calculation_results = None
            self.clear_results_display()
            
            messagebox.showinfo("成功", "土层删除成功，请重新进行设计计算")

    def clear_results_display(self):
        """清除结果显示"""
        # 清空结果表格
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        
        # 清空图形显示
        for widget in self.plot_display_frame.winfo_children():
            widget.destroy()
        
        # 清空安全评估显示
        for widget in self.safety_status_frame.winfo_children():
            widget.destroy()
        
        if hasattr(self, 'safety_text'):
            self.safety_text.delete(1.0, tk.END)
        
        self.update_status("参数已更新，请重新进行设计计算")

    def edit_soil_layer(self):
        """编辑土层"""
        selected = self.soil_tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请先选择要编辑的土层")
            return
        
        # 获取选中项的值
        item = selected[0]
        values = self.soil_tree.item(item)['values']
        
        # 创建编辑对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("编辑土层")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # 创建输入框架
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # 解析现有值
        depth_range = values[0]
        if '-' in depth_range:
            depth_start_str, depth_end_str = depth_range.split('-')
        else:
            depth_start_str, depth_end_str = "0", "5"
        
        # 深度范围输入
        ttk.Label(main_frame, text="深度范围 (m):").grid(row=0, column=0, sticky="w", pady=(0, 10))
        depth_frame = ttk.Frame(main_frame)
        depth_frame.grid(row=0, column=1, sticky="ew", pady=(0, 10))
        
        depth_start_var = tk.StringVar(value=depth_start_str)
        depth_end_var = tk.StringVar(value=depth_end_str)
        
        ttk.Entry(depth_frame, textvariable=depth_start_var, width=8).pack(side="left")
        ttk.Label(depth_frame, text=" - ").pack(side="left", padx=5)
        ttk.Entry(depth_frame, textvariable=depth_end_var, width=8).pack(side="left")
        
        # 土层名称输入
        ttk.Label(main_frame, text="土层名称:").grid(row=1, column=0, sticky="w", pady=(0, 10))
        name_var = tk.StringVar(value=values[1])
        name_combo = ttk.Combobox(main_frame, textvariable=name_var, width=20,
                                 values=["粘土", "砂土", "粉土", "淤泥", "砂砾", "岩石", "其他"])
        name_combo.grid(row=1, column=1, sticky="ew", pady=(0, 10))
        
        # 压缩模量输入
        ttk.Label(main_frame, text="压缩模量 (MPa):").grid(row=2, column=0, sticky="w", pady=(0, 10))
        modulus_var = tk.StringVar(value=values[2])
        ttk.Entry(main_frame, textvariable=modulus_var, width=20).grid(row=2, column=1, sticky="ew", pady=(0, 10))
        
        # 泊松比输入
        ttk.Label(main_frame, text="泊松比 ν:").grid(row=3, column=0, sticky="w", pady=(0, 10))
        poisson_var = tk.StringVar(value=values[3])
        poisson_combo = ttk.Combobox(main_frame, textvariable=poisson_var, width=20,
                                    values=["0.20", "0.25", "0.28", "0.30", "0.35", "0.40", "0.45"])
        poisson_combo.grid(row=3, column=1, sticky="ew", pady=(0, 10))
        
        # 配置列权重
        main_frame.columnconfigure(1, weight=1)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(20, 0))
        
        def validate_and_update():
            """验证输入并更新土层"""
            try:
                # 验证输入
                depth_start = float(depth_start_var.get())
                depth_end = float(depth_end_var.get())
                name = name_var.get().strip()
                modulus = float(modulus_var.get())
                poisson = float(poisson_var.get())
                
                # 验证数据有效性
                if depth_start >= depth_end:
                    messagebox.showerror("输入错误", "起始深度必须小于结束深度")
                    return
                
                if depth_start < 0 or depth_end < 0:
                    messagebox.showerror("输入错误", "深度不能为负数")
                    return
                    
                if not name:
                    messagebox.showerror("输入错误", "请输入土层名称")
                    return
                    
                if modulus <= 0:
                    messagebox.showerror("输入错误", "压缩模量必须大于0")
                    return
                    
                if poisson <= 0 or poisson >= 0.5:
                    messagebox.showerror("输入错误", "泊松比必须在0到0.5之间")
                    return
                
                # 检查深度范围是否与其他土层重叠（排除当前编辑的土层）
                for other_item in self.soil_tree.get_children():
                    if other_item != item:  # 排除当前编辑的项
                        other_values = self.soil_tree.item(other_item)['values']
                        existing_range = other_values[0]
                        if '-' in existing_range:
                            existing_start, existing_end = map(float, existing_range.split('-'))
                            if not (depth_end <= existing_start or depth_start >= existing_end):
                                messagebox.showerror("输入错误", f"深度范围与现有土层 '{existing_range}' 重叠")
                                return
                
                # 更新表格项
                depth_range = f"{depth_start}-{depth_end}"
                self.soil_tree.item(item, values=(depth_range, name, f"{modulus:.1f}", f"{poisson:.2f}"))
                
                # 清除旧的计算结果，提示用户重新计算
                self.calculation_results = None
                self.clear_results_display()
                
                # 关闭对话框
                dialog.destroy()
                messagebox.showinfo("成功", "土层编辑成功，请重新进行设计计算")
                
            except ValueError:
                messagebox.showerror("输入错误", "请输入有效的数值")
            except Exception as e:
                messagebox.showerror("错误", f"编辑土层时发生错误：{str(e)}")
        
        def cancel():
            """取消编辑"""
            dialog.destroy()
        
        # 添加按钮
        ttk.Button(button_frame, text="确定", command=validate_and_update).pack(side="left", padx=(0, 10))
        ttk.Button(button_frame, text="取消", command=cancel).pack(side="left")
        
        # 焦点设置到第一个输入框
        depth_frame.winfo_children()[0].focus_set()

    def delete_soil_layer(self):
        """删除土层"""
        selected = self.soil_tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请先选择要删除的土层")
            return
        
        # 确认删除
        if messagebox.askyesno("确认删除", "确定要删除选中的土层吗？"):
            for item in selected:
                self.soil_tree.delete(item)
            
            # 清除旧的计算结果，提示用户重新计算
            self.calculation_results = None
            self.clear_results_display()
            
            messagebox.showinfo("成功", "土层删除成功，请重新进行设计计算")

    def clear_results_display(self):
        """清除结果显示"""
        # 清空结果表格
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        
        # 清空图形显示
        for widget in self.plot_display_frame.winfo_children():
            widget.destroy()
        
        # 清空安全评估显示
        for widget in self.safety_status_frame.winfo_children():
            widget.destroy()
        
        if hasattr(self, 'safety_text'):
            self.safety_text.delete(1.0, tk.END)
        
        self.update_status("参数已更新，请重新进行设计计算")

    def show_help(self):
        """显示帮助信息"""
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
        messagebox.showinfo("使用帮助", help_text)
    
    def show_about(self):
        """显示关于信息"""
        about_text = """
桥梁跨越工程安全性评估软件 1.0

作者：金洪松
开发时间：2025.4.25
技术架构：Python + tkinter + matplotlib

版权所有 © 2025
        """
        messagebox.showinfo("关于软件", about_text)
    
 