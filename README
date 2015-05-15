Included Scripts
================

(The scripts will only work under Windows!)

	- 1_update_locale.cmd: 		Re-scan source files for new(updated language strings.

	- 2_compile_resource.cmd:	Make Python file from *.qrc file

	- 3_sphinx.cmd:			Re-scan source file in-place documentation

	- 4_distrib.cmd:		Build install package via PyInstaller (NOT REALLY WORKING AT THE MOMETN)


Compiling MapDrive.dll
======================

You need to install VC++ 2010 Express and if you want to compile for a 64Bit Platform, Microsoft Windows SDK v7.1 additionally.


Using PyInstaller
=================

``Please customize the path to your preoject in opsipackagebuiler.spec!``

You need to download a Python 3 compatible version of PyInstaller from www.pyinstaller.org and install it from the source package. Before you do that, modify the file:

*pyinstaller-python3\PyInstaller\utils\hooks\hookutils.py*

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
The command "qmake -query QT_INSTALL_QML" returns the path to the qml folder, but has carriage return ("\r\n") at the end of the string under windows. This can't be handled correctly, so remove it.


Infos regarding reST
====================
`Sphinx Example <https://pythonhosted.org/an_example_pypi_project/sphinx.html>`_
`reST Cheat Sheet <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_
