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

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import oPB
from oPB.gui.settings import SettingsDialog
from oPB.core.tools import LogMixin
from oPB.core.confighandler import ConfigHandler

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
        self._parentUi = parent.ui

        print("controller/SettingsController parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None

        self.logger.debug("Initialize settings dialog")

        self.model = None              # data models
        self.datamapper = None             # QDataWidgetMapper object for field mapping
        self._modelDataChanged = False  # is connect via model_data_changed function to itemChanged Signal of QStandardItemModel, will be reset in close_project()

        self._language = ConfigHandler.cfg.language

        self.generate_model()

        # create main window and logic
        self.ui = SettingsDialog(self)

        self.connect_signals()

    def generate_model(self):
        """Create data models and assign field mappings"""
        self.logger.debug("Generate configuration model")
        self.model = QtGui.QStandardItemModel(self)
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
        self.model.setItem(0, 44, QtGui.QStandardItem(ConfigHandler.cfg.editor_options))
        self.model.setItem(0, 45, QtGui.QStandardItem(ConfigHandler.cfg.editor_attachdirect))

    def connect_signals(self):
        """Connect signals"""
        self.logger.debug("Connect signals")
        self.model.itemChanged.connect(self.model_data_changed)
        self.settingsClosed.connect(self._parentUi.set_dev_folder)
        self._parent.processingStarted.connect(self.ui.splash.show_)
        self._parent.processingEnded.connect(self.ui.splash.close)

    @pyqtSlot()
    def model_data_changed(self):
        """Update model changed marker"""
        self.logger.debug("Model data changed")
        self._modelDataChanged = True

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
        ConfigHandler.cfg.editor_options = self.model.item(0, 44).text()
        ConfigHandler.cfg.editor_attachdirect = self.model.item(0, 45).text().title()

    def close_dialog(self):
        """Close settings dialog"""
        ignoreChanges = True
        if self._modelDataChanged == True:
            retval = self._parent.msgbox(translate("settingsController", "There are unsaved changes! Do you really want to continue?"), oPB.MsgEnum.MS_QUEST_YESNO, parent = self.ui)
            if retval == False:
                self.logger.debug("Unsaved changes have been ignored.")
                ignoreChanges = False

        if ignoreChanges:
            # reset language to original value, if changed and NOT saved
            if ConfigHandler.cfg.language != self.model.item(0, 34).text():
                self.model.item(0, 34).setText(ConfigHandler.cfg.language)

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

    @pyqtSlot()
    def refresh_depot_cache(self):
        self._parent.do_getdepots()
