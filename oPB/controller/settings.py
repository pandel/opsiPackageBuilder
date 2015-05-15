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

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot
from PyQt5.QtWidgets import QDataWidgetMapper, QMessageBox
import oPB
from oPB.gui.settings import SettingsDialog
from oPB.core.tools import LogMixin
from oPB.core.confighandler import ConfigHandler
from oPB.core.tools import Helper

translate = QtCore.QCoreApplication.translate

class SettingsController(QObject, LogMixin):

    settingsClosed = pyqtSignal()    # send after model or backend data has been updated

    def __init__(self, parent):
        """
        Initiate settings editing

        Signals
        * settingsClosed

        :param parent: parent window of settings dialog
        :return:
        """
        super().__init__(parent)
        self._parent = parent
        print("controller/SettingsController parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None

        self.logger.debug("Initialize settings dialog")

        self.model = None              # data models
        self.datamapper = None             # QDataWidgetMapper object for field mapping
        self._modelDataChanged = False  # is connect via model_data_changed function to itemChanged Signal of QStandardItemModel, will be reset in close_project()

        # create main window and logic
        self.ui = SettingsDialog(self._parent)

        # build special button groups for False/True choice
        self.optionGroupSrvVersion = SpecialOptionButtonGroup(self.ui.rdOpsiSrvNew, self.ui.rdOpsiSrvOld,
                                                              [self.ui.rdSUDOWithPass, self.ui.rdSUDOWithoutPass],
                                                              [self.ui.inpRootPass])

        self.optionGroupSUDO = SpecialOptionButtonGroup(self.ui.rdSUDOWithPass, self.ui.rdSUDOWithoutPass)

        self.optionGroupEditorTyp = SpecialOptionButtonGroup(self.ui.rdEditorInternal, self.ui.rdEditorExternal,
                                                             [self.ui.chkSyntaxHighlight, self.ui.chkCodeFolding],
                                                             [self.ui.btnExternalEditor, self.ui.inpExternalEditor])

        self.optionGroupDepotFuncs = SpecialOptionButtonGroup(self.ui.chkUseDepotFunctions, None, [],
                                                              [self.ui.inpInstallCommand, self.ui.inpInstSetupCommand,
                                                               self.ui.inpUninstallCommand, self.ui.inpUploadCommand])

        self.optionGroupProxy = SpecialOptionButtonGroup(self.ui.chkUseProxy, None,
                                                         [self.ui.inpProxyServer, self.ui.inpProxyPort,
                                                          self.ui.inpProxyUser, self.ui.inpProxyPass], [])

        self.optionGroupSSHKeyFile = SpecialOptionButtonGroup(self.ui.chkUseKeyFile, None,
                                                              [self.ui.btnSetKeyFile, self.ui.inpKeyFile], [])

        self.optionGroupLogFile = SpecialOptionButtonGroup(self.ui.chkWriteLog, None,
                                                              [self.ui.btnLogFile, self.ui.inpLogFile, self.ui.cmbLogLevel], [])

        self.generate_model()
        self.connect_signals()

        # open modal dialog
        self.ui.tabWidget.setCurrentIndex(0)

    def generate_model(self):
        """Create data models and assign field mappings"""
        self.logger.debug("Generate configuration model")
        self.model = QtGui.QStandardItemModel(self.ui)
        self.model.setItem(0, 0, QtGui.QStandardItem(ConfigHandler.cfg.opsi_server))
        self.model.setItem(0, 1, QtGui.QStandardItem(ConfigHandler.cfg.opsi_user))
        self.model.setItem(0, 2, QtGui.QStandardItem(ConfigHandler.cfg.opsi_pass))
        self.model.setItem(0, 3, QtGui.QStandardItem(ConfigHandler.cfg.root_pass))
        self.model.setItem(0, 4, QtGui.QStandardItem(ConfigHandler.cfg.usenetdrive))
        self.model.setItem(0, 5, QtGui.QStandardItem(ConfigHandler.cfg.age))
        self.model.setItem(0, 6, QtGui.QStandardItem(ConfigHandler.cfg.sudo))
        self.model.setItem(0, 7, QtGui.QStandardItem(ConfigHandler.cfg.sshport))
        self.model.setItem(0, 8, QtGui.QStandardItem(ConfigHandler.cfg.usekeyfile))
        self.model.setItem(0, 9, QtGui.QStandardItem(ConfigHandler.cfg.keyfilename))
        self.model.setItem(0, 10, QtGui.QStandardItem(ConfigHandler.cfg.packagemaintainer))
        self.model.setItem(0, 11, QtGui.QStandardItem(ConfigHandler.cfg.mailaddress))
        self.model.setItem(0, 12, QtGui.QStandardItem(ConfigHandler.cfg.dev_dir))
        self.model.setItem(0, 13, QtGui.QStandardItem(ConfigHandler.cfg.buildcommand))
        self.model.setItem(0, 14, QtGui.QStandardItem(ConfigHandler.cfg.installcommand))
        self.model.setItem(0, 15, QtGui.QStandardItem(ConfigHandler.cfg.uninstallcommand))
        self.model.setItem(0, 16, QtGui.QStandardItem(ConfigHandler.cfg.showoutput))
        self.model.setItem(0, 17, QtGui.QStandardItem(ConfigHandler.cfg.reload_for_at))
        self.model.setItem(0, 18, QtGui.QStandardItem(ConfigHandler.cfg.wol_lead_time))
        self.model.setItem(0, 19, QtGui.QStandardItem(ConfigHandler.cfg.uploadcommand))
        self.model.setItem(0, 20, QtGui.QStandardItem(ConfigHandler.cfg.instsetupcommand))
        self.model.setItem(0, 21, QtGui.QStandardItem(ConfigHandler.cfg.use_depot_funcs))
        self.model.setItem(0, 22, QtGui.QStandardItem(ConfigHandler.cfg.use_extended_changelog))
        self.model.setItem(0, 23, QtGui.QStandardItem(ConfigHandler.cfg.scripteditor))
        self.model.setItem(0, 24, QtGui.QStandardItem(ConfigHandler.cfg.chlog_block_marker))
        self.model.setItem(0, 25, QtGui.QStandardItem(ConfigHandler.cfg.editor_intern))
        self.model.setItem(0, 26, QtGui.QStandardItem(ConfigHandler.cfg.editor_use_styling))
        self.model.setItem(0, 27, QtGui.QStandardItem(ConfigHandler.cfg.editor_use_folding))
        self.model.setItem(0, 28, QtGui.QStandardItem(ConfigHandler.cfg.chlog_on_build))
        self.model.setItem(0, 29, QtGui.QStandardItem(ConfigHandler.cfg.chlog_on_save))
        self.model.setItem(0, 30, QtGui.QStandardItem(ConfigHandler.cfg.no_error_msg))
        self.model.setItem(0, 31, QtGui.QStandardItem(ConfigHandler.cfg.no_warning_msg))
        self.model.setItem(0, 32, QtGui.QStandardItem(ConfigHandler.cfg.no_info_msg))
        self.model.setItem(0, 33, QtGui.QStandardItem(ConfigHandler.cfg.no_at_warning_msg))
        self.model.setItem(0, 34, QtGui.QStandardItem(ConfigHandler.cfg.language))
        self.model.setItem(0, 35, QtGui.QStandardItem(ConfigHandler.cfg.useproxy))
        self.model.setItem(0, 36, QtGui.QStandardItem(ConfigHandler.cfg.updatecheck))
        self.model.setItem(0, 37, QtGui.QStandardItem(ConfigHandler.cfg.proxy_server))
        self.model.setItem(0, 38, QtGui.QStandardItem(ConfigHandler.cfg.proxy_port))
        self.model.setItem(0, 39, QtGui.QStandardItem(ConfigHandler.cfg.proxy_user))
        self.model.setItem(0, 40, QtGui.QStandardItem(ConfigHandler.cfg.proxy_pass))
        self.model.setItem(0, 41, QtGui.QStandardItem(ConfigHandler.cfg.log_always))
        self.model.setItem(0, 42, QtGui.QStandardItem(ConfigHandler.cfg.log_file))
        self.model.setItem(0, 43, QtGui.QStandardItem(ConfigHandler.cfg.log_level))

        self.logger.debug("Create data widget mapper")
        self.datamapper = QDataWidgetMapper(self.ui)
        self.datamapper.setModel(self.model)
        self.datamapper.addMapping(self.ui.inpConfigServer, 0)
        self.datamapper.addMapping(self.ui.inpOpsiUser, 1)
        self.datamapper.addMapping(self.ui.inpOpsiPass, 2)
        self.datamapper.addMapping(self.ui.inpRootPass, 3)
        self.datamapper.addMapping(self.ui.chkUseNetworkDrive, 4, "checked")
        self.datamapper.addMapping(self.optionGroupSrvVersion, 5, "checked")
        self.datamapper.addMapping(self.optionGroupSUDO, 6, "checked")
        self.datamapper.addMapping(self.ui.inpSSHPort, 7)
        self.datamapper.addMapping(self.optionGroupSSHKeyFile, 8, "checked")
        self.datamapper.addMapping(self.ui.inpKeyFile, 9)
        self.datamapper.addMapping(self.ui.inpMaintainer, 10)
        self.datamapper.addMapping(self.ui.inpMailAddress, 11)
        self.datamapper.addMapping(self.ui.inpDevFolder, 12)
        self.datamapper.addMapping(self.ui.inpBuildCommand, 13)
        self.datamapper.addMapping(self.ui.inpInstallCommand, 14)
        self.datamapper.addMapping(self.ui.inpUninstallCommand, 15)
        self.datamapper.addMapping(self.ui.chkShowOutput, 16, "checked")
        self.datamapper.addMapping(self.ui.chkAlwaysReload, 17, "checked")
        self.datamapper.addMapping(self.ui.inpWOLLeadTime, 18)
        self.datamapper.addMapping(self.ui.inpUploadCommand, 19)
        self.datamapper.addMapping(self.ui.inpInstSetupCommand, 20)
        #self.datamapper.addMapping(self.settings.chkUseDepotFunctions, 21, "checked")
        self.datamapper.addMapping(self.optionGroupDepotFuncs, 21, "checked")
        self.datamapper.addMapping(self.ui.chkExtendedEditor, 22, "checked")
        self.datamapper.addMapping(self.ui.inpExternalEditor, 23)
        self.datamapper.addMapping(self.ui.inpBlockMarker, 24)
        self.datamapper.addMapping(self.optionGroupEditorTyp, 25, "checked")
        self.datamapper.addMapping(self.ui.chkSyntaxHighlight, 26, "checked")
        self.datamapper.addMapping(self.ui.chkCodeFolding, 27, "checked")
        self.datamapper.addMapping(self.ui.chkForceEntryBuild, 28, "checked")
        self.datamapper.addMapping(self.ui.chkForceEntrySave, 29, "checked")
        self.datamapper.addMapping(self.ui.chkMsgError, 30, "checked")
        self.datamapper.addMapping(self.ui.chkMsgWarning, 31, "checked")
        self.datamapper.addMapping(self.ui.chkMsgInfo, 32, "checked")
        self.datamapper.addMapping(self.ui.chkMsgAT, 33, "checked")
        self.datamapper.addMapping(self.ui.cmbLanguage, 34, "currentText")
        self.datamapper.addMapping(self.optionGroupProxy, 35, "checked")
        self.datamapper.addMapping(self.ui.chkUpdates, 36, "checked")
        self.datamapper.addMapping(self.ui.inpProxyServer, 37)
        self.datamapper.addMapping(self.ui.inpProxyPort, 38)
        self.datamapper.addMapping(self.ui.inpProxyUser, 39)
        self.datamapper.addMapping(self.ui.inpProxyPass, 40)
        self.datamapper.addMapping(self.optionGroupLogFile, 41, "checked")
        self.datamapper.addMapping(self.ui.inpLogFile, 42)
        self.datamapper.addMapping(self.ui.cmbLogLevel, 43)
        self.datamapper.toFirst()

    def connect_signals(self):
        """Connect signals"""

        self.logger.debug("Connect signals")
        self.model.itemChanged.connect(self.model_data_changed)

        self.ui.btnSave.clicked.connect(self.save_config)
        self.ui.dataChanged.connect(self.datamapper.submit)
        self.ui.settingsAboutToBeClosed.connect(self.close_dialog)

        self.ui.rdOpsiSrvNew.clicked.connect(self.set_model_data)
        self.ui.rdOpsiSrvOld.clicked.connect(self.set_model_data)
        self.ui.rdSUDOWithPass.clicked.connect(self.set_model_data)
        self.ui.rdSUDOWithoutPass.clicked.connect(self.set_model_data)
        self.ui.rdEditorInternal.clicked.connect(self.set_model_data)
        self.ui.rdEditorExternal.clicked.connect(self.set_model_data)
        self.ui.chkUseDepotFunctions.clicked.connect(self.set_model_data)
        self.ui.chkUseProxy.clicked.connect(self.set_model_data)
        self.ui.chkUseKeyFile.clicked.connect(self.set_model_data)
        self.ui.chkWriteLog.clicked.connect(self.set_model_data)

    @pyqtSlot()
    def model_data_changed(self):
        """Update model changed marker"""
        self.logger.debug("Model data changed")
        self._modelDataChanged = True

    @pyqtSlot()
    def set_model_data(self):
        """Whenever a special radio button or checkbox is clicked,
        the corresponding model data element will be set accordingly.

        This has to be done like so, because radio buttons and checkboxes are not directly linked
        to the model, but via a SpecialOptionButtonGroup object.
        """
        self.logger.debug("Set model data values from button: " + self.sender().objectName())

        # radio buttons
        if self.sender().objectName() == "rdOpsiSrvNew":
            if self.ui.rdOpsiSrvNew.isChecked():
                self.model.item(0, 5).setText("True")

        if self.sender().objectName() == "rdOpsiSrvOld":
            if self.ui.rdOpsiSrvOld.isChecked():
                self.model.item(0, 5).setText("False")

        if self.sender().objectName() == "rdSUDOWithPass":
            if self.ui.rdSUDOWithPass.isChecked():
                self.model.item(0, 6).setText("True")

        if self.sender().objectName() == "rdSUDOWithoutPass":
            if self.ui.rdSUDOWithoutPass.isChecked():
                self.model.item(0, 6).setText("False")

        if self.sender().objectName() == "rdEditorInternal":
            if self.ui.rdEditorInternal.isChecked():
                self.model.item(0, 25).setText("True")

        if self.sender().objectName() == "rdEditorExternal":
            if self.ui.rdEditorExternal.isChecked():
                self.model.item(0, 25).setText("False")

        # check boxes
        if self.sender().objectName() == "chkUseKeyFile":
            if self.ui.chkUseKeyFile.isChecked():
                self.model.item(0, 8).setText("True")
            else:
                self.model.item(0, 8).setText("False")

        if self.sender().objectName() == "chkUseDepotFunctions":
            if self.ui.chkUseDepotFunctions.isChecked():
                self.model.item(0, 21).setText("True")
            else:
                self.model.item(0, 21).setText("False")

        if self.sender().objectName() == "chkUseProxy":
            if self.ui.chkUseProxy.isChecked():
                self.model.item(0, 35).setText("True")
            else:
                self.model.item(0, 35).setText("False")

        if self.sender().objectName() == "chkWriteLog":
            if self.ui.chkWriteLog.isChecked():
                self.model.item(0, 41).setText("True")
            else:
                self.model.item(0, 41).setText("False")

    def update_backend_data(self):
        self.logger.debug("Update config backend")
        ConfigHandler.cfg.opsi_server = self.model.item(0, 0).text()
        ConfigHandler.cfg.opsi_user = self.model.item(0, 1).text()
        ConfigHandler.cfg.opsi_pass =  self.model.item(0, 2).text()
        ConfigHandler.cfg.root_pass = self.model.item(0, 3).text()
        ConfigHandler.cfg.usenetdrive = self.model.item(0, 4).text().title()
        ConfigHandler.cfg.age = self.model.item(0, 5).text().title()
        ConfigHandler.cfg.sudo = self.model.item(0, 6).text().title()
        ConfigHandler.cfg.cfg.sshport = self.model.item(0, 7).text()
        ConfigHandler.cfg.usekeyfile = self.model.item(0, 8).text().title()
        ConfigHandler.cfg.keyfilename = self.model.item(0, 9).text()
        ConfigHandler.cfg.packagemaintainer = self.model.item(0, 10).text()
        ConfigHandler.cfg.mailaddress = self.model.item(0, 11).text()
        ConfigHandler.cfg.dev_dir = self.model.item(0, 12).text()
        ConfigHandler.cfg.buildcommand = self.model.item(0, 13).text()
        ConfigHandler.cfg.installcommand = self.model.item(0, 14).text()
        ConfigHandler.cfg.uninstallcommand = self.model.item(0, 15).text()
        ConfigHandler.cfg.showoutput = self.model.item(0, 16).text().title()
        ConfigHandler.cfg.reload_for_at = self.model.item(0, 17).text().title()
        ConfigHandler.cfg.wol_lead_time = self.model.item(0, 18).text()
        ConfigHandler.cfg.uploadcommand = self.model.item(0, 19).text()
        ConfigHandler.cfg.instsetupcommand = self.model.item(0, 20).text()
        ConfigHandler.cfg.use_depot_funcs = self.model.item(0, 21).text().title()
        ConfigHandler.cfg.use_extended_changelog = self.model.item(0, 22).text().title()
        ConfigHandler.cfg.scripteditor = self.model.item(0, 23).text()
        ConfigHandler.cfg.chlog_block_marker = self.model.item(0, 24).text()
        ConfigHandler.cfg.editor_intern = self.model.item(0, 25).text().title()
        ConfigHandler.cfg.editor_use_styling = self.model.item(0, 26).text().title()
        ConfigHandler.cfg.editor_use_folding = self.model.item(0, 27).text().title()
        ConfigHandler.cfg.chlog_on_build = self.model.item(0, 28).text().title()
        ConfigHandler.cfg.chlog_on_save = self.model.item(0, 29).text().title()
        ConfigHandler.cfg.no_error_msg = self.model.item(0, 30).text().title()
        ConfigHandler.cfg.no_warning_msg = self.model.item(0, 31).text().title()
        ConfigHandler.cfg.no_info_msg = self.model.item(0, 32).text().title()
        ConfigHandler.cfg.no_at_warning_msg = self.model.item(0, 33).text().title()
        ConfigHandler.cfg.language = self.model.item(0, 34).text()
        ConfigHandler.cfg.useproxy = self.model.item(0, 35).text().title()
        ConfigHandler.cfg.updatecheck = self.model.item(0, 36).text().title()
        ConfigHandler.cfg.proxy_server = self.model.item(0, 37).text()
        ConfigHandler.cfg.proxy_port = self.model.item(0, 38).text()
        ConfigHandler.cfg.proxy_user = self.model.item(0, 39).text()
        ConfigHandler.cfg.proxy_pass = self.model.item(0, 40).text()
        ConfigHandler.cfg.log_always = self.model.item(0, 41).text().title()
        ConfigHandler.cfg.log_file = self.model.item(0, 42).text()
        ConfigHandler.cfg.log_level = self.model.item(0, 43).text()

    def close_dialog(self):
        """Close settings dialog"""
        ignoreChanges = True
        if self._modelDataChanged == True:
            retval = QMessageBox.question(None, translate("settingsController", "Question"), translate("settingsController", "There are unsaved changes! Do you really want to continue?"), QMessageBox.Yes, QMessageBox.No)
            if retval == QMessageBox.No:
                self.logger.debug("Unsaved changes have been ignored.")
                ignoreChanges = False

        if ignoreChanges:
            self.logger.debug("Close settings dialog")
            self.ui.close()
            self.logger.debug("Emit signal settingsClosed")
            self.settingsClosed.emit()

    @pyqtSlot()
    def save_config(self):
        """Get field values and initiate saving of configuration"""
        if self._modelDataChanged:
            self.update_backend_data()
            ConfigHandler.cfg.save()
            self._modelDataChanged = None

        self.close_dialog()


class SpecialOptionButtonGroup(QtWidgets.QWidget, LogMixin):
    """This object takes care of radio buttons and checkboxes, that a9 a a counterpart (like yes/no or true/false)
    and additionally activate/deactivate other widgets
    """

    def __init__(self, left_button:QtWidgets.QWidget, right_button:QtWidgets.QWidget = None, enable_left:list = [], enable_right:list = []):
        """
        Constructor of SpecialOptionButtonGroup

        Imagine, you have two exclusive radio buttons. This object treats both widgets as one, returning "True" if the :left: is
        active and "False". if the :right: one is active.
        Additionally, if there are widgets, whose active/deactive state depends on if :left_button: is checked or not,
        this routine takes care of it, too.

        Exp. (radio buttons):

            obj = SpecialOptionButtonGroup(win.rdButtonLeft, win.rdButtonRight, [win.fieldA, win.fieldB], [win.fieldC, win.fieldD]

        a) if win.rdButtonLeft is checked: obj.getChecked == True
        aa) win.FieldA and win.FieldB will be activated, win.FieldC and win.FieldD will be deactivated
        b) if win.rdButtonRight is checked: obj.getChecked == False
        ab) win.FieldA and win.FieldB will be deactivated, win.FieldC and win.FieldD will be activated

        Exp. (checkbox):

            obj = SpecialOptionButtonGroup(win.chkBox, None, [win.fieldA, win.fieldB], [win.fieldC, win.fieldD]

        a) if win.chkBox is checked: obj.getChecked == True
        aa) win.FieldA and win.FieldB will be activated, win.FieldC and win.FieldD will be deactivated
        b) if win.chkBox is not checked: obj.getChecked == False
        bb) win.FieldA and win.FieldB will be deactivated, win.FieldC and win.FieldD will be activated

        Notice:
        This is really helpful, if you have one boolean variable, with which you want to control a whole set of widgets in your ui,
        and at the same time, map this variable via QDataWidgetMapper to a data model.

        :param left_button: in a two-button relationship, left("Answer A") button
        :param right_button: in a two-button relationship, right("Answer B") button (optional)
        :param enable_left: widgets (obj), that should be active for "Answer A" (optional)
        :param enable_right: widgets (obj), that should be active for "Answer B" (optional)
        :return:
        """
        super().__init__()

        self._checked = True
        self._left_button = left_button
        self._right_button = right_button
        self._enable_left = enable_left
        self._enable_right = enable_right

    def getChecked(self):
        """
        Return main value of this option group
        :return: True/False
        """
        return self._checked

    def setChecked(self, value):
        """
        Sets the overall option group value and activates/deactivtes the dependend widgets.
        :param value: True(=left), False(=right)
        """

        self._checked = value
        if value == True:
            self._left_button.setChecked(True)
            if self._right_button is not None: self._right_button.setChecked(False)
            for widget in self._enable_left:
                widget.setEnabled(True)
            for widget in self._enable_right:
                widget.setEnabled(False)
        else:
            self._left_button.setChecked(False)
            if self._right_button is not None: self._right_button.setChecked(True)
            for widget in self._enable_left:
                widget.setEnabled(False)
            for widget in self._enable_right:
                widget.setEnabled(True)

    checked = pyqtProperty(bool, fget=getChecked, fset=setChecked)

