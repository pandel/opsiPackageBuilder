# -*- mode: python -*-
ui_tree = Tree('oPB/ui', prefix='oPB/ui', excludes=['*.qss', '*.py'])
lang_tree = Tree('c:/Python34/Lib/site-packages/PyQt5/translations', 'PyQt5/translations', excludes=['assistant*.*', 'designer*.*', 'linguist*.*', 'qscintilla*.*'])
help_tree = Tree('oPB/help', prefix='help')
dll64_tree = Tree('oPB/core/x64', prefix='x64')
dll86_tree = Tree('oPB/core/x86', prefix='x86')

opsipackagebuilder_a = Analysis(['opsipackagebuilder.py'],
             pathex=['.'],
             hiddenimports=['sip', 'PyQt5.QtPrintSupport', 'PyQt5.QtSql'],
             hookspath=None,
             runtime_hooks=None)

helpviewer_a = Analysis(['helpviewer.py'],
             pathex=['.'],
             hiddenimports=['sip', 'PyQt5.QtPrintSupport', 'PyQt5.QtSql'],
             hookspath=None,
             runtime_hooks=None)

#MERGE( (opsipackagebuilder_a, 'opsipackagebuilder', 'opsipackagebuilder.exe'),
#        (helpviewer_a, 'helpviewer', 'helpviewer.exe') )

opsipackagebuilder_pyz = PYZ(opsipackagebuilder_a.pure)
opsipackagebuilder_exe = EXE( opsipackagebuilder_pyz,
          opsipackagebuilder_a.scripts,
          opsipackagebuilder_a.dependencies,
          exclude_binaries=True,
          name='opsipackagebuilder.exe',
          debug=False,
          strip=False,
          upx=False,
          console=True,
          icon='images/prog.ico')

helpviewer_pyz = PYZ(helpviewer_a.pure)
helpviewer_exe = EXE(helpviewer_pyz,
          helpviewer_a.scripts,
          helpviewer_a.dependencies,
          exclude_binaries=True,
          name='helpviewer.exe',
          debug=False,
          strip=False,
          upx=False,
          console=False,
          icon='images/smallIcons_1461.ico')

opsipackagebuilder_coll = COLLECT(opsipackagebuilder_exe,
                opsipackagebuilder_a.binaries,
                opsipackagebuilder_a.zipfiles,
                opsipackagebuilder_a.datas,
                ui_tree,
                lang_tree,
                help_tree,
                dll64_tree,
                dll86_tree,
                [('ui/opsipackagebuilder_rc.py', 'oPB/ui/opsipackagebuilder_rc.py', 'DATA')],
                [('ui/stylesheet.qss', 'oPB/ui/stylesheet.qss', 'DATA')],
                strip=None,
                upx=False,
                name='opsipackagebuilder')

helpviewer_coll = COLLECT(helpviewer_exe,
                helpviewer_a.binaries,
                helpviewer_a.zipfiles,
                helpviewer_a.datas,
                lang_tree,
                help_tree,
                strip=None,
                upx=False,
                name='helpviewer')
