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
import platform
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.Qt import QKeyEvent
import oPB
from oPB.gui.helpviewer import Help
from oPB.core.confighandler import ConfigHandler
from oPB.core.tools import Helper, LogMixin
from oPB.gui.utilities import SpecialOptionButtonGroup, Translator, EventMixin
from oPB.ui.ui import SettingsDialogBase, SettingsDialogUI
from oPB.gui.splash import Splash

translate = QtCore.QCoreApplication.translate


class SettingsDialog(SettingsDialogBase, SettingsDialogUI, LogMixin, EventMixin):

    settingsAboutToBeClosed = pyqtSignal()
    dataChanged = pyqtSignal()

    def __init__(self, parent):
        """
        Constructor for settings dialog

        :param parent: parent window for settings dialog
        :return:
        """
        self._parent = parent
        self._parentUi = parent._parent.ui

        SettingsDialogBase.__init__(self, self._parentUi)
        self.setupUi(self)
        self.setWindowIcon(self._parentUi.windowIcon())

        print("\tgui/SettingsDialog parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None
        print("\tgui/SettingsDialog parentUi: ", self._parentUi, " -> self: ", self) if oPB.PRINTHIER else None

        self.splash = Splash(self, translate("MainWindow", "Please wait..."))
        self.splash.close()  # only for linux

        self.helpviewer = Help(oPB.HLP_FILE, oPB.HLP_PREFIX, self)

        # take care of sys.platform
        if sys.platform.startswith("linux"):
            self.chkUseNetworkDrive.setEnabled(False)
        if sys.platform.startswith("win32"):
            self.inpLocalShareBase.setEnabled(False)

        self.datamapper = None
        self.model = self._parent.model

        # setup translation combobox, must appear before data mapper creation
        Translator.setup_language_combobox(self, self.cmbLanguage)

        # additional setup
        self.create_optionbuttongroups()
        self.create_datamapper()
        self.connect_signals()

        # reset tabs
        self.tabWidget.setCurrentIndex(0)

        # hide not needed widgets
        self.lblBlockRecognition.setVisible(False)
        self.inpBlockMarker.setVisible(False)
        self.btnResetRecognition.setVisible(False)

    def connect_signals(self):
        self.logger.debug("Connect signals")

        self.btnCancel.clicked.connect(self.request_close_dialog)
        self.btnSetDevFolder.clicked.connect(self.select_dev_dir)
        self.btnSetKeyFile.clicked.connect(self.select_keyfile)
        self.btnExternalEditor.clicked.connect(self.select_externaleditor)
        self.btnLogFile.clicked.connect(self.select_logfile)
        self.btnHelp.clicked.connect(lambda: self.helpviewer.showHelp(oPB.HLP_DST_SETTINGS, False))

        self.btnSave.clicked.connect(self._parent.save_config)
        self.btnRefreshDepotCache.clicked.connect(self._parent.refresh_depot_cache)
        self.dataChanged.connect(self.datamapper.submit)
        self.settingsAboutToBeClosed.connect(self._parent.close_dialog)

        self.rdWBOld.clicked.connect(self.set_model_data)
        self.rdWBNew.clicked.connect(self.set_model_data)
        self.rdOpsi40.clicked.connect(self.set_model_data)
        self.rdOpsi41.clicked.connect(self.set_model_data)
        self.rdOpsiSrvNew.clicked.connect(self.set_model_data)
        self.rdOpsiSrvOld.clicked.connect(self.set_model_data)
        self.rdSUDOWithPass.clicked.connect(self.set_model_data)
        self.rdSUDOWithoutPass.clicked.connect(self.set_model_data)
        self.rdEditorInternal.clicked.connect(self.set_model_data)
        self.rdEditorExternal.clicked.connect(self.set_model_data)
        self.chkUseDepotFunctions.clicked.connect(self.set_model_data)
        self.chkUseProxy.clicked.connect(self.set_model_data)
        self.chkUseKeyFile.clicked.connect(self.set_model_data)
        self.chkWriteLog.clicked.connect(self.set_model_data)

    def create_datamapper(self):
        self.logger.debug("Create data widget mapper")
        self.datamapper = QDataWidgetMapper(self)
        self.datamapper.setModel(self._parent.model)
        self.datamapper.addMapping(self.inpConfigServer, 0)
        self.datamapper.addMapping(self.inpOpsiUser, 1)
        self.datamapper.addMapping(self.inpOpsiPass, 2)
        self.datamapper.addMapping(self.inpRootPass, 3)
        self.datamapper.addMapping(self.chkUseNetworkDrive, 4, b"checked")
        self.datamapper.addMapping(self.optionGroupSrvVersion, 5, b"checked")
        self.datamapper.addMapping(self.optionGroupSUDO, 6, b"checked")
        self.datamapper.addMapping(self.inpSSHPort, 7)
        self.datamapper.addMapping(self.optionGroupSSHKeyFile, 8, b"checked")
        self.datamapper.addMapping(self.inpKeyFile, 9)
        self.datamapper.addMapping(self.inpMaintainer, 10)
        self.datamapper.addMapping(self.inpMailAddress, 11)
        self.datamapper.addMapping(self.inpDevFolder, 12)
        self.datamapper.addMapping(self.inpBuildCommand, 13)
        self.datamapper.addMapping(self.inpInstallCommand, 14)
        self.datamapper.addMapping(self.inpUninstallCommand, 15)
        self.datamapper.addMapping(self.chkShowOutput, 16, b"checked")
        self.datamapper.addMapping(self.chkAlwaysReload, 17, b"checked")
        self.datamapper.addMapping(self.inpWOLLeadTime, 18)
        self.datamapper.addMapping(self.inpUploadCommand, 19)
        self.datamapper.addMapping(self.inpInstSetupCommand, 20)
        #self.datamapper.addMapping(self.settings.chkUseDepotFunctions, 21, "checked")
        self.datamapper.addMapping(self.optionGroupDepotFuncs, 21, b"checked")
        self.datamapper.addMapping(self.chkExtendedEditor, 22, b"checked")
        self.datamapper.addMapping(self.inpExternalEditor, 23)
        self.datamapper.addMapping(self.inpBlockMarker, 24)
        self.datamapper.addMapping(self.optionGroupEditorTyp, 25, b"checked")
        self.datamapper.addMapping(self.chkSyntaxHighlight, 26, b"checked")
        self.datamapper.addMapping(self.chkCodeFolding, 27, b"checked")
        self.datamapper.addMapping(self.chkForceEntryBuild, 28, b"checked")
        self.datamapper.addMapping(self.chkForceEntrySave, 29, b"checked")
        self.datamapper.addMapping(self.chkMsgError, 30, b"checked")
        self.datamapper.addMapping(self.chkMsgWarning, 31, b"checked")
        self.datamapper.addMapping(self.chkMsgInfo, 32, b"checked")
        self.datamapper.addMapping(self.chkMsgAT, 33, b"checked")
        self.datamapper.addMapping(self.cmbLanguage, 34, b"currentText")
        self.datamapper.addMapping(self.optionGroupProxy, 35, b"checked")
        self.datamapper.addMapping(self.chkUpdates, 36, b"checked")
        self.datamapper.addMapping(self.inpProxyServer, 37)
        self.datamapper.addMapping(self.inpProxyPort, 38)
        self.datamapper.addMapping(self.inpProxyUser, 39)
        self.datamapper.addMapping(self.inpProxyPass, 40)
        self.datamapper.addMapping(self.optionGroupLogFile, 41, b"checked")
        self.datamapper.addMapping(self.inpLogFile, 42)
        self.datamapper.addMapping(self.cmbLogLevel, 43)
        self.datamapper.addMapping(self.inpEditorOptions, 44)
        self.datamapper.addMapping(self.chkAttachDirect, 45, b"checked")
        self.datamapper.addMapping(self.inpLocalShareBase, 46)
        self.datamapper.addMapping(self.optionGroupBaseOS, 47, b"checked")
        self.datamapper.addMapping(self.optionGroupOpsi41, 48, b"checked")
        self.datamapper.toFirst()

    def create_optionbuttongroups(self):
        self.logger.debug("Create option button group")
        # build special button groups for False/True choice
        self.optionGroupSrvVersion = SpecialOptionButtonGroup(self.rdOpsiSrvNew, self.rdOpsiSrvOld,
                                                              [self.rdSUDOWithPass, self.rdSUDOWithoutPass],
                                                              [self.inpRootPass])

        self.optionGroupOpsi41 = SpecialOptionButtonGroup(self.rdOpsi41, self.rdOpsi40)

        self.optionGroupBaseOS = SpecialOptionButtonGroup(self.rdWBNew, self.rdWBOld)

        self.optionGroupSUDO = SpecialOptionButtonGroup(self.rdSUDOWithPass, self.rdSUDOWithoutPass)

        self.optionGroupEditorTyp = SpecialOptionButtonGroup(self.rdEditorInternal, self.rdEditorExternal,
                                                             [self.chkSyntaxHighlight, self.chkCodeFolding],
                                                             [self.btnExternalEditor, self.inpExternalEditor, self.inpEditorOptions,
                                                              self.chkAttachDirect])

        self.optionGroupDepotFuncs = SpecialOptionButtonGroup(self.chkUseDepotFunctions, None,
                                                              [self.btnRefreshDepotCache],
                                                              [self.inpInstallCommand, self.inpInstSetupCommand,
                                                               self.inpUninstallCommand, self.inpUploadCommand])

        self.optionGroupProxy = SpecialOptionButtonGroup(self.chkUseProxy, None,
                                                         [self.inpProxyServer, self.inpProxyPort,
                                                          self.inpProxyUser, self.inpProxyPass], [])

        self.optionGroupSSHKeyFile = SpecialOptionButtonGroup(self.chkUseKeyFile, None,
                                                              [self.btnSetKeyFile, self.inpKeyFile], [])

        self.optionGroupLogFile = SpecialOptionButtonGroup(self.chkWriteLog, None,
                                                              [self.btnLogFile, self.inpLogFile, self.cmbLogLevel], [])

    @pyqtSlot()
    def set_model_data(self):
        """
        Whenever a special radio button or checkbox is clicked,
        the corresponding model data element will be set accordingly.

        This has to be done like so, because radio buttons and checkboxes are not directly linked
        to the model, but via a SpecialOptionButtonGroup object.
        """
        self.logger.debug("Set model data values from button: " + self.sender().objectName())

        # radio buttons
        if self.sender().objectName() == "rdOpsiSrvNew":
            if self.rdOpsiSrvNew.isChecked():
                self.model.item(0, 5).setText("True")

        if self.sender().objectName() == "rdOpsiSrvOld":
            if self.rdOpsiSrvOld.isChecked():
                self.model.item(0, 5).setText("False")

        if self.sender().objectName() == "rdSUDOWithPass":
            if self.rdSUDOWithPass.isChecked():
                self.model.item(0, 6).setText("True")

        if self.sender().objectName() == "rdSUDOWithoutPass":
            if self.rdSUDOWithoutPass.isChecked():
                self.model.item(0, 6).setText("False")

        if self.sender().objectName() == "rdEditorInternal":
            if self.rdEditorInternal.isChecked():
                self.model.item(0, 25).setText("True")

        if self.sender().objectName() == "rdEditorExternal":
            if self.rdEditorExternal.isChecked():
                self.model.item(0, 25).setText("False")

        # check boxes
        if self.sender().objectName() == "chkUseKeyFile":
            if self.chkUseKeyFile.isChecked():
                self.model.item(0, 8).setText("True")
            else:
                self.model.item(0, 8).setText("False")

        if self.sender().objectName() == "chkUseDepotFunctions":
            if self.chkUseDepotFunctions.isChecked():
                self.model.item(0, 21).setText("True")
            else:
                self.model.item(0, 21).setText("False")

        if self.sender().objectName() == "chkUseProxy":
            if self.chkUseProxy.isChecked():
                self.model.item(0, 35).setText("True")
            else:
                self.model.item(0, 35).setText("False")

        if self.sender().objectName() == "chkWriteLog":
            if self.chkWriteLog.isChecked():
                self.model.item(0, 41).setText("True")
            else:
                self.model.item(0, 41).setText("False")

        if self.sender().objectName() == "rdWBNew":
            if self.rdWBNew.isChecked():
                self.model.item(0, 47).setText("True")

        if self.sender().objectName() == "rdWBOld":
            if self.rdWBOld.isChecked():
                self.model.item(0, 47).setText("False")

        if self.sender().objectName() == "rdOpsi41":
            if self.rdOpsi41.isChecked():
                self.model.item(0, 48).setText("True")
                self.change_build_command()

        if self.sender().objectName() == "rdOpsi40":
            if self.rdOpsi40.isChecked():
                self.model.item(0, 48).setText("False")
                self.change_build_command()

    def change_build_command(self):
        if self.optionGroupOpsi41.getChecked() == True:
            #com: str = self.inpBuildCommand.text()
            #com = com.replace(oPB.OPB_BUILD40, oPB.OPB_BUILD41)
            #self.inpBuildCommand.setText(com)
            self.inpBuildCommand.setText(oPB.OPB_BUILD41)
        else:
            #com: str = self.inpBuildCommand.text()
            #com = com.replace(oPB.OPB_BUILD41, oPB.OPB_BUILD40)
            #com = com.replace("--no-md5", "")
            #com = com.replace("--no-zsync", "")
            #self.inpBuildCommand.setText(com)
            self.inpBuildCommand.setText(oPB.OPB_BUILD40)
        self.dataChanged.emit()

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
        """Development directory selector dialog"""
        self.logger.debug("Select development directory")
        directory = QFileDialog.getExistingDirectory(self, translate("SettingsDialog", "Select development folder"),
                                                     ConfigHandler.cfg.dev_dir, QFileDialog.ShowDirsOnly)

        if not directory == "":
            self.logger.info("Chosen directory: " + directory)
            value = Helper.concat_path_native(directory, "")
            if value[-1:] == "/" or value[-1:] == '\\':
                value = value[:-1]
            self.inpDevFolder.setText(value)
            self.inpLocalShareBase.setText(value)
            self.dataChanged.emit()
        else:
            self.logger.debug("Dialog aborted.")

    @pyqtSlot()
    def select_keyfile(self):
        """SSH keyfile selector dialog"""
        self.logger.debug("Select SSH keyfile dialog")

        ext = "Private key file (" + (" ").join(["*." + x for x in oPB.KEYFILE_EXT]) + ")"  # generate file extension selection string for dialog

        script = QFileDialog.getOpenFileName(self, translate("SettingsDialog", "Choose keyfile"),
                                            ConfigHandler.cfg.dev_dir, ext)

        if not script == ("", ""):
            self.logger.debug("Selected SSH keyfile: " + script[0])
            self.inpKeyFile.setText(Helper.concat_path_native(script[0], ""))
            self.dataChanged.emit()
        else:
            self.logger.debug("Dialog aborted.")

    @pyqtSlot()
    def select_externaleditor(self):
        """External editor selector dialog"""
        self.logger.debug("Select scripteditor dialog")

        if platform.system() != "Windows":
            ext = "Program (" + (" ").join(["*." + x for x in oPB.PRG_EXT]) + ")"  # generate file extension selection string for dialog
        else:
            ext = "Any (*)"

        script = QFileDialog.getOpenFileName(self, translate("SettingsDialog", "Choose Scripteditor"),
                                            ConfigHandler.cfg.dev_dir, ext)

        if not script == ("", ""):
            self.logger.debug("Selected Scripeditor: " + script[0])
            self.inpExternalEditor.setText(Helper.concat_path_native(script[0], ""))
            self.dataChanged.emit()
        else:
            self.logger.debug("Dialog aborted.")

    @pyqtSlot()
    def select_logfile(self):
        """Logfile selector dialog"""
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
            self.inpLogFile.setText(Helper.concat_path_native(directory, "opb-session.log"))
            self.dataChanged.emit()
        else:
            self.logger.debug("Dialog aborted.")
