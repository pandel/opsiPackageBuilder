# -*- mode: python -*-
a = Analysis(['D:\\Pythonprojects\\Python oPB\\opsiPackageBuilder.py'],
             pathex=['d:\\Pythonprojects\\Python oPB'],
             hiddenimports=['sip'],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='opsiPackageBuilder.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True , icon='D:\\Pythonprojects\\Python oPB\\images\\prog.ico')
platforms_tree = Tree('c:\\Python34\\Lib\\site-packages\\PyQt5\plugins\\platforms', prefix='qt5_plugins\\platforms')
ui_tree = Tree('d:\\Pythonprojects\\Python oPB\\oPB\\ui', prefix='oPB\\ui')
img_tree = Tree('c:\\Python34\\Lib\\site-packages\\PyQt5\plugins\\imageformats', prefix='qt5_plugins\\imageformats')
icon_tree = Tree('c:\\Python34\\Lib\\site-packages\\PyQt5\plugins\\iconengines', prefix='qt5_plugins\\iconengines')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               platforms_tree,
               ui_tree,
               img_tree,
               icon_tree,
               strip=None,
               upx=True,
               name='opsiPackageBuilder')
