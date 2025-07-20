import sys
from cx_Freeze import setup, Executable

# 增加递归限制
sys.setrecursionlimit(5000)

# 构建选项
build_exe_options = {
    "packages": [
        "numpy", "pandas", "matplotlib", "tkinter", "PIL", 
        "openpyxl", "seaborn", "scipy", "calculation", "gui"
    ],
    "excludes": [
        "test", "unittest", "email", "html", "http", "urllib", 
        "xml", "pydoc", "doctest", "argparse", "difflib"
    ],
    "include_files": [
        ("resources/", "resources/"),
        ("templates/", "templates/"),
        ("docs/", "docs/")
    ],
    "optimize": 2,
    # 移除了 zip_include_packages 选项以避免冲突
    "bin_excludes": ["VCRUNTIME140.dll", "MSVCP140.dll"],
}

# 可执行文件配置
executables = [
    Executable(
        "main.py",
        base="Win32GUI",  # 隐藏控制台窗口
        target_name="高架桥桩基沉降计算软件.exe",
        icon="resources/高架桥桩.ico"
    )
]

setup(
    name="高架桥桩基沉降计算软件",
    version="1.0",
    description="高架桥桩基沉降影响范围计算软件",
    options={"build_exe": build_exe_options},
    executables=executables
)