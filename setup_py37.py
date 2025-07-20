from cx_Freeze import setup, Executable
import sys
import os

# 构建选项
build_exe_options = {
    "packages": [
        "numpy", "pandas", "matplotlib", "tkinter", 
        "openpyxl", "xlsxwriter", "json", "csv", "datetime",
        "pickle", "_pickle", "copyreg", "types",
        # 添加NumPy相关依赖
        "numpy.core", "numpy.core.multiarray", "numpy.core.overrides",
        "numpy.lib", "numpy.lib.format", "numpy.random",
        # 添加系统模块
        "io", "sys", "os", "collections", "functools", "itertools",
        "warnings", "weakref", "gc", "threading", "queue",
        # 添加文档字符串相关模块
        "inspect", "textwrap", "string"
    ],
    "excludes": ["test", "unittest", "distutils"],
    "include_files": [
        ("images/", "images/"),
        ("resources/", "resources/"),
    ],
    "optimize": 0,  # 改为0，避免过度优化导致的问题
    "build_exe": "build/exe.win-amd64-3.7",
    # 添加zip_include_packages来处理NumPy
    "zip_include_packages": ["*"],
    "zip_exclude_packages": ["numpy", "matplotlib"]
}

# 可执行文件配置
executables = [
    Executable(
        "main.py",
        base="Win32GUI" if sys.platform == "win32" else None,
        target_name="桥梁跨越工程安全性评估软件.exe",
        icon="resources/高架桥桩.ico"
    )
]

# 设置
setup(
    name="桥梁跨越工程安全性评估软件",
    version="1.0",
    description="高架桥桩基沉降影响范围计算软件",
    options={"build_exe": build_exe_options},
    executables=executables
)