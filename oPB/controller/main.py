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
import shutil
import tempfile
import subprocess, sys
from copy import deepcopy
from pathlib import PurePath
from urllib import request, parse, error as urlerror
from distutils.version import LooseVersion
from configparser import ConfigParser

from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *

from oPB.gui.mainwindow import MainWindow
from oPB.gui.startup import StartupDialog
from oPB.gui.scripttree import ScriptTreeDialog
from oPB.core.datadefinition import *
from oPB.core.confighandler import ConfigHandler
from oPB.core.tools import Helper
from oPB.gui.utilities import EventMixin
from oPB.core.scriptscanner import ScriptTree
from oPB.controller.base import BaseController
from oPB.controller.settings import SettingsController
from oPB.controller.components.changelog import ChangelogEditorComponent
from oPB.controller.components.scheduler import SchedulerComponent
from oPB.controller.components.quickuninstall import QuickUninstallComponent
from oPB.controller.components.deployagent import DeployAgentComponent
from oPB.controller.components.depotmanager import DepotManagerComponent
from oPB.controller.components.bundle import BundleComponent
from oPB.controller.components.lockedproducts import LockedProductsComponent

translate = QtCore.QCoreApplication.translate

class MainWindowController(BaseController, QObject, EventMixin):

    # send after model or backend data has been updated
    # tab index to switch to
    modelDataUpdated = pyqtSignal(int)
    # send after project image has been found under base project directory
    projectImageLoaded = pyqtSignal(list)
    # send after loading of new project has been finished, regardless if loading was successful
    projectLoaded = pyqtSignal([str])
    # for certain progress information
    progressChanged = pyqtSignal([float], [int])

    def __init__(self, cmd_line):
        super().__init__(cmd_line)
        print("controller/MainWindowController self: ", self) if oPB.PRINTHIER else None

        self.logger.debug("Initialize main window")

        self.model_fields = None
        self.model_properties = None
        self.model_dependencies = None

        self._modelDataChanged = False  # see self.model_data_changed()
        self._active_project = False
        self._download_in_progress = False # stop leaving program if download is in progress
        self._run_updater = "" # if this has a value (=path to updater exe), run it after application quits

        # we have to generate the model first
        # because it is needed for creating the correct
        # data mapping in the ui class
        self.generate_model()

        # create windows and append additional components
        self.ui = MainWindow(self)
        self.ui.setWindowIcon(qApp.property("prog_icon"))

        self.settingsCtr = SettingsController(self)
        self.startup = StartupDialog(self)
        self.treedlg = ScriptTreeDialog(self)
        self.quickuninstall = QuickUninstallComponent(self)
        self.scheduler = SchedulerComponent(self)
        self.deployagent = DeployAgentComponent(self)
        self.depotmanager = DepotManagerComponent(self)
        self.bundle = BundleComponent(self)
        self.lockedproducts = LockedProductsComponent(self)

        self.ui.init_recent()

        self.connect_signals()

        # show main ui and set saved geometry or default
        self.logger.debug("Show main window")
        if ConfigHandler.cfg.posX == 0 and ConfigHandler.cfg.posY == 0:
            screen = QDesktopWidget().screenGeometry(self.ui)
            hpos = (screen.width() - ConfigHandler.cfg.width) / 2
            vpos = (screen.height() - ConfigHandler.cfg.height) / 2
            self.ui.move(hpos, vpos)
        else:
            self.ui.setGeometry(ConfigHandler.cfg.posX, ConfigHandler.cfg.posY, ConfigHandler.cfg.width, ConfigHandler.cfg.height)

        self.ui.show()

        # if --path defined, try to load project
        if not self.args.path == "":
            self._active_project = True
            self.run_command_line()
        else:
            self.startup.show_me()

    def generate_model(self):
        """Create data models"""

        self.logger.debug("Generate field model")
        self.model_fields = QtGui.QStandardItemModel(self)
        self.model_fields.setObjectName("model_fields")
        self.model_fields.setItem(0, 0, QtGui.QStandardItem(self.controlData.projectfolder))
        self.model_fields.setItem(0, 1, QtGui.QStandardItem(self.controlData.id))
        self.model_fields.setItem(0, 2, QtGui.QStandardItem(self.controlData.name))
        self.model_fields.setItem(0, 3, QtGui.QStandardItem(self.controlData.description))
        self.model_fields.setItem(0, 4, QtGui.QStandardItem(self.controlData.advice))
        self.model_fields.setItem(0, 5, QtGui.QStandardItem(self.controlData.type))
        self.model_fields.setItem(0, 6, QtGui.QStandardItem(self.controlData.productversion))
        self.model_fields.setItem(0, 7, QtGui.QStandardItem(self.controlData.packageversion))
        self.model_fields.setItem(0, 8, QtGui.QStandardItem(self.controlData.priority))
        self.model_fields.setItem(0, 9, QtGui.QStandardItem(self.controlData.licenseRequired))
        self.model_fields.setItem(0, 10, QtGui.QStandardItem(self.controlData.setupScript))
        self.model_fields.setItem(0, 11, QtGui.QStandardItem(self.controlData.uninstallScript))
        self.model_fields.setItem(0, 12, QtGui.QStandardItem(self.controlData.updateScript))
        self.model_fields.setItem(0, 13, QtGui.QStandardItem(self.controlData.alwaysScript))
        self.model_fields.setItem(0, 14, QtGui.QStandardItem(self.controlData.onceScript))
        self.model_fields.setItem(0, 15, QtGui.QStandardItem(self.controlData.customScript))
        self.model_fields.setItem(0, 16, QtGui.QStandardItem(self.controlData.userLoginScript))
        self.model_fields.setItem(0, 16, QtGui.QStandardItem(self.controlData.userLoginScript))

        self.logger.debug("Generate dependencies table model")
        self.model_dependencies = QtGui.QStandardItemModel(0, 5, self)
        self.model_dependencies.setObjectName("model_dependencies")

        self.logger.debug("Generate properties table model")
        self.model_properties = QtGui.QStandardItemModel(0, 7, self)
        self.model_properties.setObjectName("model_properties")

        self.retranslateMsg()

    def connect_signals(self):
        """Connect object events to slots"""
        self.logger.debug("Connect signals")

        # itemChanged wird erst emitted, wenn der Focus wechselt!!!!
        self.model_fields.itemChanged.connect(self.model_data_changed)

        self.model_dependencies.itemChanged.connect(self.model_data_changed)
        self.model_dependencies.rowsRemoved.connect(self.model_data_changed)
        self.model_dependencies.rowsInserted.connect(self.model_data_changed)

        self.model_properties.itemChanged.connect(self.model_data_changed)
        self.model_properties.rowsRemoved.connect(self.model_data_changed)
        self.model_properties.rowsInserted.connect(self.model_data_changed)

        self.controlData.dataLoaded.connect(self.update_model_data)
        self.controlData.dataSaved.connect(self.update_model_data)

        self.ui.actionSettings.triggered.connect(self.showSettings)

    def showSettings(self):
        if not self._active_project:
            self.startup.hide_()
            self.settingsCtr.ui.exec()
            self.startup.show_()
        else:
            self.settingsCtr.ui.exec()
            
    def update_model_data(self):
        """
        Updates model whenever backend data has changed.

        Hint: update_model_data should always be called, whenever backend 'controlData' object is changed
        -> connect to a signal
        """
        self.logger.debug("Update field model data")
        self.model_fields.itemChanged.disconnect(self.model_data_changed)
        self.model_fields.item(0, 0).setText(self.controlData.projectfolder)
        self.model_fields.item(0, 1).setText(self.controlData.id)
        self.model_fields.item(0, 2).setText(self.controlData.name)
        self.model_fields.item(0, 3).setText(self.controlData.description)
        self.model_fields.item(0, 4).setText(self.controlData.advice)
        self.model_fields.item(0, 5).setText(self.controlData.type)
        self.model_fields.item(0, 6).setText(self.controlData.productversion)
        self.model_fields.item(0, 7).setText(self.controlData.packageversion)
        self.model_fields.item(0, 8).setText(str(self.controlData.priority))
        self.model_fields.item(0, 9).setText(self.controlData.licenseRequired)
        self.model_fields.item(0, 10).setText(self.controlData.setupScript)
        self.model_fields.item(0, 11).setText(self.controlData.uninstallScript)
        self.model_fields.item(0, 12).setText(self.controlData.updateScript)
        self.model_fields.item(0, 13).setText(self.controlData.alwaysScript)
        self.model_fields.item(0, 14).setText(self.controlData.onceScript)
        self.model_fields.item(0, 15).setText(self.controlData.customScript)
        self.model_fields.item(0, 16).setText(self.controlData.userLoginScript)
        self.model_fields.itemChanged.connect(self.model_data_changed)

        self.update_table_model(self.model_dependencies, self.controlData.dependencies)
        self.update_table_model(self.model_properties, self.controlData.properties)

        # emit signal
        self.logger.debug("Emit signal modelDataUpdated")
        self.modelDataUpdated.emit(-1)

    def update_table_model(self, model, data, itemclass = QtGui.QStandardItem, checkable = False):
        """
        Remove all rows from given tabel model and rebuild with new data
        from backend object.

        :param model: QtStandardItemModel as QTableView model
        :param data: list with data rows
        :param itemclass: item class for use in row generation
        :param checkable: activate checkboxes for first column in a row
        :return:
        """
        self.logger.debug("Update table model data: " + model.objectName())

        try:
            model.itemChanged.disconnect(self.model_data_changed)
            model.rowsRemoved.disconnect(self.model_data_changed)
            model.rowsInserted.disconnect(self.model_data_changed)
        except:
            pass

        # cleanup model
        items = model.rowCount()
        for i in range(items, -1, -1):
            model.removeRow(i)

        # insert items
        for elem in data:
            row = []
            for val in elem:
                if type(val) == list:
                    val = ', '.join(map(str, val))  # connect elements to a single comma-separated string
                item = itemclass()
                if checkable:
                    if elem[0] == val:
                        item.setCheckable(True)
                item.setData(val, QtCore.Qt.DisplayRole)
                item.setEditable(False)
                row.append(item)
            model.appendRow(row)

        try:
            model.itemChanged.connect(self.model_data_changed)
            model.rowsRemoved.connect(self.model_data_changed)
            model.rowsInserted.connect(self.model_data_changed)
        except:
            pass

    def model_append_row(self, model, data):
        row = []
        for val in data:
            if type(val) == list:
                val = ', '.join(map(str, val))  # connect elements to a single comma-separated string
            item = QtGui.QStandardItem(val)
            item.setEditable(False)
            row.append(item)
        model.insertRow(0, row)

    def update_backend_data(self):
        """Write data from model into backend"""
        self.logger.debug("Updateing backend data from model")

        self.controlData.id = self.model_fields.item(0, 1).text()
        self.controlData.name = self.model_fields.item(0, 2).text()
        self.controlData.description = self.model_fields.item(0, 3).text()
        self.controlData.advice = self.model_fields.item(0, 4).text()
        self.controlData.type = self.model_fields.item(0, 5).text()
        self.controlData.productversion = self.model_fields.item(0, 6).text()
        self.controlData.packageversion = self.model_fields.item(0, 7).text()
        self.controlData.priority = int(self.model_fields.item(0, 8).text())
        self.controlData.licenseRequired = self.model_fields.item(0, 9).text()
        self.controlData.setupScript = self.model_fields.item(0, 10).text()
        self.controlData.uninstallScript = self.model_fields.item(0, 11).text()
        self.controlData.updateScript = self.model_fields.item(0, 12).text()
        self.controlData.alwaysScript = self.model_fields.item(0, 13).text()
        self.controlData.onceScript = self.model_fields.item(0, 14).text()
        self.controlData.customScript = self.model_fields.item(0, 15).text()
        self.controlData.userLoginScript = self.model_fields.item(0, 16).text()

        rows = self.model_dependencies.rowCount()
        self.controlData.dependencies = []
        if self.model_dependencies.item(0, 0) is not None:  # empty dependency list
            for i in range(0, rows, 1):
                #self.logger.debug("Reading dependency: " + str(i))
                dep = ProductDependency()
                dep.dependencyForAction = self.model_dependencies.item(i, 0).text()
                dep.requiredProductId = self.model_dependencies.item(i, 1).text()
                dep.requiredAction = self.model_dependencies.item(i, 2).text()
                dep.requiredInstallationStatus = self.model_dependencies.item(i, 3).text()
                dep.requirementType = self.model_dependencies.item(i, 4).text()
                self.controlData.dependencies_append(dep)

        rows = self.model_properties.rowCount()
        self.controlData.properties = []
        if self.model_properties.item(0, 0) is not None:  # empty property list
            for i in range(0, rows, 1):
                #self.logger.debug("Reading property: " + str(i))
                prop = ProductProperty()
                prop.name = self.model_properties.item(i, 0).text()
                prop.type = self.model_properties.item(i, 1).text()
                prop.multivalue = self.model_properties.item(i, 2).text()
                prop.editable = self.model_properties.item(i, 3).text()
                prop.description = self.model_properties.item(i, 4).text()
                if prop.type == "bool":
                    prop.values = ""
                    prop.default = self.model_properties.item(i, 6).text()
                else:
                    prop.values = Helper.paramlist2list(self.model_properties.item(i, 5).text())
                    prop.default = Helper.paramlist2list(self.model_properties.item(i, 6).text())
                self.controlData.properties_append(prop)

    @pyqtSlot()
    def add_dependency(self):
        self.logger.debug("Add dependency")
        self.model_append_row(self.model_dependencies, ["setup", "new_dependency", "", "installed", "before"])

        # emit signal
        self.logger.debug("Emit signal modelDataUpdated")
        self.modelDataUpdated.emit(1)

    @pyqtSlot(int)
    def remove_dependency(self, idx):
        self.logger.debug("Remove dependency")
        self.model_dependencies.removeRow(idx)
        # emit signal
        self.logger.debug("Emit signal modelDataUpdated")
        self.modelDataUpdated.emit(1)

    @pyqtSlot()
    def add_property(self, name = "new_property"):
        self.logger.debug("Add property")
        self.model_append_row(self.model_properties, [name, "unicode", "False", "True", "New product property", "", ""])

        # emit signal
        self.logger.debug("Emit signal modelDataUpdated")
        self.modelDataUpdated.emit(2)

    @pyqtSlot(int)
    def remove_property(self, idx):
        self.logger.debug("Remove property")
        self.model_properties.removeRow(idx)
        # emit signal
        self.logger.debug("Emit signal modelDataUpdated")
        self.modelDataUpdated.emit(2)

    def model_data_changed(self, item):
        """
        Sets a dataChanged marker for model data.

        :param item: item which send the signal
        :return:
        """
        self.logger.debug("Model data changed received")
        self._modelDataChanged = True

    @pyqtSlot(str, str)
    def set_selected_script(self, script, script_type):
        """
        Receives select signal from window button, writes filename to model
        and emits itemChanged signal

        :param script: full pathname to script
        :param script_type: type of script
        """
        self.logger.debug("Set selected script: (" + script + ") (" + script_type + ")")
        if script_type == "setup":
            self.model_fields.item(0, 10).setText(Helper.get_file_from_path(script))
        if script_type == "uninstall":
            self.model_fields.item(0, 11).setText(Helper.get_file_from_path(script))
        if script_type == "update":
            self.model_fields.item(0, 12).setText(Helper.get_file_from_path(script))
        if script_type == "always":
            self.model_fields.item(0, 13).setText(Helper.get_file_from_path(script))
        if script_type == "once":
            self.model_fields.item(0, 14).setText(Helper.get_file_from_path(script))
        if script_type == "custom":
            self.model_fields.item(0, 15).setText(Helper.get_file_from_path(script))
        if script_type == "userlogin":
            self.model_fields.item(0, 16).setText(Helper.get_file_from_path(script))

    def reset_state(self):
        """Reset special label fields"""
        self.logger.debug("Reset main window")

        self.reset_backend()

        self._modelDataChanged = False
        self._active_project = False

    @pyqtSlot()
    def project_close(self, startup = True):
        """
        Initiate project closing and reset backend, model and window states .

        :param startup: show/don't show startup dialog after closing, see i.e. oPB.gui.mainwindow.MainWindow.open_project()
        """
        self.logger.debug("Close project")
        ignoreChanges = True
        if self._modelDataChanged is True:
            reply = self.msgbox(translate("mainController", "There are possibly unsaved changes! Are you sure you want to continue?" ), oPB.MsgEnum.MS_QUEST_YESNO)
            print(reply)
            if reply is False:
                self.logger.debug("Unsaved changed have not been ignored.")
                ignoreChanges = False

        if ignoreChanges is True:
            [self.treedlg.close(), None][self.treedlg.isVisible()] # instance is always there, since __init__
            try:
                [self.chLogEditor.ui.close(), None][self.chLogEditor.ui.isVisible()] # instance only conditional available (when user has ever openend the dialog
            except AttributeError:
                pass
            self.ui.set_current_project(self.controlData.projectfolder)
            self.reset_state()
            if startup is True:
                self.startup.show_me()

        return ignoreChanges

    @pyqtSlot(QtCore.QEvent)
    def quit_application(self, event):
        """
        Main window exit handler
        """
        ret = self.project_close(False)

        if self._download_in_progress:
            self.msgbox(translate("mainController", "There is an active download. Please wait until the download is complete."), oPB.MsgEnum.MS_ALWAYS, self.startup)
            event.ignore()
            return

        if ret:
            self.startup.hide_()

            if self._run_updater != "":
                reply = self.msgbox(translate("mainController", "Are you sure (update pending)?"), oPB.MsgEnum.MS_QUEST_YESNO, self.startup)
            else:
                reply = self.msgbox(translate("mainController", "Are you sure?"), oPB.MsgEnum.MS_QUEST_YESNO, self.startup)

            if reply is True:
                self._cancel_download = True
                ConfigHandler.cfg.posX = self.ui.geometry().x()
                ConfigHandler.cfg.posY = self.ui.geometry().y()
                ConfigHandler.cfg.width = self.ui.width()
                ConfigHandler.cfg.height = self.ui.height()
                ConfigHandler.cfg.save()
                self.logger.debug("Emit closeAppRequested")
                self.closeAppRequested.emit(0)
                if self._run_updater != "":
                    DETACHED_PROCESS = 0x00000008
                    self.logger.info("Running product updater: " + self._run_updater)
                    subprocess.Popen([self._run_updater], creationflags = DETACHED_PROCESS)
                event.accept()
            else:
                self.startup.show_()
                event.ignore()
        else:
            event.ignore()

    @pyqtSlot()
    def project_save(self):
        """Initiate saving of backend data and set save marker accordingly."""
        self.logger.debug("Save project")
        self.update_backend_data()
        self.save_backend()

        if self._dataSaved:
            self._modelDataChanged = False

    @pyqtSlot()
    def project_build(self):
        if self._modelDataChanged is True:
            self.project_save()
        self.do_build()

    @pyqtSlot(str)
    def project_load(self, project_name):
        """Load project data."""
        self.load_backend(project_name)

        if not self._dataLoaded:
            self.startup.show_me()
        else:
            self._active_project = True
            self.get_package_logos()
            self.startup.hide_me()

        self.projectLoaded.emit(self.controlData.projectfolder)

    @pyqtSlot(str)
    def project_create(self, project_name):
        """Create new project"""
        if not self.project_close():
            return

        self.logger.info("Create new project: " + project_name)

        self.reset_state()
        try:
            self.create_backend(project_name)
        except Exception:
            self.logger.warning(translate("mainController", "Error during project creation."))
            return

        if self._dataLoaded:
            self._active_project = True
            self.logger.info("Backend data loaded")
            self.startup.hide_me()

    @pyqtSlot(str)
    def project_copy(self, project_folder):
        """
        Copies current project data to new project destination

        :param destination: destination for copied project
        """

        dest_data = ""
        val = 0

        def sizeof_fmt(num, suffix='B'):
            for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
                if abs(num) < 1024.0:
                    return "%3.1f%s%s" % (num, unit, suffix)
                num /= 1024.0
            return "%.1f%s%s" % (num, 'Yi', suffix)

        def copy2_(src, dst):
            self.logger.debug("Copying to destination file: " + str(dst))
            self.msgbox("CLIENT_DATA: " + str(dst).replace(dest_data, ""), oPB.MsgEnum.MS_STAT)
            self.progressChanged.emit(val)
            shutil.copy2(src,dst)

        def countFiles(directory):
            files = []
            total_size = 0
            if os.path.isdir(directory):
                for path, dirs, filenames in os.walk(directory):
                    files.extend(filenames)
                    for f in filenames:
                        fp = os.path.join(path, f)
                        total_size += os.path.getsize(fp)

            return len(files), total_size

        def copyDirectory(src, dest):
            self.logger.info("Copying files")
            self.logger.debug("Source: " + src)
            self.logger.debug("Destination:" + dest)
            if os.path.exists(dest):
                shutil.rmtree(dest)
            try:
                shutil.copytree(src, dest, copy_function=copy2_)
            # Directories are the same
            except shutil.Error as e:
                self.logger.error('Directory not copied. Error: %s' % e)
            # Any error saying that the directory doesn't exist
            except OSError as e:
                self.logger.error('Directory not copied. Error: %s' % e)

        self.logger.info("Create new project from current: " + project_folder)

        # create new control object as copy

        if os.path.exists(Helper.concat_path_native(project_folder, "CLIENT_DATA")):
            self.logger.error("CLIENT_DATA subdirectory in destination folder detected. This is not allowed for security reason!")
            self.msgbox(translate("mainController", "CLIENT_DATA subdirectory in destination folder detected. This is not allowed for security reason!"),
                        oPB.MsgEnum.MS_ERR)
            return

        newControl = deepcopy(self.controlData)
        self.create_project_paths(project_folder)
        project_name = PurePath(project_folder).name.replace(" ","_")
        newControl.id = project_name
        newControl.projectfolder = project_folder

        # add changelog entry for this copy process
        text = "Project copied from: " + self.controlData.packagename
        newentry = ChangelogEntry(newControl.id)
        newentry.version = "(" + newControl.productversion + "-" + newControl.packageversion + ")"
        newentry.status = oPB.CHLOG_STATI[0]
        newentry.urgency = oPB.CHLOG_BLOCKMARKER + oPB.CHLOG_URGENCIES[0]
        newentry.text = "\n" + text + changelog_footer()
        newControl.changelog_append(newentry)

        try:
            self.processingStarted.emit()

            newControl.save_data()
            self.logger.debug("New control data saved.")

            dest_data = Helper.concat_path_native(newControl.projectfolder, "CLIENT_DATA")
            total, total_size = countFiles(Helper.concat_path_native(self.controlData.projectfolder, "CLIENT_DATA"))
            val = 100 / total

            reply = self.msgbox(translate("mainController", "Copy files now? This can't be canceled.") + "\n\nTotal: " +  str(total) + "\n" + sizeof_fmt(total_size),
                                oPB.MsgEnum.MS_QUEST_YESNO)
            if reply is True:
                copyDirectory(Helper.concat_path_native(self.controlData.projectfolder, "CLIENT_DATA"),
                              Helper.concat_path_native(newControl.projectfolder, "CLIENT_DATA")
                              )
                self.logger.debug("Files copied.")

            self.processingEnded.emit(True)

            # close current project an re-open clone
            if not self.project_close():
                return

            self.project_load(project_name)
        except:
            self.logger.error("Project could not be copied and re-opened.")


    def package_import(self, pack: str):
        """
        Import opsi package file into development folder and open it, if successful

        :param pack: package file path
        """
        self.logger.debug("Importing package")

        if self._active_project:
            if not self.project_close():
                return

            self.reset_state()

        # extract product id from package path
        file = Helper.get_file_from_path(pack)
        product = file[:file.rfind("_")]  # remove everything behind product name (version, file extension, etc.)
        project = Helper.concat_path_native(ConfigHandler.cfg.dev_dir, product)

        # import
        try:
            self.startup.hide_me()
            self.do_import(pack)
        except:
            self.logger.error("Package import unsuccessful!")
        else:
            # open
            try:
                self.project_load(project)
            except:
                self.logger.err("Imported package could not be opened!")

    @pyqtSlot()
    def show_changelogeditor(self):
        self.update_backend_data()
        # changelog editor
        self.chLogEditor = ChangelogEditorComponent(self)
        self.chLogEditor.model.itemChanged.connect(self.model_data_changed)
        self.chLogEditor.model.rowsRemoved.connect(self.model_data_changed)
        self.chLogEditor.model.rowsInserted.connect(self.model_data_changed)
        self.chLogEditor.ui.show()
        # sometimes the window isn't activated, so...
        self.chLogEditor.ui.activateWindow()

    def msgbox(self, msgtext = "", typ = oPB.MsgEnum.MS_STAT, parent = None, preload = ""):
        """ Messagebox function

        Valid values for typ:
            * oPB.MsgEnum.MS_ERR -> Error message (status bar/ popup)
            * oPB.MsgEnum.MS_WARN -> Warning (status bar/ popup)
            * oPB.MsgEnum.MS_INFO -> Information (status bar/ popup)
            * oPB.MsgEnum.MS_STAT -> Information (only status bar)
            * oPB.MsgEnum.MS_ALWAYS -> Display this message ALWAYS, regardless of which message **typ** is deactivated via settings
            * oPB.MsgEnum.MS_PARSE -> just parse message text and return it
            * oPB.MsgEnum.MS_QUEST_YESNO
            * oPB.MsgEnum.MS_QUEST_CTC
            * oPB.MsgEnum.MS_QUEST_OKCANCEL
            * oPB.MsgEnum.MS_QUEST_PHRASE
            * oPB.MsgEnum.MS_QUEST_PASS
            * oPB.MsgEnum.MS_QUEST_DEPOT

        :param msgtext: Message text
        :param typ: type of message window, see oPB.core enums
        :param parent: parent ui of message box
        :param preload: pre-fill input boxes with this text
        """
        if parent is None:
            parent = self.ui

        # first parse text, is argument is str
        if type(msgtext) is str:
            msgtext = Helper.parse_text(msgtext)

        if typ == oPB.MsgEnum.MS_ERR:
            self.msgSend.emit(msgtext)
            if ConfigHandler.cfg.no_error_msg == "False":
                QMessageBox.critical(parent, translate("mainController", "Error"), msgtext, QMessageBox.Ok)

        elif typ == oPB.MsgEnum.MS_WARN:
            self.msgSend.emit(msgtext)
            if ConfigHandler.cfg.no_warning_msg == "False":
                QMessageBox.warning(parent, translate("mainController", "Warning"), msgtext, QMessageBox.Ok)

        elif typ == oPB.MsgEnum.MS_INFO:
            self.msgSend.emit(msgtext)
            if ConfigHandler.cfg.no_info_msg == "False":
                QMessageBox.information(parent, translate("mainController", "Message"), msgtext, QMessageBox.Ok)

        elif typ == oPB.MsgEnum.MS_STAT:
            self.msgSend.emit(msgtext)

        elif typ == oPB.MsgEnum.MS_ALWAYS:
            QMessageBox.information(parent, translate("mainController", "Message"), msgtext, QMessageBox.Ok)

        elif typ == oPB.MsgEnum.MS_PARSE:
            return msgtext

        elif typ == oPB.MsgEnum.MS_QUEST_YESNO:
            retval = QMessageBox.question(parent, translate("mainController", "Question"), msgtext, QMessageBox.Yes, QMessageBox.No)
            if retval == QMessageBox.No:
                return False
            else:
                return True

        elif typ == oPB.MsgEnum.MS_QUEST_CTC:
            msgBox = QMessageBox(parent)
            msgBox.setWindowTitle(translate("mainController", "Question"))
            msgBox.setText(msgtext)
            msgBox.setIcon(QMessageBox.Question)
            cancelBtn = QPushButton(translate("mainController", "Cancel"))
            rebuildBtn = QPushButton(translate("mainController", "Rebuild"))
            addBtn = QPushButton(translate("mainController", "Add version"))
            msgBox.addButton(cancelBtn, QMessageBox.RejectRole)
            msgBox.addButton(rebuildBtn, QMessageBox.AcceptRole)
            msgBox.addButton(addBtn, QMessageBox.AcceptRole)
            msgBox.exec_()
            if msgBox.clickedButton() == cancelBtn:
                return 0
            elif msgBox.clickedButton() == rebuildBtn:
                return 1
            else:
                return 2

        elif typ == oPB.MsgEnum.MS_QUEST_OKCANCEL:
            retval = QMessageBox.question(parent, translate("mainController", "Question"), msgtext, QMessageBox.Ok, QMessageBox.Cancel)
            if retval == QMessageBox.Cancel:
                return False
            else:
                return True

        elif typ == oPB.MsgEnum.MS_QUEST_PHRASE:
            text = QInputDialog.getText(parent, translate("mainController", "Additional information"),
                                          msgtext, QLineEdit.Normal, preload)
            return text

        elif typ == oPB.MsgEnum.MS_QUEST_PASS:
            text = QInputDialog.getText(parent, translate("mainController", "Additional information"),
                                          msgtext, QLineEdit.Password, preload)
            return text

        elif typ == oPB.MsgEnum.MS_QUEST_DEPOT:
            preselectlist = [i for i, j in enumerate(msgtext) if ConfigHandler.cfg.opsi_server in j]
            if preselectlist:
                preselect = preselectlist[0]
            else:
                preselect = -1
            item = QInputDialog.getItem(parent, translate("mainController", "Question"), translate("mainController", "Select which depot to use (Cancel = default opsi server):"), msgtext, preselect, False)
            return item

        elif typ == oPB.MsgEnum.MS_ABOUTQT:
            QMessageBox.aboutQt(parent, translate("mainController", "About Qt"))

    def get_properties_from_scripts(self):
        found_props = set()
        self.logger.debug("Get properties from scripts")

        # first, find all product properties in every script and return a set
        for script in range(10, 16):
            scriptname = self.model_fields.item(0, script).text()
            if scriptname != "":
                scriptname = self.controlData.projectfolder.replace('\\', '/') + "/CLIENT_DATA/" + scriptname
                self.logger.debug("Script to scan : " + scriptname)

                r = re.compile('GetProductProperty\(\"(.*?)\"')

                with open(scriptname, 'r') as f:
                    for line in f:
                        m = r.search(line)
                        if m:
                            found_props.add(m.group(1))

        # now get all current properties and add any NEW property
        used_props = []
        rows = self.model_properties.rowCount()
        for i in range(0, rows, 1):
            used_props.append(self.model_properties.item(i, 0).text())

        for p in found_props:
            if p not in used_props:
                self.add_property(p)

    def get_package_logos(self):
        self.logger.debug("Trying to find project logos...")

        extensions = ['.png', '.gif', '.jpg', '.jpeg']
        files = os.listdir(self.controlData.projectfolder.replace('\\', '/') + "/CLIENT_DATA/")
        pics_list = [self.controlData.projectfolder.replace('\\', '/') + "/CLIENT_DATA/" + i for i in files if (i.startswith(self.controlData.id) and i.endswith(tuple(extensions)))]
        self.projectImageLoaded.emit(list(set(pics_list)))

    @pyqtSlot()
    def show_scripttree(self):
        """Open script structure treeview"""
        scripts = []

        for script in range(10, 16):
            scripts.append(self.model_fields.item(0, script).text())

        run = ScriptTree(self.controlData.projectfolder, scripts)

        self.logger.debug("Complete script tree:")

        for line in run.root.__str__().split("\n"):
            self.logger.debug(line)

        #self.treedlg.assign_model(ScriptTree.model)
        self.treedlg.assign_model(run.model)
        self.treedlg.show()
        # sometimes the window isn't activated, so...
        self.treedlg.activateWindow()

    @pyqtSlot()
    def quickuninstall_dialog(self):
        """Open quickuninstall dialog"""
        self.quickuninstall.ui.show_()

    @pyqtSlot()
    def lockedproducts_dialog(self):
        """Open quickuninstall dialog"""
        self.lockedproducts.ui.show_()

    @pyqtSlot()
    def bundle_dialog(self):
        """Open bundle creation dialog"""
        self.bundle.ui.show_()

    @pyqtSlot()
    def scheduler_dialog(self):
        """Open job scheduler dialog"""
        self.scheduler.ui_joblist.show_()

    @pyqtSlot()
    def deployagent_dialog(self):
        """Open opsi client agent deploy dialog"""
        self.deployagent.ui.show_()

    @pyqtSlot()
    def depotmanager_dialog(self):
        """Open depot manager dialog"""
        self.depotmanager.ui.show_()

    def retranslateMsg(self):
        """Retranslate model headers, will be called via changeEvent of self.ui """
        self.logger.debug("Retranslating further messages...")
        self.model_dependencies.setHorizontalHeaderLabels([translate("mainController", "name"),
                                                        translate("mainController", "product id"),
                                                        translate("mainController", "required action"),
                                                        translate("mainController", "installation status"),
                                                        translate("mainController", "type")]
                                                        )
        self.model_properties.setHorizontalHeaderLabels([translate("mainController", "name"),
                                                        translate("mainController", "type"),
                                                        translate("mainController", "multivalue"),
                                                        translate("mainController", "editable"),
                                                        translate("mainController", "description"),
                                                        translate("mainController", "values"),
                                                        translate("mainController", "default")]
                                                        )

    def download_file(self, url, desc = ""):
        """
        File downloader

        :param url: Full URL of file to download
        :param desc: Destination for file download
        :return:
        """
        self.logger.debug("Trying to download file: " + url)

        if ConfigHandler.cfg.useproxy:
            proxystr = ConfigHandler.cfg.proxy_user + ":" + ConfigHandler.cfg.proxy_pass + "@" + ConfigHandler.cfg.proxy_server + ":" + ConfigHandler.cfg.proxy_port
            pdict = {'http': 'http://' + proxystr, 'https': 'http://' + proxystr}
            proxy = request.ProxyHandler(pdict)
            auth = request.HTTPBasicAuthHandler()
            opener = request.build_opener(proxy, auth, request.HTTPHandler, request.HTTPSHandler)
            self.logger.info("Proxy handler installed.")
        else:
            opener = request.build_opener(request.HTTPHandler, request.HTTPHandler)

        request.install_opener(opener)

        try:
            u = request.urlopen(url)
        except urlerror.URLError as err:
            self.logger.warning("Error while opening download URL: " + repr(err))
            return None
        except urlerror.HTTPError as err:
            self.logger.warning("Error while opening HTTP connection: " + repr(err))
            return None

        scheme, netloc, path, query, fragment = parse.urlsplit(url)
        filename = os.path.basename(path)

        if not filename:
            filename = 'downloaded.file'

        if desc != "":
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
            self.msgbox(translate("MainWindow", "Downloading: {0} Bytes: {1}").format(url, file_size), oPB.MsgEnum.MS_STAT)

            file_size_dl = 0
            block_sz = 8192

            self._download_in_progress = True

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

                self.progressChanged.emit(len(buffer) * 100 / file_size) # progressChanged is connected to splash.incProgress ;-)
                self.msgbox(translate("MainWindow", "Downloading: {0} - Bytes: {1} of {2}").format(url, file_size_dl, file_size), oPB.MsgEnum.MS_STAT)

            self._download_in_progress = False
            return filename

        return None

    """
    url = "http://download.thinkbroadband.com/10MB.zip"
    filename = download_file(url)
    print(filename)
    """

    def update_check(self):

        if self.args.noupdate == True:
            self.logger.info("Update check disabled via command line")
            return

        self.logger.debug("Downloading version.ini")

        self.msgbox(translate("MainWindow", "Update check in progress..."), oPB.MsgEnum.MS_STAT)

        version_ini = self.download_file(oPB.UPDATER_URL + "/version.ini")

        if version_ini is not None:
            parser = ConfigParser()
            try:
                with open(version_ini) as file:
                    parser.read_file(file)
                    self.logger.info("version.ini file successfully loaded.")
            except IOError:
                self.logger.warning("version.ini file could not be loaded.")
                self.processingEnded.emit(False)
                return

            if LooseVersion(parser.get("Version", "Version")) > LooseVersion(oPB.PROGRAM_VERSION):
                self.msgbox(translate("MainWindow", "New program version available! Update possible!"), oPB.MsgEnum.MS_STAT)
                self.logger.info("New program version available! Update possible!")
                self.logger.info("Current program version is: " + oPB.PROGRAM_VERSION)
                self.logger.info("version.ini file contains version: " + parser.get("Version", "Version"))

                msg = translate("MainWindow", "New program version available:") + " " + parser.get("Version", "Version") + "\n\n"
                msg += translate("MainWindow", "Do you want to download and install the new version?")

                # ask, if updater should be downloaded and run after program end
                ret = self.msgbox(msg, oPB.MsgEnum.MS_QUEST_YESNO, self.startup)
                if ret:

                    directory = QFileDialog.getExistingDirectory(self.ui, translate("MainWindow", "Choose download directory"),
                                                                 os.environ['USERPROFILE'] + "/Desktop", QFileDialog.ShowDirsOnly)

                    upd_executable = self.download_file(parser.get("Version", "download"), directory)

                    if upd_executable is not None:
                        self.processingEnded.emit(False)

                        self.logger.info("Updater executable retrieved successfully.")
                        msg = translate("MainWindow", "File successfully saved to:") + "\n" + '\\'.join(upd_executable.split('/'))
                        self.msgbox(translate("MainWindow", "File successfully saved to:") + " " + '\\'.join(upd_executable.split('/')), oPB.MsgEnum.MS_STAT)
                        msg += "\n\n" + translate("MainWindow", "Quit application to start the update process.")
                        self.msgbox(msg, oPB.MsgEnum.MS_ALWAYS)

                        self._run_updater = '/'.join(upd_executable.split('\\'))

                    else:
                        self.processingEnded.emit(False)
                        self.logger.warning("Updater executable could not be retrieved or has been canceled manually.")
                else:
                    self.processingEnded.emit(True)
                    self.logger.info("Program update canceled.")
            else:
                self.processingEnded.emit(False)
                self.msgbox(translate("MainWindow", "No new program version available!"), oPB.MsgEnum.MS_STAT)