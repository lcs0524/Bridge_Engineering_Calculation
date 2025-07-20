# -*- mode: python ; coding: utf-8 -*-

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
