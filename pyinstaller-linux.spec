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
          name='opsipackagebuilder',
          debug=False,
          strip=None,
          upx=True,
          console=True , icon='images/prog.ico')
ui_tree = Tree('oPB/ui', prefix='oPB/ui', excludes=['*.qss'])
help_tree = Tree('oPB/help', prefix='help')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               ui_tree,
               help_tree,
               [('ui/opsipackagebuilder_rc.py', 'oPB/ui/opsipackagebuilder_rc.py', 'DATA')],
               [('ui/stylesheet.qss', 'oPB/ui/stylesheet.qss', 'DATA')],
               strip=None,
               upx=True,
               name='opsipackagebuilder')
