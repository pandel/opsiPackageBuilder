General hint regarding opsi Package Builder
===========================================

opsi PackageBuilder (oPB) is meant as a helpful tool regarding package creation and maintenance for the `opsi <http://www.opsi.org>`_ open source client management system.
The oPB is currently being developed under Python 3.6 and PyQt 5.10.1, but you can find older versions of it in this Github repository, which will work with Python 3.4 and PyQt 5.5. Minimum requirements for running the current version of oPB should be Python 3.4 and PyQt 5.6.

Current requirements or recommendations
=======================================

- Microsoft Visual C++ 2010 Redistributable (https://www.microsoft.com/de-de/download/details.aspx?id=5555)
- Python (3.6.2)
- PyQt5 (5.9.0+)
- spur (0.3.20)
- pycryptodome (3.4.6)
- virtualenv (optional)
- virtualenvwrapper-win (only Windows, optional)

For generation of help files:

- Releases (1.4.0)
- Sphinx (1.7.1 - depends on Releases)

To freeze the script and build the installer:

- PyInstaller 3.3.1 or later (at least for me, because of Python 3.6 support)
- Inno Setup 5

For my personal convenience, I'm using a virtualenv environment from now on. This is important, because the pyinstaller \*.spec files refer to the new env location. I set up my virtualenv under ``os.getenv("USERPROFILE") + '/Envs/oPB/``. If your virtualenv is in another location, you have to edit the corresponding pyinstaller \*.spec file. accordingly.

Included scripts and files
==========================

+---------------------------------------+------------------------------------------------------------------------+
| 0_version.cmd                         | Change current version number throughout                               |
|                                       | all necessary files (only Windows)                                     |
+---------------------------------------+------------------------------------------------------------------------+
| 1_update_locale.cmd/.sh:              | Re-scan source files for new or updated language strings.              |
+---------------------------------------+------------------------------------------------------------------------+
| 2_compile_resource.cmd/.sh:           | Make Python file from \*.qrc file                                      |
+---------------------------------------+------------------------------------------------------------------------+
| 3_sphinx.cmd/.sh:                     | Re-scan source file in-place documentation                             |
+---------------------------------------+------------------------------------------------------------------------+
| 4_distrib.cmd/.sh/-mac.sh:            | Build install package via PyInstaller                                  |
+---------------------------------------+------------------------------------------------------------------------+
| pyinstaller-(linux/windows/mac).spec: | Packaging control files for PyInstaller (sorry, but only the windows   |
|                                       | one is the most actively maintained file here)                         |
+---------------------------------------+------------------------------------------------------------------------+
| linux/debreate-normal.dbp:            | Control file for Debian Package creator                                |
|                                       | `Debreate <http://debreate.sourceforge.net>`_ (Standard package)       |
+---------------------------------------+------------------------------------------------------------------------+
| linux/debreate-self-contained.dbp:    | Control file for Debian Package creator                                |
|                                       | `Debreate <http://debreate.sourceforge.net>`_ (Self-contained package) |
+---------------------------------------+------------------------------------------------------------------------+

DISCLAIMER:
All the above mentioned scripts are simple little helpers for me and my workflow. I leave them inside the repository for your convenience, but you have to take a look for yourself what they are supposed to do and how they work. It is highly possible that they fail on your system, so use them at your own risk!

Pre-compiled files
==================

Installing Spur / PyCrypto from source
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


Running oPB under MacOS X or Linux
==================================

Running oPB UNDER MacOS X or Linux is considered to be EXPERIMENTAL! Try on your own risk!

I have successfully run oPB under OSX Yosemite and Ubuntu Linux 15.04 before. Python3, PyQt5 and mostly anything else installed via homebrew package manager or apt.
But I cannot assure that it will work at the moment (Python 3.6.2, Qt 5.9) as I don't have any time to test it.


Using PyInstaller
=================

Generally, you need to download a Python 3.6 compatible version of PyInstaller from www.pyinstaller.org and install it a) via pip or b) from the source package as follows

    - clone debug branch: git clone -b debug https://github.com/pyinstaller/pyinstaller.git
    - see README.rst for information on how to install PyInstaller


Infos regarding reST
====================
`Sphinx Example <https://pythonhosted.org/an_example_pypi_project/sphinx.html>`_

`reST Cheat Sheet <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_
