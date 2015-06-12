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

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.Qt import QKeyEvent
import oPB
import oPB.gui.helpviewer
from oPB.core.tools import Helper, LogMixin
from oPB.gui.utilities import EventMixin
from oPB.ui.ui import UninstallDialogBase, UninstallDialogUI
from oPB.gui.splash import Splash


translate = QtCore.QCoreApplication.translate


class UninstallDialog(UninstallDialogBase, UninstallDialogUI, LogMixin, EventMixin):

    dialogOpened = pyqtSignal()
    dialogClosed = pyqtSignal()

    def __init__(self, parent):
        """
        Constructor for UninstallDialog dialog

        :param parent: parent controller instance
        :return:
        """
        self._parent = parent
        self._parentUi = parent._parent.ui

        UninstallDialogBase.__init__(self, self._parentUi, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)

        print("\tgui/UninstallDialog parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None
        print("\tgui/UninstallDialog parentUi: ", self._parentUi, " -> self: ", self) if oPB.PRINTHIER else None

        self.splash = Splash(self, translate("MainWindow", "Please wait..."))
        self.splash.close()  # only for linux

        self.model = None

        self.assign_model(self._parent.model_products)
        self.connect_signals()

    def connect_signals(self):
        self.dialogOpened.connect(self.update_ui)
        self.btnRefresh.clicked.connect(lambda: self.update_ui(True))
        self.btnUninstall.clicked.connect(self.uninstall)
        self.btnClose.clicked.connect(self.dialogClosed.emit)
        self.btnHelp.clicked.connect(lambda: oPB.gui.helpviewer.Help(oPB.HLP_FILE, oPB.HLP_PREFIX, oPB.HLP_DST_QUNINST))

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

    def show_(self):
        self.logger.debug("Open quick uninstall dialog")

        self.show()
        self.activateWindow()

        self.dialogOpened.emit()

    def update_ui(self, force = False):
        """
        Update model data and reset tableviews

        See: :meth:`oPB.controller.components.quickuninstall.QuickUninstallComponent.update_model_data`

        :param force: Force ui AND backend data refresh
        """
        self.logger.debug("Update UI")
        self.splash.show_()
        self._parent.update_model_data(force)
        self.resizeTable()
        self.splash.close()

    def uninstall(self):
        """
        Initiate product removal via backend

        See: :meth:`oPB.controller.components.quickuninstall.QuickUninstallComponent.uninstall_selection`
        """
        self.close()

        prods = []
        for row in self.tblProducts.selectionModel().selectedRows():
            prods.append(self.model.item(row.row(), 0).text())

        self._parent.uninstall_selection(prods)

        self.dialogClosed.emit()

    def retranslateMsg(self):
        self.logger.debug("Retranslating further messages...")
        self.splash.msg = translate("MainWindow", "Please wait...")