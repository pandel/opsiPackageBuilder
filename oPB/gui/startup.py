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

import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import QKeyEvent
import oPB
from oPB.core.tools import LogMixin
from oPB.gui.utilities import EventMixin
from oPB.ui.ui import StartupDialogBase, StartupDialogUI

# X11 seems to handle SplashScreen a little different
if sys.platform.lower() == "linux":
    winAttribs = QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint
else:
    winAttribs = QtCore.Qt.SplashScreen | QtCore.Qt.FramelessWindowHint

translate = QtCore.QCoreApplication.translate

class StartupDialog(StartupDialogBase, StartupDialogUI, LogMixin, EventMixin):

    def __init__(self, parent):
        """
        Constructor for startup splash

        :param parent: parent window for startup splash dialog
        :return:
        """
        self._parent = parent
        self._parentUi = parent.ui

        #StartupDialogBase.__init__(self, self._parentUi, QtCore.Qt.SplashScreen | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint)
        StartupDialogBase.__init__(self, self._parentUi, winAttribs)
        self.setupUi(self)
        self.setWindowIcon(self._parentUi.windowIcon())

        print("\tgui/StartupWin parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None
        print("\tgui/StartupWin parentUi: ", self._parentUi, " -> self: ", self) if oPB.PRINTHIER else None

        self.menuRecent = QMenu()

        btnGrp = [self.btnStartNew,
        self.btnStartOpen,
        self.btnStartSettings,
        self.btnStartRecent,
        self.btnStartShowLog,
        self.btnStartExit,
        self.btnStartBundle,
        self.btnStartDepotMgmt,
        self.btnStartJobSched,
        self.btnStartInstall,
        self.btnStartUpload,
        self.btnStartUninstall,
        self.btnStartDeploy,
        self.btnStartImport,
        self.btnStartBundle,
        self.btnStartDepotMgmt,
        self.btnStartJobSched,
        self.btnStartInstall,
        self.btnStartUpload,
        self.btnStartUninstall,
        self.btnStartDeploy,
        self.btnStartImport]
        
        for btn in btnGrp:
            btn.setProperty("startbtn", "set")
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()

        self.connect_signals()

    def connect_signals(self):
        # assign slots to actions and indiv. methods
        self.btnStartNew.clicked.connect(self._parentUi.actionNew.triggered)
        self.btnStartOpen.clicked.connect(self._parentUi.actionOpen.triggered)

        self.btnStartSettings.clicked.connect(self._parentUi.actionSettings.triggered)
        self.btnStartRecent.setMenu(self.menuRecent)
        self.btnStartShowLog.clicked.connect(self._parentUi.actionShowLog.triggered)
        self.btnStartExit.clicked.connect(self._parentUi.close)
        self._parentUi.windowMoved.connect(self.set_position)

        if oPB.NETMODE != "offline":
            self.btnStartBundle.clicked.connect(self._parentUi.actionBundleCreation.triggered)
            self.btnStartDepotMgmt.clicked.connect(self._parentUi.actionDepotManager.triggered)
            self.btnStartJobSched.clicked.connect(self._parentUi.actionScheduler.triggered)
            self.btnStartInstall.clicked.connect(self._parentUi.actionInstall.triggered)
            self.btnStartUpload.clicked.connect(self._parentUi.actionUpload.triggered)
            self.btnStartUninstall.clicked.connect(self._parentUi.actionUninstall.triggered)
            self.btnStartUnlock.clicked.connect(self._parentUi.actionLockedProducts.triggered)
            self.btnStartDeploy.clicked.connect(self._parentUi.actionDeploy.triggered)
            self.btnStartImport.clicked.connect(self._parentUi.actionImport.triggered)
        else:
            self.gBoxMiddle.setVisible(False)
            self.btnStartBundle.setVisible(False)
            self.btnStartDepotMgmt.setVisible(False)
            self.btnStartJobSched.setVisible(False)
            self.btnStartInstall.setVisible(False)
            self.btnStartUpload.setVisible(False)
            self.btnStartUninstall.setVisible(False)
            self.btnStartUnlock.setVisible(False)
            self.btnStartDeploy.setVisible(False)
            self.btnStartImport.setVisible(False)

    def keyPressEvent(self, evt: QKeyEvent):
        """
        Ignore escape key event, because it would close startup window.
        Any other key will be passed to the super class key event handler for further
        processing.

        :param evt: key event
        :return:
        """
        if evt.key() == QtCore.Qt.Key_Escape:
            pass
        else:
            super().keyPressEvent(evt)

    def closeEvent(self, event:QtCore.QEvent):
        """Disable closeEvent for Alt+F4"""
        event.setAccepted(not event.spontaneous())

    @pyqtSlot()
    def hide_(self):
        """Overrides standard hide() method, check for active_project state before"""
        if not self._parent._active_project:
            self.logger.debug("Temporarily hide startup window")
            self.hide()

    @pyqtSlot()
    def hide_me(self):
        """Hides startup window and reactivates main window functionality."""
        self.logger.debug("Hide startup window and activate main")
        self.close()
        self._parentUi.centralWidget().setEnabled(True)
        self._parentUi.oPB_menu.setEnabled(True)
        self._parentUi.activateWindow()

    @pyqtSlot()
    def show_(self):
        """Overrides standard show() method, check for active_project state before"""
        if not self._parent._active_project:
            self.logger.debug("Show temporarily hidden startup window")
            self.show()

    @pyqtSlot()
    def show_me(self):
        """Showes startup window and deactivates main window functionality."""
        self.logger.debug("Show startup window and deactivate main")
        self.set_position()
        self._parentUi.centralWidget().setEnabled(False)
        self._parentUi.oPB_menu.setEnabled(False)
        self.show()
        self.activateWindow()

    @pyqtSlot()
    def set_position(self):
        parentUi = self._parentUi.geometry()
        mysize = self.geometry()
        hpos = int(parentUi.x() + ((parentUi.width() - mysize.width()) / 2))
        vpos = int(parentUi.y() + ((parentUi.height() - mysize.height()) / 2))
        self.move(hpos, vpos)
