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
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.Qt import QKeyEvent
import oPB
from oPB.core.tools import Helper, LogMixin
from oPB.ui.ui import ChangelogEditorDialogExtendedBase,ChangelogEditorDialogSimpleBase, \
    ChangelogEditorDialogExtendedUI, ChangelogEditorDialogSimpleUI


translate = QtCore.QCoreApplication.translate


class ChangelogEditorDialog(LogMixin):

    def __init__(self, parent, base, ui):
        """
        Constructor for settings dialog

        :param parent: parent window for settings dialog
        :return:
        """
        base.__init__(self, parent._parent.ui, QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinMaxButtonsHint)
        self.setupUi(self)

        self._parent = parent
        print("gui/Changelog parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None
        print("gui/Changelog parent._parent.ui: ", self._parent._parent.ui) if oPB.PRINTHIER else None

        self.datamapper = None
        self.model = self._parent.model

        self.create_datamapper()
        self.connect_signals()

    def create_datamapper(self):
        pass

    def connect_signals(self):
        pass

    def keyPressEvent(self, evt: QKeyEvent):
        """
        Ignore escape key event, because it would close startup window.
        Any other key will be passed to the super class key event handler for further
        processing.

        :param evt: key event
        :return:
        """
        if evt.key() == QtCore.Qt.Key_Escape:
            self._parent.close_dialog()
        else:
            super().keyPressEvent(evt)


class ChangelogEditorDialogExtended(ChangelogEditorDialog, ChangelogEditorDialogExtendedBase, ChangelogEditorDialogExtendedUI):

    def __init__(self, parent):
        """
        Constructor for extended changelog editor

        :param parent: parent window
        :return:
        """
        super().__init__(parent, ChangelogEditorDialogExtendedBase, ChangelogEditorDialogExtendedUI)
        print("gui/ChangelogEditorExtended parent: ", parent, " -> self: ", self) if oPB.PRINTHIER else None

    def create_datamapper(self):
        self.logger.debug("Create data widget mapper")
        self.datamapper = QDataWidgetMapper(self)
        # self.datamapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.datamapper.setModel(self._parent.model)
        #self.datamapper.addMapping(self.ui.lblHeader, 0, "text")
        self.datamapper.addMapping(self.cmbStatus, 2)
        self.datamapper.addMapping(self.cmbUrgency, 3)
        self.datamapper.addMapping(self.editDetail, 4)
        self.datamapper.toFirst()

    def connect_signals(self):
        self.tblEntries.setModel(self.model)

        self.btnAdd.clicked.connect(self._parent.add_entry)
        self.btnSubmit.clicked.connect(self.datamapper.submit)
        self.btnDelete.clicked.connect(lambda a: self._parent.remove_entry(self.tblEntries.selectionModel().currentIndex().row()))
        self.btnClose.clicked.connect(self._parent.close_dialog)

        selectionModel = self.tblEntries.selectionModel()
        selectionModel.selectionChanged.connect(self.datamapper.submit)
        selectionModel.selectionChanged.connect(self.update_fields)

        self._parent.modelDataUpdated.connect(self.reset_datamapper_and_display)

    @pyqtSlot()
    def reset_datamapper_and_display(self):
        # select first row in mapped model
        self.logger.debug("Reset datamapper and display")

        self.datamapper.toFirst()
        self.tblEntries.setColumnHidden(4, True) # hide main text, will be shown in edit field
        self.tblEntries.selectRow(0)
        self.tblEntries.resizeRowsToContents()
        self.tblEntries.resizeColumnsToContents()

    @pyqtSlot(QtCore.QItemSelection)
    def update_fields(self, idx:QtCore.QItemSelection):
        # indexes() returns list of selected items
        # as we only have 1 at a time, return first item and get corresponding row number
        if not idx.indexes() == []:
            row = idx.indexes()[0].row()
            self.datamapper.setCurrentIndex(row)
            self.lblHeader.setText(self.model.item(row, 0).text() + " " +
                                      self.model.item(row, 1).text())
        else:
            self.datamapper.toFirst()


class ChangelogEditorDialogSmall(ChangelogEditorDialog, ChangelogEditorDialogSimpleBase, ChangelogEditorDialogSimpleUI):

    def __init__(self, parent: QMainWindow):
        """
        Constructor for small changelog editor

        :param parent: parent window
        :return:
        """
        super().__init__(parent, ChangelogEditorDialogSimpleBase, ChangelogEditorDialogSimpleUI)
        print("gui/ChangelogEditorSmall parent: ", parent, " -> self: ", self) if oPB.PRINTHIER else None

    def create_datamapper(self):
        self.logger.debug("Create data widget mapper")
        self.datamapper = QDataWidgetMapper(self)
        self.datamapper.setModel(self._parent.model)
        self.datamapper.addMapping(self.editChangelog, 0)
        self.datamapper.toFirst()

    def connect_signals(self):
        self.btnClose.clicked.connect(self._parent.close_dialog)
