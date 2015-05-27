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

import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.Qt import QKeyEvent
import oPB
from oPB.core.confighandler import ConfigHandler
from oPB.core.tools import Helper, LogMixin
from oPB.ui.ui import SettingsDialogBase, SettingsDialogUI


translate = QtCore.QCoreApplication.translate


class SettingsDialog(SettingsDialogBase, SettingsDialogUI, LogMixin):

    settingsAboutToBeClosed = pyqtSignal()
    dataChanged = pyqtSignal()

    def __init__(self, parent):
        """
        Constructor for settings dialog

        :param parent: parent window for settings dialog
        :return:
        """
        SettingsDialogBase.__init__(self, parent)
        self.setupUi(self)

        self._parent = parent
        print("gui/Settings parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None

        # take care of sys.platform
        if sys.platform.startswith("linux"):
            self.chkUseNetworkDrive.setEnabled(False)

        self.connect_signals()

    def connect_signals(self):
        """Connect signals to parent"""
        self.logger.debug("Connect signals")

        self.btnCancel.clicked.connect(self.request_close_dialog)
        self.btnSetDevFolder.clicked.connect(self.select_dev_dir)
        self.btnSetKeyFile.clicked.connect(self.select_keyfile)
        self.btnExternalEditor.clicked.connect(self.select_externaleditor)
        self.btnLogFile.clicked.connect(self.select_logfile)

    def keyPressEvent(self, evt: QKeyEvent):
        """
        Ignore escape key event, because it would close startup window.
        Any other key will be passed to the super class key event handler for further
        processing.

        :param evt: key event
        :return:
        """
        if evt.key() == QtCore.Qt.Key_Escape:
            self.request_close_dialog()
        else:
            super().keyPressEvent(evt)

    @pyqtSlot()
    def request_close_dialog(self):
        """Request closing of settings dialog"""
        self.logger.debug("Emit signal settingsAboutToBeClosed")
        self.settingsAboutToBeClosed.emit()

    @pyqtSlot()
    def select_dev_dir(self):
        self.logger.debug("Select development directory")
        directory = QFileDialog.getExistingDirectory(self, translate("SettingsDialog", "Select development folder"),
                                                     ConfigHandler.cfg.dev_dir, QFileDialog.ShowDirsOnly)

        if not directory == "":
            self.logger.info("Chosen directory: " + directory)
            self.inpDevFolder.setText(Helper.concat_path_and_file(directory, ""))
            self.dataChanged.emit()
        else:
            self.logger.debug("Dialog aborted.")

    @pyqtSlot()
    def select_keyfile(self):
        self.logger.debug("Select SSH keyfile dialog")

        ext = "Private key file (" + ("; ").join(["*." + x for x in oPB.KEYFILE_EXT]) + ")"  # generate file extension selection string for dialog

        script = QFileDialog.getOpenFileName(self, translate("SettingsDialog", "Choose keyfile"),
                                            ConfigHandler.cfg.dev_dir, ext)

        if not script == ("", ""):
            self.logger.debug("Selected SSH keyfile: " + script[0])
            self.inpKeyFile.setText(Helper.concat_path_and_file(script[0], ""))
            self.dataChanged.emit()
        else:
            self.logger.debug("Dialog aborted.")

    @pyqtSlot()
    def select_externaleditor(self):
        self.logger.debug("Select scripteditor dialog")

        ext = "Program (" + ("; ").join(["*." + x for x in oPB.PRG_EXT]) + ")"  # generate file extension selection string for dialog

        script = QFileDialog.getOpenFileName(self, translate("SettingsDialog", "Choose Scripteditor"),
                                            ConfigHandler.cfg.dev_dir, ext)

        if not script == ("", ""):
            self.logger.debug("Selected Scripeditor: " + script[0])
            self.inpExternalEditor.setText(Helper.concat_path_and_file(script[0], ""))
            self.dataChanged.emit()
        else:
            self.logger.debug("Dialog aborted.")

    @pyqtSlot()
    def select_logfile(self):
        self.logger.debug("Select log file dialog")

        """
        ext = "Log (*.log)"  # generate file extension selection string for dialog

        script = QFileDialog.getOpenFileName(self, translate("SettingsDialog", "Choose folder for logfile"),
                                             ConfigHandler.cfg.log_file, ext)

        if not script == ("", ""):
            self.logger.debug("Selected Logile: " + script[0])
        """

        directory = QFileDialog.getExistingDirectory(self, translate("SettingsDialog", "Select logfile folder"),
                                                     ConfigHandler.cfg.dev_dir, QFileDialog.ShowDirsOnly)

        if not directory == "":
            self.logger.info("Chosen directory: " + directory)
            self.inpLogFile.setText(Helper.concat_path_and_file(directory, "opb-session.log"))
            self.dataChanged.emit()
        else:
            self.logger.debug("Dialog aborted.")
