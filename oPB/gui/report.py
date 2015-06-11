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
from itertools import zip_longest

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtGui import QKeyEvent

import oPB
from oPB.core.tools import HTMLTools, LogMixin
from oPB.gui.depotmanager import translate
from oPB.gui.splash import Splash
from oPB.gui.utilities import HtmlDialog, EventMixin
from oPB.ui.ui import ReportSelectorDialogBase, ReportSelectorDialogUI

translate = QtCore.QCoreApplication.translate


class ReportSelectorDialog(ReportSelectorDialogBase, ReportSelectorDialogUI, LogMixin, EventMixin):

    dialogOpened = pyqtSignal()
    dialogClosed = pyqtSignal()

    def __init__(self, parent):
        """
        Constructor for settings dialog

        :param parent: parent controller instance
        :return:
        """
        self._parent = parent
        self._parentUi = parent._parent.ui

        ReportSelectorDialogBase.__init__(self, self._parentUi, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)

        print("\tgui/ReportSelectorDialog parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None
        print("\tgui/ReportSelectorDialog parentUi: ", self._parentUi, " -> self: ", self) if oPB.PRINTHIER else None

        self.splash = Splash(self, translate("MainWindow", "Please wait..."))
        self.viewer = HtmlDialog(self)

        self.model_left = None
        self.model_right = None

        self.assign_model(self._parent.model_report, self._parent.model_report)
        self.connect_signals()

    def connect_signals(self):
        self.btnSelAll.clicked.connect(lambda: self.select(True))
        self.btnSelNone.clicked.connect(lambda: self.select(False))
        self.btnGenerate.clicked.connect(self.generate_report)
        self._parent.modelDataUpdated.connect(self.splash.close)

    def show_(self):
        """Open report selector dialog and update values"""
        self.logger.debug("Open report selector")

        self.dialogOpened.emit()

        self.btnSelNone.setVisible(False)
        self.show()
        self._parent.update_reportmodel_data()

        self.resizeTables()
        self.select(None)
        self.activateWindow()

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

    def assign_model(self, model_left, model_right):
        self.logger.debug("Assign data model")
        self.model_left = model_left
        self.model_right = model_right
        self.tblSrvLeft.setModel(self.model_left)
        self.tblSrvRight.setModel(self.model_right)
        self.resizeTables()

    def resizeTables(self):
        self.resizeLeft()
        self.resizeRight()

    def resizeLeft(self):
        self.tblSrvLeft.resizeRowsToContents()
        self.tblSrvLeft.resizeColumnsToContents()

    def resizeRight(self):
        self.tblSrvRight.resizeRowsToContents()
        self.tblSrvRight.resizeColumnsToContents()

    def select(self, all_: bool):
        """
        Select / Unselect every row in tableview

        :param all_: True = select all / False = select nothing
        :return:
        """
        if all_:
            self.btnSelAll.setVisible(False)
            self.btnSelNone.setVisible(True)
            for row in range(self.tblSrvRight.selectionModel().model().rowCount()):
                for col in [0, 1]:
                    idx = self.tblSrvRight.selectionModel().model().indexFromItem(
                        self.tblSrvRight.selectionModel().model().item(row,col)
                    )
                    self.tblSrvRight.selectionModel().select(idx, QtCore.QItemSelectionModel.Select)
        else:
            self.btnSelAll.setVisible(True)
            self.btnSelNone.setVisible(False)
            self.tblSrvRight.selectionModel().clearSelection()

    def generate_report(self):
        """
        Generate HTML comparison report

        :return:
        """
        self.logger.debug("Generate HTML report")
        left = ""
        time = ""
        html = ""

        if self.rdDepot.isChecked():
            modus = "depot"
        else:
            modus = "repo"

        try:
            self.logger.debug("Getting reference server from left tableview")
            server_left = self.tblSrvLeft.selectionModel().model().item(
                self.tblSrvLeft.selectionModel().selectedRows()[0].row(),
                0).text()
        except:
            self.logger.debug("No reference server selected.")
            return

        self.logger.debug("Getting list of server to compare to from right tableview")
        slave = self.tblSrvRight.selectionModel().selectedRows()
        if not slave:
            self.logger.debug("Nothing to compare to selected.")
            return

        steps = 1 + len(slave)
        step = 100 / steps

        self.splash.incProgress(step)

        if modus == "depot":
            self.logger.debug("Depot comparison modus")
            html = HTMLTools.HTMLHeader(translate("depotManagerController", "Compare depots:") + " " + server_left + " / " + str(datetime.now()),
                                        "#ffffff", "#F0F9FF", "#007EE5", "#000000", "#ffffff")
            data_left = self.get_prodlist_to_server(server_left, self._parent.productsondepotslist)
        else:
            self.logger.debug("Repository comparison modus")
            html = HTMLTools.HTMLHeader(translate("depotManagerController", "Compare repositories:") + " " + server_left + " / " + str(datetime.now()),
                                        "#ffffff", "#F0F9FF", "#007EE5", "#000000", "#ffffff")
            data_left = self.get_repolist_to_server(self._parent.do_getrepocontent(dest = server_left))

        self.logger.debug("Processing server list...")
        for row in slave:
            self.splash.incProgress(step)
            server_right = self.tblSrvRight.selectionModel().model().item(row.row(), 0).text()
            self.logger.debug("Processing server: " + server_right)
            if modus == "depot":
                data_right = self.get_prodlist_to_server(server_right, self._parent.productsondepotslist)
            else:
                data_right = self.get_repolist_to_server(self._parent.do_getrepocontent(dest = server_right))

            tmp = self.compare(data_left, data_right, tablefill="")
            if tmp:
                colspan = len(tmp[0]) / 2
            else:
                tmp = []
                colspan = 1

            tmp.insert(0, [translate("depotManagerController", "Reference:") + " " + server_left, "Depot: " + server_right])

            if tmp:
                html += HTMLTools.Array2HTMLTable(element_list = tmp, colspan = colspan, title = '', bodybgcolor = "#ffffff", hightlightbgcolor = "#F0F9FF",
                                                  headerbgcolor = "#007EE5", bodytxtcolor = "#000000", headertxtcolor = "#ffffff", headers_on = True, only_table = True)

        html += HTMLTools.HTMLFooter()

        self.splash.close()

        self.viewer.showHtml(html)

    def get_repolist_to_server(self, repolist):
        """
        Turn raw repository product list into comparable list format

        :param repolist: raw list of products in repository

        :return: list of products
        """
        self.logger.debug("Return product list to server via list")
        ret = []

        for elem in repolist:
            d = elem.split(";")
            ret.append([d[0], d[2] + "-" + d[3], d[1]])  # [['mysql.workbench, '6.2.4-go1', 456453de782...],...]

        return ret

    def get_prodlist_to_server(self, depot, dict_):
        """
        Evalute products to named depot server from server-product dictionary.

        :param depot: depotserver name
        :param dict_: server-product dictionary
        :return: list of products
        """
        self.logger.debug("Return product list to server via dict")

        tmplist = []
        if dict_:
            for elem in dict_:
                d = elem.split(";")
                if d[4] == depot:
                    tmplist.append([d[0], d[2] + "-" + d[3]])    # [['mysql.workbench, '6.2.4-go1'],...]

        return tmplist

    @pyqtSlot()
    def compare(self, data_left: list, data_right: list, tablefill: str = "--"):
        """
        Compare two lists and combine them side by side.

        :param data_left: left list
        :param data_right: right list
        :param tablefill: fill empty values with ``tablefill``
        :return: combined list
        """
        self.logger.debug("Comparing sides")

        uniqueLeft = [item for item in data_left if item not in data_right]
        uniqueRight = [item for item in data_right if item not in data_left]

        try:
            maxLeft = max(len(s) for s in uniqueLeft)
        except:
            maxLeft = 0

        try:
            maxRight = max(len(s) for s in uniqueRight)
        except:
            maxRight = 0

        fillvalue = []
        if maxLeft >= maxRight:
            fillvalue.extend([tablefill] * maxLeft)
        else:
            fillvalue.extend([tablefill] * maxRight)

        zipped = zip_longest(uniqueLeft, uniqueRight, fillvalue = fillvalue)

        ret = []
        for row in zipped:
            row_zip = []
            for part in row:
                row_zip += part if part else ['']

            ret.append(row_zip)

        if len(ret) == 0:
            ret.append([translate("depotManagerController", "(no differences found)"), ""])

        return ret

    def retranslateMsg(self):
        self.logger.debug("Retranslating further messages...")
        self.splash.msg = translate("MainWindow", "Please wait...")