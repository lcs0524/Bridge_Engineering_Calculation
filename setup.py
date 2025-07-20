from cx_Freeze import setup, Executable
import sys

# 依赖包
packages = ["numpy", "matplotlib", "pandas", "scipy", "openpyxl", "PIL", "tkinter", "seaborn"]

# 包含的文件
include_files = [
    ("resources", "resources"),
    ("templates", "templates")
]

# 构建选项
build_exe_options = {
    "packages": packages,
    "include_files": include_files,
    "excludes": ["test"],
    "optimize": 2
}

# 可执行文件配置
executables = [
    Executable(
        "main.py",
        base="Win32GUI" if sys.platform == "win32" else None,
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