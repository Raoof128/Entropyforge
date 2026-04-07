# -*- mode: python ; coding: utf-8 -*-
# One-folder bundle: pyinstaller entropyforge_onedir.spec

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
    [],
    exclude_binaries=True,
    name="EntropyForge",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="EntropyForge",
)
