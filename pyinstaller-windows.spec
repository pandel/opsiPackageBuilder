# -*- mode: python -*-
import os

block_cipher = None


ui_tree = Tree('oPB/ui', prefix='oPB/ui', excludes=['*.qss', '*.py'])

# further information regarding Qt(WebEngine) deploy,
# see https://doc.qt.io/qt-5.10/qtwebengine-deploying.html
# http://doc.qt.io/qt-5/windows-deployment.html


files_tree = [('libEGL.dll', os.getenv("USERPROFILE") + '/Envs/oPB/Lib/site-packages/PyQt5/Qt/bin/libEGL.dll', 'DATA'),
           ('libGLESv2.dll', os.getenv("USERPROFILE") + '/Envs/oPB/Lib/site-packages/PyQt5/Qt/bin/libGLESv2.dll', 'DATA')]

help_tree = Tree('oPB/help', prefix='help')

qss_win_tree = [('ui/stylesheet.qss', 'oPB/ui/stylesheet.qss', 'DATA')]

a = Analysis(['opsipackagebuilder.py'],
             pathex=['.'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
b = Analysis(['helpviewer.py'],
             pathex=['.'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.dependencies,
          exclude_binaries=True,
          name='opsipackagebuilder',
          debug=False,
          strip=False,
          upx=False,
          console=True,
          icon='images/prog_icons/opb/package_256x256.ico')

pyzb = PYZ(b.pure, b.zipped_data,
             cipher=block_cipher)
exeb = EXE(pyzb,
          b.scripts,
          b.dependencies,
          exclude_binaries=True,
          name='helpviewer',
          debug=False,
          strip=False,
          upx=False,
          console=False,
          icon='images/prog_icons/help/help.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               ui_tree,
               files_tree,
               help_tree,
               [('ui/opsipackagebuilder_rc.py', 'oPB/ui/opsipackagebuilder_rc.py', 'DATA')],
               qss_win_tree,
               strip=False,
               upx=False,
               name='opsipackagebuilder')

collb = COLLECT(exeb,
               b.binaries,
               b.zipfiles,
               b.datas,
               ui_tree,
               files_tree,
               help_tree,
               [('ui/opsipackagebuilder_rc.py', 'oPB/ui/opsipackagebuilder_rc.py', 'DATA')],
               qss_win_tree,
               strip=False,
               upx=False,
               name='helpviewer')
