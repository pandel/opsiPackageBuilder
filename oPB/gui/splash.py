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

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QObject
from oPB.core.tools import LogMixin
from oPB.gui.utilities import EventMixin
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QSplashScreen, QProgressBar, qApp

translate = QtCore.QCoreApplication.translate


class Splash(QObject, LogMixin, EventMixin):
    """Splash screen class"""

    def __init__(self, parent, msg = ""):
        """
        Constructor of Splash screen

        :param parent: ui parent
        :param msg: initial message text

        """
        super().__init__()
        self._parent = parent
        self.isHidden = True
        self._progress = 0
        self._progressBar = None
        self.msg = msg

        pixmap = QtGui.QPixmap(380, 100)
        pixmap.fill(QtGui.QColor("darkgreen"))

        self._splash = QSplashScreen(pixmap)
        self._splash.setParent(self._parent)

        self.add_progressbar()

    def add_progressbar(self):
        """Add separate progress bar to splash screen"""

        self._progressBar = QProgressBar(self._splash)
        self._progressBar.setGeometry(self._splash.width() / 10, 8 * self._splash.height() / 10,
                               8 * self._splash.width() / 10, self._splash.height() / 10)
        self._progressBar.hide()

    def setProgress(self, val):
        """
        Set progress bar to ``val``

        If splash has no progressbar, it will be added dynamically.
        Remove progressbar with ``val`` as None.

        :param val: absolut percent value
        :return:
        """
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
        """
        Increase progressbar value by ``val``

        If splash has no progressbar, it will be added dynamically.
        Remove progressbar with ``val`` as None.

        :param val: value to increase by
        :return:
        """

        if val is not None:
            self._progressBar.show()
            self._progressBar.setTextVisible(True)
            self.progress = self.progress + val
            try:
                self._progressBar.setValue(self.progress)
                qApp.processEvents()
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
        """Set splash's parent"""
        self._parent = parent
        self._splash.setParent(parent)

    @pyqtSlot()
    @pyqtSlot(bool)
    def close(self, dummy = True):
        self.logger.debug("Hide splash")
        self.isHidden = True
        self._progressBar.hide()
        self._progressBar.reset()
        self._splash.close()

    @pyqtSlot()
    @pyqtSlot(str)
    def show_(self, msg = ""):

        if msg != "":
            self._splash.showMessage(msg, QtCore.Qt.AlignCenter, QtCore.Qt.white)
        else:
            self.logger.debug("Show splash, parent: " + str(self._parent))
            self._splash.showMessage(self.msg, QtCore.Qt.AlignCenter, QtCore.Qt.white)

        try:
        #if platform.system() == "Linux":
            parentUi = self._parent.centralwidget.geometry()  # need to use centralwidget for linux preferably, don't know why
        except:
        #else:
            parentUi = self._parent.childrenRect()

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