General hint regarding opsi Package Builder
===========================================

This repository is work in progress. There are many things that won't work at the moment and will change over time. so don't use this in production.

I take no responsibility for your decision to use anything from here!!!

opsi PackageBuilder is only tested with Python 3.4 and PyQT5.

Requirements
============
- PyQt5
- spur
- sphinx_rtd_theme
- PyCrypto
- simple-crypt>=4.0.0

Included scripts and files
==========================

(The scripts will only work under Windows!)

- 1_update_locale.cmd/.sh: 		Re-scan source files for new(updated language strings.
- 2_compile_resource.cmd/.sh:		Make Python file from \*.qrc file
- 3_sphinx.cmd/.sh:			Re-scan source file in-place documentation
- 4_distrib.cmd/.sh:			Build install package via PyInstaller
- pyinstaller-(linux/windows).spec:	Packaging control files for PyInstaller
- debreate-packager-control.dbp:	Control file for Debian Package creator Debreate (http://debreate.sourceforge.net)

Pre-compiled files
==================

oPB/core/(x64(x86)/MapDrive.dll: easy network drive mounting DLL

See src/MapDrive/READMA for details.

Compiling MapDrive.dll
----------------------

You need to install VC++ 2010 Express and, additionally, Microsoft Windows SDK v7.1, if you want to compile for a 64Bit Platform.

Using PyInstaller
=================

You need to download a Python 3 compatible version of PyInstaller from www.pyinstaller.org and install it from the source package. 

On Linux:
    - clone python3 branch: git clone -b python3 https://github.com/pyinstaller/pyinstaller.git
    - install from PyInstaller directory via setup.py

On Windows:
    - follow the instruction on http://pythonhosted.org/PyInstaller/#installing-in-windows and install from archive
    - Before you do that, modify the file:

        ``pyinstaller-python3/PyInstaller/utils/hooks/hookutils.py``

        according to this:

        .. code-block:: html

        	def qt5_qml_dir():
        	    try:
        	        qmldir = compat.exec_command("qmake", "-query", "QT_INSTALL_QML")
        	        qmldir = qmldir.strip()
        	    except IOError:
        	        qmldir = ''
        	    if len(qmldir) == 0:
        		....

Reason:
Under Windows , the command "qmake -query QT_INSTALL_QML" returns the path to the qml folder, but has carriage return ("\\r\\n") at the end of the string under windows. This can't be handled correctly, so remove it.

Infos regarding reST
====================
`Sphinx Example <https://pythonhosted.org/an_example_pypi_project/sphinx.html>`_

`reST Cheat Sheet <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_
