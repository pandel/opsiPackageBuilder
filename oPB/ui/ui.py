#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This module is part of the opsi PackageBuilder
see: https://forum.opsi.org/viewforum.php?f=22

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use, 
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software 
is furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

__author__ = 'Holger Pandel'
__copyright__ = "Copyright 2013-2015, Holger Pandel"
__license__ = "MIT"
__maintainer__ = "Holger Pandel"
__email__ = "holger.pandel@googlemail.com"
__status__ = "Production"

"""Pre-define every UI component to be used in oPB.gui classes"""

import os
import sys
import platform
from PyQt5 import QtCore, uic

translate = QtCore.QCoreApplication.translate

if platform.system() =="Darwin" and getattr(sys, 'frozen', False):
    path = __file__
    while not path.endswith('.app'):
        path = os.path.dirname(path)
    path = os.path.join(path,"Contents/Resources/oPB/ui")
    #base = os.environ['RESOURCEPATH']
    #path = os.path.join(base, 'oPB/ui')
    sys.path.append(path)
    #from oPB.ui import opsipackagebuilder_rc as opsipackagebuilder_rc
else:
    # get the directory of this script
    path = os.path.dirname(os.path.abspath(__file__))


MainWindowUI, MainWindowBase = uic.loadUiType(os.path.join(path, 'mainwindow.ui'))
ChangelogEditorDialogExtendedUI, ChangelogEditorDialogExtendedBase = uic.loadUiType(os.path.join(path, 'changelogeditorextended.ui'))
ChangelogEditorDialogSimpleUI, ChangelogEditorDialogSimpleBase = uic.loadUiType(os.path.join(path, 'changelogeditorsimple.ui'))
SettingsDialogUI, SettingsDialogBase = uic.loadUiType(os.path.join(path, 'settings.ui'))
ScriptTreeDialogUI, ScriptTreeDialogBase = uic.loadUiType(os.path.join(path, 'scripttree.ui'))
StartupDialogUI, StartupDialogBase = uic.loadUiType(os.path.join(path, 'startup.ui'))
LogDialogUI, LogDialogBase = uic.loadUiType(os.path.join(path, 'log.ui'))
UninstallDialogUI, UninstallDialogBase = uic.loadUiType(os.path.join(path, 'quickuninstall.ui'))
JobListDialogUI, JobListDialogBase = uic.loadUiType(os.path.join(path, 'joblist.ui'))
JobCreatorDialogUI, JobCreatorDialogBase = uic.loadUiType(os.path.join(path, 'jobcreatortree.ui'))
BundleDialogUI, BundleDialogBase = uic.loadUiType(os.path.join(path, 'bundle.ui'))
DeployAgentDialogUI, DeployAgentDialogBase = uic.loadUiType(os.path.join(path, 'deployagent.ui'))
DepotManagerDialogUI, DepotManagerDialogBase = uic.loadUiType(os.path.join(path, 'depotmanager.ui'))
ReportSelectorDialogUI, ReportSelectorDialogBase = uic.loadUiType(os.path.join(path, 'reportselector.ui'))
LockedProductsDialogUI, LockedProductsDialogBase = uic.loadUiType(os.path.join(path, 'lockedproducts.ui'))

"""
Example:
from PyQt4 import QtCore, QtGui, uic


MainWindowUI, MainWindowBase = uic.loadUiType(
    os.path.join(path, 'mainwindow.ui'))

LandingPageUI, LandingPageBase = uic.loadUiType(
    os.path.join(path, 'landing.ui'))

class MainWindow(MainWindowBase, MainWindowUI):
    def __init__(self, parent=None):
        MainWindowBase.__init__(self, parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.handleButton)

    def handleButton(self):
        # keep a reference to the landing page
        self.landing = LandingPage()
        self.landing.show()

class LandingPage(LandingPageBase, LandingPageUI):
    def __init__(self, parent=None):
        LandingPageBase.__init__(self, parent)
        self.setupUi(self)
"""