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
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QSplashScreen, QProgressBar, qApp

__author__ = 'Holger Pandel'
__copyright__ = "Copyright 2013-2015, Holger Pandel"
__license__ = "MIT"
__maintainer__ = "Holger Pandel"
__email__ = "holger.pandel@googlemail.com"
__status__ = "Production"

from PyQt5 import QtCore, QtGui
from oPB.core import *
from oPB.core.tools import Helper, LogMixin

translate = QtCore.QCoreApplication.translate


class Splash(LogMixin):
    def __init__(self, parent, msg):
        self._parent = parent
        self.isHidden = True
        self._progress = 0
        self._progressBar = None

        pixmap = QtGui.QPixmap(380, 100)
        pixmap.fill(QtGui.QColor("darkgreen"))

        self._splash = QSplashScreen(pixmap)
        self._splash.setParent(self._parent)
        self._splash.showMessage(msg, QtCore.Qt.AlignCenter, QtCore.Qt.white)

        self.add_progressbar()

    def add_progressbar(self):
        self._progressBar = QProgressBar(self._splash)
        self._progressBar.setGeometry(self._splash.width() / 10, 8 * self._splash.height() / 10,
                               8 * self._splash.width() / 10, self._splash.height() / 10)
        self._progressBar.hide()

    def setProgress(self, val):
        if val is not None:
            self._progressBar.show()
            self._progressBar.setTextVisible(True)
            self.progress = val
            try:
                self._progressBar.setValue(self.progress)
            except:
                pass
        else:
            self._progressBar.setTextVisible(False)
            self._progressBar.hide()
            self._progressBar.reset()

        if self.isHidden is True:
            self.isHidden = False
            self.show_()

    def incProgress(self, val):
        if val is not None:
            self._progressBar.show()
            self._progressBar.setTextVisible(True)
            self.progress = self.progress + val
            try:
                self._progressBar.setValue(self.progress)
            except:
                pass
        else:
            self._progressBar.setTextVisible(False)
            self._progressBar.hide()
            self._progressBar.reset()

        if self.isHidden is True:
            self.isHidden = False
            self.show_()

    def setParent(self, parent):
        self._parent = parent
        self._splash.setParent(parent)

    @pyqtSlot()
    def close(self):
        self.logger.debug("Hide splash")
        self.isHidden = True
        self._progressBar.hide()
        self._progressBar.reset()
        self._splash.close()

    @pyqtSlot()
    def show_(self):
        self.logger.debug("Show splash, parent: " + str(self._parent))
        try:
            parentUi = self._parent.centralwidget.geometry()  # need to use centralwidget for linux
        except:
            parentUi = self._parent.childrenRect()  # need to use centralwidget for linux

        mysize = self._splash.geometry()

        hpos = parentUi.x() + ((parentUi.width() - mysize.width()) / 2)
        vpos = parentUi.y() + ((parentUi.height() - mysize.height()) / 2)

        self._splash.move(hpos, vpos)
        self._splash.show()

        qApp.processEvents()

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        # create new exception handling vor properties
        # if (value != "True") and (value != "False"):
        #    raise ValueError("describe exception")
        if value > 100:
            value = 0
        if value < 0:
            value = 0
        self._progress = value