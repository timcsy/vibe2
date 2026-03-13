# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for the Voxel Sandbox game."""

import sys
from pathlib import Path

block_cipher = None

a = Analysis(
    ["src/main.py"],
    pathex=[str(Path(".").resolve())],
    binaries=[],
    datas=[
        ("config.json", "."),
        ("assets", "assets"),
    ],
    hiddenimports=[
        "src",
        "src.world",
        "src.world.block",
        "src.world.chunk",
        "src.world.world",
        "src.player",
        "src.player.player",
        "src.player.inventory",
        "src.player.health",
        "src.entities",
        "src.entities.enemy",
        "src.entities.item_drop",
        "src.crafting",
        "src.crafting.recipe",
        "src.crafting.crafting_ui",
        "src.ui",
        "src.ui.hud",
        "src.ui.main_menu",
        "src.persistence",
        "src.persistence.save_manager",
        "noise",
        "pickle",
        "json",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "pytest",
        "pytest_mock",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="VoxelSandbox",
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
    name="VoxelSandbox",
)
