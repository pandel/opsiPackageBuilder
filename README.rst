General hint regarding opsi Package Builder
===========================================

This repository is work in progress. There are many things that won't work at the moment and will change over time. so don't use this in production.

I take no responsibility for your decision to use anything from here!!!

opsi PackageBuilder is only tested with Python 3.4 and PyQt5.

Requirements
============
- Python (3.4.3 tested)
- PyQt5 (5.4.2 tested
- spur (0.3.14 tested)
- PyCrypto (2.6.1 tested)
- Sphinx (current)
- Releases (current)

Included scripts and files
==========================

- 1_update_locale.cmd/.sh: 		Re-scan source files for new(updated language strings.
- 2_compile_resource.cmd/.sh:		Make Python file from \*.qrc file
- 3_sphinx.cmd/.sh:			Re-scan source file in-place documentation
- 4_distrib.cmd/.sh/-mac.sh:		Build install package via PyInstaller
- pyinstaller-(linux/windows/mac).spec:	Packaging control files for PyInstaller
- linux/debreate-normal.dbp:		Control file for Debian Package creator Debreate (http://debreate.sourceforge.net) (Standard package)
- linux/debreate-self-contained.dbp:	Control file for Debian Package creator Debreate (http://debreate.sourceforge.net) (Self-contained package)

Pre-compiled files
==================

oPB/core/(x64(x86)/MapDrive.dll: easy network drive mounting DLL

See src/MapDrive/README for details.

Installing Spur / PyCrypto and compiling MapDrive.dll from source
-----------------------------------------------------------------

You need to install VC++ 2010 Express and, additionally, Microsoft Windows SDK v7.1, if you want to compile for a 64Bit Platform:

- install VC++ via Visual Studio 2010 Express ISO
    `English ISO <http://download.microsoft.com/download/1/E/5/1E5F1C0A-0D5B-426A-A603-1798B951DDAE/VS2010Express1.iso>`_
    `German ISO <http://go.microsoft.com/?linkid=9709973>`_
- install Windows SDK v7.1  ISO
    `Link to Microsoft page <https://www.microsoft.com/en-us/download/details.aspx?id=8442>`_
    Get DVD named: GRMSDKX_EN_DVD.iso (64bit)
- If you can't install the SDK, then it is perhaps because VC++ Studio installed an older VC++ 2010 Redistributable Package on you computer before. Go to Software and uninstall it first, then install the SDK.
- IMPORTANT: install `this MS hotfix <https://support.microsoft.com/de-de/kb/2519277>`_, because it can happen that a Windows update removes your VC++ compilers ;-)
- Create file **vcvars64.bat** under **C:\\Program Files (x86)\\Microsoft Visual Studio 10.0\\VC\\bin\\amd64** with following content:

    call "C:\\Program Files\\Microsoft SDKs\\Windows\\v7.1\\bin\\setenv.cmd" /x64


Running oPB under Mac OSX
===================================

I have successfully run oPB under OSX Yosemite. Python3, PyQt5 and mostly anything else installed via howmebrew package manager.


Using PyInstaller
=================

You need to download a Python 3 compatible version of PyInstaller from www.pyinstaller.org and install it from the source package. 

On Linux:
    - clone python3 branch: git clone -b python3 https://github.com/pyinstaller/pyinstaller.git
    - install from PyInstaller directory via setup.py

On Windows:
    - follow the instruction on http://pythonhosted.org/PyInstaller/#installing-in-windows and install from archive

Infos regarding reST
====================
`Sphinx Example <https://pythonhosted.org/an_example_pypi_project/sphinx.html>`_

`reST Cheat Sheet <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_
