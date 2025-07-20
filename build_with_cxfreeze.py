import sys
from cx_Freeze import setup, Executable
import os

# 构建选项
build_exe_options = {
    "packages": [
        "tkinter", "tkinter.ttk", "tkinter.messagebox", "tkinter.filedialog",
        "numpy", "pandas", "matplotlib", "scipy", "openpyxl", "PIL", 
        "matplotlib.backends.backend_tkagg", "scipy.interpolate"
    ],
    "excludes": ["unittest"],
    "include_files": [
        ("resources", "resources"),
        ("templates", "templates")
    ],
    "optimize": 2,
    "build_exe": "dist_cxfreeze"
}

# 可执行文件配置
executables = [
    Executable(
        "main.py",
        base="Win32GUI",  # 隐藏控制台窗口
        target_name="高架桥桩基沉降计算软件.exe",
        icon="resources/高架桥桩.ico" if os.path.exists("resources/高架桥桩.ico") else None
    )
]

# 设置
setup(
    name="高架桥桩基沉降计算软件",
    version="1.0",
    description="高架桥桩基沉降影响范围计算软件",
    options={"build_exe": build_exe_options},
    executables=executables
) 