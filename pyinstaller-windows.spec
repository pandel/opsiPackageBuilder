# -*- mode: python -*-
import os

block_cipher = None


ui_tree = Tree('oPB/ui', prefix='oPB/ui', excludes=['*.qss', '*.py'])
lang_tree = [('PyQt5/translations/qt_de.qm', os.getenv("USERPROFILE") + '/Envs/oPB/Lib/site-packages/PyQt5/Qt/translations/qt_de.qm', 'DATA'),
	   ('PyQt5/translations/qt_en.qm', os.getenv("USERPROFILE") + '/Envs/oPB/Lib/site-packages/PyQt5/Qt/translations/qt_en.qm', 'DATA'),
	   ('PyQt5/translations/qthelp_de.qm', os.getenv("USERPROFILE") + '/Envs/oPB/Lib/site-packages/PyQt5/Qt/translations/qt_help_de.qm', 'DATA'),
	   ('PyQt5/translations/qthelp_en.qm', os.getenv("USERPROFILE") + '/Envs/oPB/Lib/site-packages/PyQt5/Qt/translations/qt_help_en.qm', 'DATA'),
	   ('PyQt5/translations/qtbase_de.qm', os.getenv("USERPROFILE") + '/Envs/oPB/Lib/site-packages/PyQt5/Qt/translations/qtbase_de.qm', 'DATA'),
	   ('PyQt5/translations/qtbase_en.qm', os.getenv("USERPROFILE") + '/Envs/oPB/Lib/site-packages/PyQt5/Qt/translations/qtbase_en.qm', 'DATA'),
	   ('PyQt5/translations/qtwebengine_de.qm', os.getenv("USERPROFILE") + '/Envs/oPB/Lib/site-packages/PyQt5/Qt/translations/qtwebengine_de.qm', 'DATA'),
	   ('PyQt5/translations/qtwebengine_en.qm', os.getenv("USERPROFILE") + '/Envs/oPB/Lib/site-packages/PyQt5/Qt/translations/qtwebengine_en.qm', 'DATA'),
	   ('qtwebengine_locales/de.pak', os.getenv("USERPROFILE") + '/Envs/oPB/Lib/site-packages/PyQt5/Qt/translations/qtwebengine_locales/de.pak', 'DATA'),
	   ('qtwebengine_locales/en-US.pak', os.getenv("USERPROFILE") + '/Envs/oPB/Lib/site-packages/PyQt5/Qt/translations/qtwebengine_locales/en-US.pak', 'DATA'),
	   ('qtwebengine_locales/en-GB.pak', os.getenv("USERPROFILE") + '/Envs/oPB/Lib/site-packages/PyQt5/Qt/translations/qtwebengine_locales/en-GB.pak', 'DATA')]

files_tree = [('QtWebEngineProcess.exe', os.getenv("USERPROFILE") + '/Envs/oPB/Lib/site-packages/PyQt5/Qt/bin/QtWebEngineProcess.exe', 'DATA'),
           ('icudtl.dat', os.getenv("USERPROFILE") + '/Envs/oPB/Lib/site-packages/PyQt5/Qt/resources/icudtl.dat', 'DATA'),
           ('qtwebengine_devtools_resources.pak', os.getenv("USERPROFILE") + '/Envs/oPB/Lib/site-packages/PyQt5/Qt/resources/qtwebengine_devtools_resources.pak', 'DATA'),
           ('qtwebengine_resources.pak', os.getenv("USERPROFILE") + '/Envs/oPB/Lib/site-packages/PyQt5/Qt/resources/qtwebengine_resources.pak', 'DATA'),
           ('qtwebengine_resources_100p.pak', os.getenv("USERPROFILE") + '/Envs/oPB/Lib/site-packages/PyQt5/Qt/resources/qtwebengine_resources_100p.pak', 'DATA'),
           ('qtwebengine_resources_200p.pak', os.getenv("USERPROFILE") + '/Envs/oPB/Lib/site-packages/PyQt5/Qt/resources/qtwebengine_resources_200p.pak', 'DATA'),
           ('libEGL.dll', os.getenv("USERPROFILE") + '/Envs/oPB/Lib/site-packages/PyQt5/Qt/bin/libEGL.dll', 'DATA'),
           ('libGLESv2.dll', os.getenv("USERPROFILE") + '/Envs/oPB/Lib/site-packages/PyQt5/Qt/bin/libGLESv2.dll', 'DATA')]

help_tree = Tree('oPB/help', prefix='help')
dll64_tree = Tree('oPB/core/x64', prefix='x64')
dll86_tree = Tree('oPB/core/x86', prefix='x86')


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
               lang_tree,
               files_tree,
               help_tree,
               dll64_tree,
               dll86_tree,
               [('ui/opsipackagebuilder_rc.py', 'oPB/ui/opsipackagebuilder_rc.py', 'DATA')],
               [('ui/stylesheet.qss', 'oPB/ui/stylesheet.qss', 'DATA')],
               strip=False,
               upx=False,
               name='opsipackagebuilder')

collb = COLLECT(exeb,
               b.binaries,
               b.zipfiles,
               b.datas,
               ui_tree,
               lang_tree,
               files_tree,
               help_tree,
               dll64_tree,
               dll86_tree,
               [('ui/opsipackagebuilder_rc.py', 'oPB/ui/opsipackagebuilder_rc.py', 'DATA')],
               [('ui/stylesheet.qss', 'oPB/ui/stylesheet.qss', 'DATA')],
               strip=False,
               upx=False,
               name='helpviewer')
