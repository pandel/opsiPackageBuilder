# -*- mode: python -*-
a = Analysis(['D:\\Pythonprojects\\opsipackagebuilder-dropbox\\opsiPackageBuilder.py'],
             pathex=['d:\\Pythonprojects\\opsipackagebuilder-dropbox'],
             hiddenimports=['sip'],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='opsipackagebuilder.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True , icon='D:\\Pythonprojects\\opsipackagebuilder-dropbox\\images\\prog.ico')
platforms_tree = Tree('c:\\Python34\\Lib\\site-packages\\PyQt5\plugins\\platforms', prefix='qt5_plugins\\platforms')
ui_tree = Tree('d:\\Pythonprojects\\opsipackgebuilder-github\\oPB\\ui', prefix='oPB\\ui')
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
               name='opsipackagebuilder')
