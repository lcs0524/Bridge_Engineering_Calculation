#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高架桥桩基沉降影响范围计算软件打包脚本
使用PyInstaller将Python程序打包成exe文件
"""

import os
import sys
import shutil
import subprocess
import platform
import time
from pathlib import Path


def check_environment():
    """检查环境是否满足打包条件"""
    print("检查环境...")
    
    # 检查Python版本
    python_version = sys.version.split()[0]
    print(f"Python版本: {python_version}")
    
    # 检查操作系统
    os_name = platform.system()
    os_version = platform.version()
    print(f"操作系统: {os_name} {os_version}")
    
    # 检查PyInstaller是否安装
    try:
        import PyInstaller
        print(f"PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("PyInstaller未安装，将自动安装...")
        return False
    
    # 检查其他必要库
    required_packages = ["numpy", "matplotlib", "pandas", "scipy", "openpyxl", "pillow"]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"缺少以下库: {', '.join(missing_packages)}，将自动安装...")
        return False
    
    print("环境检查完成")
    return True


def clean_build():
    """清理构建目录"""
    print("清理构建目录...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"删除目录: {dir_name}")
    
    # 清理spec文件
    spec_files = Path('.').glob('*.spec')
    for spec_file in spec_files:
        spec_file.unlink()
        print(f"删除文件: {spec_file}")


def install_dependencies():
    """安装必要的依赖"""
    dependencies = [
        "pyinstaller",
        "numpy",
        "matplotlib",
        "pandas",
        "scipy",
        "openpyxl",
        "pillow",
        "tk"
    ]
    
    for dep in dependencies:
        print(f"正在安装 {dep}...")
        subprocess.call([sys.executable, "-m", "pip", "install", dep])
    
    print("依赖安装完成")


def create_pyinstaller_spec():
    """创建PyInstaller规格文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('resources', 'resources'),
        ('templates', 'templates'),
    ],
    hiddenimports=[
        'numpy',
        'matplotlib',
        'pandas',
        'scipy',
        'openpyxl',
        'openpyxl.cell',
        'openpyxl.styles',
        'openpyxl.utils',
        'openpyxl.drawing',
        'PIL',
        'PIL.Image',
        'tkinter',
        'matplotlib.backends.backend_tkagg',
        'scipy.interpolate',
        'utils.exporter',
        'utils.validator',
        'visualization.plotter',
        'calculation.settlement'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='高架桥桩基沉降计算软件',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/高架桥桩.ico' if os.path.exists('resources/高架桥桩.ico') else ('resources/icon.ico' if os.path.exists('resources/icon.ico') else None),
)
'''
    
    with open('software.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("创建PyInstaller规格文件完成")


def build_executable():
    """构建可执行文件"""
    print("开始执行PyInstaller构建...")
    
    # 确保resources目录存在
    if not os.path.exists('resources'):
        os.makedirs('resources', exist_ok=True)
        print("创建resources目录")
    
    # 确保templates目录存在
    if not os.path.exists('templates'):
        os.makedirs('templates', exist_ok=True)
        print("创建templates目录")
    
    # 检查icon.ico是否存在，如果不存在则创建一个简单的图标
    if not os.path.exists('resources/icon.ico'):
        try:
            # 尝试从其他位置复制图标，或使用PIL创建一个简单的图标
            from PIL import Image, ImageDraw
            icon_size = (48, 48)
            icon_img = Image.new('RGBA', icon_size, color=(255, 255, 255, 0))
            draw = ImageDraw.Draw(icon_img)
            
            # 绘制一个简单的图标
            draw.rectangle([5, 5, 43, 43], fill=(0, 120, 212), outline=(0, 0, 0))
            draw.ellipse([10, 10, 38, 38], fill=(255, 255, 255))
            
            # 保存为.ico格式
            icon_path = os.path.join('resources', 'icon.ico')
            icon_img.save(icon_path, format='ICO')
            print(f"创建默认图标: {icon_path}")
        except Exception as e:
            print(f"创建图标失败: {e}")
    
    try:
        # 使用spec文件构建
        subprocess.check_call([
            sys.executable, '-m', 'PyInstaller',
            'software.spec',
            '--noconfirm'
        ])
        
        print("可执行文件构建完成")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return False


def copy_resources():
    """复制资源文件"""
    print("复制资源文件...")
    
    # 创建dist目录下的资源文件夹
    os.makedirs('dist/resources', exist_ok=True)
    os.makedirs('dist/templates', exist_ok=True)
    
    # 复制resources目录中的所有文件
    if os.path.exists('resources'):
        for file in os.listdir('resources'):
            src = os.path.join('resources', file)
            dst = os.path.join('dist/resources', file)
            if os.path.isfile(src):
                shutil.copy2(src, dst)
    
    # 复制templates目录中的所有文件
    if os.path.exists('templates'):
        for file in os.listdir('templates'):
            src = os.path.join('templates', file)
            dst = os.path.join('dist/templates', file)
            if os.path.isfile(src):
                shutil.copy2(src, dst)
    
    print("资源文件复制完成")


def copy_additional_files():
    """复制额外文件到发布目录"""
    print("复制额外文件...")
    
    dist_dir = Path('dist')
    if not dist_dir.exists():
        print("发布目录不存在")
        return False
    
    # 创建文档目录
    docs_dir = dist_dir / 'docs'
    docs_dir.mkdir(exist_ok=True)
    
    # 复制文档文件
    files_to_copy = {
        'README.md': '使用说明.md',
        'requirements.txt': 'requirements.txt'
    }
    
    for src, dst in files_to_copy.items():
        if os.path.exists(src):
            shutil.copy2(src, docs_dir / dst)
            print(f"复制文件: {src} -> {dst}")
    
    print("额外文件复制完成")
    return True


def create_readme():
    """创建使用说明文件"""
    readme_content = """# 高架桥桩基沉降影响范围计算软件 1.0

## 软件介绍
本软件基于Boussinesq理论，结合工程实际应用的修正系数，用于计算高架桥桩基沉降对周围环境的影响范围。

## 主要功能
1. **基于Boussinesq理论的沉降计算**
2. **工程参数修正（FLAC3D标定）**
3. **16个标准计算点分析**
4. **图形化结果展示**
5. **安全评估和工程建议**
6. **多格式结果导出**

## 使用方法
1. 双击运行"高架桥桩基沉降计算软件.exe"
2. 输入桩基基本参数（桩径、桩长、荷载等）
3. 设置土层参数（深度、压缩模量、泊松比等）
4. 点击"设计计算"开始计算
5. 查看计算结果和图形分析
6. 导出计算报告

## 技术参数
- **计算理论**: Boussinesq弹性理论
- **修正方法**: FLAC3D数值模拟标定
- **技术规范**: JTG D30-2015《公路路基设计规范》
- **计算精度**: 毫米级沉降计算
- **适用范围**: 桩径0.3-5.0m，桩长3-80m

## 系统要求
- Windows 7/8/10/11 (64位)
- 内存: 4GB以上
- 硬盘空间: 500MB以上

## 注意事项
1. 输入参数应符合工程实际情况
2. 土层参数需根据实际地质勘探资料确定
3. 计算结果仅供工程设计参考
4. 重要工程建议进行专项论证

## 技术支持
开发者：金洪松
开发时间：2025年4月25日
版权所有 © 2025

## 更新历史
- v1.0 (2025.4.25): 初始版本发布
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("创建使用说明文件完成")


def main():
    """主函数"""
    print("=== 开始构建可执行文件 ===")
    
    # 检查环境
    if not check_environment():
        print("环境检查未通过，将尝试安装必要依赖...")
    
    # 清理旧的构建文件
        clean_build()
        
    # 检查必要文件
    if not os.path.exists('main.py'):
        print("错误: 找不到主程序文件main.py")
        return False
        
    # 检查必要目录
    required_dirs = ['utils', 'visualization', 'calculation', 'gui']
    for directory in required_dirs:
        if not os.path.exists(directory):
            print(f"警告: 找不到目录 {directory}，请确认项目结构是否完整")
    
    # 安装依赖
    install_dependencies()
    
    # 创建PyInstaller规格文件
    create_pyinstaller_spec()
        
    # 执行PyInstaller构建
    success = build_executable()
    if not success:
        print("PyInstaller构建失败")
        return False
        
    # 复制资源文件
    copy_resources()
    
    # 复制额外文件
    copy_additional_files()
        
    print("=== 构建完成 ===")
    print("可执行文件已生成在dist目录下")
    return True
        

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("程序打包成功！")
        else:
            print("程序打包失败，请检查错误信息。")
    except Exception as e:
        print(f"打包过程中发生未知错误: {e}")
        import traceback
        traceback.print_exc()
    
    # 等待用户按键退出
    input("按任意键退出...")