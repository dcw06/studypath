# -*- mode: python ; coding: utf-8 -*-

import os
block_cipher = None

BASE = os.path.dirname(os.path.abspath(SPEC))

a = Analysis(
    ['main.py'],
    pathex=[BASE],
    binaries=[],
    datas=[
        (os.path.join(BASE, 'templates'), 'templates'),
        (os.path.join(BASE, 'static'),    'static'),
        (os.path.join(BASE, '.env'),      '.'),
    ],
    hiddenimports=[
        'flask',
        'authlib',
        'authlib.integrations.flask_client',
        'dotenv',
        'requests',
        'webview',
        'webview.platforms.cocoa',
        'bank',
        'storage',
        'config',
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
    [],
    exclude_binaries=True,
    name='SignIn',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SignIn',
)

app = BUNDLE(
    coll,
    name='SignIn.app',
    icon=None,
    bundle_identifier='com.yourname.signin',
    info_plist={
        'NSHighResolutionCapable': True,
        'LSUIElement': False,
        'CFBundleShortVersionString': '1.0.0',
    },
)
