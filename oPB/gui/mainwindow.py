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

import os.path
import webbrowser
import platform

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot

import oPB
from oPB.core.confighandler import ConfigHandler
from oPB.core.tools import Helper, LogMixin
from oPB.controller.settings import SettingsController
from oPB.ui.ui import MainWindowBase, MainWindowUI

translate = QtCore.QCoreApplication.translate


class MainWindow(MainWindowBase, MainWindowUI, LogMixin):
    """MainWindow UI class"""
    showLogRequested = pyqtSignal()
    windowMoved = pyqtSignal()

    MaxRecentFiles = 5

    def __init__(self, parent):
        MainWindowBase.__init__(self)
        self.setupUi(self)

        self.recentFileActions = []

        if oPB.NETMODE == "offline":
            self.setWindowTitle("opsiPackageBuilder ( OFFLINE MODE )")

        self._parent = parent
        print("gui/MainWindow parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None

        self.datamapper = None             # QDataWidgetMapper object for field mapping
        self.datamapper_dependencies = None
        self.datamapper_properties = None

        # settings dialog / splash
        self.settingsCtr = SettingsController(self)
        self.settingsCtr.settingsClosed.connect(self.set_dev_folder)

        self.splash = Splash(self, translate("MainWindow", "Please wait..."))
        self.splash.close()  # only for linux

        self.create_datamapper()
        self.connect_signals()
        self.connect_validators()

        self.reset_datamapper_and_display()

    def init_recent(self):
        for i in range(MainWindow.MaxRecentFiles):
                    self.recentFileActions.append(
                            QAction(self, visible=False,
                                    triggered=self.open_recent_project))
        for i in range(MainWindow.MaxRecentFiles):
                    self.menuRecent.addAction(self.recentFileActions[i])
                    self._parent.startup.menuRecent.addAction(self.recentFileActions[i])

        self.update_recent_file_actions()

    def update_recent_file_actions(self):
        files = ConfigHandler.cfg.recent

        numRecentFiles = min(len(files), MainWindow.MaxRecentFiles)

        for i in range(numRecentFiles):
            text = "&%d %s" % (i + 1, self.strippedName(files[i]))
            self.recentFileActions[i].setText(text)
            self.recentFileActions[i].setData(files[i])
            self.recentFileActions[i].setVisible(True)

        for j in range(numRecentFiles, MainWindow.MaxRecentFiles):
            self.recentFileActions[j].setVisible(False)

    def strippedName(self, fullFileName):
        return QtCore.QFileInfo(fullFileName).fileName()

    def setCurrentProject(self, project):
        files = ConfigHandler.cfg.recent

        try:
            files.remove(project)
        except ValueError:
            pass

        files.insert(0, project)
        del files[MainWindow.MaxRecentFiles:]

        ConfigHandler.cfg.recent = files

        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, MainWindow):
                widget.update_recent_file_actions()

    def create_datamapper(self):
        """Create datamapper for fields and tables"""
        self.logger.debug("Create data widget mapper for fields")
        self.datamapper = QDataWidgetMapper(self)
        self.datamapper.setModel(self._parent.model_fields)
        self.datamapper.addMapping(self.lblPacketFolder, 0, "text")  # "text" property name must be added for QLabel to work with QDataWidgetmapper
        self.datamapper.addMapping(self.inpProductId, 1)
        self.datamapper.addMapping(self.inpProductName, 2)
        self.datamapper.addMapping(self.editDesc, 3)
        self.datamapper.addMapping(self.editAdvice, 4)
        self.datamapper.addMapping(self.cmbProductType, 5)
        self.datamapper.addMapping(self.inpProductVer, 6)
        self.datamapper.addMapping(self.inpPackageVer, 7)
        self.datamapper.addMapping(self.sldPrio, 8)
        self.datamapper.addMapping(self.cmbLicense, 9)
        self.datamapper.addMapping(self.inpScrSetup, 10)
        self.datamapper.addMapping(self.inpScrUninstall, 11)
        self.datamapper.addMapping(self.inpScrUpdate, 12)
        self.datamapper.addMapping(self.inpScrAlways, 13)
        self.datamapper.addMapping(self.inpScrOnce, 14)
        self.datamapper.addMapping(self.inpScrCustom, 15)
        self.datamapper.addMapping(self.inpScrUserLogin, 16)
        self.datamapper.toFirst()

        self.logger.debug("Create data widget mapper for dependencies")
        self.datamapper_dependencies = QDataWidgetMapper(self)
        self.datamapper_dependencies.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.datamapper_dependencies.setModel(self._parent.model_dependencies)
        self.datamapper_dependencies.addMapping(self.cmbDepAction, 0)
        self.datamapper_dependencies.addMapping(self.cmbDepProdID, 1)
        self.datamapper_dependencies.addMapping(self.cmbDepReqAction, 2)
        self.datamapper_dependencies.addMapping(self.cmbDepInstState, 3)
        self.datamapper_dependencies.addMapping(self.cmbDepRequirement, 4)
        self.datamapper_dependencies.toFirst()

        self.logger.debug("Create data widget mapper for properties")
        self.datamapper_properties = QDataWidgetMapper(self)
        self.datamapper_properties.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.datamapper_properties.setModel(self._parent.model_properties)
        self.datamapper_properties.addMapping(self.inpPropName, 0)
        self.datamapper_properties.addMapping(self.cmbPropType, 1)
        self.datamapper_properties.addMapping(self.cmbPropMulti, 2)
        self.datamapper_properties.addMapping(self.cmbPropEdit, 3)
        self.datamapper_properties.addMapping(self.inpPropDesc, 4)
        self.datamapper_properties.addMapping(self.inpPropVal, 5)
        self.datamapper_properties.addMapping(self.inpPropDef, 6)
        self.datamapper_properties.addMapping(self.cmbPropDef, 6)
        self.datamapper_properties.toFirst()

    def connect_signals(self):
        """Connect signals and slots"""
        self.logger.debug("Connect signals")
        self.actionNew.triggered.connect(self.new_project)
        self.actionOpen.triggered.connect(self.open_project)
        self.actionClose.triggered.connect(self._parent.project_close)
        self.actionQuit.triggered.connect(self.close)
        self.actionSave.triggered.connect(self._parent.save_project)
        self.actionSettings.triggered.connect(self.settingsCtr.ui.exec)
        self.actionShowLog.triggered.connect(self.showLogRequested.emit)
        self.actionSaveAs.triggered.connect(self.not_working)
        self.actionStartWinst.triggered.connect(self.not_working)
        self.actionScriptEditor.triggered.connect(self.not_working)
        self.actionHelp.triggered.connect(self.not_working)
        self.actionSearchForUpdates.triggered.connect(self.not_working)
        self.actionShowChangeLog.triggered.connect(self.not_working)
        self.actionAbout.triggered.connect(self.not_working)

        if oPB.NETMODE != "offline":
            # connect online menu action signals
            self.actionSetRights.triggered.connect(self._parent.do_setrights)
            self.actionInstall.triggered.connect(self.quickinstall)
            self.actionUpload.triggered.connect(self.upload)
            self.actionScheduler.triggered.connect(self._parent.scheduler_dialog)
            self.actionUninstall.triggered.connect(self.quickuninstall)
            self.actionDeploy.triggered.connect(self._parent.deployagent_dialog)
            self.actionBundleCreation.triggered.connect(self.not_working)
            self.actionDepotManager.triggered.connect(self._parent.depotmanager_dialog)
        else:
            # connect online menu action signals
            self.actionSetRights.triggered.connect(self.offline)
            self.actionInstall.triggered.connect(self.offline)
            self.actionUpload.triggered.connect(self.offline)
            self.actionScheduler.triggered.connect(self.offline)
            self.actionUninstall.triggered.connect(self.offline)
            self.actionDeploy.triggered.connect(self.offline)
            self.actionBundleCreation.triggered.connect(self.offline)
            self.actionDepotManager.triggered.connect(self.offline)

        # buttons
        self.btnSave.clicked.connect(self._parent.save_project)
        self.btnChangelogEdit.clicked.connect(self._parent.show_changelogeditor)
        self.btnShowScrStruct.clicked.connect(self._parent.show_script_structure)

        self.btnScrSetup.clicked.connect(lambda: self.select_script_dialog("setup"))
        self.btnScrUninstall.clicked.connect(lambda: self.select_script_dialog("uninstall"))
        self.btnScrUpdate.clicked.connect(lambda: self.select_script_dialog("update"))
        self.btnScrAlways.clicked.connect(lambda: self.select_script_dialog("always"))
        self.btnScrOnce.clicked.connect(lambda: self.select_script_dialog("once"))
        self.btnScrCustom.clicked.connect(lambda: self.select_script_dialog("custom"))
        self.btnScrUserLogin.clicked.connect(lambda: self.select_script_dialog("userlogin"))
        self.btnScrSetupDel.clicked.connect(lambda: self.select_script_dialog("setup", False))
        self.btnScrUninstallDel.clicked.connect(lambda: self.select_script_dialog("uninstall", False))
        self.btnScrUpdateDel.clicked.connect(lambda: self.select_script_dialog("update", False))
        self.btnScrAlwaysDel.clicked.connect(lambda: self.select_script_dialog("always", False))
        self.btnScrOnceDel.clicked.connect(lambda: self.select_script_dialog("once", False))
        self.btnScrCustomDel.clicked.connect(lambda: self.select_script_dialog("custom", False))
        self.btnScrUserLoginDel.clicked.connect(lambda: self.select_script_dialog("userlogin", False))
        self.btnScrSetupEdit.clicked.connect(self.not_working)
        self.btnScrUninstallEdit.clicked.connect(self.not_working)
        self.btnScrUpdateEdit.clicked.connect(self.not_working)
        self.btnScrAlwaysEdit.clicked.connect(self.not_working)
        self.btnScrOnceEdit.clicked.connect(self.not_working)
        self.btnScrCustomEdit.clicked.connect(self.not_working)
        self.btnScrUserLoginEdit.clicked.connect(self.not_working)

        if oPB.NETMODE != "offline":
            self.btnBuild.clicked.connect(self._parent.project_build)
            self.btnInstall.clicked.connect(self._parent.do_install)
            self.btnInstSetup.clicked.connect(self._parent.do_installsetup)
            self.btnUninstall.clicked.connect(self._parent.do_uninstall)
        else:
            self.btnBuild.clicked.connect(self.offline)
            self.btnInstall.clicked.connect(self.offline)
            self.btnInstSetup.clicked.connect(self.offline)
            self.btnUninstall.clicked.connect(self.offline)

        self.btnDevFolder.clicked.connect(self.open_project_folder)

        self.btnDepAdd.clicked.connect(self._parent.add_dependency)
        self.btnDepModify.clicked.connect(self.submit_dependencies)
        self.btnDepDelete.clicked.connect(lambda a: self._parent.remove_dependency(self.tblDependencies.selectionModel().currentIndex().row()))

        self.btnPropAdd.clicked.connect(self._parent.add_property)
        self.btnPropModify.clicked.connect(self.submit_properties)
        self.btnPropDelete.clicked.connect(lambda a: self._parent.remove_property(self.tblProperties.selectionModel().currentIndex().row()))
        self.btnPropRead.clicked.connect(self._parent.get_properties_from_scripts)

        self.tblProperties.setModel(self._parent.model_properties)
        self.tblDependencies.setModel(self._parent.model_dependencies)
        self.tblDependencies.selectionModel().selectionChanged.connect(self.update_dependency_fields)
        self.tblProperties.selectionModel().selectionChanged.connect(self.update_property_fields)

        self._parent.modelDataUpdated.connect(self.reset_datamapper_and_display)
        self._parent.msgSend.connect(self.set_statbar_text)
        self._parent.processingStarted.connect(self.splash.show_)
        self._parent.processingEnded.connect(self.splash.close)
        self._parent.processingEnded.connect(self.set_button_state)

    def connect_validators(self):
        """Connect field validators"""
        self.logger.debug("Connect validators to fields")
        # set validators
        if ConfigHandler.cfg.age == "True":
            self.set_regex_validator(self.inpProductId, oPB.OPB_PRODUCT_ID_REGEX_NEW)
            self.set_regex_validator(self.cmbDepProdID, oPB.OPB_PRODUCT_ID_REGEX_NEW)
            self.set_regex_validator(self.inpPropName, oPB.OPB_PROPERTY_REGEX_NEW)
        else:
            self.set_regex_validator(self.inpProductId, oPB.OPB_PRODUCT_ID_REGEX_OLD)
            self.set_regex_validator(self.cmbDepProdID, oPB.OPB_PRODUCT_ID_REGEX_OLD)
            self.set_regex_validator(self.inpPropName, oPB.OPB_PROPERTY_REGEX_OLD)

        # product id
        self.inpProductId.textChanged.connect(self.check_state)
        self.inpProductId.textChanged.emit(self.inpProductId.text())
        self.inpProductId.textChanged.connect(self.set_button_state)

        self.cmbDepProdID.editTextChanged.connect(self.check_state)
        self.cmbDepProdID.editTextChanged.emit(self.cmbDepProdID.currentText())
        # property names
        self.inpPropName.textChanged.connect(self.check_state)
        self.inpPropName.textChanged.emit(self.inpPropName.text())

        # product version
        self.set_regex_validator(self.inpProductVer, oPB.OPB_PRODUCT_VER_REGEX)
        self.inpProductVer.textChanged.connect(self.check_state)
        self.inpProductVer.textChanged.emit(self.inpProductVer.text())
        self.inpProductVer.textChanged.connect(self.set_button_state)

        # package version
        self.set_regex_validator(self.inpPackageVer, oPB.OPB_PACKAGE_VER_REGEX)
        self.inpPackageVer.textChanged.connect(self.check_state)
        self.inpPackageVer.textChanged.emit(self.inpPackageVer.text())
        self.inpPackageVer.textChanged.connect(self.set_button_state)

        # script validator
        self.set_scriptfile_validator(self.inpScrSetup)
        self.inpScrSetup.textChanged.connect(self.check_state)
        self.inpScrSetup.textChanged.emit(self.inpScrSetup.text())
        self.set_scriptfile_validator(self.inpScrUninstall)
        self.inpScrUninstall.textChanged.connect(self.check_state)
        self.inpScrUninstall.textChanged.emit(self.inpScrUninstall.text())
        self.set_scriptfile_validator(self.inpScrUpdate)
        self.inpScrUpdate.textChanged.connect(self.check_state)
        self.inpScrUpdate.textChanged.emit(self.inpScrUpdate.text())
        self.set_scriptfile_validator(self.inpScrAlways)
        self.inpScrAlways.textChanged.connect(self.check_state)
        self.inpScrAlways.textChanged.emit(self.inpScrAlways.text())
        self.set_scriptfile_validator(self.inpScrOnce)
        self.inpScrOnce.textChanged.connect(self.check_state)
        self.inpScrOnce.textChanged.emit(self.inpScrOnce.text())
        self.set_scriptfile_validator(self.inpScrCustom)
        self.inpScrCustom.textChanged.connect(self.check_state)
        self.inpScrCustom.textChanged.emit(self.inpScrCustom.text())
        self.set_scriptfile_validator(self.inpScrUserLogin)
        self.inpScrUserLogin.textChanged.connect(self.check_state)
        self.inpScrUserLogin.textChanged.emit(self.inpScrUserLogin.text())
        # special combobox checker
        self.cmbDepReqAction.currentIndexChanged.connect(self.check_combobox_selection)
        self.cmbDepInstState.currentIndexChanged.connect(self.check_combobox_selection)
        self.cmbPropType.currentIndexChanged.connect(self.check_combobox_selection)

    @pyqtSlot()
    def not_working(self):
        self._parent.msgbox(translate("MainWindow", "Sorry, this function doesn't work at the moment!"), oPB.MsgEnum.MS_ALWAYS, self)

    @pyqtSlot()
    def offline(self):
        self._parent.msgbox(translate("MainWindow", "You are working in offline mode. Functionality not available!"), oPB.MsgEnum.MS_ALWAYS, self)

    @pyqtSlot()
    def quickinstall(self):
        self.logger.debug("Quick install package")

        ext = "opsi Package (*.opsi;)"  # generate file extension selection string for dialog

        script = QFileDialog.getOpenFileName(self, translate("MainWindow", "Choose package file"),
                                            "", ext)

        if not script == ("", ""):
            self.logger.debug("Selected package: " + script[0])
            self._parent.startup.hide_me()
            self._parent.do_quickinstall(script[0])
            self._parent.startup.show_me()
        else:
            self.logger.debug("Dialog aborted.")

    @pyqtSlot()
    def quickuninstall(self):
        """Open quickuninstall dialog"""
        self._parent.quickuninstall.show_()

    @pyqtSlot()
    def upload(self):
        self.logger.debug("Upload package")

        ext = "opsi Package (*.opsi;)"  # generate file extension selection string for dialog

        script = QFileDialog.getOpenFileName(self, translate("MainWindow", "Choose package file"),
                                            "", ext)

        if not script == ("", ""):
            self.logger.debug("Selected package: " + script[0])
            self._parent.startup.hide_me()
            self._parent.do_upload(script[0])
            self._parent.startup.show_me()
        else:
            self.logger.debug("Dialog aborted.")

    @pyqtSlot()
    def set_button_state(self):
        self.logger.debug("Set button state")
        if self.isFileAvailable():
            self.btnInstall.setEnabled(True)
            self.btnInstSetup.setEnabled(True)
        else:
            self.btnInstall.setEnabled(False)
            self.btnInstSetup.setEnabled(False)

    def isFileAvailable(self):
        pack = self.lblPacketFolder.text().replace("\\","/") + "/" + self.inpProductId.text() + \
               "_" + self.inpProductVer.text() + "-" + self.inpPackageVer.text() + ".opsi"
        return os.path.isfile(pack)

    @pyqtSlot(int)
    def reset_datamapper_and_display(self, tabIdx = 0):
        """Reset tables and fields"""
        self.logger.debug("Reset datamapper and display")

        # select first row in mapped model
        self.datamapper.toFirst()
        self.tblProperties.selectRow(0)
        self.tblDependencies.selectRow(0)

        self.tblDependencies.resizeRowsToContents()
        self.tblProperties.resizeRowsToContents()

        self.tabWidget.setCurrentIndex(tabIdx)
        self.set_dev_folder()

    @pyqtSlot(QtCore.QItemSelection)
    def update_dependency_fields(self, idx:QtCore.QItemSelection):
        # indexes() returns list of selected items
        # as we only have 1 at a time, return first item and get corresponding row number
        self.logger.debug("Update dependency fields")
        if not idx.indexes() == []:
            row = idx.indexes()[0].row()
            self.datamapper_dependencies.setCurrentIndex(row)
        else:
            self.datamapper_dependencies.toFirst()

    @pyqtSlot(QtCore.QItemSelection)
    def update_property_fields(self, idx:QtCore.QItemSelection):
        # indexes() returns list of selected items
        # as we only have 1 at a time, return first item and get corresponding row number
        self.logger.debug("Update property fields")
        if not idx.indexes() == []:
            row = idx.indexes()[0].row()
            if self._parent.model_properties.item(row, 1).text() == 'bool':
                self.datamapper_properties.removeMapping(self.inpPropDef)
                self.datamapper_properties.addMapping(self.cmbPropDef, 6)
                self.inpPropVal.setEnabled(False)
                self.inpPropDef.setEnabled(False)
                self.cmbPropMulti.setEnabled(False)
                self.cmbPropEdit.setEnabled(False)
                self.cmbPropDef.setEnabled(True)
            else:
                self.datamapper_properties.addMapping(self.inpPropDef, 6)
                self.datamapper_properties.removeMapping(self.cmbPropDef)
                self.inpPropVal.setEnabled(True)
                self.inpPropDef.setEnabled(True)
                self.cmbPropMulti.setEnabled(True)
                self.cmbPropEdit.setEnabled(True)
                self.cmbPropDef.setEnabled(False)
            self.datamapper_properties.setCurrentIndex(row)
        else:
            self.datamapper_properties.toFirst()

    @pyqtSlot()
    def submit_properties(self):
        """
        Submit changes in property edit widgets to model
        and update fields again
        """
        self.logger.debug("Submit properties")
        self.datamapper_properties.submit()
        selection = self.tblProperties.selectionModel().selection()
        self.update_property_fields(selection)

    @pyqtSlot()
    def submit_dependencies(self):
        """
        Submit changes in dependency edit widgets to model
        and update fields again
        """
        self.logger.debug("Submit dependencies")
        self.datamapper_dependencies.submit()
        selection = self.tblDependencies.selectionModel().selection()
        self.update_dependency_fields(selection)

    @pyqtSlot()
    def set_dev_folder(self):
        """Set special label text"""
        self.lblDevFolder.setText(ConfigHandler.cfg.dev_dir)

    @pyqtSlot()
    def open_project(self):
        """
        Opens a folder selection dialog and emits selected folder name via Signal projectLoadRequested
        """
        self.logger.debug("Open project dialog")
        directory = QFileDialog.getExistingDirectory(self, translate("MainWindow", "Open project"),
                                                     ConfigHandler.cfg.dev_dir, QFileDialog.ShowDirsOnly)

        # sometimes window disappears into background, force to front
        self.activateWindow()

        if not directory == "":
            self.logger.info("Chosen existing project directory: " + directory)
            self._parent.project_load(directory)
        else:
            self.logger.debug("Dialog aborted.")

    @pyqtSlot()
    def open_recent_project(self):
        action = self.sender()
        if action:
            self.logger.debug("Chosen recent project: " + action.data())
            self._parent.project_close()
            self._parent.project_load(action.data())

    @pyqtSlot()
    def new_project(self):
        """
        Opens a folder selection dialog and emits selected folder name via Signal projectNewRequested
        """
        self.logger.debug("New project dialog")
        directory = QFileDialog.getExistingDirectory(self, translate("MainWindow", "Create new project"),
                                                     ConfigHandler.cfg.dev_dir, QFileDialog.ShowDirsOnly)

        # sometimes window disappears into background, force to front
        self.activateWindow()

        if not directory == "":
            self.logger.info("Chosen directory for new project: " + directory)
            self._parent.project_create(directory)
        else:
            self.logger.debug("Dialog aborted.")

    def closeEvent(self, event):
        """Delegate closeEvent handling to parent controller"""
        self._parent.quit_application(event)

    def moveEvent(self, *args, **kwargs):
        """Send signal if main window is moved"""
        self.windowMoved.emit()

    def resizeEvent(self, *args, **kwargs):
        """Send signal if main window is resized"""
        self.windowMoved.emit()

    def open_project_folder(self):
        self.logger.debug("Open project folder" + platform.system())
        if platform.system() in ["Windows", "Linux"]:
            webbrowser.open(self.lblPacketFolder.text())
        elif platform.system() == "Darwin":
            webbrowser.open("file://" + self.lblPacketFolder.text())

    @pyqtSlot()
    def select_script_dialog(self, script_type, setvalue = True):
        """
        Opens a dialog to select a script file / Clear field content

        :param script_type: field type identifier (setup, uninstall, update, always, once, custom, userlogin)
        :param setvalue: set new value = True, empty field only = False
        """
        self.logger.debug("Select script dialog")

        ext = "Scripts (" + "; ".join(["*." + x for x in oPB.SCRIPT_EXT]) + ")"  # generate file extension selection string for dialog

        if setvalue:
            if self.lblPacketFolder.text() == "":
                script = QFileDialog.getOpenFileName(self, translate("MainWindow", "Choose script"),
                                                     ConfigHandler.cfg.dev_dir, ext)
            else:
                script = QFileDialog.getOpenFileName(self, translate("MainWindow", "Choose script"),
                                                     Helper.concat_path_and_file(self.lblPacketFolder.text(), "CLIENT_DATA"), ext)

            if not script == ("", ""):
                self._parent.set_selected_script(script[0], script_type)
        else:
            self._parent.set_selected_script("", script_type)

    """
    @pyqtSlot()
    def get_inputfield_and_value(self):
        field = self.sender()
        if type(field) is QPlainTextEdit:
            print(field.objectName() + ": " + field.toPlainText())
        if type(field) is QLineEdit:
            print(field.objectName() + ": " + field.text())
    """

    @pyqtSlot()
    def check_state(self, *args, **kwargs):
        """Sets background color of QLineEdit depending on validator state"""
        sender = self.sender()
        validator = sender.validator()

        # get validator state
        if type(sender) == QLineEdit:
            state = validator.validate(sender.text(), 0)[0]
        elif type(sender) == QComboBox:
            state = validator.validate(sender.currentText(), 0)[0]

        # associate state with color
        if state == QtGui.QValidator.Acceptable: # ACC
            colStat = "ACC"
        elif state == QtGui.QValidator.Intermediate: # INT
            colStat = "INT"
        else:
            colStat = "ERR"
            if type(validator) == ScriptFileValidator:
                self._parent.msgbox(sender.text() + "@@" +
                            translate("MainWindow", "The script has to be inside the CLIENT_DATA folder of the package!"),
                            oPB.MsgEnum.MS_ERR)

        # set background color according to state into dynamic field property
        sender.setProperty("checkState", colStat)
        sender.style().unpolish(sender)
        sender.style().polish(sender)
        sender.update()

    @pyqtSlot(str, str)
    def set_statbar_text(self, msg):
        """Sets status bar text"""
        self.oPB_statBar.showMessage(msg.replace("<br>", " ").strip(), 0)

    @pyqtSlot(int)
    def check_combobox_selection(self, value):
        """Check combobox status and update ui (set widgets enabled/disabled accordingly)"""
        if self.sender() == self.cmbDepReqAction:
            if value != 0: self.cmbDepInstState.setCurrentIndex(0)
        elif self.sender() == self.cmbDepInstState:
            if value != 0: self.cmbDepReqAction.setCurrentIndex(0)
        elif self.sender() == self.cmbPropType:
            if value == 1:
                self.inpPropVal.setText("")
                self.inpPropDef.setText("")
                self.datamapper_properties.addMapping(self.cmbPropDef, 6)
                self.datamapper_properties.removeMapping(self.inpPropDef)
                self.cmbPropMulti.setCurrentIndex(0)
                self.cmbPropEdit.setCurrentIndex(0)
                self.inpPropVal.setEnabled(False)
                self.inpPropDef.setEnabled(False)
                self.cmbPropMulti.setEnabled(False)
                self.cmbPropEdit.setEnabled(False)
                self.cmbPropDef.setEnabled(True)
                self.cmbPropDef.setCurrentIndex(0)
            else:
                self.datamapper_properties.addMapping(self.inpPropDef, 6)
                self.datamapper_properties.removeMapping(self.cmbPropDef)
                self.inpPropVal.setEnabled(True)
                self.inpPropDef.setEnabled(True)
                self.cmbPropMulti.setEnabled(True)
                self.cmbPropEdit.setEnabled(True)
                self.cmbPropDef.setEnabled(False)

    def set_regex_validator(self, field, regex):
        """
        Set validator for input field

        :param field: field to validate
        :param regex: regular expression
        """
        valexp = QtCore.QRegExp(regex)
        validator = QtGui.QRegExpValidator(valexp)
        field.setValidator(validator)

    def set_scriptfile_validator(self, field):
        """
        Assign file validator to field

        :param field: field to validate
        """
        validator = ScriptFileValidator(self, field)
        field.setValidator(validator)

class ScriptFileValidator(QtGui.QValidator):
    """
    Validator to check for existing files

    (Constructor has to be called with parent and field,
    because validate() needs to access some values from
    different window elements.)
    """

    def __init__(self, parent, field):
        """
        Constructor of ScriptFileValidator

        :param parent: parent window
        :param field: field object to validate
        """
        super().__init__(parent)
        self._parent = parent
        self._field = field

    def validate(self, p_str, p_int):
        if p_str == "":
            return ScriptFileValidator.Intermediate, p_str, p_int
        if os.path.exists(Helper.concat_path_and_file(self._parent.lblPacketFolder.text().replace('\\','/') + "/CLIENT_DATA/", p_str)):
            return ScriptFileValidator.Acceptable, p_str, p_int
        else:
            return ScriptFileValidator.Invalid, p_str, p_int

class Splash(LogMixin):
    def __init__(self, parent, msg, withProgressbar = False):
        self._parent = parent
        self.isHidden = True
        self._progress = 0

        pixmap = QtGui.QPixmap(380, 100)
        pixmap.fill(QtGui.QColor("darkgreen"))

        self._splash = QSplashScreen(pixmap)
        self._splash.setParent(self._parent)
        self._splash.showMessage(msg, QtCore.Qt.AlignCenter, QtCore.Qt.white)

        self._progressBar = None

        if withProgressbar == True:
            self.add_progressbar()

    def add_progressbar(self):
        self._progressBar = QProgressBar(self._splash)
        self._progressBar.setGeometry(self._splash.width() / 10, 8 * self._splash.height() / 10,
                               8 * self._splash.width() / 10, self._splash.height() / 10)

    def setProgress(self, val: int):
        if self.isHidden is True:
            self.isHidden = False
            self.show_()
        self.progress = val
        try:
            self._progressBar.setValue(self.progress)
        except:
            pass

    def incProgress(self, val: int):
        if self.isHidden is True:
            self.isHidden = False
            self.show_()
        self.progress = self.progress + val
        try:
            self.logger.debug("Set progress: " + str(self.progress))
            self._progressBar.setValue(self.progress)
        except:
            pass

    def setParent(self, parent):
        self._parent = parent
        self._splash.setParent(parent)

    @pyqtSlot()
    def close(self):
        self.logger.debug("Hide splash, parent: " + str(self._parent))
        self.isHidden = True
        self._splash.close()

    @pyqtSlot()
    def show_(self):
        self.logger.debug("Show splash, parent: " + str(self._parent))
        try:
            parentUi = self._parent.centralwidget.geometry()  # need to use centralwidget for linux
        except:
            parentUi = self._parent.childrenRect()  # need to use centralwidget for linux

        mysize = self._splash.geometry()

        hpos = parentUi.x() + ((parentUi.width() - mysize.width()) / 2)
        vpos = parentUi.y() + ((parentUi.height() - mysize.height()) / 2)

        self._splash.move(hpos, vpos)
        self._splash.show()

        qApp.processEvents()

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        # create new exception handling vor properties
        # if (value != "True") and (value != "False"):
        #    raise ValueError("describe exception")
        if value > 100:
            value = 0
        if value < 0:
            value = 0
        self._progress = value

