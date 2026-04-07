# -*- mode: python ; coding: utf-8 -*-
# Build (from repo root, venv active, pip install -e . done):
#   pyinstaller entropyforge.spec

a = Analysis(
    ["src/entropyforge/__main__.py"],
    pathex=["src"],
    binaries=[],
    datas=[("src/entropyforge/locales", "entropyforge/locales")],
    hiddenimports=["customtkinter", "entropyforge", "entropyforge.ui"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="EntropyForge",
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
)
