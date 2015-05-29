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

from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.Qt import QKeyEvent
import oPB
from oPB.core.tools import Helper, LogMixin
from oPB.ui.ui import JobListDialogUI, JobCreatorDialogUI, JobListDialogBase, JobCreatorDialogBase


translate = QtCore.QCoreApplication.translate


class JobListDialog(JobListDialogBase, JobListDialogUI, LogMixin):

    def __init__(self, parent):
        """
        Constructor for settings dialog

        :param parent: parent controller instance
        :return:
        """
        self._parent = parent

        JobListDialogBase.__init__(self, self._parent, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)

        print("\tgui/JobListDialog parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None

        self.model = None

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
        self.tblJobs.setModel(self.model)
        self.resizeTable()

    def resizeTable(self):
        self.tblJobs.resizeRowsToContents()
        self.tblJobs.resizeColumnsToContents()
        self.tblJobs.sortByColumn(5, QtCore.Qt.AscendingOrder)

class JobCreatorDialog(JobCreatorDialogBase, JobCreatorDialogUI, LogMixin):

    def __init__(self, parent):
        """
        Constructor for settings dialog

        :param parent: parent controller instance
        :return:
        """
        self._parent = parent

        JobCreatorDialogBase.__init__(self, self._parent, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)

        print("\tgui/JobCreatorDialog parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None

        self.model_clients = None
        self.model_products = None

        self.dateSelector.setSelectedDate(datetime.now().date())
        self.timeSelector.setTime(datetime.now().time())

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

    def assign_model(self, model_clients, model_products):
        self.model_clients = model_clients
        self.model_products = model_products
        self.tblClients.setModel(self.model_clients)
        self.tblProducts.setModel(self.model_products)

    def resizeTableClients(self):
        self.tblClients.resizeRowsToContents()
        self.tblClients.resizeColumnsToContents()

    def resizeTableProducts(self):
        self.tblProducts.resizeRowsToContents()
        self.tblProducts.resizeColumnsToContents()