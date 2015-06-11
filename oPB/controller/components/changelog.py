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
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

import oPB
from oPB.core.datadefinition import ChangelogEntry, changelog_footer
from oPB.gui.changelog import ChangelogEditorDialogExtended, ChangelogEditorDialogSmall
from oPB.core.tools import Helper, LogMixin
from oPB.core.confighandler import ConfigHandler

translate = QtCore.QCoreApplication.translate


class ChangelogEditorComponent(QObject, LogMixin):

    modelDataUpdated = pyqtSignal()    # send after model or backend data has been updated
    changelogClosed = pyqtSignal()    # send after model or backend data has been updated

    def __init__(self, parent):
        """
        Initiate changelog editing

        Signals
        * changelogClosed

        :param parent: parent window
        :return:
        """
        super().__init__(parent)
        self._parent = parent
        print("controller/ChangelogComponent parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None

        self.logger.debug("Initialize changelog editor")

        self.model = None              # data models

        self.datamapper = None             # QDataWidgetMapper object for field mapping
        self._modelDataChanged = False  # is connect via model_data_changed function to itemChanged Signal of QStandardItemModel, will be reset in close_project()

        self.generate_model()

        # create main window and logic
        if ConfigHandler.cfg.use_extended_changelog == "True":
            self.ui = ChangelogEditorDialogExtended(self)
        else:
            self.ui = ChangelogEditorDialogSmall(self)

        self.connect_signals()

        # some inititalization for extended editor
        self.update_table_model(self.model, self._parent.controlData.changelog_gettable()) if ConfigHandler.cfg.use_extended_changelog == "True" else None

    def generate_model(self):
        self.logger.debug("Dispatch configuration model generation")
        if ConfigHandler.cfg.use_extended_changelog == "True":
            self.generate_extended_model()
        else:
            self.generate_simple_model()

    def generate_simple_model(self):
        self.logger.debug("Generate simple configuration model")
        self.model = QtGui.QStandardItemModel(self)
        self.model.setItem(0, 0, QtGui.QStandardItem(self._parent.controlData.changelog))

    def generate_extended_model(self):
        self.logger.debug("Generate extended configuration model")
        self.model = QtGui.QStandardItemModel(0, 4, self)
        self.retranslateMsg()

    def connect_signals(self):
        self.logger.debug("Connect signals")
        self.model.itemChanged.connect(self.model_data_changed)
        self.model.rowsRemoved.connect(self.model_data_changed)
        self.model.rowsInserted.connect(self.model_data_changed)

    def update_backend_data(self):
        self.logger.debug("Update backend data")
        if ConfigHandler.cfg.use_extended_changelog == "True":
            entries = []
            for row in range(0, self.model.rowCount(), 1):
                entry = ChangelogEntry(self.model.item(row, 0).text())
                entry.version = self.model.item(row, 1).text()
                entry.status = self.model.item(row, 2).text()
                entry.urgency = self.model.item(row, 3).text()
                entry.text = self.model.item(row, 4).text()
                entries.append(entry)
            self._parent.controlData.changelog = entries
        else:
            self._parent.controlData.changelog = self.model.item(0, 0).text()

    def close_dialog(self):
        """Close changelog editor"""
        ignoreChanges = True
        if self._modelDataChanged == True:
            try:
                self.update_backend_data()
            except:
                self.logger.error("Error while updating backend data, check for erroneous changelog entries.")
                self._parent.msgbox(translate("changelogController", "Error in changelog data, check for erroneous changelog entries or use simple editor mode."), oPB.MsgEnum.MS_ERR)
                ignoreChanges = True

        if ignoreChanges:
            self.logger.debug("Close changelog editor")
            self.ui.close()
            self.logger.debug("Emit signal changelogClosed")
            self.changelogClosed.emit()

    def update_table_model(self, model, data):
        """
        Remove all rows from given tabel model and rebuild with new data
        from backend object.

        :param model: QtStandardItemModel as QTableView model
        :param data: list with data rows
        :return:
        """
        self.logger.debug("Update table model data")
        model.itemChanged.disconnect(self.model_data_changed)
        items = model.rowCount()
        for i in range(items, -1, -1):
            model.removeRow(i)
        for elem in data:
            row = []
            for val in elem:
                if type(val) == list:
                    val = ', '.join(map(str, val))  # connect elements to a single comma-separated string
                item = QtGui.QStandardItem(val)
                item.setEditable(False)
                row.append(item)
            model.appendRow(row)
        model.itemChanged.connect(self.model_data_changed)

        # emit signal
        self.logger.debug("Emit signal modelDataUpdated")
        self.modelDataUpdated.emit()

    @pyqtSlot()
    def model_data_changed(self):
        """Update model changed marker"""
        self.logger.debug("Model data changed received")
        self._modelDataChanged = True

    def add_entry(self):
        values = [
            self._parent.controlData.id,
            "(" + self._parent.controlData.productversion + "-" + self._parent.controlData.packageversion + ")",
            oPB.CHLOG_STATI[0],
            oPB.CHLOG_BLOCKMARKER + oPB.CHLOG_URGENCIES[0],
            "\n" + translate("changelogController", "Please add a short description.") + changelog_footer()
            ]
        row = []
        for val in values:
            item = QtGui.QStandardItem(val)
            item.setEditable(False)
            row.append(item)
        self.model.insertRow(0, row)


    def remove_entry(self, idx):
        if self.model.rowCount() == 1:
            self._parent.msgbox(translate("changelogController", "Last entry can't be deleted!"), oPB.MsgEnum.MS_WARN)
        else:
            self.model.removeRow(idx)

    def retranslateMsg(self):
        self.logger.debug("Retranslating further messages...")
        """Retranslate model headers, will be called via changeEvent of self.ui """
        self.model.setHorizontalHeaderLabels([translate("changelogController", "product id"),
                                              translate("changelogController", "version"),
                                              translate("changelogController", "status"),
                                              translate("changelogController", "urgency")]
                                             )
