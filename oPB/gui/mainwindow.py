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
import subprocess
import tempfile
from urllib import request, parse

from configparser import ConfigParser
#from subprocess import Popen, PIPE, STDOUT
from time import sleep

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot

import oPB
import oPB.gui.helpviewer
from oPB.core.confighandler import ConfigHandler
from oPB.core.tools import Helper, LogMixin
from oPB.gui.splash import Splash
from oPB.gui.utilities import ScriptFileValidator, EventMixin
from oPB.ui.ui import MainWindowBase, MainWindowUI

translate = QtCore.QCoreApplication.translate


class MainWindow(MainWindowBase, MainWindowUI, LogMixin, EventMixin):

    showLogRequested = pyqtSignal()
    windowMoved = pyqtSignal()

    MaxRecentFiles = 5

    def __init__(self, parent):
        """
        Constructor of MainWindow

        :param parent: parent
        :return:
        """
        self._parent = parent
        print("\tgui/MainWindow parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None

        MainWindowBase.__init__(self)
        self.setupUi(self)

        self.recentFileActions = []

        if oPB.NETMODE == "offline":
            self.setWindowTitle("opsiPackageBuilder ( OFFLINE MODE )")

        self.datamapper = None             # QDataWidgetMapper object for field mapping
        self.datamapper_dependencies = None
        self.datamapper_properties = None

        self.splash = Splash(self, translate("MainWindow", "Please wait..."))
        self.splash.close()  # only for linux

        self.create_datamapper()
        self.connect_signals()
        self.connect_validators()

        self.reset_datamapper_and_display(0)
        self.fill_cmbDepProdID()

    def init_recent(self):
        """Init recent files menu items"""
        for i in range(MainWindow.MaxRecentFiles):
                    self.recentFileActions.append(
                            QAction(self, visible=False,
                                    triggered=self.open_recent_project))
        for i in range(MainWindow.MaxRecentFiles):
                    self.menuRecent.addAction(self.recentFileActions[i])
                    self._parent.startup.menuRecent.addAction(self.recentFileActions[i])

        self.update_recent_file_actions()

    def update_recent_file_actions(self):
        """Update recent file menu actions"""
        files = ConfigHandler.cfg.recent

        numRecentFiles = min(len(files), MainWindow.MaxRecentFiles)

        for i in range(numRecentFiles):
            text = "&%d %s" % (i + 1, self.stripped_name(files[i]))
            self.recentFileActions[i].setText(text)
            self.recentFileActions[i].setData(files[i])
            self.recentFileActions[i].setVisible(True)

        for j in range(numRecentFiles, MainWindow.MaxRecentFiles):
            self.recentFileActions[j].setVisible(False)

    def stripped_name(self, fullFileName):
        """
        Remove any path component from ``fullFileName``

        :param fullFileName: complete path of file or folder
        :return: last path part
        """
        return QtCore.QFileInfo(fullFileName).fileName()

    def set_current_project(self, project):
        """
        Insert current project into recent files list
        :param project: project name
        """
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
        self.logger.debug("Connect signals")
        self.actionNew.triggered.connect(self.new_project)
        self.actionOpen.triggered.connect(self.open_project)
        self.actionClose.triggered.connect(self._parent.project_close)
        self.actionQuit.triggered.connect(self.close)
        self.actionSave.triggered.connect(self._parent.project_save)
        self.actionShowLog.triggered.connect(self.showLogRequested.emit)
        self.actionSaveAs.triggered.connect(self.save_as)
        self.actionStartWinst.triggered.connect(self.start_winst)
        self.actionScriptEditor.triggered.connect(self.open_scripteditor)
        self.actionHelp.triggered.connect(lambda: oPB.gui.helpviewer.Help(oPB.HLP_FILE, oPB.HLP_PREFIX))
        #self.actionSearchForUpdates.triggered.connect(self.update_check)
        self.actionSearchForUpdates.triggered.connect(self.not_working)
        self.actionShowChangeLog.triggered.connect(lambda: oPB.gui.helpviewer.Help(oPB.HLP_FILE, oPB.HLP_PREFIX, oPB.HLP_DST_CHANGELOG))
        self.actionAbout.triggered.connect(self.not_working)

        if oPB.NETMODE != "offline":
            # connect online menu action signals
            self.actionSetRights.triggered.connect(self._parent.do_setrights)
            self.actionInstall.triggered.connect(self.quickinstall)
            self.actionUpload.triggered.connect(self.upload)
            self.actionScheduler.triggered.connect(self._parent.scheduler_dialog)
            self.actionUninstall.triggered.connect(self._parent.quickuninstall_dialog)
            self.actionDeploy.triggered.connect(self._parent.deployagent_dialog)
            self.actionBundleCreation.triggered.connect(self._parent.bundle_dialog)
            self.actionDepotManager.triggered.connect(self._parent.depotmanager_dialog)
            self.actionImport.triggered.connect(self.package_import)
        else:
            # connect online menu action signals
            self.actionSetRights.triggered.connect(self.offline)
            self.actionInstall.triggered.connect(self.offline)
            self.actionUpload.triggered.connect(self.offline)
            self.actionScheduler.triggered.connect(self.offline)
            self.actionUninstall.triggered.connect(self.offline)
            self.actionDeploy.triggered.connect(self.offline)
            self.actionBundleCreation.triggered.connect(self.offline)
            self.actionImport.triggered.connect(self.offline)

        # buttons
        self.btnSave.clicked.connect(self._parent.project_save)
        self.btnChangelogEdit.clicked.connect(self._parent.show_changelogeditor)
        self.btnShowScrStruct.clicked.connect(self._parent.show_scripttree)
        self.btnHelpPacket.clicked.connect(lambda: oPB.gui.helpviewer.Help(oPB.HLP_FILE, oPB.HLP_PREFIX, oPB.HLP_DST_TABPACKET))
        self.btnHelpDependencies.clicked.connect(lambda: oPB.gui.helpviewer.Help(oPB.HLP_FILE, oPB.HLP_PREFIX, oPB.HLP_DST_TABDEPEND))
        self.btnHelpProperties.clicked.connect(lambda: oPB.gui.helpviewer.Help(oPB.HLP_FILE, oPB.HLP_PREFIX, oPB.HLP_DST_TABPROP))

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
        self.btnScrSetupEdit.clicked.connect(self.open_scripteditor)
        self.btnScrUninstallEdit.clicked.connect(self.open_scripteditor)
        self.btnScrUpdateEdit.clicked.connect(self.open_scripteditor)
        self.btnScrAlwaysEdit.clicked.connect(self.open_scripteditor)
        self.btnScrOnceEdit.clicked.connect(self.open_scripteditor)
        self.btnScrCustomEdit.clicked.connect(self.open_scripteditor)
        self.btnScrUserLoginEdit.clicked.connect(self.open_scripteditor)

        if oPB.NETMODE != "offline":
            self.btnBuild.clicked.connect(self._parent.project_build)
            self.btnInstall.clicked.connect(lambda: self._parent.do_install(depot = self._parent.query_depot(parent = self)))
            self.btnInstSetup.clicked.connect(lambda: self._parent.do_installsetup(depot = self._parent.query_depot(parent = self)))
            self.btnUninstall.clicked.connect(lambda: self._parent.do_uninstall(depot = self._parent.query_depot(parent = self)))
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
        self._parent.progressChanged.connect(self.splash.incProgress)
        self._parent.processingEnded.connect(self.splash.close)
        self._parent.processingEnded.connect(self.set_button_state)

    def connect_validators(self):
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

    def fill_cmbDepProdID(self):
        """Fill combobox with values from opsi_depot share"""
        self.cmbDepProdID.clear()

        if oPB.NETMODE != "offline":
            try:
                subpath = "\\\\" + ConfigHandler.cfg.opsi_server + "\\" + oPB.DEPOTSHARE_BASE
                subdirs = Helper.get_subdirlist(subpath)
                subdirs.sort()

                for elem in subdirs:
                    self.cmbDepProdID.addItem(elem)
            except:
                pass

    @pyqtSlot()
    def not_working(self):
        """Show a short "Not working" message"""
        self._parent.msgbox(translate("MainWindow", "Sorry, this function doesn't work at the moment!"), oPB.MsgEnum.MS_ALWAYS, self)

    @pyqtSlot()
    def offline(self):
        """Show offline message"""
        self._parent.msgbox(translate("MainWindow", "You are working in offline mode. Functionality not available!"), oPB.MsgEnum.MS_ALWAYS, self)

    @pyqtSlot()
    def start_winst(self):
        """Start opsi winst32"""
        self.logger.debug("Start Winst under " + platform.system())
        if platform.system() in ["Windows"]:
            if os.path.exists(oPB.OPB_WINST_NT):
                subprocess.call([oPB.OPB_WINST_NT, self.lblPacketFolder.text().replace("\\","/")])
            else:
                self._parent.msgbox(translate("MainWindow", "Local opsi-winst installation not found or client-agent not installed!"), oPB.MsgEnum.MS_ERR, self)
        else:
            self._parent.msgbox(translate("MainWindow", "Function not available at the moment for system:" + " " + platform.system()), oPB.MsgEnum.MS_ALWAYS, self)

    @pyqtSlot()
    def open_scripteditor(self):
        """
        Open configured script editor.

        Method reaction depends on calling widget (self.sender())
        """
        self.logger.debug("Start scripteditor")

        if ConfigHandler.cfg.editor_intern == "True":
            self._parent.msgbox(translate("MainWindow", "Internal editor not available at the moment. Use external editor instead!"), oPB.MsgEnum.MS_ALWAYS, self)
            self.actionSettings.trigger()
            return

        if os.path.exists(ConfigHandler.cfg.scripteditor):
            path = Helper.concat_path_native(self.lblPacketFolder.text(), "CLIENT_DATA")
            if self.sender() == self.btnScrSetupEdit:
                if self.inpScrSetup.text().strip() == "":
                    script = "setup.opsiscript"
                else:
                    script = self.inpScrSetup.text()
            elif self.sender() == self.btnScrUninstallEdit:
                if self.inpScrUninstall.text().strip() == "":
                    script = "uninstall.opsiscript"
                else:
                    script = self.inpScrUninstall.text()
            elif self.sender() == self.btnScrUpdateEdit:
                if self.inpScrUpdate.text().strip() == "":
                    script = "update.opsiscript"
                else:
                    script = self.inpScrUpdate.text()
            elif self.sender() == self.btnScrAlwaysEdit:
                if self.inpScrAlways.text().strip() == "":
                    script = "always.opsiscript"
                else:
                    script = self.inpScrAlways.text()
            elif self.sender() == self.btnScrOnceEdit:
                if self.inpScrOnce.text().strip() == "":
                    script = "once.opsiscript"
                else:
                    script = self.inpScrOnce.text()
            elif self.sender() == self.btnScrCustomEdit:
                if self.inpScrCustom.text().strip() == "":
                    script = "custom.opsiscript"
                else:
                    script = self.inpScrCustom.text()
            elif self.sender() == self.btnScrUserLoginEdit:
                if self.inpScrUserLogin.text().strip() == "":
                    script = "userlogin.opsiscript"
                else:
                    script = self.inpScrUserLogin.text()
            elif self.sender() == self.actionScriptEditor:
                script = "new.opsiscript"

            # script editor from menu
            if path != "" and script != "":
                path = Helper.concat_path_native(path, script)

            self.logger.debug("Opening script: " + path)
            # construct calling array
            # first add basic scripteditor executable
            cmd = [ConfigHandler.cfg.scripteditor]
            # if there are options, split and append them
            if (ConfigHandler.cfg.editor_options).strip() != "":
                for part in (ConfigHandler.cfg.editor_options).split():
                    cmd.append(part)
                # if attach direct is true, combine last option with script file path
                if ConfigHandler.cfg.editor_attachdirect == "True":
                    cmd[-1] = cmd[-1] + path
                # or else, append as separate value to list
                else:
                    cmd.append(path)
            else:
                cmd.append(path)

            self.logger.debug("Executing subprocess: " + str(cmd))
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            outs, errs = proc.communicate()
            self.logger.info(outs)
            self.logger.error(errs)
            if proc.returncode != 0 and proc.returncode != 555:
                self._parent.msgbox(translate("MainWindow", "Editor startup did not cleanup correctly.\n\nThe following message(s) returned:") +
                                    "\n\nStandard Out:\n" + outs +
                                    "\nStandard Err:\n" + errs +
                                    "\n\nReturn code: " + str(proc.returncode),
                                    oPB.MsgEnum.MS_WARN, self)
        else:
            self._parent.msgbox(translate("MainWindow", "Editor not found:" + " " + ConfigHandler.cfg.scripteditor), oPB.MsgEnum.MS_ERR, self)

    @pyqtSlot()
    def quickinstall(self):
        """
        Initiate backend quick install

        See: :meth:`oPB.controller.base.BaseController.do_quickinstall`

        """
        self.logger.debug("Quick install package")

        ext = "opsi Package (*.opsi)"  # generate file extension selection string for dialog

        script = QFileDialog.getOpenFileName(self, translate("MainWindow", "Choose package file"),
                                            "", ext)

        if not script == ("", ""):
            self.logger.debug("Selected package: " + script[0])
            self._parent.startup.hide_me()
            self._parent.do_quickinstall(pack = script[0], depot = self._parent.query_depot(parent = self))
            self._parent.startup.show_me()
        else:
            self.logger.debug("Dialog aborted.")

    @pyqtSlot()
    def upload(self):
        """
        Initiate backend package upload

        See: :meth:`oPB.controller.base.BaseController.do_upload`

        """
        self.logger.debug("Upload package")

        ext = "opsi Package (*.opsi)"  # generate file extension selection string for dialog

        script = QFileDialog.getOpenFileName(self, translate("MainWindow", "Choose package file"),
                                            "", ext)

        if not script == ("", ""):
            self.logger.debug("Selected package: " + script[0])
            self._parent.startup.hide_me()
            self._parent.do_import(script[0], depot = self._parent.query_depot(parent = self))
            self._parent.startup.show_me()
        else:
            self.logger.debug("Dialog aborted.")

    @pyqtSlot()
    def package_import(self):
        """
        Initiate package import

        See: :meth:`oPB.controller.base.BaseController.do_import`

        """
        self.logger.debug("Import package")

        if self._parent.startup.isVisible():
            pt = self._parent.startup
        else:
            pt = self

        ext = "opsi Package (*.opsi)"  # generate file extension selection string for dialog

        script = QFileDialog.getOpenFileName(pt, translate("MainWindow", "Choose package file"),
                                            "", ext)

        if not script == ("", ""):
            self.logger.debug("Selected package: " + script[0])
            self._parent.package_import(script[0])
        else:
            self.logger.debug("Dialog aborted.")

    @pyqtSlot()
    def save_as(self):
        """
        Initiate SaveAs

        """
        self.logger.debug("Save package as new")

        directory = QFileDialog.getExistingDirectory(self, translate("MainWindow", "Save current project as..."),
                                                     ConfigHandler.cfg.dev_dir, QFileDialog.ShowDirsOnly)

        # sometimes window disappears into background, force to front
        self.activateWindow()

        if not directory == "":
            self.logger.info("Chosen directory for new project: " + directory)
            self._parent.project_copy(directory)
        else:
            self.logger.debug("Dialog aborted.")

    @pyqtSlot()
    def set_button_state(self):
        """Set state of online install/instsetup buttons"""

        # if sender is _parent, then signal is processingEnded from BaseController
        # this is too fast for os.path.isfile (because of disk flushing), so we need
        # to wait a short moment
        if self.sender() == self._parent:
            sleep(0.5)

        self.logger.debug("Set button state")
        if self.is_file_available():
            self.btnInstall.setEnabled(True)
            self.btnInstSetup.setEnabled(True)
        else:
            self.btnInstall.setEnabled(False)
            self.btnInstSetup.setEnabled(False)

    def is_file_available(self):
        """
        Check if opsi package file is available

        :return: True/False
        """
        pack = self.lblPacketFolder.text().replace("\\","/") + "/" + self.inpProductId.text() + \
               "_" + self.inpProductVer.text() + "-" + self.inpPackageVer.text() + ".opsi"

        return os.path.isfile(pack)

    @pyqtSlot(int)
    def reset_datamapper_and_display(self, tabIdx = -1):
        """Reset tables and fields"""
        self.logger.debug("Reset datamapper and display")

        tab = self.tabWidget.currentIndex() if tabIdx == -1 else tabIdx

        # select first row in mapped model
        self.datamapper.toFirst()
        self.tblProperties.selectRow(0)
        self.tblDependencies.selectRow(0)

        self.tblDependencies.resizeRowsToContents()
        self.tblProperties.resizeRowsToContents()

        self.tabWidget.setCurrentIndex(tab)
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
        # execute process loop to assure updating of label text
        qApp.processEvents()

    @pyqtSlot()
    def open_project(self):
        """
        Opens a folder selection dialog and emits selected folder name via signal projectLoadRequested
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
        """Open project via recent files menu entry"""
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
        """
        Send signal if main window is moved

        Used to position startup windows
        """
        self.windowMoved.emit()

    def resizeEvent(self, *args, **kwargs):
        """
        Send signal if main window is resized

        Used to position startup windows
        """
        self.windowMoved.emit()

    def open_project_folder(self):
        """Open os based explorer dialog"""
        self.logger.debug("Open project folder" + platform.system())
        if platform.system() in ["Windows", "Linux"]:
            webbrowser.open(self.lblPacketFolder.text())
        elif platform.system() == "Darwin":
            webbrowser.open("file://" + self.lblPacketFolder.text())

    @pyqtSlot()
    def select_script_dialog(self, script_type, setvalue = True):
        """
        Opens a dialog to select a script file or clear field content

        :param script_type: field type identifier (setup, uninstall, update, always, once, custom, userlogin)
        :param setvalue: set new value = True, empty field only = False
        """
        self.logger.debug("Select script dialog")

        ext = "Scripts (" + " ".join(["*." + x for x in oPB.SCRIPT_EXT]) + ")"  # generate file extension selection string for dialog

        if setvalue:
            if self.lblPacketFolder.text() == "":
                script = QFileDialog.getOpenFileName(self, translate("MainWindow", "Choose script"),
                                                     ConfigHandler.cfg.dev_dir, ext)
            else:
                script = QFileDialog.getOpenFileName(self, translate("MainWindow", "Choose script"),
                                                     Helper.concat_path_native(self.lblPacketFolder.text(), "CLIENT_DATA"), ext)

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
        """
        Sets background color of QLineEdit depending on validator state
        """
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
        """
        Sets status bar text

        :param msg: message text
        """
        self.oPB_statBar.showMessage(msg.replace("<br>", " ").strip(), 0)

    @pyqtSlot(int)
    def check_combobox_selection(self, value):
        """
        Check combobox status and update ui (set widgets enabled/disabled accordingly)

        :param value: control value dependend on self.sender(), see :meth:`check_combobox_selection`
        """
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

    def retranslateMsg(self):
        self.logger.debug("Retranslating further messages...")
        self.splash.msg = translate("MainWindow", "Please wait...")

    def download_file(self, url, desc=None):
        self.logger.debug("Trying to download file: " + url)

        proxystr = ConfigHandler.cfg.proxy_user + ":" + ConfigHandler.cfg.proxy_pass + "@" + ConfigHandler.cfg.proxy_server + ":" + ConfigHandler.cfg.proxy_port
        proxy = request.ProxyHandler({'http': 'http://' + proxystr})
        auth = request.HTTPBasicAuthHandler()
        opener = request.build_opener(proxy, auth, request.HTTPHandler)
        request.install_opener(opener)

        u = request.urlopen(url)
        return


        scheme, netloc, path, query, fragment = parse.urlsplit(url)
        filename = os.path.basename(path)

        if not filename:
            filename = 'downloaded.file'

        if desc:
            filename = os.path.join(desc, filename)
        else:
            filename = os.path.join(tempfile.gettempdir(), filename)

        with open(filename, 'wb') as f:
            meta = u.info()
            meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
            meta_length = meta_func("Content-Length")
            file_size = None
            if meta_length:
                file_size = int(meta_length[0])
            self._parent.msgbox(translate("MainWindow", "Downloading: {0} Bytes: {1}").format(url, file_size), oPB.MsgEnum.MS_STAT, self)

            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break

                file_size_dl += len(buffer)
                f.write(buffer)

                status = "{0:16}".format(file_size_dl)
                if file_size:
                    status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
                status += chr(13)
                #print(status, end="")
                self.splash.setProgress(file_size_dl * 100 / file_size)
            self.splash.close()
            return filename

        return None

    """
    url = "http://download.thinkbroadband.com/10MB.zip"
    filename = download_file(url)
    print(filename)
    """

    def update_check(self):
        self.logger.debug("Downloading version.ini")

        version_ini = self.download_file(oPB.UPDATER_URL + "/version.ini")

        if version_ini is not None:
            parser = ConfigParser()
            try:
                with open(version_ini) as file:
                    parser.read_file(file)
                    self.logger.info("Version.ini file successfully loaded.")
            except IOError:
                self.logger.error("Version.ini file could not be loaded.")
                return

            print(parser.get("Version", "Version"))