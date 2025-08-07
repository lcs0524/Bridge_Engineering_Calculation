# -*- coding: utf-8 -*-
"""
多模块主窗口 - 支持桥梁沉降、路基顶管、电线塔基础三大模块
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
from calculation.pipeline_calculator import PipelineCalculator
from calculation.tower_calculator import TowerCalculator
from visualization.plotter import ResultPlotter
from utils.validator import InputValidator
from utils.exporter import ResultExporter


class MultiModuleWindow:
    """多模块主窗口类"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("桥梁跨越工程综合安全性评估软件 v2.0")
        self.root.geometry("1400x900")
        
        # 初始化计算器
        self.settlement_calculator = SettlementCalculator()
        self.pipeline_calculator = PipelineCalculator()
        self.tower_calculator = TowerCalculator()
        self.plotter = ResultPlotter()
        self.validator = InputValidator()
        self.exporter = ResultExporter()
        
        # 当前模块
        self.current_module = "bridge"
        
        # 计算结果存储
        self.calculation_results = {
            'bridge': None,
            'pipeline': None,
            'tower': None
        }
        
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
        
        self.figure = None
        self.axes = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 创建主菜单
        self.create_menu()
        
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, pady=5)
        
        # 创建模块选择标签页
        self.create_module_tabs(main_frame)
        
        # 创建状态栏
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
        calc_menu.add_command(label="桥梁沉降分析", command=lambda: self.switch_module("bridge"))
        calc_menu.add_command(label="路基顶管计算", command=lambda: self.switch_module("pipeline"))
        calc_menu.add_command(label="电线塔基础稳定性", command=lambda: self.switch_module("tower"))
        
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
    
    def create_module_tabs(self, parent):
        """创建模块选择标签页"""
        # 创建Notebook用于模块切换
        self.module_notebook = ttk.Notebook(parent)
        self.module_notebook.pack(fill="both", expand=True)
        
        # 创建各模块界面
        self.create_bridge_tab()
        self.create_pipeline_tab()
        self.create_tower_tab()
        
        # 绑定标签页切换事件
        self.module_notebook.bind("<<NotebookTabChanged>>", self.on_module_changed)
    
    def create_bridge_tab(self):
        """创建桥梁沉降分析标签页"""
        bridge_frame = ttk.Frame(self.module_notebook)
        self.module_notebook.add(bridge_frame, text="桥梁沉降分析")
        
        # 创建左右分割面板
        paned = ttk.PanedWindow(bridge_frame, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True)
        
        # 左侧输入区域
        input_frame = self.create_bridge_input_area(paned)
        paned.add(input_frame, weight=1)
        
        # 右侧结果显示区域
        result_frame = self.create_result_area(paned)
        paned.add(result_frame, weight=3)
    
    def create_pipeline_tab(self):
        """创建路基顶管计算标签页"""
        pipeline_frame = ttk.Frame(self.module_notebook)
        self.module_notebook.add(pipeline_frame, text="路基顶管计算")
        
        # 创建左右分割面板
        paned = ttk.PanedWindow(pipeline_frame, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True)
        
        # 左侧输入区域
        input_frame = self.create_pipeline_input_area(paned)
        paned.add(input_frame, weight=1)
        
        # 右侧结果显示区域
        result_frame = self.create_pipeline_result_area(paned)
        paned.add(result_frame, weight=3)
    
    def create_tower_tab(self):
        """创建电线塔基础稳定性标签页"""
        tower_frame = ttk.Frame(self.module_notebook)
        self.module_notebook.add(tower_frame, text="电线塔基础稳定性")
        
        # 创建左右分割面板
        paned = ttk.PanedWindow(tower_frame, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True)
        
        # 左侧输入区域
        input_frame = self.create_tower_input_area(paned)
        paned.add(input_frame, weight=1)
        
        # 右侧结果显示区域
        result_frame = self.create_tower_result_area(paned)
        paned.add(result_frame, weight=3)
    
    def create_bridge_input_area(self, parent):
        """创建桥梁沉降分析输入区域"""
        input_frame = ttk.LabelFrame(parent, text="桥梁沉降分析 - 输入参数", padding="10")
        
        # 项目信息
        project_frame = ttk.LabelFrame(input_frame, text="项目信息", padding="5")
        project_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(project_frame, text="项目名称:").grid(row=0, column=0, sticky="w")
        self.bridge_project_name = tk.StringVar(value="高架桥桩基沉降分析项目")
        ttk.Entry(project_frame, textvariable=self.bridge_project_name, width=30).grid(row=0, column=1, padx=5)
        
        # 桩参数
        pile_frame = ttk.LabelFrame(input_frame, text="桩基参数", padding="5")
        pile_frame.pack(fill="x", pady=(0, 10))
        
        # 桩1参数
        ttk.Label(pile_frame, text="桩1 - 直径(m):").grid(row=0, column=0, sticky="w")
        self.pile1_diameter = tk.StringVar(value="1.0")
        ttk.Entry(pile_frame, textvariable=self.pile1_diameter, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(pile_frame, text="桩长(m):").grid(row=0, column=2, sticky="w", padx=(20, 5))
        self.pile1_length = tk.StringVar(value="20.0")
        ttk.Entry(pile_frame, textvariable=self.pile1_length, width=10).grid(row=0, column=3, padx=5)
        
        ttk.Label(pile_frame, text="荷载(kN):").grid(row=0, column=4, sticky="w", padx=(20, 5))
        self.pile1_load = tk.StringVar(value="1000.0")
        ttk.Entry(pile_frame, textvariable=self.pile1_load, width=10).grid(row=0, column=5, padx=5)
        
        # 桩2参数
        ttk.Label(pile_frame, text="桩2 - 直径(m):").grid(row=1, column=0, sticky="w", pady=5)
        self.pile2_diameter = tk.StringVar(value="1.0")
        ttk.Entry(pile_frame, textvariable=self.pile2_diameter, width=10).grid(row=1, column=1, padx=5)
        
        ttk.Label(pile_frame, text="桩长(m):").grid(row=1, column=2, sticky="w", padx=(20, 5))
        self.pile2_length = tk.StringVar(value="20.0")
        ttk.Entry(pile_frame, textvariable=self.pile2_length, width=10).grid(row=1, column=3, padx=5)
        
        ttk.Label(pile_frame, text="荷载(kN):").grid(row=1, column=4, sticky="w", padx=(20, 5))
        self.pile2_load = tk.StringVar(value="1000.0")
        ttk.Entry(pile_frame, textvariable=self.pile2_load, width=10).grid(row=1, column=5, padx=5)
        
        # 公路参数
        road_frame = ttk.LabelFrame(input_frame, text="被跨越公路参数", padding="5")
        road_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(road_frame, text="路基宽度(m):").grid(row=0, column=0, sticky="w")
        self.road_width = tk.StringVar(value="12.0")
        ttk.Entry(road_frame, textvariable=self.road_width, width=15).grid(row=0, column=1, padx=5)
        
        ttk.Label(road_frame, text="与桩1距离(m):").grid(row=1, column=0, sticky="w", pady=5)
        self.road_pile1_distance = tk.StringVar(value="5.0")
        ttk.Entry(road_frame, textvariable=self.road_pile1_distance, width=15).grid(row=1, column=1, padx=5)
        
        ttk.Label(road_frame, text="与桩2距离(m):").grid(row=1, column=2, sticky="w", padx=(20, 5))
        self.road_pile2_distance = tk.StringVar(value="5.0")
        ttk.Entry(road_frame, textvariable=self.road_pile2_distance, width=15).grid(row=1, column=3, padx=5)
        
        # 土层参数 (简化版本)
        soil_frame = ttk.LabelFrame(input_frame, text="土层参数", padding="5")
        soil_frame.pack(fill="x", pady=(0, 10))
        
        self.bridge_soil_layers = []
        soil_data = [("0-5", "粘土", "10.0", "0.35"), ("5-10", "砂土", "15.0", "0.30")]
        
        for i, (depth, name, modulus, poisson) in enumerate(soil_data):
            row_frame = ttk.Frame(soil_frame)
            row_frame.pack(fill="x", pady=2)
            
            ttk.Label(row_frame, text=f"{depth}m:").pack(side="left", padx=5)
            ttk.Label(row_frame, text=name).pack(side="left", padx=5)
            ttk.Label(row_frame, text=f"Es={modulus}MPa").pack(side="left", padx=5)
            ttk.Label(row_frame, text=f"ν={poisson}").pack(side="left", padx=5)
        
        # 计算按钮
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(button_frame, text="计算沉降", 
                  command=lambda: self.run_bridge_calculation()).pack(side="left", padx=5)
        
        return input_frame
    
    def create_pipeline_input_area(self, parent):
        """创建路基顶管计算输入区域"""
        input_frame = ttk.LabelFrame(parent, text="路基顶管计算 - 输入参数", padding="10")
        
        # 项目信息
        project_frame = ttk.LabelFrame(input_frame, text="项目信息", padding="5")
        project_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(project_frame, text="项目名称:").grid(row=0, column=0, sticky="w")
        self.pipeline_project_name = tk.StringVar(value="路基顶管施工项目")
        ttk.Entry(project_frame, textvariable=self.pipeline_project_name, width=30).grid(row=0, column=1, padx=5)
        
        # 管道参数
        pipe_frame = ttk.LabelFrame(input_frame, text="管道参数", padding="5")
        pipe_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(pipe_frame, text="管道外径(m):").grid(row=0, column=0, sticky="w")
        self.pipe_diameter = tk.StringVar(value="1.0")
        ttk.Entry(pipe_frame, textvariable=self.pipe_diameter, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(pipe_frame, text="管壁厚度(m):").grid(row=0, column=2, sticky="w", padx=(20, 5))
        self.pipe_thickness = tk.StringVar(value="0.1")
        ttk.Entry(pipe_frame, textvariable=self.pipe_thickness, width=10).grid(row=0, column=3, padx=5)
        
        ttk.Label(pipe_frame, text="顶进长度(m):").grid(row=1, column=0, sticky="w", pady=5)
        self.pipe_length = tk.StringVar(value="100.0")
        ttk.Entry(pipe_frame, textvariable=self.pipe_length, width=10).grid(row=1, column=1, padx=5)
        
        ttk.Label(pipe_frame, text="覆土深度(m):").grid(row=1, column=2, sticky="w", padx=(20, 5))
        self.cover_depth = tk.StringVar(value="2.0")
        ttk.Entry(pipe_frame, textvariable=self.cover_depth, width=10).grid(row=1, column=3, padx=5)
        
        # 材料选择
        material_frame = ttk.LabelFrame(input_frame, text="材料参数", padding="5")
        material_frame.pack(fill="x", pady=(0, 10))
        
        self.pipe_material = tk.StringVar(value="混凝土")
        ttk.Label(material_frame, text="管道材料:").grid(row=0, column=0, sticky="w")
        ttk.Combobox(material_frame, textvariable=self.pipe_material, 
                    values=["混凝土", "高密度聚乙烯"], state="readonly", width=15).grid(row=0, column=1, padx=5)
        
        # 土质参数
        soil_frame = ttk.LabelFrame(input_frame, text="土质参数", padding="5")
        soil_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(soil_frame, text="土质类型:").grid(row=0, column=0, sticky="w")
        self.pipeline_soil_type = tk.StringVar(value="黏土")
        ttk.Combobox(soil_frame, textvariable=self.pipeline_soil_type,
                    values=["黏土", "砂土", "粉土"], state="readonly", width=15).grid(row=0, column=1, padx=5)
        
        ttk.Label(soil_frame, text="土体重度(kN/m³):").grid(row=1, column=0, sticky="w", pady=5)
        self.soil_unit_weight = tk.StringVar(value="18.0")
        ttk.Entry(soil_frame, textvariable=self.soil_unit_weight, width=10).grid(row=1, column=1, padx=5)
        
        # 计算按钮
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(button_frame, text="计算顶推力", 
                  command=lambda: self.run_pipeline_calculation()).pack(side="left", padx=5)
        
        return input_frame
    
    def create_tower_input_area(self, parent):
        """创建电线塔基础稳定性输入区域"""
        input_frame = ttk.LabelFrame(parent, text="电线塔基础稳定性 - 输入参数", padding="10")
        
        # 项目信息
        project_frame = ttk.LabelFrame(input_frame, text="项目信息", padding="5")
        project_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(project_frame, text="项目名称:").grid(row=0, column=0, sticky="w")
        self.tower_project_name = tk.StringVar(value="电线塔基础稳定性项目")
        ttk.Entry(project_frame, textvariable=self.tower_project_name, width=30).grid(row=0, column=1, padx=5)
        
        # 基础参数
        base_frame = ttk.LabelFrame(input_frame, text="基础参数", padding="5")
        base_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(base_frame, text="基础宽度(m):").grid(row=0, column=0, sticky="w")
        self.base_width = tk.StringVar(value="2.0")
        ttk.Entry(base_frame, textvariable=self.base_width, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(base_frame, text="基础长度(m):").grid(row=0, column=2, sticky="w", padx=(20, 5))
        self.base_length = tk.StringVar(value="3.0")
        ttk.Entry(base_frame, textvariable=self.base_length, width=10).grid(row=0, column=3, padx=5)
        
        ttk.Label(base_frame, text="基础埋深(m):").grid(row=1, column=0, sticky="w", pady=5)
        self.embedment_depth = tk.StringVar(value="1.5")
        ttk.Entry(base_frame, textvariable=self.embedment_depth, width=10).grid(row=1, column=1, padx=5)
        
        ttk.Label(base_frame, text="基础重力(kN):").grid(row=1, column=2, sticky="w", padx=(20, 5))
        self.base_weight = tk.StringVar(value="200.0")
        ttk.Entry(base_frame, textvariable=self.base_weight, width=10).grid(row=1, column=3, padx=5)
        
        # 荷载参数
        load_frame = ttk.LabelFrame(input_frame, text="荷载参数", padding="5")
        load_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(load_frame, text="铁塔压力(kN):").grid(row=0, column=0, sticky="w")
        self.tower_load = tk.StringVar(value="500.0")
        ttk.Entry(load_frame, textvariable=self.tower_load, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(load_frame, text="水平力(kN):").grid(row=0, column=2, sticky="w", padx=(20, 5))
        self.horizontal_force = tk.StringVar(value="50.0")
        ttk.Entry(load_frame, textvariable=self.horizontal_force, width=10).grid(row=0, column=3, padx=5)
        
        ttk.Label(load_frame, text="力作用高度(m):").grid(row=1, column=0, sticky="w", pady=5)
        self.force_height = tk.StringVar(value="15.0")
        ttk.Entry(load_frame, textvariable=self.force_height, width=10).grid(row=1, column=1, padx=5)
        
        # 土质参数
        soil_frame = ttk.LabelFrame(input_frame, text="土质参数", padding="5")
        soil_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(soil_frame, text="土质类型:").grid(row=0, column=0, sticky="w")
        self.tower_soil_type = tk.StringVar(value="黏土")
        ttk.Combobox(soil_frame, textvariable=self.tower_soil_type,
                    values=["黏土", "砂土", "粉土", "岩石"], state="readonly", width=15).grid(row=0, column=1, padx=5)
        
        # 计算按钮
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(button_frame, text="计算稳定性", 
                  command=lambda: self.run_tower_calculation()).pack(side="left", padx=5)
        
        return input_frame
    
    def create_result_area(self, parent):
        """创建桥梁沉降结果显示区域"""
        result_frame = ttk.LabelFrame(parent, text="桥梁沉降分析结果", padding="10")
        
        # 创建Notebook用于分页显示
        self.bridge_notebook = ttk.Notebook(result_frame)
        self.bridge_notebook.pack(fill="both", expand=True)
        
        # 数值结果页
        self.bridge_table_frame = ttk.Frame(self.bridge_notebook)
        self.bridge_notebook.add(self.bridge_table_frame, text="数值结果")
        
        # 创建结果表格
        columns = ("计算点", "X坐标", "Y坐标", "总沉降值(mm)", "安全评估")
        self.bridge_result_tree = ttk.Treeview(self.bridge_table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.bridge_result_tree.heading(col, text=col)
            self.bridge_result_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(self.bridge_table_frame, orient="vertical", 
                                command=self.bridge_result_tree.yview)
        self.bridge_result_tree.configure(yscrollcommand=scrollbar.set)
        
        self.bridge_result_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 图形结果页
        self.bridge_plot_frame = ttk.Frame(self.bridge_notebook)
        self.bridge_notebook.add(self.bridge_plot_frame, text="图形分析")
        
        # 添加完整的图表功能
        self.create_bridge_plot_area()
        
        return result_frame
    
    def create_bridge_plot_area(self):
        """创建桥梁模块的完整图表功能"""
        print("DEBUG: create_bridge_plot_area 被调用")
        
        # 图形控制面板
        plot_control_frame = ttk.Frame(self.bridge_plot_frame)
        plot_control_frame.pack(fill="x", padx=5, pady=5)
        
        # 第一行控制
        control_row1 = ttk.Frame(plot_control_frame)
        control_row1.pack(fill="x", pady=(0, 5))
        
        ttk.Label(control_row1, text="图表类型:").pack(side="left", padx=(0, 5))
        
        self.bridge_plot_type_var = tk.StringVar(value="工程示意简图")
        plot_type_combo = ttk.Combobox(
            control_row1, textvariable=self.bridge_plot_type_var,
            values=["工程示意简图", "沉降分析图", "等高线图", "雷达图", "瀑布图"],
            state="readonly", width=15
        )
        plot_type_combo.pack(side="left", padx=(0, 10))
        plot_type_combo.bind("<<ComboboxSelected>>", self.on_bridge_plot_type_changed)
        
        ttk.Button(control_row1, text="重新绘制", command=self.plot_bridge_results).pack(side="left", padx=(0, 5))
        ttk.Button(control_row1, text="保存图片", command=self.save_bridge_plot).pack(side="left", padx=(0, 5))
        ttk.Button(control_row1, text="保存所有图表", command=self.save_all_bridge_plots).pack(side="left")
        
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
        self.bridge_plot_display_frame = ttk.Frame(self.bridge_plot_frame)
        self.bridge_plot_display_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        
        # 添加初始提示
        tip_label = ttk.Label(self.bridge_plot_display_frame, 
                             text="请先点击【计算沉降】按钮进行计算，然后选择图表类型查看分析结果。",
                             font=("", 10))
        tip_label.pack(expand=True)
        
        print("DEBUG: 图形控制面板创建完成")
    
    def on_bridge_plot_type_changed(self, event=None):
        """桥梁图表类型改变时的处理"""
        if self.calculation_results['bridge']:
            self.plot_bridge_results()
    
    def plot_bridge_results(self):
        """绘制桥梁结果图形"""
        if not self.calculation_results['bridge']:
            messagebox.showwarning("提示", "请先进行桥梁沉降计算")
            return
        
        try:
            # 清除之前的图形
            for widget in self.bridge_plot_display_frame.winfo_children():
                widget.destroy()
            
            # 获取当前输入参数
            current_params = self.get_bridge_input_parameters()
            updated_results = self.calculation_results['bridge'].copy()
            updated_results['input_parameters'] = current_params
            
            # 根据选择的图表类型创建图形
            plot_type = self.bridge_plot_type_var.get()
            self.figure = self.create_bridge_plot_by_type(plot_type, updated_results)
            
            # 获取主要的axes对象
            self.axes = self.figure.get_axes()[0] if self.figure.get_axes() else None
            
            # 保存原始视图状态
            if self.axes:
                self.view_state['original_xlim'] = self.axes.get_xlim()
                self.view_state['original_ylim'] = self.axes.get_ylim()
                self.view_state['current_xlim'] = self.axes.get_xlim()
                self.view_state['current_ylim'] = self.axes.get_ylim()
            
            # 创建画布
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
            self.canvas = FigureCanvasTkAgg(self.figure, self.bridge_plot_display_frame)
            self.canvas.draw()
            
            # 获取画布widget
            canvas_widget = self.canvas.get_tk_widget()
            canvas_widget.pack(fill="both", expand=True)
            
            # 创建工具栏
            toolbar_frame = ttk.Frame(self.bridge_plot_display_frame)
            toolbar_frame.pack(fill="x", side="bottom")
            self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
            self.toolbar.update()
            
            # 绑定交互事件
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
    
    def create_bridge_plot_by_type(self, plot_type, updated_results):
        """根据类型创建桥梁图形"""
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
            points_3d = [(p['x'], p['y'], p['z']) for p in self.calculation_results['bridge']['points']]
            settlements = [p['settlement_mm'] for p in self.calculation_results['bridge']['points']]
            
            # 获取安全阈值
            safety_assessment = self.calculation_results['bridge'].get('safety_assessment', {})
            max_settlement_threshold = safety_assessment.get('bridge_limit', 150)
            
            # 计算单桩沉降值（用于显示）
            pile1_settlement = max([p.get('pile1_settlement', 0) * 1000 for p in self.calculation_results['bridge']['points']])
            pile2_settlement = max([p.get('pile2_settlement', 0) * 1000 for p in self.calculation_results['bridge']['points']])
            
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
            context_menu.add_command(label="💾 保存图片", command=self.save_bridge_plot)
            context_menu.add_command(label="🔄 重新绘制", command=self.plot_bridge_results)
            
            # 显示菜单
            context_menu.tk_popup(event.x_root, event.y_root)
            
        except Exception as e:
            print(f"右键菜单失败: {e}")
        finally:
            try:
                context_menu.grab_release()
            except:
                pass
    
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
    
    def save_bridge_plot(self):
        """保存桥梁图表"""
        if not self.calculation_results['bridge']:
            messagebox.showwarning("提示", "请先进行桥梁沉降计算")
            return
        
        plot_type = self.bridge_plot_type_var.get()
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG图片", "*.png"), ("PDF文件", "*.pdf"), ("所有文件", "*.*")],
            initialname=f"桥梁_{plot_type.replace('图', '')}_分析图"
        )
        
        if filename:
            try:
                if self.figure:
                    self.figure.savefig(filename, dpi=300, bbox_inches='tight')
                    messagebox.showinfo("保存成功", f"图表已保存到：\n{filename}")
                else:
                    messagebox.showerror("保存失败", "没有找到可保存的图表")
            except Exception as e:
                messagebox.showerror("保存失败", f"保存图表时发生错误：\n{str(e)}")
    
    def save_all_bridge_plots(self):
        """保存所有桥梁图表"""
        if not self.calculation_results['bridge']:
            messagebox.showwarning("提示", "请先进行桥梁沉降计算")
            return
        
        output_dir = filedialog.askdirectory(title="选择保存目录")
        if output_dir:
            try:
                saved_files = self.plotter.save_all_plots(self.calculation_results['bridge'], output_dir)
                messagebox.showinfo("保存成功", 
                                  f"已保存 {len(saved_files)} 个图表到：\n{output_dir}")
            except Exception as e:
                messagebox.showerror("保存失败", f"保存图表时发生错误：\n{str(e)}")
    
    def get_bridge_input_parameters(self):
        """获取桥梁模块输入参数"""
        # 这里需要实现获取桥梁输入参数的逻辑
        # 暂时返回默认参数
        return {
            'pile1': {
                'diameter': float(self.pile1_diameter.get() or 1.0),
                'length': float(self.pile1_length.get() or 20.0),
                'load': float(self.pile1_load.get() or 1000.0)
            },
            'pile2': {
                'diameter': float(self.pile2_diameter.get() or 1.0),
                'length': float(self.pile2_length.get() or 20.0),
                'load': float(self.pile2_load.get() or 1000.0)
            },
            'road_params': {
                'width': float(self.road_width.get() or 12.0),
                'pile1_distance': float(self.road_pile1_distance.get() or 5.0),
                'pile2_distance': float(self.road_pile2_distance.get() or 5.0)
            }
        }
    
    def create_pipeline_result_area(self, parent):
        """创建路基顶管结果显示区域"""
        result_frame = ttk.LabelFrame(parent, text="路基顶管计算结果", padding="10")
        
        # 创建Notebook用于分页显示
        self.pipeline_notebook = ttk.Notebook(result_frame)
        self.pipeline_notebook.pack(fill="both", expand=True)
        
        # 顶推力计算结果
        self.pipeline_push_frame = ttk.Frame(self.pipeline_notebook)
        self.pipeline_notebook.add(self.pipeline_push_frame, text="顶推力计算")
        
        # 创建结果显示文本框
        self.pipeline_result_text = tk.Text(self.pipeline_push_frame, wrap=tk.WORD, height=20)
        scrollbar = ttk.Scrollbar(self.pipeline_push_frame, orient="vertical", 
                                command=self.pipeline_result_text.yview)
        self.pipeline_result_text.configure(yscrollcommand=scrollbar.set)
        
        self.pipeline_result_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 管道沉降结果
        self.pipeline_settlement_frame = ttk.Frame(self.pipeline_notebook)
        self.pipeline_notebook.add(self.pipeline_settlement_frame, text="管道沉降验算")
        
        self.pipeline_settlement_text = tk.Text(self.pipeline_settlement_frame, wrap=tk.WORD, height=20)
        scrollbar2 = ttk.Scrollbar(self.pipeline_settlement_frame, orient="vertical", 
                                 command=self.pipeline_settlement_text.yview)
        self.pipeline_settlement_text.configure(yscrollcommand=scrollbar2.set)
        
        self.pipeline_settlement_text.pack(side="left", fill="both", expand=True)
        scrollbar2.pack(side="right", fill="y")
        
        return result_frame
    
    def create_tower_result_area(self, parent):
        """创建电线塔基础稳定性结果显示区域"""
        result_frame = ttk.LabelFrame(parent, text="电线塔基础稳定性结果", padding="10")
        
        # 创建Notebook用于分页显示
        self.tower_notebook = ttk.Notebook(result_frame)
        self.tower_notebook.pack(fill="both", expand=True)
        
        # 地基承载力结果
        self.tower_bearing_frame = ttk.Frame(self.tower_notebook)
        self.tower_notebook.add(self.tower_bearing_frame, text="地基承载力")
        
        self.tower_result_text = tk.Text(self.tower_bearing_frame, wrap=tk.WORD, height=20)
        scrollbar = ttk.Scrollbar(self.tower_bearing_frame, orient="vertical", 
                                command=self.tower_result_text.yview)
        self.tower_result_text.configure(yscrollcommand=scrollbar.set)
        
        self.tower_result_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 稳定性验算结果
        self.tower_stability_frame = ttk.Frame(self.tower_notebook)
        self.tower_notebook.add(self.tower_stability_frame, text="稳定性验算")
        
        self.tower_stability_text = tk.Text(self.tower_stability_frame, wrap=tk.WORD, height=20)
        scrollbar2 = ttk.Scrollbar(self.tower_stability_frame, orient="vertical", 
                                 command=self.tower_stability_text.yview)
        self.tower_stability_text.configure(yscrollcommand=scrollbar2.set)
        
        self.tower_stability_text.pack(side="left", fill="both", expand=True)
        scrollbar2.pack(side="right", fill="y")
        
        return result_frame
    
    def create_status_bar(self):
        """创建状态栏"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side="bottom", fill="x", pady=5)
        
        self.status_label = ttk.Label(status_frame, text="准备就绪")
        self.status_label.pack(side="left", padx=10)
        
        self.spec_label = ttk.Label(status_frame, text="当前模块: 桥梁沉降分析")
        self.spec_label.pack(side="right", padx=10)
    
    def on_module_changed(self, event):
        """模块切换事件处理"""
        tab_id = self.module_notebook.select()
        tab_text = self.module_notebook.tab(tab_id, "text")
        
        module_map = {
            "桥梁沉降分析": "bridge",
            "路基顶管计算": "pipeline",
            "电线塔基础稳定性": "tower"
        }
        
        if tab_text in module_map:
            self.current_module = module_map[tab_text]
            self.spec_label.config(text=f"当前模块: {tab_text}")
            self.update_status(f"已切换到{tab_text}模块")
    
    def switch_module(self, module_name):
        """切换到指定模块"""
        module_tabs = {
            "bridge": 0,
            "pipeline": 1,
            "tower": 2
        }
        
        if module_name in module_tabs:
            self.module_notebook.select(module_tabs[module_name])
    
    def run_bridge_calculation(self):
        """运行桥梁沉降计算"""
        try:
            self.update_status("正在进行桥梁沉降计算...")
            
            # 验证输入参数
            if not self.validate_bridge_inputs():
                return
            
            # 获取输入参数
            params = self.get_bridge_input_parameters()
            
            # 添加默认土层数据（简化版本）
            params['soil_layers'] = [
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
            
            # 添加项目信息
            params['project_name'] = self.bridge_project_name.get()
            params['project_type'] = '高架桥'
            params['road_level'] = '一级公路'
            params['lane_count'] = 4
            
            # 执行计算
            self.calculation_results['bridge'] = self.settlement_calculator.calculate_settlement(params)
            
            # 显示结果
            self.display_bridge_results()
            
            # 自动绘制第一个图表
            self.plot_bridge_results()
            
            self.update_status("桥梁沉降计算完成")
            messagebox.showinfo("计算完成", "桥梁沉降计算已完成，请查看结果。")
            
        except Exception as e:
            self.update_status("桥梁计算失败")
            messagebox.showerror("计算错误", f"桥梁计算过程中发生错误：\n{str(e)}")
            import traceback
            traceback.print_exc()
    
    def validate_bridge_inputs(self):
        """验证桥梁输入参数"""
        try:
            # 验证项目信息
            if not self.bridge_project_name.get().strip():
                messagebox.showerror("输入错误", "请输入项目名称")
                return False
            
            # 验证桩1参数
            pile1_diameter = float(self.pile1_diameter.get())
            pile1_length = float(self.pile1_length.get())
            pile1_load = float(self.pile1_load.get())
            
            if pile1_diameter <= 0 or pile1_length <= 0 or pile1_load <= 0:
                messagebox.showerror("输入错误", "桩1的桩径、桩长和荷载必须大于0")
                return False
            
            # 验证桩2参数
            pile2_diameter = float(self.pile2_diameter.get())
            pile2_length = float(self.pile2_length.get())
            pile2_load = float(self.pile2_load.get())
            
            if pile2_diameter <= 0 or pile2_length <= 0 or pile2_load <= 0:
                messagebox.showerror("输入错误", "桩2的桩径、桩长和荷载必须大于0")
                return False
            
            # 验证被跨越公路参数
            road_width = float(self.road_width.get())
            road_pile1_dist = float(self.road_pile1_distance.get())
            road_pile2_dist = float(self.road_pile2_distance.get())
            
            if road_width <= 0 or road_pile1_dist < 0 or road_pile2_dist < 0:
                messagebox.showerror("输入错误", "路基宽度必须大于0，距离不能为负数")
                return False
            
            return True
        
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数值")
            return False
    
    def display_bridge_results(self):
        """显示桥梁计算结果"""
        if not self.calculation_results['bridge']:
            return
        
        # 清除现有结果
        for item in self.bridge_result_tree.get_children():
            self.bridge_result_tree.delete(item)
        
        # 显示计算点结果
        results = self.calculation_results['bridge']
        points = results.get('points', [])
        
        for i, point in enumerate(points):
            x = point.get('x', 0)
            y = point.get('y', 0) 
            settlement = point.get('settlement_mm', 0)
            
            # 安全评估
            safety_limit = results.get('safety_assessment', {}).get('bridge_limit', 150)
            if settlement <= safety_limit:
                safety = "安全"
            else:
                safety = "超限"
            
            self.bridge_result_tree.insert("", "end", values=(
                f"点{i+1}", f"{x:.1f}", f"{y:.1f}", f"{settlement:.2f}", safety
            ))
    
    def run_pipeline_calculation(self):
        """运行路基顶管计算"""
        try:
            self.update_status("正在进行路基顶管计算...")
            
            # 获取输入参数
            params = {
                'pipe_diameter': float(self.pipe_diameter.get()),
                'wall_thickness': float(self.pipe_thickness.get()),
                'pipe_length': float(self.pipe_length.get()),
                'cover_depth': float(self.cover_depth.get()),
                'material': self.pipe_material.get(),
                'soil_type': self.pipeline_soil_type.get(),
                'soil_unit_weight': float(self.soil_unit_weight.get())
            }
            
            # 验证参数
            is_valid, errors = self.pipeline_calculator.validate_parameters(params)
            if not is_valid:
                messagebox.showerror("参数错误", "\n".join(errors))
                return
            
            # 执行计算
            self.calculation_results['pipeline'] = self.pipeline_calculator.calculate_pipeline_stability(params)
            
            # 显示结果
            self.display_pipeline_results()
            
            self.update_status("路基顶管计算完成")
            messagebox.showinfo("计算完成", "路基顶管计算已完成")
            
        except Exception as e:
            self.update_status("顶管计算失败")
            messagebox.showerror("计算错误", f"顶管计算过程中发生错误：\n{str(e)}")
    
    def run_tower_calculation(self):
        """运行电线塔基础稳定性计算"""
        try:
            self.update_status("正在进行电线塔基础稳定性计算...")
            
            # 获取输入参数
            params = {
                'tower_load': float(self.tower_load.get()),
                'horizontal_force': float(self.horizontal_force.get()),
                'force_height': float(self.force_height.get()),
                'base_weight': float(self.base_weight.get()),
                'base_width': float(self.base_width.get()),
                'base_length': float(self.base_length.get()),
                'embedment_depth': float(self.embedment_depth.get()),
                'soil_type': self.tower_soil_type.get()
            }
            
            # 验证参数
            is_valid, errors = self.tower_calculator.validate_parameters(params)
            if not is_valid:
                messagebox.showerror("参数错误", "\n".join(errors))
                return
            
            # 执行计算
            self.calculation_results['tower'] = self.tower_calculator.calculate_comprehensive_stability(params)
            
            # 显示结果
            self.display_tower_results()
            
            self.update_status("电线塔基础稳定性计算完成")
            messagebox.showinfo("计算完成", "电线塔基础稳定性计算已完成")
            
        except Exception as e:
            self.update_status("电线塔计算失败")
            messagebox.showerror("计算错误", f"电线塔计算过程中发生错误：\n{str(e)}")
    
    def display_pipeline_results(self):
        """显示路基顶管计算结果"""
        if not self.calculation_results['pipeline']:
            return
            
        results = self.calculation_results['pipeline']
        push_calc = results['push_calculation']
        settlement_calc = results['settlement_calculation']
        
        # 显示顶推力计算结果
        push_text = f"""
=== 路基顶管顶推力计算结果 ===

一、顶推力计算
总顶推力: {push_calc.total_push_force:.2f} kN
管道外壁摩擦阻力: {push_calc.friction_resistance:.2f} kN
工具管正面阻力: {push_calc.front_resistance:.2f} kN
管道接口摩擦阻力: {push_calc.interface_resistance:.2f} kN

二、承载能力验算
管道承压能力: {push_calc.pipe_capacity:.2f} kN
工作井后背墙抗力: {push_calc.work_well_capacity:.2f} kN

三、验算结果
强度验算: {"✓ 满足" if push_calc.strength_check else "✗ 不满足"}
工作井稳定性: {"✓ 满足" if push_calc.work_well_check else "✗ 不满足"}

四、安全系数
设计安全系数: {push_calc.safety_factor:.2f}
"""
        
        self.pipeline_result_text.delete(1.0, tk.END)
        self.pipeline_result_text.insert(tk.END, push_text)
        
        # 显示管道沉降计算结果
        settlement_text = f"""
=== 管道沉降验算结果 ===

一、荷载计算
垂直土压力: {settlement_calc.vertical_soil_pressure:.2f} kPa
车辆活载: {settlement_calc.live_load_pressure:.2f} kPa
总压力: {settlement_calc.total_pressure:.2f} kPa

二、应力变形计算
环向应力: {settlement_calc.hoop_stress:.2f} kPa
管体变形: {settlement_calc.pipe_deformation:.3f} mm

三、验算结果
强度验算: {"✓ 满足" if settlement_calc.stress_check else "✗ 不满足"}
变形验算: {"✓ 满足" if settlement_calc.deformation_check else "✗ 不满足"}

四、允许值对比
允许应力: {settlement_calc.allowable_stress:.2f} kPa
允许变形: {settlement_calc.allowable_deformation:.3f} mm
"""
        
        self.pipeline_settlement_text.delete(1.0, tk.END)
        self.pipeline_settlement_text.insert(tk.END, settlement_text)
    
    def display_tower_results(self):
        """显示电线塔基础稳定性计算结果"""
        if not self.calculation_results['tower']:
            return
            
        results = self.calculation_results['tower']
        normal_calc = results['normal_condition']
        extreme_calc = results['extreme_condition']
        
        # 显示地基承载力结果
        bearing_text = f"""
=== 电线塔基础稳定性计算结果 ===

一、正常使用工况
修正地基承载力: {normal_calc.corrected_bearing_capacity:.2f} kPa
最大基底压力: {normal_calc.max_base_pressure:.2f} kPa
最小基底压力: {normal_calc.min_base_pressure:.2f} kPa
平均基底压力: {normal_calc.average_base_pressure:.2f} kPa

二、极端工况
修正地基承载力: {extreme_calc.corrected_bearing_capacity:.2f} kPa
最大基底压力: {extreme_calc.max_base_pressure:.2f} kPa
最小基底压力: {extreme_calc.min_base_pressure:.2f} kPa

三、抗倾覆稳定性
抗倾覆力矩: {normal_calc.overturning_resistance_moment:.2f} kN·m
倾覆力矩: {normal_calc.overturning_moment:.2f} kN·m
抗倾覆安全系数: {normal_calc.overturning_safety_factor:.2f}
要求安全系数: ≥1.5
验算结果: {"✓ 满足" if normal_calc.overturning_check else "✗ 不满足"}

四、抗滑移稳定性
抗滑移力: {normal_calc.sliding_resistance_force:.2f} kN
滑移力: {normal_calc.sliding_force:.2f} kN
抗滑移安全系数: {normal_calc.sliding_safety_factor:.2f}
要求安全系数: ≥1.3
验算结果: {"✓ 满足" if normal_calc.sliding_check else "✗ 不满足"}
"""
        
        self.tower_result_text.delete(1.0, tk.END)
        self.tower_result_text.insert(tk.END, bearing_text)
        
        # 显示稳定性验算结果
        stability_text = f"""
=== 综合稳定性评估 ===

一、整体安全性评估
正常使用工况: {"✓ 安全" if (normal_calc.bearing_check and 
                                      normal_calc.overturning_check and 
                                      normal_calc.sliding_check) else "✗ 不安全"}
极端工况: {"✓ 安全" if (extreme_calc.bearing_check and 
                                extreme_calc.overturning_check and 
                                extreme_calc.sliding_check) else "✗ 不安全"}

二、验算结果汇总
地基承载力: {"✓ 满足" if normal_calc.bearing_check else "✗ 不满足"}
抗倾覆稳定性: {"✓ 满足" if normal_calc.overturning_check else "✗ 不满足"}
抗滑移稳定性: {"✓ 满足" if normal_calc.sliding_check else "✗ 不满足"}

三、工程建议
"""
        
        for i, rec in enumerate(results['safety_assessment']['recommendations'], 1):
            stability_text += f"{i}. {rec}\n"
        
        self.tower_stability_text.delete(1.0, tk.END)
        self.tower_stability_text.insert(tk.END, stability_text)
    
    def new_project(self):
        """新建项目"""
        # 清空所有输入和结果
        self.calculation_results = {'bridge': None, 'pipeline': None, 'tower': None}
        
        # 重置桥梁参数
        self.bridge_project_name.set("高架桥桩基沉降分析项目")
        self.pile1_diameter.set("1.0")
        self.pile1_length.set("20.0")
        self.pile1_load.set("1000.0")
        self.pile2_diameter.set("1.0")
        self.pile2_length.set("20.0")
        self.pile2_load.set("1000.0")
        self.road_width.set("12.0")
        self.road_pile1_distance.set("5.0")
        self.road_pile2_distance.set("5.0")
        
        # 重置顶管参数
        self.pipeline_project_name.set("路基顶管施工项目")
        self.pipe_diameter.set("1.0")
        self.pipe_thickness.set("0.1")
        self.pipe_length.set("100.0")
        self.cover_depth.set("2.0")
        
        # 重置电线塔参数
        self.tower_project_name.set("电线塔基础稳定性项目")
        self.tower_load.set("500.0")
        self.horizontal_force.set("50.0")
        self.force_height.set("15.0")
        self.base_weight.set("200.0")
        self.base_width.set("2.0")
        self.base_length.set("3.0")
        self.embedment_depth.set("1.5")
        
        # 清空结果显示
        self.clear_all_results()
        
        self.update_status("新建项目完成")
    
    def clear_all_results(self):
        """清空所有结果显示"""
        # 清空桥梁结果
        for item in self.bridge_result_tree.get_children():
            self.bridge_result_tree.delete(item)
        
        # 清空顶管结果
        self.pipeline_result_text.delete(1.0, tk.END)
        self.pipeline_settlement_text.delete(1.0, tk.END)
        
        # 清空电线塔结果
        self.tower_result_text.delete(1.0, tk.END)
        self.tower_stability_text.delete(1.0, tk.END)
    
    def open_project(self):
        """打开项目文件"""
        messagebox.showinfo("功能提示", "项目文件导入功能正在开发中...")
    
    def save_project(self):
        """保存项目文件"""
        messagebox.showinfo("功能提示", "项目文件保存功能正在开发中...")
    
    def show_results(self):
        """显示详细结果"""
        current_tab = self.module_notebook.select()
        tab_text = self.module_notebook.tab(current_tab, "text")
        messagebox.showinfo("结果查询", f"{tab_text}结果已显示在右侧区域")
    
    def export_report(self):
        """导出计算报告"""
        if not any(self.calculation_results.values()):
            messagebox.showwarning("提示", "请先进行计算")
            return
            
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")]
            )
            
            if filename:
                # 根据当前模块导出相应结果
                if self.current_module == "bridge" and self.calculation_results['bridge']:
                    self.exporter.export_to_excel(self.calculation_results['bridge'], filename)
                elif self.current_module == "pipeline" and self.calculation_results['pipeline']:
                    # 创建管道计算的综合报告
                    self.export_pipeline_report(filename)
                elif self.current_module == "tower" and self.calculation_results['tower']:
                    # 创建电线塔计算的综合报告
                    self.export_tower_report(filename)
                
                messagebox.showinfo("导出成功", f"报告已导出到：\n{filename}")
                
        except Exception as e:
            messagebox.showerror("导出失败", f"导出报告时发生错误：\n{str(e)}")
    
    def export_pipeline_report(self, filename):
        """导出管道计算报告"""
        # 这里可以实现管道计算的专用导出功能
        pass
    
    def export_tower_report(self, filename):
        """导出电线塔计算报告"""
        # 这里可以实现电线塔计算的专用导出功能
        pass
    
    def plot_results(self):
        """绘制结果图形"""
        if not any(self.calculation_results.values()):
            messagebox.showwarning("提示", "请先进行计算")
            return
        
        # 根据当前模块显示相应图形
        if self.current_module == "bridge":
            messagebox.showinfo("图形", "桥梁沉降图形功能正在开发中...")
        elif self.current_module == "pipeline":
            messagebox.showinfo("图形", "路基顶管图形功能正在开发中...")
        elif self.current_module == "tower":
            messagebox.showinfo("图形", "电线塔基础图形功能正在开发中...")
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
桥梁跨越工程综合安全性评估软件 v2.0 使用说明

1. 模块选择：
   - 桥梁沉降分析：分析桥梁桩基对路基的沉降影响
   - 路基顶管计算：计算顶管施工的顶推力和管道强度
   - 电线塔基础稳定性：验算电线塔基础的三大稳定性

2. 输入参数：
   在每个模块的输入区域填写相应参数

3. 计算操作：
   点击各模块的计算按钮开始计算

4. 结果查看：
   计算结果将显示在右侧结果区域

技术规范：
- 桥梁沉降：JTG D30-2015
- 路基顶管：GB50268-2008
- 电线塔基础：GB50545-2010, DL/T5219-2014
        """
        messagebox.showinfo("使用帮助", help_text)
    
    def show_about(self):
        """显示关于信息"""
        about_text = """
桥梁跨越工程综合安全性评估软件 v2.0

新增功能：
- 路基顶管施工计算
- 电线塔基础稳定性验算
- 多模块集成界面

技术架构：
- Python 3.8+
- tkinter + matplotlib
- 符合最新规范要求

版权所有 © 2025
        """
        messagebox.showinfo("关于软件", about_text)
    
    def update_status(self, message):
        """更新状态栏信息"""
        self.status_label.config(text=message)
        self.root.update_idletasks()