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

import os
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.Qt import QKeyEvent
import oPB
from oPB.core.tools import Helper, LogMixin
from oPB.ui.ui import BundleDialogBase, BundleDialogUI


translate = QtCore.QCoreApplication.translate


class BundleDialog(BundleDialogBase, BundleDialogUI, LogMixin):

    def __init__(self, parent):
        """
        Constructor for settings dialog

        :param parent: parent controller instance
        :return:
        """
        self._parent = parent
        self._parentUi = parent._parent.ui

        BundleDialogBase.__init__(self, self._parentUi, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)

        print("gui/BundleDialog parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None

        self.model = None

        self.assign_model(self._parent.model_products)

    def keyPressEvent(self, evt: QKeyEvent):
        """
        Ignore escape key event, because it would close startup window.
        Any other key will be passed to the super class key event handler for further
        processing.

        :param evt: key event
        :return:
        """
        if evt.key() == QtCore.Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(evt)
        pass

    def assign_model(self, model):
        self.model = model
        self.tblProducts.setModel(self.model)
        self.resizeTable()

    def resizeTable(self):
        self.tblProducts.resizeRowsToContents()
        self.tblProducts.resizeColumnsToContents()
