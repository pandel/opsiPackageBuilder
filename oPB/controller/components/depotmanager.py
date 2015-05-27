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
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
import oPB
from oPB.core.tools import Helper
from oPB.controller.base import BaseController
from oPB.core.confighandler import ConfigHandler
from oPB.gui.depotmanager import DepotManagerDialog

translate = QtCore.QCoreApplication.translate

class DepotManagerComponent(BaseController, QObject):

    dataAboutToBeAquired = pyqtSignal(int)
    dataAquired = pyqtSignal()
    modelDataUpdated = pyqtSignal()

    def __init__(self, parent):
        super().__init__(self)

        self._parent = parent
        self.ui = None
        self.model_left = None
        self.model_right = None
        self._data_left = []
        self._data_right = []
        self._type_left = "depot"  # depot / repo modus
        self._type_right = "depot"  # depot / repo modus
        self._ui_box_left = None  # left depot combobox selecotor
        self._ui_box_right = None  # right depot combobox selecotor
        self._ui_repobtn_left = None  # left fetch repo button
        self._ui_repobtn_right = None  # right fetch repo button
        self._active_side = None

        self._compare = False

        self.generate_model()

        self.ui = DepotManagerDialog(self)

    def generate_model(self):
        # create model from data and assign, if not done before
        if self.model_left == None:
            self.logger.debug("Generate left table model")
            self.model_left = QtGui.QStandardItemModel(0, 3, self)
            self.model_left.setObjectName("model_left")
            self.model_left.setHorizontalHeaderLabels([translate("quickuninstallController", "product id"),
                                            translate("quickuninstallController", "product version"),
                                            translate("quickuninstallController", "package version"),
                                            translate("quickuninstallController", "type")]
                                            )

        if self.model_right == None:
            self.logger.debug("Generate right table model")
            self.model_right = QtGui.QStandardItemModel(0, 3, self)
            self.model_right.setObjectName("model_right")
            self.model_right.setHorizontalHeaderLabels([translate("quickuninstallController", "product id"),
                                            translate("quickuninstallController", "product version"),
                                            translate("quickuninstallController", "package version"),
                                            translate("quickuninstallController", "type")]
                                            )

    def update_model_data(self, side, depot, dict):
        self.logger.debug("Update model data")

        tmplist = []
        prodlist = []
        if dict:
            for elem in dict:
                d = elem.split(";")
                if d[4] == depot:
                    prodlist.append((";").join([d[0], "", d[2],d[3]]))
                    tmplist.append([d[0], d[2], d[3], d[1]])

        if side == 0:
            self._parent.update_table_model(self.model_left, sorted(tmplist))
            # save abstract product list, but only if NOT in comparison mode
            if self._compare is False:
                self._data_left = prodlist
        else:
            self._parent.update_table_model(self.model_right, sorted(tmplist))
            # save abstract product list, but only if NOT in comparison mode
            if self._compare is False:
                self._data_right = prodlist

    def update_data(self):
        self.logger.debug("Update data")

        if self.sender() == self.ui.btnRefresh:
            self._type_left = "depot" # depot / repo modus
            self._type_right = "depot"  # depot / repo modus
            self._compare = False
            Force = True
        else:
            Force = False

        self.dataAboutToBeAquired.emit(33)

        if ConfigHandler.cfg.depotcache == {} or Force == True:
            self._parent.do_getdepots()

        self.dataAboutToBeAquired.emit(66)

        if BaseController.productsondepotslist == None or Force == True:
            self._parent.do_getproductsondepots()

        self.modelDataUpdated.emit()

    @pyqtSlot()
    def switch_content(self):
        self.logger.debug("Switch content")

        # if self.sender() == self._ui_box_left:
        #     self.logger.debug("Sender is left combo box")
        #     self.side_content(self._ui_box_left.currentText(), "left")
        #
        # if self.sender() == self._ui_box_right:
        #     self.logger.debug("Sender is right combo box")
        #     self.side_content(self._ui_box_right.currentText(), "right")

        if self.sender() == self._ui_repobtn_left:
            self.logger.debug("Sender is left button")
            if self._type_left == "depot":
                self._type_left = "repo"
            else:
                self._type_left = "depot"
            self.side_content(self._ui_box_left.currentText(), "left")

        if self.sender() == self._ui_repobtn_right:
            self.logger.debug("Sender is right button")
            if self._type_right == "depot":
                self._type_right = "repo"
            else:
                self._type_right = "depot"
            self.side_content(self._ui_box_right.currentText(), "right")

        if self._compare is True:
            self.compare_leftright()

    @pyqtSlot(str)
    def side_content(self, param, side = None):

        if param != "":
            if self.sender() == self._ui_box_left or side == "left":
                self.dataAboutToBeAquired.emit(33)
                if self._type_left == "repo":
                    self.logger.debug("Left pane: repo content")
                    tmplist = self._parent.do_getrepocontent(param.split()[0])
                    self.update_model_data(0, param.split()[0], tmplist)
                else:
                    self.logger.debug("Left pane: depot content")
                    self.update_model_data(0, param.split()[0], BaseController.productsondepotslist)

            if self.sender() == self._ui_box_right or side == "right":
                self.dataAboutToBeAquired.emit(66)
                if self._type_right == "repo":
                    self.logger.debug("Right pane: repo content")
                    tmplist = self._parent.do_getrepocontent(param.split()[0])
                    self.update_model_data(1, param.split()[0], tmplist)
                else:
                    self.logger.debug("Right pane: depot content")
                    self.update_model_data(1, param.split()[0], BaseController.productsondepotslist)

        else:
            if self.sender() == self._ui_box_left:
                self.dataAboutToBeAquired.emit(33)
                self.logger.debug("Left pane: clean selection")
                self.update_model_data(0, "", None)
                self._type_left = "depot"

            if self.sender() == self._ui_box_right:
                self.dataAboutToBeAquired.emit(66)
                self.logger.debug("Right pane: clean selection")
                self.update_model_data(1, "", None)
                self._type_right = "depot"

        self.dataAquired.emit()

    @pyqtSlot()
    def compare_leftright(self):
        self.logger.debug("Comparing sides")

        if self._compare is True:

            uniqueLeft = [item for item in self._data_left if item not in self._data_right]
            uniqueRight = [item for item in self._data_right if item not in self._data_left]

            if self._type_left != self._type_right:
                uniqueLeft = [item.replace(";;",";(repo<->depo);") for item in uniqueLeft]
                uniqueRight = [item.replace(";;",";(repo<->depo);") for item in uniqueRight]

            self.update_model_data(0, self._ui_box_left.currentText(), [item + ";" + self._ui_box_left.currentText() for item in uniqueLeft])
            self.update_model_data(1, self._ui_box_right.currentText(), [item + ";" + self._ui_box_right.currentText() for item in uniqueRight])

        else:
            self.side_content(self._ui_box_left.currentText(), "left")
            self.side_content(self._ui_box_right.currentText(), "right")

        self.dataAquired.emit()

    @pyqtSlot()
    def delete_from_repo(self):
        self.logger.debug("Delete product from repository folder")
        self._parent.ui.not_working()
        pass

    @pyqtSlot()
    def remove_from_depot(self):
        self.logger.debug("Remove product from depot")
        self._parent.ui.not_working()
        pass

    @pyqtSlot()
    def unregister_depot(self):
        self.logger.debug("Unregister depot")
        self._parent.ui.not_working()
        pass

    @pyqtSlot()
    def set_rights(self):
        self.logger.debug("Set rights")
        self._parent.ui.not_working()
        pass

    @pyqtSlot()
    def run_product_updater(self):
        self.logger.debug("Start produkt updater")
        if self._active_side == "left":
            depot = self._ui_box_left.currentText().split()[0]
        else:
            depot = self._ui_box_right.currentText().split()[0]

        msg = "\n\n" + translate("depotmanagerController", "Selected depot:") + "\n\n" + depot
        reply = self._parent.msgbox(translate("depotmanagerController", "Start opsi product updater now?") + msg, oPB.MsgEnum.MS_QUEST_YESNO)
        if reply is True:
            self.logger.debug("Selected depot: " + depot)

            self.dataAboutToBeAquired.emit(0)
            self._parent.do_runproductupdater(depot)
            self.dataAquired.emit()

    @pyqtSlot()
    def generate_md5(self):
        self.logger.debug("Generate MD5")
        self._parent.ui.not_working()
        pass

    @pyqtSlot()
    def onlinecheck(self):
        self.logger.debug("Online check")
        if self._active_side == "left":
            depot = self._ui_box_left.currentText().split()[0]
        else:
            depot = self._ui_box_right.currentText().split()[0]

        msg = "\n\n" + translate("depotmanagerController", "Selected depot:") + "\n" + depot
        self.logger.debug("Selected depot: " + depot)

        ret = Helper.test_port(depot, ConfigHandler.cfg.sshport, 0.5)
        print(ret)

        if ret is True:
            self._parent.msgbox(translate("depotmanagerController", "The selected depot is ONLINE.") + msg, oPB.MsgEnum.MS_ALWAYS)
        else:
            msg  += "\n\n" + str(ret)
            self._parent.msgbox(translate("depotmanagerController", "The selected depot is OFFLINE.") + msg, oPB.MsgEnum.MS_ALWAYS)

    @pyqtSlot()
    def reboot_depot(self):
        self.logger.debug("Reboot depot")

        if self._active_side == "left":
            depot = self._ui_box_left.currentText().split()[0]
        else:
            depot = self._ui_box_right.currentText().split()[0]

        msg = "\n\n" + translate("depotmanagerController", "Selected depot:") + "\n\n" + depot
        reply = self._parent.msgbox(translate("depotmanagerController", "Do you really want to reboot the selected depot?") + msg, oPB.MsgEnum.MS_QUEST_YESNO)
        if reply is True:
            self.logger.debug("Selected depot: " + depot)
            user = ""
            password = ""
            while user == "":
                (user, accept) = self._parent.msgbox(translate("depotmanagerController","Please enter username with sufficient priviledges:"), oPB.MsgEnum.MS_QUEST_PHRASE)
            while password == "":
                (password, accept) = self._parent.msgbox(translate("depotmanagerController","Please enter password:"), oPB.MsgEnum.MS_QUEST_PASS)

            self.dataAboutToBeAquired.emit(0)
            self._parent.do_reboot(depot, user, password)
            self.dataAquired.emit()


    @pyqtSlot()
    def poweroff_depot(self):
        self.logger.debug("Poweroff depot")

        if self._active_side == "left":
            depot = self._ui_box_left.currentText().split()[0]
        else:
            depot = self._ui_box_right.currentText().split()[0]

        msg = "\n\n" + translate("depotmanagerController", "Selected depot:") + "\n\n" + depot
        reply = self._parent.msgbox(translate("depotmanagerController", "Do you really want to power off the selected depot?") + msg, oPB.MsgEnum.MS_QUEST_YESNO)
        if reply is True:
            self.logger.debug("Selected depot: " + depot)
            user = ""
            password = ""
            while user == "":
                (user, accept) = self._parent.msgbox(translate("depotmanagerController","Please enter username with sufficient priviledges:"), oPB.MsgEnum.MS_QUEST_PHRASE)
            while password == "":
                (password, accept) = self._parent.msgbox(translate("depotmanagerController","Please enter password:"), oPB.MsgEnum.MS_QUEST_PASS)

            self.dataAboutToBeAquired.emit(0)
            self._parent.do_poweroff(depot, user, password)
            self.dataAquired.emit()

    @pyqtSlot()
    def report(self):
        self.logger.debug("Generate report")
        self._parent.ui.not_working()
        pass
