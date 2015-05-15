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

import os.path
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import QKeyEvent
import oPB
from oPB.core.tools import Helper, LogMixin
from oPB.ui.ui import StartupDialogBase, StartupDialogUI


translate = QtCore.QCoreApplication.translate


class StartupDialog(StartupDialogBase, StartupDialogUI, LogMixin):

    def __init__(self, parent):
        """
        Constructor for startup splash

        :param parent: parent window for startup splash dialog
        :return:
        """
        StartupDialogBase.__init__(self, parent, QtCore.Qt.ApplicationModal | QtCore.Qt.SplashScreen | QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)

        self._parent = parent
        print("gui/StartupWin parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None

        # assign slots
        self.btnStartNew.clicked.connect(self._parent.new_project)
        self.btnStartOpen.clicked.connect(self._parent.open_project)
        self.btnStartExit.clicked.connect(self._parent.close)
        self.btnStartSettings.clicked.connect(self._parent.settingsCtr.ui.exec)

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
    def hide_me(self):
        self.logger.debug("Hide startup window")
        self.close()
        self._parent.centralWidget().setEnabled(True)
        self._parent.oPB_menu.setEnabled(True)
        self._parent.activateWindow()

    @pyqtSlot()
    def show_me(self):
        self.logger.debug("Show startup window")
        self.set_position()
        self._parent.centralWidget().setEnabled(False)
        self._parent.oPB_menu.setEnabled(False)
        self.show()
        self.activateWindow()

    @pyqtSlot()
    def set_position(self):
        parentUi = self._parent.geometry()
        mysize = self.geometry()
        hpos = parentUi.x() + ((parentUi.width() - mysize.width()) / 2)
        vpos = parentUi.y() + ((parentUi.height() - mysize.height()) / 2)
        self.move(hpos, vpos)

