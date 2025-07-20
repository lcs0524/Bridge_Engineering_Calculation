# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

# TCL/TK 库路径配置
tcl_library = r'C:\ProgramData\anaconda3\envs\bridge_calc\Library\lib\tcl8.6'
tk_library = r'C:\ProgramData\anaconda3\envs\bridge_calc\Library\lib\tk8.6'

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[
        (r'C:\ProgramData\anaconda3\envs\bridge_calc\Library\bin\tcl86t.dll', '.'),
        (r'C:\ProgramData\anaconda3\envs\bridge_calc\Library\bin\tk86t.dll', '.'),
        (r'C:\ProgramData\anaconda3\envs\bridge_calc\Library\lib\tcl8.6', 'tcl8.6'),
        (r'C:\ProgramData\anaconda3\envs\bridge_calc\Library\lib\tk8.6', 'tk8.6'),
    ],
    datas=[
        ('resources', 'resources'),
        ('templates', 'templates'),
        ('images', 'images'),
        (tcl_library, 'tcl'),
        (tk_library, 'tk'),
    ],
    hiddenimports=[
        'numpy',
        'matplotlib',
        'matplotlib.pyplot',
        'matplotlib.backends.backend_tkagg',
        'pandas',
        'scipy',
        'scipy.interpolate',
        'openpyxl',
        'openpyxl.cell',
        'openpyxl.styles', 
        'openpyxl.utils',
        'openpyxl.drawing',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        '_tkinter',
        'utils.exporter',
        'utils.validator',
        'visualization.plotter',
        'calculation.settlement'
    ],
    hookspath=['hooks'],
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
    name='桥梁跨越工程安全性评估软件',
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
    icon='images/高架桥桩.png' if os.path.exists('images/高架桥桩.png') else ('resources/高架桥桩.ico' if os.path.exists('resources/高架桥桩.ico') else None),
) 