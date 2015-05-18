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

import re
import linecache

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *

import oPB
from oPB.gui.mainwindow import MainWindow
from oPB.gui.startup import StartupDialog
from oPB.gui.scripttree import ScriptTreeDialog
from oPB.gui.quickuninstall import UninstallDialog
from oPB.core.datadefinition import *
from oPB.core.confighandler import ConfigHandler
from oPB.core.tools import Helper
from oPB.core.scriptscanner import ScriptTree
from oPB.controller.base import BaseController
from oPB.controller.changelog import ChangelogController

translate = QtCore.QCoreApplication.translate


class MainWindowController(BaseController, QObject):

    # send after model or backend data has been updated
    # tab index to switch to
    modelDataUpdated = pyqtSignal(int)

    def __init__(self, cmd_line):
        super().__init__(cmd_line)
        print("controller/MainWindowController self: ", self) if oPB.PRINTHIER else None

        self.logger.debug("Initialize main window")

        self.model_fields = None
        self.model_properties = None
        self.model_dependencies = None
        self.model_products = None

        self._modelDataChanged = False  # see self.model_data_changed()

        # we have to generate the model first
        # because it is needed for creating the correct
        # data mapping in the ui class
        self.generate_model()

        # create windows and additional controllers
        self.ui = MainWindow(self)
        self.startup = StartupDialog(self.ui)
        self.treedlg = ScriptTreeDialog(self.ui)
        self.quickuninstall = UninstallDialog(self.ui)

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
        self.model_dependencies.setHorizontalHeaderLabels([translate("mainController", "name"),
                                                        translate("mainController", "product id"),
                                                        translate("mainController", "required action"),
                                                        translate("mainController", "installation status"),
                                                        translate("mainController", "type")]
                                                        )

        self.logger.debug("Generate properties table model")
        self.model_properties = QtGui.QStandardItemModel(0, 7, self)
        self.model_properties.setObjectName("model_properties")
        self.model_properties.setHorizontalHeaderLabels([translate("mainController", "name"),
                                                        translate("mainController", "type"),
                                                        translate("mainController", "multivalue"),
                                                        translate("mainController", "editable"),
                                                        translate("mainController", "description"),
                                                        translate("mainController", "values"),
                                                        translate("mainController", "default")]
                                                        )

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

        self.ui.windowMoved.connect(self.startup.set_position)

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
        self.modelDataUpdated.emit(0)

    def update_table_model(self, model, data):
        """
        Remove all rows from given tabel model and rebuild with new data
        from backend object.

        :param model: QtStandardItemModel as QTableView model
        :param data: list with data rows
        :return:
        """
        self.logger.debug("Update table model data: " + model.objectName())

        try:
            model.itemChanged.disconnect(self.model_data_changed)
            model.rowsRemoved.disconnect(self.model_data_changed)
            model.rowsInserted.disconnect(self.model_data_changed)
        except:
            pass

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
        """
        Write data from model into backend

        :return:
        """
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
        if type(self.model_dependencies.item(0, 0)) is not None:  # empty dependency list
            for i in range(0, rows, 1):
                dep = ProductDependency()
                dep.dependencyForAction = self.model_dependencies.item(i, 0).text()
                dep.requiredProductId = self.model_dependencies.item(i, 1).text()
                dep.requiredAction = self.model_dependencies.item(i, 2).text()
                dep.requiredInstallationStatus = self.model_dependencies.item(i, 3).text()
                dep.requirementType = self.model_dependencies.item(i, 4).text()
                self.controlData.dependencies_append(dep)

        rows = self.model_properties.rowCount()
        self.controlData.properties = []
        if type(self.model_properties.item(0, 0)) is not None:  # empty property list
            for i in range(0, rows, 1):
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

    @pyqtSlot(QtGui.QStandardItem)
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
        self._dataSaved = None
        self._dataSaved = None

    @pyqtSlot()
    def close_project(self):
        """Initiate project closing and reset backend, model and window states ."""
        self.logger.debug("Close project")
        ignoreChanges = True
        if self._modelDataChanged is True:
            reply = self.msgbox(translate("mainController", "There are possibly unsaved changes! Are you sure you want to continue?" ), oPB.MsgEnum.MS_QUEST_YESNO)
            if reply is False:
                self.logger.debug("Unsaved changed have been ignored.")
                ignoreChanges = False

        if ignoreChanges:
            [self.treedlg.close(), None][self.treedlg.isVisible()] # instance is always there, since __init__
            try:
                [self.chLogEditor.ui.close(), None][self.chLogEditor.ui.isVisible()] # instance only conditional available (when user has ever openend the dialog
            except AttributeError:
                pass
            self.reset_state()
            self.startup.show_me()

        return ignoreChanges

    @pyqtSlot(QtCore.QEvent)
    def quit_application(self, event):
        """
        Main window exit handler
        """
        ret = self.close_project()
        if ret:
            reply = self.msgbox(translate("mainController", "Are you sure?"), oPB.MsgEnum.MS_QUEST_YESNO, self.startup)
            if reply is True:
                self.startup.hide_me()
                ConfigHandler.cfg.posX = self.ui.geometry().x()
                ConfigHandler.cfg.posY = self.ui.geometry().y()
                ConfigHandler.cfg.width = self.ui.width()
                ConfigHandler.cfg.height = self.ui.height()
                ConfigHandler.cfg.save()
                self.logger.debug("Emit closeAppRequested")
                self.closeAppRequested.emit(0)
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    @pyqtSlot()
    def save_project(self):
        """Initiate saving of backend data and set save marker accordingly."""
        self.logger.debug("Save project")
        self.update_backend_data()
        self.save_backend()
        while self._dataSaved is None: # _dataSaved has to be True or False
            pass

        if not self._dataSaved:
            self.logger.error("Backend data could not be saved")
            self.msgbox(translate("mainController", "Project could not be saved successfully!"), oPB.MsgEnum.MS_ERR)
        else:
            #reset saving and change marker back to undefined state
            self.logger.info("Data saved successfully")
            self.msgbox(translate("mainController", "Project saved successfully!"), oPB.MsgEnum.MS_INFO)
            self._dataSaved = None
            self._modelDataChanged = False

    @pyqtSlot()
    def build_project(self):
        if self._modelDataChanged is True:
            self.save_project()
        self.do_build()

    @pyqtSlot(str)
    def load_project(self, project_name):
        """Load project data."""
        self.load_backend(project_name)

        if not self._dataLoaded:
            self.msgbox(translate("mainController", "Project could not be loaded!"), oPB.MsgEnum.MS_ERR)
            self.startup.show_me()
        else:
            self.msgbox(translate("mainController", "Project loaded successfully!"), oPB.MsgEnum.MS_STAT)
            self.startup.hide_me()

    @pyqtSlot(str)
    def create_project(self, project_name):
        self.close_project()
        self.logger.info("Create new project: " + project_name)
        self.reset_state()
        try:
            self.create_backend(project_name)
        except Exception:
            self.logger.warning(translate("mainController", "Error during project creation."))
            return

        while self._dataLoaded is None:
            pass

        if not self._dataLoaded:
            #reset loading marker back to unsaved state
            self.logger.error("Backend data could not be loaded.")
            self._dataLoaded = None;
            self.msgbox(translate("mainController", "Project could not be created!"), oPB.MsgEnum.MS_ERR)
        else:
            self.logger.info("Backend data loaded")
            self.startup.hide_me()

    @pyqtSlot()
    def open_changelog_editor(self):
        # changelog editor
        self.chLogEditor = ChangelogController(self)
        self.chLogEditor.model.itemChanged.connect(self.model_data_changed)
        self.chLogEditor.model.rowsRemoved.connect(self.model_data_changed)
        self.chLogEditor.model.rowsInserted.connect(self.model_data_changed)
        self.chLogEditor.ui.show()
        # sometimes the window isn't activated, so...
        self.chLogEditor.ui.activateWindow()


    def msgbox(self, msgtext = "", typ = oPB.MsgEnum.MS_STAT, parent = None):
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

        :param msgtext: Message text
        :param typ: type of message window, see oPB.core enums
        """
        if parent is None:
            parent = self.ui

        # first parse text
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
                                          msgtext, QLineEdit.Normal,"")
            return text

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

    def show_script_structure(self):

        scripts = []

        for script in range(10, 16):
            scripts.append(self.model_fields.item(0, script).text())

        run = ScriptTree(self.controlData.projectfolder, scripts)

        self.logger.debug("Complete script tree:")

        for line in run.root.__str__().split("\n"):
            self.logger.debug(line)

        self.treedlg.assign_model(ScriptTree.model)
        self.treedlg.show()
        # sometimes the window isn't activated, so...
        self.treedlg.activateWindow()

    def show_quickuninstall(self):

        self.logger.debug("Open quick uninstall")

        self.startup.hide_me()
        self.quickuninstall.finished.connect(self.startup.show_me)
        self.quickuninstall.btnRefresh.clicked.connect(self.upd_quickuninstall)
        self.quickuninstall.btnUninstall.clicked.connect(self.uninstall_products)

        # create model from data and assign, if not done before
        if self.model_products == None:
            self.logger.debug("Generate product table model")
            self.model_products = QtGui.QStandardItemModel(0, 3, self)
            self.model_products.setObjectName("model_products")
            self.model_products.setHorizontalHeaderLabels([translate("mainController", "product id"),
                                            translate("mainController", "version"),
                                            translate("mainController", "description")]
                                            )

            self.quickuninstall.assign_model(self.model_products)

            # first time opened after program start?
            if self.productlist_dict == None:
                self.upd_quickuninstall()

        self.quickuninstall.show()
        self.quickuninstall.activateWindow()

    def upd_quickuninstall(self):

        self.ui.splash.show()
        self.do_getproducts()
        self.ui.splash.close()

        if self.productlist_dict:
            tmplist = []
            for elem in self.productlist_dict:
                tmplist.append([elem["id"], elem["productVersion"] + "-" + elem["productVersion"], elem["description"]])

            self.update_table_model(self.model_products, sorted(tmplist))

    def uninstall_products(self):
        prods = []
        for row in self.quickuninstall.tableView.selectionModel().selectedRows():
            prods.append(self.quickuninstall.model.item(row.row(), 0).text())

        if prods:
            reply = self.msgbox(translate("mainController", "Do you really want to remove the selected product(s)? This can't be undone!" ), oPB.MsgEnum.MS_QUEST_YESNO)
            if reply is True:
                self.logger.debug("Selected product(s): " + str(prods))
                self.quickuninstall.hide()
                self.ui.splash.show()
                self.do_quickuninstall(prods)
                self.ui.splash.close()
                self.quickuninstall.show()
        else:
            self.logger.debug("Nothing selected.")
