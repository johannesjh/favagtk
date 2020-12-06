# -*- mode: python ; coding: utf-8 -*-

import importlib
import os

from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import copy_metadata

hidden_imports = collect_submodules(
    "beancount", filter=lambda name: "test" not in name
)

# add fava version information:
data_files = copy_metadata("fava")

# add fava static files:
fava_dir = os.path.dirname(importlib.import_module("fava").__file__)
data_files += [
    (fava_dir + "/help", "fava/help"),
    (fava_dir + "/static", "fava/static"),
    (fava_dir + "/templates", "fava/templates"),
    (fava_dir + "/translations", "fava/translations"),
]

# add beancount version file:
beancount_dir = os.path.dirname(importlib.import_module("beancount").__file__)
beancount_version_file = os.path.join(beancount_dir, "VERSION")
data_files += [(beancount_version_file, "beancount")]

a = Analysis(['../../fava_desktop/main.py'],
             pathex=['/home/jh/repos/beancount/fava-desktop'],
             binaries=[],
             datas=data_files,
             hiddenimports=hidden_imports,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=None,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
          cipher=None)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='fava-desktop',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True)
