# -*- mode: python -*-
a = Analysis(['opsipackagebuilder.py'],
             pathex=[''],
             hiddenimports=['sip', 'PyQt5.QtPrintSupport', 'PyQt5.QtSql'],
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
          console=True , icon='images/prog.ico')
platforms_tree = Tree('c:/Python34/Lib/site-packages/PyQt5/plugins/platforms', prefix='qt5_plugins/platforms')
img_tree = Tree('c:/Python34/Lib/site-packages/PyQt5/plugins/imageformats', prefix='qt5_plugins/imageformats')
icon_tree = Tree('c:/Python34/Lib/site-packages/PyQt5/plugins/iconengines', prefix='qt5_plugins/iconengines')
sql_tree = Tree('c:/Python34/Lib/site-packages/PyQt5/plugins/sqldrivers', prefix='qt5_plugins/sqldrivers')
ui_tree = Tree('oPB/ui', prefix='oPB/ui', excludes=['*.qss', 'opsipackagebuilder_rc.py'])
help_tree = Tree('oPB/help', prefix='help')
dll64_tree = Tree('oPB/core/x64', prefix='x64')
dll86_tree = Tree('oPB/core/x86', prefix='x86')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               platforms_tree,
               ui_tree,
               help_tree,
               dll64_tree,
               dll86_tree,
               [('ui/opsipackagebuilder_rc.py', 'oPB/ui/opsipackagebuilder_rc.py', 'DATA')],
               [('ui/stylesheet.qss', 'oPB/ui/stylesheet.qss', 'DATA')],
               img_tree,
               icon_tree,
			   sql_tree,
               strip=None,
               upx=True,
               name='opsipackagebuilder')
