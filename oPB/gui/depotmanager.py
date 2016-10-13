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
pyqt qstandarditem setdata
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
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.Qt import QKeyEvent

import oPB
import oPB.gui.helpviewer
from oPB.core.tools import LogMixin
from oPB.gui.utilities import EventMixin
from oPB.core.confighandler import ConfigHandler
from oPB.ui.ui import DepotManagerDialogBase, DepotManagerDialogUI
from oPB.gui.splash import Splash

translate = QtCore.QCoreApplication.translate

class DepotManagerDialog(DepotManagerDialogBase, DepotManagerDialogUI, LogMixin, EventMixin):

    dialogOpened = pyqtSignal()
    dialogClosed = pyqtSignal()

    def __init__(self, parent):
        """
        Constructor for DepotManager dialog

        :param parent: parent controller instance
        :return:
        """
        self._parent = parent
        self._parentUi = parent._parent.ui

        DepotManagerDialogBase.__init__(self, self._parentUi, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)

        print("\tgui/DepotManagerDialog parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None
        print("\tgui/DepotManagerDialog parentUi: ", self._parentUi, " -> self: ", self) if oPB.PRINTHIER else None

        self.model_left = None
        self.model_right = None

        self.assign_model(self._parent.model_left, self._parent.model_right)

        self.splash = Splash(self, translate("MainWindow", "Please wait..."))

        self.connect_signals()

        self._parent._ui_box_left = self.cmbDepotLeft
        self._parent._ui_box_right = self.cmbDepotRight
        self._parent._ui_repobtn_left = self.btnFetchRepoLeft
        self._parent._ui_repobtn_right = self.btnFetchRepoRight

        self.update_ui()

    def connect_signals(self):
        self.finished.connect(self.dialogClosed.emit)
        self._parent.dataAboutToBeAquired.connect(self.splash.setProgress)
        self._parent.dataAquired.connect(self.update_ui)
        self._parent.dataAquired.connect(self.splash.close)

        self._parent.modelDataUpdated.connect(self.update_fields)
        self._parent.modelDataUpdated.connect(self.update_ui)

        self.btnRefresh.clicked.connect(lambda: self._parent.update_data(True))
        self.btnCompare.clicked.connect(self.compare_sides)
        self.btnShowLog.clicked.connect(self._parentUi.showLogRequested)
        self.btnReport.clicked.connect(self._parent.ui_report.show_)
        self.btnInstall.clicked.connect(self._parent.install)
        self.btnUninstall.clicked.connect(self.remove_delegate)
        self.btnUpload.clicked.connect(self._parentUi.upload)
        self.btnUnregister.clicked.connect(self._parent.unregister_depot)
        self.btnSetRights.clicked.connect(self._parent.set_rights)
        self.btnRunProdUpdater.clicked.connect(self._parent.run_product_updater)
        self.btnGenMD5.clicked.connect(self.generate_md5)
        self.btnOnlineCheck.clicked.connect(self._parent.onlinecheck)
        self.btnReboot.clicked.connect(self._parent.reboot_depot)
        self.btnPoweroff.clicked.connect(self._parent.poweroff_depot)
        self.btnHelp.clicked.connect(lambda: oPB.gui.helpviewer.Help(oPB.HLP_FILE, oPB.HLP_PREFIX, oPB.HLP_DST_DEPOTM))

        #self.cmbDepotLeft.currentTextChanged.connect(self._parent.side_content) #side_content
        #self.cmbDepotRight.currentTextChanged.connect(self._parent.side_content)
        self.cmbDepotLeft.currentTextChanged.connect(self._parent.switch_content) #side_content
        self.cmbDepotRight.currentTextChanged.connect(self._parent.switch_content)
        self.cmbDepotLeft.currentTextChanged.connect(self.set_active_side) #side_content
        self.cmbDepotRight.currentTextChanged.connect(self.set_active_side)

        self.tblDepotLeft.clicked.connect(self.set_active_side)
        self.tblDepotRight.clicked.connect(self.set_active_side)

        self.btnFetchRepoLeft.clicked.connect(self._parent.switch_content)
        self.btnFetchRepoRight.clicked.connect(self._parent.switch_content)


    def closeEvent(self, event):
        """
        Overrides base method, disconnects custom signals

        :param event: close event
        """
        try:
            self._parent.dataAboutToBeAquired.disconnect(self.splash.show_)
            self._parent.dataAquired.disconnect(self.splash.close)
        except:
            pass

        event.accept()
        self.finished.emit(0) # we have to emit this manually, because of subclassing closeEvent

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
        self.tblDepotLeft.setModel(self.model_left)
        self.tblDepotRight.setModel(self.model_right)
        self.resizeTables()

    def resizeTables(self):
        self.resizeLeft()
        self.resizeRight()

    @pyqtSlot()
    def resizeLeft(self):
        self.tblDepotLeft.resizeRowsToContents()
        self.tblDepotLeft.resizeColumnsToContents()

    def resizeRight(self):
        self.tblDepotRight.resizeRowsToContents()
        self.tblDepotRight.resizeColumnsToContents()

    @pyqtSlot()
    def update_ui(self):
        """Update ui state"""
        self.logger.debug("Update ui")

        self.resizeTables()

        # enable / disable buttons
        if self.cmbDepotLeft.currentIndex() == -1:
            self.btnFetchRepoLeft.setEnabled(False)
        else:
            self.btnFetchRepoLeft.setEnabled(True)

        if self.cmbDepotRight.currentIndex() == -1:
            self.btnFetchRepoRight.setEnabled(False)
        else:
            self.btnFetchRepoRight.setEnabled(True)

        if self.cmbDepotLeft.currentIndex() == -1 or self.cmbDepotRight.currentIndex() == -1:
            self.btnCompare.setEnabled(False)
        else:
            self.btnCompare.setEnabled(True)

        if self._parent._active_side is None:
            self.btnInstall.setEnabled(False)
            self.btnUninstall.setEnabled(False)
            self.btnUpload.setEnabled(False)
            self.btnUnregister.setEnabled(False)
            self.btnSetRights.setEnabled(False)
            self.btnRunProdUpdater.setEnabled(False)
            self.btnGenMD5.setEnabled(False)
            self.btnOnlineCheck.setEnabled(False)
            self.btnPoweroff.setEnabled(False)
            self.btnReboot.setEnabled(False)
        else:
            if self._parent._compare is False:
                self.btnInstall.setEnabled(True)
                self.btnUninstall.setEnabled(True)
                self.btnUpload.setEnabled(True)
            else:
                self.btnInstall.setEnabled(False)
                self.btnUninstall.setEnabled(False)
                self.btnUpload.setEnabled(False)

            self.btnUnregister.setEnabled(True)
            self.btnOnlineCheck.setEnabled(True)
            self.btnPoweroff.setEnabled(True)
            self.btnReboot.setEnabled(True)

            if self._parent._active_side == "left":
                if self._parent._type_left == "depot":
                    self.btnSetRights.setEnabled(False)
                    self.btnRunProdUpdater.setEnabled(False)
                    self.btnGenMD5.setEnabled(False)
                    self.btnUninstall.setText(translate("DepotManagerDialog", "Uninstall"))
                else:
                    if self._parent._compare is not True:
                        self.btnSetRights.setEnabled(True)
                        self.btnRunProdUpdater.setEnabled(True)
                        self.btnGenMD5.setEnabled(True)
                    self.btnUninstall.setText(translate("DepotManagerDialog", "Delete"))
            else:
                if self._parent._type_right == "depot":
                    self.btnSetRights.setEnabled(False)
                    self.btnRunProdUpdater.setEnabled(False)
                    self.btnGenMD5.setEnabled(False)
                    self.btnUninstall.setText(translate("DepotManagerDialog", "Uninstall"))
                else:
                    if self._parent._compare is not True:
                        self.btnSetRights.setEnabled(True)
                        self.btnRunProdUpdater.setEnabled(True)
                        self.btnGenMD5.setEnabled(True)
                    self.btnUninstall.setText(translate("DepotManagerDialog", "Delete"))

        if self._parent._compare is False:
            self.decorate_button(self.btnCompare, "")
        else:
            self.decorate_button(self.btnCompare, "green")

        # set decoration and text
        if self._parent._type_left == "repo":
            self.decorate_button(self.btnFetchRepoLeft, "blue")
            self.btnFetchRepoLeft.setText(translate("DepotManagerDialog", "Fetch DEPOT content"))
        else:
            self.decorate_button(self.btnFetchRepoLeft, "")
            self.btnFetchRepoLeft.setText(translate("DepotManagerDialog", "Fetch REPO content"))

        if self._parent._type_right == "repo":
            self.decorate_button(self.btnFetchRepoRight, "blue")
            self.btnFetchRepoRight.setText(translate("DepotManagerDialog", "Fetch DEPOT content"))
        else:
            self.decorate_button(self.btnFetchRepoRight, "")
            self.btnFetchRepoRight.setText(translate("DepotManagerDialog", "Fetch REPO content"))

    @pyqtSlot()
    def update_fields(self):
        """Reload combobox content and reset their state"""
        self.logger.debug("Update field content")
        l = []
        for key, val in ConfigHandler.cfg.depotcache.items():
            l.append(key + " (" + val + ")")
        l.sort()

        # temporary disconnect events for smoother display
        self.cmbDepotLeft.currentTextChanged.disconnect(self._parent.switch_content)
        self.cmbDepotRight.currentTextChanged.disconnect(self._parent.switch_content)
        self.cmbDepotLeft.currentTextChanged.disconnect(self.set_active_side)
        self.cmbDepotRight.currentTextChanged.disconnect(self.set_active_side)

        self.cmbDepotLeft.clear()
        self.cmbDepotRight.clear()
        self.cmbDepotLeft.addItems(l)
        self.cmbDepotRight.addItems(l)

        self.cmbDepotLeft.currentTextChanged.connect(self._parent.switch_content)
        self.cmbDepotRight.currentTextChanged.connect(self._parent.switch_content)

        self.cmbDepotLeft.setCurrentIndex(-1)
        self.cmbDepotRight.setCurrentIndex(-1)

        self.cmbDepotLeft.currentTextChanged.connect(self.set_active_side)
        self.cmbDepotRight.currentTextChanged.connect(self.set_active_side)

    def decorate_button(self, button, state):
        """
        Set custom button property ``dispState``

        ``dispState`` is a conditional CSS parameter, like::

            QPushButton[dispState="red"] {
                color: rgb(255, 0, 0);
            }

        Dependend on its value, the button will be colored differently.

        :param button: QPushButton
        :param state: color ["red", "green", "blue"]
        """
        button.setProperty("dispState", state)
        button.style().unpolish(button)
        button.style().polish(button)
        button.update()

    def show_(self):
        self.logger.debug("Open depot manager")

        self.dialogOpened.emit()

        self.show()

        w = self.splitter.geometry().width()
        self.splitter.setSizes([w*(1/2), w*(1/2)])

        self._parent.update_data()
        self._parent.dataAquired.emit()

        self.cmbDepotLeft.setCurrentIndex(-1)
        self.cmbDepotRight.setCurrentIndex(-1)

        self.resizeTables()
        self.activateWindow()

    @pyqtSlot()
    def compare_sides(self):
        """
        Initiate side-by-side comparison of table views

        See: :meth:`oPB.controller.components.depotmanager.DepotManagerComponent.compare_leftright`
        """

        if self.cmbDepotLeft.currentIndex() == -1 or self.cmbDepotRight.currentIndex() == -1:
            return

        self._parent._compare = True if self._parent._compare is False else False
        self._parent.compare_leftright()

    @pyqtSlot()
    def set_active_side(self):
        """Set active table marker and initiate ui update accordingly"""

        if self.sender() == self.tblDepotLeft or self.sender() == self.cmbDepotLeft:
            self.logger.debug("Set active tableview: left")
            self._parent._active_side = "left"

        if self.sender() == self.tblDepotRight or self.sender() == self.cmbDepotRight:
            self.logger.debug("Set active tableview: right")
            self._parent._active_side = "right"

        self.update_ui()

    @pyqtSlot()
    def remove_delegate(self):
        """
        Decide between depot or repository removal of selected product(s)

        See: :meth:`oPB.controller.components.depotmanager.DepotManagerComponent.remove_from_depot`
        See: :meth:`oPB.controller.components.depotmanager.DepotManagerComponent.delete_from_repo`
        """

        if self._parent._active_side == "left":
            depot = self.cmbDepotLeft.currentText().split()[0]
            selection = self.tblDepotLeft.selectionModel().selectedRows()
            prodIdx = []

            if self._parent._type_left == "depot":
                for row in selection:
                    prodIdx.append(self.model_left.item(row.row(), 0).text())
                self._parent.remove_from_depot(depot, prodIdx)

            else:
                for row in selection:
                    prodIdx.append(self.model_left.item(row.row(), 0).text() + "_" + self.model_left.item(row.row(), 1).text() + "-" +
                                   self.model_left.item(row.row(),2).text())
                self._parent.delete_from_repo(depot, prodIdx)

        if self._parent._active_side == "right":
            depot = self.cmbDepotLeft.currentText().split()[0]
            selection = self.tblDepotRight.selectionModel().selectedRows()
            prodIdx = []

            if self._parent._type_right == "depot":
                for row in selection:
                    prodIdx.append(self.model_right.item(row.row(), 0).text())
                self._parent.remove_from_depot(depot, prodIdx)

            else:
                for row in selection:
                    prodIdx.append(self.model_right.item(row.row(), 0).text() + "_" + self.model_right.item(row.row(), 1).text() + "-" +
                                   self.model_right.item(row.row(),2).text())
                self._parent.delete_from_repo(depot, prodIdx)

    def generate_md5(self):
        """
        Get dialog widget state and initiate backend MD5 generation

        See: :meth:`oPB.controller.components.depotmanager.DepotManagerComponent.generate_md5`
        """
        if self._parent._active_side == "left":
            depot = self.cmbDepotLeft.currentText().split()[0]
            selection = self.tblDepotLeft.selectionModel().selectedRows()
            prodIdx = []

            if self._parent._type_left == "repo":
                for row in selection:
                    prodIdx.append(self.model_left.item(row.row(), 0).text() + "_" + self.model_left.item(row.row(), 1).text() + "-" +
                                   self.model_left.item(row.row(),2).text())
                self._parent.generate_md5(depot, prodIdx)

        if self._parent._active_side == "right":
            depot = self.cmbDepotLeft.currentText().split()[0]
            selection = self.tblDepotRight.selectionModel().selectedRows()
            prodIdx = []

            if self._parent._type_right == "repo":
                for row in selection:
                    prodIdx.append(self.model_right.item(row.row(), 0).text() + "_" + self.model_right.item(row.row(), 1).text() + "-" +
                                   self.model_right.item(row.row(),2).text())
                self._parent.generate_md5(depot, prodIdx)

    def retranslateMsg(self):
        self.logger.debug("Retranslating further messages...")
        self.splash.msg = translate("MainWindow", "Please wait...")