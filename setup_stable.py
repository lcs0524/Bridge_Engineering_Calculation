from cx_Freeze import setup, Executable
import sys
import os

# 构建选项
build_exe_options = {
    "packages": [
        "numpy", "pandas", "matplotlib", "tkinter", 
        "openpyxl", "xlsxwriter", "PIL", "json", "csv"
    ],
    "excludes": [
        "unittest", "pydoc", "difflib", "doctest", 
        "inspect", "multiprocessing", "concurrent.futures"
    ],
    "include_files": [
        ("images/", "images/"),
        ("resources/", "resources/"),
        ("calculation/", "calculation/"),
        ("gui/", "gui/"),
        ("utils/", "utils/"),
        ("visualization/", "visualization/")
    ],
    "optimize": 2,
    "include_msvcrt": True
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

setup(
    name="桥梁跨越工程安全性评估软件",
    version="1.0",
    description="桥梁跨越工程安全性评估软件",
    options={"build_exe": build_exe_options},
    executables=executables
)