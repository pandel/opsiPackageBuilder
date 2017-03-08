#from PyInstaller.build import Tree

# -*- mode: python -*-
ui_tree = Tree('oPB/ui', prefix='oPB/ui', excludes=['*.qss'])
help_tree = Tree('oPB/help', prefix='help')
#lang_tree = Tree('/usr/local/opt/qt5/translations', 'translations', excludes=['assistant*.*', 'designer*.*', 'linguist*.*', 'qscintilla*.*'])


lang_tree = [('translations/qt_de.qm', '/usr/local/opt/qt5/translations/qt_de.qm', 'DATA'),
	   ('translations/qt_help_de.qm', '/usr/local/opt/qt5/translations/qt_help_de.qm', 'DATA'),
	   ('translations/qtbase_de.qm', '/usr/local/opt/qt5/translations/qtbase_de.qm', 'DATA')]


bundle_version = '8.1.5'


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
          console=False,
          icon='images/prog_icons/mac/opsipackagebuilder.icns')

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
          icon='images/prog_icons/mac/help.icns')

opsipackagebuilder_coll = COLLECT(opsipackagebuilder_exe,
                opsipackagebuilder_a.binaries,
                opsipackagebuilder_a.zipfiles,
                opsipackagebuilder_a.datas,
                ui_tree,
                lang_tree,
                help_tree,
                [('ui/opsipackagebuilder_rc.py', 'oPB/ui/opsipackagebuilder_rc.py', 'DATA')],
                [('ui/stylesheet.qss', 'oPB/ui/stylesheet.qss', 'DATA')],
                [('ui/stylesheet-mac.qss', 'oPB/ui/stylesheet-mac.qss', 'DATA')],
                strip=None,
                upx=False,
                name='opsipackagebuilder')

helpviewer_coll = COLLECT(helpviewer_exe,
                helpviewer_a.binaries,
                helpviewer_a.zipfiles,
                helpviewer_a.datas,
                ui_tree,
                lang_tree,
                help_tree,
                [('ui/opsipackagebuilder_rc.py', 'oPB/ui/opsipackagebuilder_rc.py', 'DATA')],
                [('ui/stylesheet.qss', 'oPB/ui/stylesheet.qss', 'DATA')],
                [('ui/stylesheet-mac.qss', 'oPB/ui/stylesheet-mac.qss', 'DATA')],
                strip=None,
                upx=False,
                name='helpviewer')

app1 = BUNDLE(opsipackagebuilder_coll,
                name=os.path.join('dist', 'opsiPackageBuilder.app'),
                appname="opsiPackageBuilder",
                version = bundle_version)

app2 = BUNDLE(helpviewer_coll,
                name=os.path.join('dist', 'opbHelpViewer.app'),
                appname="oPB HelpViewer",
                version = bundle_version)
                