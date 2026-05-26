# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

# 1. Базовые файлы проекта
datas = [('templates', 'templates'), ('icon.ico', '.'), ('static', 'static')]
binaries = []
hiddenimports = [
    'flask', 'openai', 'google.generativeai', 'groq',
    'app', 'detector', 'pypdf',
    '_cffi_backend' # Принудительно указываем сишный бэкенд
]

# 2. ПРИНУДИТЕЛЬНЫЙ СБОР ВСЕГО
# collect_all вытаскивает все зависимости, DLL и скрипты, которые PyInstaller не видит сам
for pkg in ['webview', 'clr_loader', 'pythonnet', 'cffi']:
    pkg_datas, pkg_binaries, pkg_hiddenimports = collect_all(pkg)
    datas += pkg_datas
    binaries += pkg_binaries
    hiddenimports += pkg_hiddenimports

a = Analysis(
    ['setup_and_run.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Ellibria',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False, # Строго False!
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)