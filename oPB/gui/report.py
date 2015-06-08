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
from PyQt5.QtPrintSupport import QPrintPreviewDialog, QPrinter
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtGui import QKeyEvent

import oPB
from oPB.core.tools import HTMLTools, LogMixin
from oPB.gui.depotmanager import translate
from oPB.gui.splash import Splash
from oPB.ui.ui import ReportSelectorDialogBase, ReportSelectorDialogUI

translate = QtCore.QCoreApplication.translate


class ReportSelectorDialog(ReportSelectorDialogBase, ReportSelectorDialogUI, LogMixin):

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

        self.model_left = None
        self.model_right = None

        self.assign_model(self._parent.model_report, self._parent.model_report)
        self.connect_signals()

    def connect_signals(self):
        self.btnSelAll.clicked.connect(lambda: self.select(True))
        self.btnSelNone.clicked.connect(lambda: self.select(False))
        self.btnGenerate.clicked.connect(self.generate_report)

    def show_(self):
        self.logger.debug("Open report selector")

        self.dialogOpened.emit()

        self.btnSelNone.setVisible(False)
        self.show()
        self._parent.update_reportmodel_data()

        self.resizeTables()
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

    def select(self, all):
        if all:
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

    def showReport(self, html):
        self.logger.debug("Show HTML report")

        # base dialog widget
        ui = QDialog(self, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCloseButtonHint )
        vertLayout = QVBoxLayout()

        # print button
        print = QPushButton()
        print.setText(translate("ReportDialog", "Print"))
        print.setMaximumWidth(100)

        # webview for help information
        wv = QWebView()

        # build structure
        vertLayout.addWidget(print)
        vertLayout.addWidget(wv)

        ui.setLayout(vertLayout)

        print.clicked.connect(lambda: wv.print_(QPrinter()))
        wv.setHtml(html)

        ui.show()

    def generate_report(self):
        self.logger.debug("Generate HTML report")
        left = ""
        time = ""
        html = ""

        if self.rdDepot.isChecked():
            modus = "depot"
        else:
            modus = "repo"

        server_left = self.tblSrvLeft.selectionModel().model().item(
            self.tblSrvLeft.selectionModel().selectedRows()[0].row(),
            0).text()
        slave = self.tblSrvRight.selectionModel().selectedRows()

        steps = 1 + len(slave)
        step = 100 / steps

        self.splash.incProgress(step)

        if modus == "depot":
            html = HTMLTools.HTMLHeader(translate("depotManagerController", "Compare depots:") + " " + server_left + " / " + str(datetime.now()),
                                        "#ffffff", "#F0F9FF", "#007EE5", "#000000", "#ffffff")
            data_left = self.get_prodlist_to_server(server_left, self._parent.productsondepotslist)
        else:
            html = HTMLTools.HTMLHeader(translate("depotManagerController", "Compare repositories:") + " " + server_left + " / " + str(datetime.now()),
                                        "#ffffff", "#F0F9FF", "#007EE5", "#000000", "#ffffff")
            data_left = self.trim_prodlist_to_server(self._parent.do_getrepocontent(dest = server_left))

        for row in slave:
            self.splash.incProgress(step)
            server_right = self.tblSrvRight.selectionModel().model().item(row.row(), 0).text()
            if modus == "depot":
                data_right = self.get_prodlist_to_server(server_right, self._parent.productsondepotslist)
            else:
                data_right = self.trim_prodlist_to_server(self._parent.do_getrepocontent(dest = server_right))

            tmp = self.compare(data_left, data_right)
            tmp.insert(0, ["Depot (Ref): " + server_left, "Depot: " + server_right])

            if tmp:
                html += HTMLTools.Array2HTMLTable(tmp, '', "#ffffff", "#F0F9FF", "#007EE5", "#000000", "#ffffff", True, True)

        html += HTMLTools.HTMLFooter()

        self.splash.close()

        self.showReport(html)

    def trim_prodlist_to_server(self, repolist):
        self.logger.debug("Return product list to server via list")
        ret = []

        for elem in repolist:
            d = elem.split(";")
            ret.append(d[0] + "_" + d[2] + "-" + d[3] + "(" + d[1] + ")")

        return ret

    def get_prodlist_to_server(self, depot, dict_):
        self.logger.debug("Return product list to server vua dict")

        tmplist = []
        prodlist = []
        if dict_:
            for elem in dict_:
                d = elem.split(";")
                if d[4] == depot:
                    #prodlist.append((";").join([d[0], "", d[2],d[3]]))
                    #tmplist.append([d[0], d[2], d[3]])    # [['mysql.workbench', '6.2.4', 'go1'],...]
                    tmplist.append(d[0] + "_" + d[2] + "-" + d[3])    # [['mysql.workbench', '6.2.4', 'go1'],...]
        return tmplist

    @pyqtSlot()
    def compare(self, data_left, data_right, modus = "depot"):
        self.logger.debug("Comparing sides")

        uniqueLeft = [item for item in data_left if item not in data_right]
        uniqueRight = [item for item in data_right if item not in data_left]

        zipped = zip_longest(uniqueLeft, uniqueRight)
        ret = []

        try:
            for elem in zipped:
                ret.append([elem[0], elem[1] if elem[1] is not None else ''])
        except:
            pass

        if len(ret) == 0:
            ret.append(["(no differences found)", ""])

        return ret
