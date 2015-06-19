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

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
import oPB
from oPB.core.models import OpsiProductTableModel
from oPB.core.tools import Helper
from oPB.controller.base import BaseController
from oPB.core.confighandler import ConfigHandler
from oPB.gui.depotmanager import DepotManagerDialog
from oPB.gui.report import ReportSelectorDialog

translate = QtCore.QCoreApplication.translate

class DepotManagerComponent(BaseController, QObject):

    modelDataUpdated = pyqtSignal()

    def __init__(self, parent):
        super().__init__(self)

        self._parent = parent
        print("controller/DepotManagerComponent parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None

        self.ui = None
        self.ui_report = None

        self.model_left = None
        self.model_right = None
        self.model_report = None

        self._type_left = "depot"  # depot / repo modus
        self._type_right = "depot"  # depot / repo modus
        self._select_left = ""
        self._select_right = ""
        self._depot_data_left = []
        self._depot_data_right = []
        self._repo_data_left = []
        self._repo_data_right = []
        self.reportlist = []


        self._ui_box_left = QtWidgets.QComboBox  # left depot combobox selecotor
        self._ui_box_right = QtWidgets.QComboBox # right depot combobox selecotor
        self._ui_repobtn_left = QtWidgets.QPushButton  # left fetch repo button
        self._ui_repobtn_right = QtWidgets.QPushButton # right fetch repo button

        self._active_side = None

        self._compare = False

        self.generate_model()

        self.ui_report = ReportSelectorDialog(self)
        self.ui = DepotManagerDialog(self)

        self.connect_signals()

    def connect_signals(self):
        self.ui.dialogOpened.connect(self._parent.startup.hide_)
        self.ui.dialogClosed.connect(self._parent.startup.show_)

    def generate_model(self):
        # create model from data and assign, if not done before
        if self.model_left == None:
            self.logger.debug("Generate left table model")
            self.model_left = OpsiProductTableModel(0, 3, self)
            self.model_left.set_error_column(3)
            self.model_left.set_error_color(oPB.OPB_COLOR_ERROR)
            self.model_left.append_error_marker("Error")
            self.model_left.setObjectName("model_left")

        if self.model_right == None:
            self.logger.debug("Generate right table model")
            self.model_right = OpsiProductTableModel(0, 3, self)
            self.model_right.set_error_column(3)
            self.model_right.set_error_color(oPB.OPB_COLOR_ERROR)
            self.model_right.append_error_marker("Error")
            self.model_right.setObjectName("model_right")

        if self.model_report == None:
            self.logger.debug("Generate report table model")
            self.model_report = QStandardItemModel(0, 2, self)
            self.model_report.setObjectName("model_report")

        self.retranslateMsg()

    def update_model_data(self, side, dict_):
        self.logger.debug("Update model data")

        tmplist = []

        if dict_:
            for elem in dict_:
                d = elem.split(";")
                tmplist.append([d[0], d[2], d[3], d[1]])

        if side == 0:
            self._parent.update_table_model(self.model_left, sorted(tmplist))
        else:
            self._parent.update_table_model(self.model_right, sorted(tmplist))

    def update_reportmodel_data(self):
        self.logger.debug("Update report model data")

        self.reportlist = []
        for key, val in ConfigHandler.cfg.depotcache.items():
            self.reportlist.append([key, val])

        self._parent.update_table_model(self.model_report, sorted(self.reportlist))

        self.modelDataUpdated.emit()

    def update_data(self, resetgui = True):
        self.logger.debug("Update data")

        if self.sender() == self.ui.btnRefresh:
            self._select_left = "" # depot / repo modus
            self._select_right = ""  # depot / repo modus
            self._type_left = "depot" # depot / repo modus
            self._type_right = "depot"  # depot / repo modus
            self._depot_data_left = []
            self._depot_data_right = []
            self._repo_data_left = []
            self._repo_data_right = []
            self._compare = False
            self._active_side = None

        self.dataAboutToBeAquired.emit(33)

        if ConfigHandler.cfg.depotcache == {} or self.sender() == self.ui.btnRefresh:
            self._parent.do_getdepots()

        self.dataAboutToBeAquired.emit(66)

        if BaseController.productsondepotslist == None or self.sender() == self.ui.btnRefresh:
            self._parent.do_getproductsondepots()

        if resetgui:
            self.modelDataUpdated.emit()

    @pyqtSlot(str)
    def switch_content(self, param = ""):
        self.logger.debug("Switch content")

        if self.sender() == self._ui_repobtn_left:
            self.logger.debug("Sender is left button")
            uiserver = self._ui_box_left.currentText().split()[0]
            if self._type_left == "depot":
                self._type_left = "repo"
            else:
                self._type_left = "depot"
            self.side_content(uiserver, "left")

        elif self.sender() == self._ui_repobtn_right:
            self.logger.debug("Sender is right button")
            uiserver = self._ui_box_right.currentText().split()[0]
            if self._type_right == "depot":
                self._type_right = "repo"
            else:
                self._type_right = "depot"
            self.side_content(uiserver, "right")

        else:
            try:
                uiserver = param.split()[0]
            except:
                uiserver = ""

            if self.sender() == self._ui_box_left:
                # get server name from combobox
                if self._select_left != uiserver:
                    self._repo_data_left = []
                self.side_content(uiserver, "left")

            if self.sender() == self._ui_box_right:
                # get server name from combobox
                if self._select_right != uiserver:
                    self._repo_data_right = []
                self.side_content(uiserver, "right")

        if self._compare is True:
            self.compare_leftright()

        self.dataAquired.emit()

    def side_content(self, uiserver = "", side = None):

        if uiserver != "":
            if side == "left":

                # depot data
                if self._select_left != uiserver:

                    self._depot_data_left = []
                    for elem in BaseController.productsondepotslist:
                        d = elem.split(";")
                        if d[4] == uiserver:
                            self._depot_data_left.append((";").join([d[0], d[1], d[2],d[3]]))

                    self._select_left = uiserver

                # repo data
                if self._type_left == "repo" and not self._repo_data_left:
                    self.dataAboutToBeAquired.emit(None)
                    self._repo_data_left = self._parent.do_getrepocontent(dest = uiserver)
                    self.dataAquired.emit()

                if self._type_left == "repo":
                    self.logger.debug("Left pane: repo content")
                    self.update_model_data(0, self._repo_data_left)
                else:
                    self.logger.debug("Left pane: depot content")
                    self.update_model_data(0, self._depot_data_left)

            # -------------------------------------------------------------------------------------------------

            if side == "right":

                # depot data
                if self._select_right != uiserver:

                    self._depot_data_right = []
                    for elem in BaseController.productsondepotslist:
                        d = elem.split(";")
                        if d[4] == uiserver:
                            self._depot_data_right.append((";").join([d[0], d[1], d[2],d[3]]))

                    self._select_right = uiserver

                # repo data
                if self._type_right == "repo" and not self._repo_data_right:
                    self.dataAboutToBeAquired.emit(None)
                    self._repo_data_right = self._parent.do_getrepocontent(dest = uiserver)
                    self.dataAquired.emit()

                if self._type_right == "repo":
                    self.logger.debug("Right pane: repo content")
                    self.update_model_data(1, self._repo_data_right)
                else:
                    self.logger.debug("Right pane: depot content")
                    self.update_model_data(1, self._depot_data_right)

        else:
            if self.sender() == self._ui_box_left:
                self.logger.debug("Left pane: clean selection")
                self.update_model_data(0, None)
                self._type_left = "depot"
                self._depot_data_left = []
                self._select_left = ""

            if self.sender() == self._ui_box_right:
                self.logger.debug("Right pane: clean selection")
                self.update_model_data(1, None)
                self._type_right = "depot"
                self._depot_data_right = []
                self._select_right = ""

    @pyqtSlot()
    def compare_leftright(self):
        self.logger.debug("Comparing sides")

        if self._compare is True:

            if self._type_left != self._type_right:

                if self._type_left == "depot":
                    tmpLeft = [(";").join([item.split(";")[0], "(repo<->depo)", item.split(";")[2], item.split(";")[3]])  for item in self._depot_data_left]
                else:
                    tmpLeft = [(";").join([item.split(";")[0], "(repo<->depo)", item.split(";")[2], item.split(";")[3]])  for item in self._repo_data_left]

                if self._type_right == "depot":
                    tmpRight = [(";").join([item.split(";")[0], "(repo<->depo)", item.split(";")[2], item.split(";")[3]])  for item in self._depot_data_right]
                else:
                    tmpRight = [(";").join([item.split(";")[0], "(repo<->depo)", item.split(";")[2], item.split(";")[3]])  for item in self._repo_data_right]

            else:

                if self._type_left == "depot":
                    tmpLeft = self._depot_data_left
                    tmpRight = self._depot_data_right
                else:
                    tmpLeft = self._repo_data_left
                    tmpRight = self._repo_data_right

            uniqueLeft = [item for item in tmpLeft if item not in tmpRight]
            uniqueRight = [item for item in tmpRight if item not in tmpLeft]

            self.update_model_data(0, uniqueLeft)
            self.update_model_data(1, uniqueRight)
            self.dataAquired.emit()

        else:
            self.side_content(self._ui_box_left.currentText().split()[0], "left")
            self.side_content(self._ui_box_right.currentText().split()[0], "right")
            self.dataAquired.emit()

    @pyqtSlot()
    def delete_from_repo(self, depot, packs):
        self.logger.debug("Delete file(s) from repository folder")
        if not packs:
            self._parent.msgbox(translate("depotmanagerController", "Nothing selected."), oPB.MsgEnum.MS_ALWAYS,
                                    parent = self.ui)
            return

        msg = "\n\n" + translate("depotmanagerController", "Selected depot:") + "\n" + depot
        pmsg = "\n\n" + translate("depotmanagerController", "Selected packages:") + "\n" + ("\n").join(packs)
        reply = self._parent.msgbox(translate("depotmanagerController", "Remove selected packages from repository now?") + msg + pmsg, oPB.MsgEnum.MS_QUEST_YESNO,
                                    parent = self.ui)
        if reply is True:
            self.logger.debug("Selected depot: " + depot)
            self.logger.debug("Selected packages: " + (", ").join(packs))

            self.dataAboutToBeAquired.emit(None)
            self._parent.do_deletefilefromrepo(packs = packs, dest = depot)
            self.dataAquired.emit()

            if self._active_side == "left":
                self._repo_data_left = []
                self.side_content(self._ui_box_left.currentText().split()[0], "left")
            else:
                self._repo_data_right = []
                self.side_content(self._ui_box_right.currentText().split()[0], "right")

            self.dataAquired.emit()

        else:
            self.logger.debug("Dialog canceled.")


    @pyqtSlot()
    def remove_from_depot(self, depot, packs):
        self.logger.debug("Uninstall product(s) from depot")
        if not packs:
            self._parent.msgbox(translate("depotmanagerController", "Nothing selected."), oPB.MsgEnum.MS_ALWAYS,
                                    parent = self.ui)
            return

        msg = "\n\n" + translate("depotmanagerController", "Selected depot:") + "\n" + depot
        pmsg = "\n\n" + translate("depotmanagerController", "Selected packages:") + "\n" + ("\n").join(packs)
        reply = self._parent.msgbox(translate("depotmanagerController", "Uninstall selected packages from depot now?") + msg + pmsg, oPB.MsgEnum.MS_QUEST_YESNO,
                                    parent = self.ui)
        if reply is True:
            self.logger.debug("Selected depot: " + depot)
            self.logger.debug("Selected packages: " + (", ").join(packs))

            BaseController.productsondepotslist = None
            self.dataAboutToBeAquired.emit(None)
            self._parent.do_quickuninstall(packs = packs, depot = depot)
            self.update_data(resetgui = False)

            if self._active_side == "left":
                self._select_left = ""
                self.side_content(self._ui_box_left.currentText().split()[0], "left")
            else:
                self._select_right = ""
                self.side_content(self._ui_box_right.currentText().split()[0], "right")

            self.dataAquired.emit()

        else:
            self.logger.debug("Dialog canceled.")

    @pyqtSlot()
    def unregister_depot(self):
        self.logger.debug("Unregister depot")
        if self._active_side == "left":
            depot = self._ui_box_left.currentText().split()[0]
        else:
            depot = self._ui_box_right.currentText().split()[0]

        msg = "<br><br><h3>" + translate("depotmanagerController", "Selected depot:") + "</h3>" + depot
        cfgmsg = "<br><br><h3>" + translate("depotmanagerController", "Config server:") + "</h3>" + ConfigHandler.cfg.opsi_server
        reply = self._parent.msgbox('<h2 class="warning">' +
                                    translate("depotmanagerController", "Do you really want to unregister the depot from the config server? This CAN'T be undone!") +
                                    "</h2>" + msg + cfgmsg, oPB.MsgEnum.MS_QUEST_YESNO,
                                    parent = self.ui)
        if reply is True:
            reply = self._parent.msgbox('<h2 class="warning">' +
                                        translate("depotmanagerController", "Are you absolutely sure?") +
                                        "</h2>" + msg + cfgmsg, oPB.MsgEnum.MS_QUEST_YESNO,
                                        parent = self.ui)
            if reply is True:
                self.logger.debug("Selected depot: " + depot)

                self.dataAboutToBeAquired.emit(None)
                self._parent.do_unregisterdepot(depot = depot)
                self.update_data()
                self.dataAquired.emit()

            else:
                self.logger.debug("Dialog canceled.")

        else:
            self.logger.debug("Dialog canceled.")

    @pyqtSlot()
    def set_rights(self):
        self.logger.debug("Set rights on repository")
        if self._active_side == "left":
            depot = self._ui_box_left.currentText().split()[0]
        else:
            depot = self._ui_box_right.currentText().split()[0]

        msg = "\n\n" + translate("depotmanagerController", "Selected depot:") + "\n\n" + depot
        reply = self._parent.msgbox(translate("depotmanagerController", "Set rights on repository folder now?") + msg, oPB.MsgEnum.MS_QUEST_YESNO,
                                    parent = self.ui)
        if reply is True:
            self.logger.debug("Selected depot: " + depot)

            self.dataAboutToBeAquired.emit(None)
            self._parent.do_setrights_on_repo(dest = depot)

            if self._active_side == "left":
                self._repo_data_left = []
                self.side_content(self._ui_box_left.currentText().split()[0], "left")
            else:
                self._repo_data_right = []
                self.side_content(self._ui_box_right.currentText().split()[0], "right")

            self.dataAquired.emit()

        else:
            self.logger.debug("Dialog canceled.")

    @pyqtSlot()
    def run_product_updater(self):
        self.logger.debug("Start produkt updater")
        if self._active_side == "left":
            depot = self._ui_box_left.currentText().split()[0]
        else:
            depot = self._ui_box_right.currentText().split()[0]

        msg = "\n\n" + translate("depotmanagerController", "Selected depot:") + "\n\n" + depot
        reply = self._parent.msgbox(translate("depotmanagerController", "Start opsi product updater now?") + msg, oPB.MsgEnum.MS_QUEST_YESNO,
                                    parent = self.ui)
        if reply is True:
            self.logger.debug("Selected depot: " + depot)

            self.dataAboutToBeAquired.emit(None)
            self._parent.do_runproductupdater(dest = depot)
            self.dataAquired.emit()

        else:
            self.logger.debug("Dialog canceled.")

    @pyqtSlot()
    def generate_md5(self, depot, packs):
        self.logger.info("Generate MD5")
        if not packs:
            return
        msg = "\n\n" + translate("depotmanagerController", "Selected depot:") + "\n" + depot
        pmsg = "\n\n" + translate("depotmanagerController", "Selected packages:") + "\n" + ("\n").join(packs)
        reply = self._parent.msgbox(translate("depotmanagerController", "Generate MD5 checksums now?") + msg + pmsg, oPB.MsgEnum.MS_QUEST_YESNO,
                                    parent = self.ui)
        if reply is True:
            self.logger.debug("Selected depot: " + depot)
            self.logger.debug("Selected packages: " + (", ").join(packs))

            self.dataAboutToBeAquired.emit(None)
            self._parent.do_generate_md5(packs = packs, dest = depot)

            if self._active_side == "left":
                self._repo_data_left = []
                self.side_content(self._ui_box_left.currentText().split()[0], "left")
            else:
                self._repo_data_right = []
                self.side_content(self._ui_box_right.currentText().split()[0], "right")

            self.dataAquired.emit()

        else:
            self.logger.debug("Dialog canceled.")

    @pyqtSlot()
    def onlinecheck(self):
        self.logger.info("Online check")
        if self._active_side == "left":
            depot = self._ui_box_left.currentText().split()[0]
        else:
            depot = self._ui_box_right.currentText().split()[0]

        msg = "\n\n" + translate("depotmanagerController", "Selected depot:") + "\n" + depot
        self.logger.debug("Selected depot: " + depot)

        ret = Helper.test_port(depot, ConfigHandler.cfg.sshport, 0.5)
        print(ret)

        if ret is True:
            self._parent.msgbox(translate("depotmanagerController", "The selected depot is ONLINE.") + msg, oPB.MsgEnum.MS_ALWAYS,
                                    parent = self.ui)
        else:
            msg  += "\n\n" + str(ret)
            self._parent.msgbox(translate("depotmanagerController", "The selected depot is OFFLINE.") + msg, oPB.MsgEnum.MS_ALWAYS,
                                    parent = self.ui)

    @pyqtSlot()
    def reboot_depot(self):
        self.logger.info("Reboot depot")

        if self._active_side == "left":
            depot = self._ui_box_left.currentText().split()[0]
        else:
            depot = self._ui_box_right.currentText().split()[0]

        msg = "\n\n" + translate("depotmanagerController", "Selected depot:") + "\n\n" + depot
        reply = self._parent.msgbox(translate("depotmanagerController", "Do you really want to reboot the selected depot?") + msg, oPB.MsgEnum.MS_QUEST_YESNO,
                                    parent = self.ui)
        if reply is True:
            self.logger.debug("Selected depot: " + depot)
            user = ""
            password = ""
            while user == "":
                (user, accept) = self._parent.msgbox(translate("depotmanagerController","Please enter username with sufficient priviledges:"),
                                    oPB.MsgEnum.MS_QUEST_PHRASE,
                                    parent = self.ui)
            while password == "":
                (password, accept) = self._parent.msgbox(translate("depotmanagerController","Please enter password:"), oPB.MsgEnum.MS_QUEST_PASS,
                                    parent = self.ui)

            self.dataAboutToBeAquired.emit(None)
            self._parent.do_reboot(user = user, password = password, dest = depot)
            self.dataAquired.emit()

        else:
            self.logger.debug("Dialog canceled.")


    @pyqtSlot()
    def poweroff_depot(self):
        self.logger.info("Poweroff depot")

        if self._active_side == "left":
            depot = self._ui_box_left.currentText().split()[0]
        else:
            depot = self._ui_box_right.currentText().split()[0]

        msg = "\n\n" + translate("depotmanagerController", "Selected depot:") + "\n\n" + depot
        reply = self._parent.msgbox(translate("depotmanagerController", "Do you really want to power off the selected depot?") + msg, oPB.MsgEnum.MS_QUEST_YESNO,
                                    parent = self.ui)
        if reply is True:
            self.logger.debug("Selected depot: " + depot)
            user = ""
            password = ""
            while user == "":
                (user, accept) = self._parent.msgbox(translate("depotmanagerController","Please enter username with sufficient priviledges:"),
                                                     oPB.MsgEnum.MS_QUEST_PHRASE, parent = self.ui, preload = "root")
            while password == "":
                (password, accept) = self._parent.msgbox(translate("depotmanagerController","Please enter password:"), oPB.MsgEnum.MS_QUEST_PASS,
                                    parent = self.ui)

            self.dataAboutToBeAquired.emit(None)
            self._parent.do_poweroff(user = user, password = password, dest = depot)
            self.dataAquired.emit()

        else:
            self.logger.debug("Dialog canceled.")

    @pyqtSlot()
    def report(self):
        self.logger.debug("Generate report")
        self._parent.ui.not_working()
        pass

    @pyqtSlot()
    def install(self):
        self.logger.debug("Quick install package")

        if self._active_side == "left":
            depot = self._ui_box_left.currentText().split()[0]
        else:
            depot = self._ui_box_right.currentText().split()[0]

        ext = "opsi Package (*.opsi)"  # generate file extension selection string for dialog

        script = QFileDialog.getOpenFileName(self.ui, translate("depotmanagerController", "Choose package file"),
                                            "", ext)

        if not script == ("", ""):
            self.logger.debug("Selected package: " + script[0])

            BaseController.productsondepotslist = None
            self.dataAboutToBeAquired.emit(None)
            self._parent.do_quickinstall(pack = script[0], depot = depot)
            self.update_data(resetgui = False)

            if self._active_side == "left":
                self._select_left = ""
                self.side_content(self._ui_box_left.currentText().split()[0], "left")
            else:
                self._select_right = ""
                self.side_content(self._ui_box_right.currentText().split()[0], "right")

            self.dataAquired.emit()

        else:
            self.logger.debug("Dialog canceled.")

    def retranslateMsg(self):
        self.logger.debug("Retranslating further messages...")
        """Retranslate model headers, will be called via changeEvent of self.ui """
        self.model_left.setHorizontalHeaderLabels([translate("depotmanagerController", "product id"),
                                        translate("depotmanagerController", "product version"),
                                        translate("depotmanagerController", "package version"),
                                        translate("depotmanagerController", "type")]
                                        )
        self.model_right.setHorizontalHeaderLabels([translate("depotmanagerController", "product id"),
                                        translate("depotmanagerController", "product version"),
                                        translate("depotmanagerController", "package version"),
                                        translate("depotmanagerController", "type")]
                                        )
        self.model_report.setHorizontalHeaderLabels([translate("depotmanagerController", "server name"),
                                        translate("depotmanagerController", "description")]
                                        )
