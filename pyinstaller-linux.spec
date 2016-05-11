# -*- mode: python -*-
ui_tree = Tree('oPB/ui', prefix='oPB/ui', excludes=['*.qss'])
help_tree = Tree('oPB/help', prefix='help')
#lang_tree = Tree('/usr/share/qt5/translations', 'translations', excludes=['assistant*.*', 'designer*.*', 'linguist*.*', 'qscintilla*.*'])

lang_tree = [('translations/qt_de.qm', '/usr/share/qt5/translations/qt_de.qm', 'DATA'),
	   ('translations/qt_en.qm', '/usr/share/qt5/translations/qt_en.qm', 'DATA'),
	   ('translations/qthelp_de.qm', '/usr/share/qt5/translations/qthelp_de.qm', 'DATA'),
	   ('translations/qthelp_en.qm', '/usr/share/qt5/translations/qthelp_en.qm', 'DATA'),
	   ('translations/qtbase_de.qm', '/usr/share/qt5/translations/qtbase_de.qm', 'DATA'),
	   ('translations/qtbase_en.qm', '/usr/share/qt5/translations/qtbase_en.qm', 'DATA')]

opsipackagebuilder_a = Analysis(['opsipackagebuilder.py'],
             pathex=['.'],
#             hiddenimports=['sip', 'PyQt5.QtPrintSupport', 'PyQt5.QtSql'],
             hookspath=None,
             runtime_hooks=None)

helpviewer_a = Analysis(['helpviewer.py'],
             pathex=['.'],
#             hiddenimports=['sip', 'PyQt5.QtPrintSupport', 'PyQt5.QtSql'],
             hookspath=None,
             runtime_hooks=None)


opsipackagebuilder_pyz = PYZ(opsipackagebuilder_a.pure)
opsipackagebuilder_exe = EXE( opsipackagebuilder_pyz,
          opsipackagebuilder_a.scripts,
          opsipackagebuilder_a.dependencies,
          exclude_binaries=True,
          name='opsipackagebuilder',
          debug=False,
          strip=False,
          upx=False,
          console=True,
          icon='images/prog_icons/opb/package_256x256.png')

helpviewer_pyz = PYZ(helpviewer_a.pure)
helpviewer_exe = EXE(helpviewer_pyz,
          helpviewer_a.scripts,
          helpviewer_a.dependencies,
          exclude_binaries=True,
          name='helpviewer',
          debug=False,
          strip=False,
          upx=False,
          console=False,
          icon='images/prog_icons/help/256x256.png')

opsipackagebuilder_coll = COLLECT(opsipackagebuilder_exe,
                opsipackagebuilder_a.binaries,
                opsipackagebuilder_a.zipfiles,
                opsipackagebuilder_a.datas,
                ui_tree,
                lang_tree,
                help_tree,
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

