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
from PyQt5.QtCore import QObject

import oPB
from oPB.core.confighandler import ConfigHandler
from oPB.controller.base import BaseController
from oPB.gui.scheduler import JobListDialog, JobCreatorDialog

translate = QtCore.QCoreApplication.translate

class SchedulerComponent(BaseController, QObject):

    def __init__(self, parent):
        super().__init__(self)

        self._parent = parent
        print("controller/SchedulerComponent parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None

        self.model_clients = None
        self.model_products = None
        self.model_jobs = None
        self.at_server = ""

        self.msgbox = self._parent.msgbox

        self.generate_model()

        # create ui and assign models, signals
        self.ui_jobcreator = JobCreatorDialog(self)
        self.ui_joblist = JobListDialog(self)

        self.connect_signals()

    def connect_signals(self):
        self.ui_joblist.dialogOpened.connect(self._parent.startup.hide_)
        self.ui_joblist.dialogClosed.connect(self._parent.startup.show_)

    def generate_model(self):
        if self.model_jobs == None:
            self.logger.debug("Generate job table model")
            self.model_jobs = QtGui.QStandardItemModel(0, 7, self)
            self.model_jobs.setObjectName("model_jobs")
        # create model from data and assign, if not done before
        if self.model_clients == None:
            self.logger.debug("Generate client table model")
            self.model_clients = QtGui.QStandardItemModel(0, 1, self)
            self.model_clients.setObjectName("model_clients")
        if self.model_products == None:
            self.logger.debug("Generate product table model")
            self.model_products = QtGui.QStandardItemModel(0, 3, self)
            self.model_products.setObjectName("model_products")

        self.retranslateMsg()

    def update_model_data_clients(self, force = False):
        self.logger.debug("Update model data: clients")

        # first time opened after program start?
        if BaseController.clientlist_dict == None or force == True:
            self._parent.do_getclients(dest = self.at_server)

        if BaseController.clientlist_dict:
            tmplist = []
            for elem in BaseController.clientlist_dict:
                tmplist.append([elem["id"] + " (" + elem["description"] + ")"])

            self._parent.update_table_model(self.model_clients, sorted(tmplist))

    def update_model_data_products(self, force = False):
        self.logger.debug("Update model data: products")

        if BaseController.productlist_dict == None or force == True:
            self._parent.do_getproducts(dest = self.at_server)

        if BaseController.productlist_dict:
            tmplist = []
            for elem in BaseController.productlist_dict:
                tmplist.append([elem["id"], elem["productVersion"] + "-" + elem["packageVersion"], elem["name"]])

            self._parent.update_table_model(self.model_products, sorted(tmplist))

    def update_model_data_jobs(self, force = False, querydepot = True):
        self.logger.debug("Update model data: jobs")

        # not the first time after program start?
        if not BaseController.joblist or force == True:
            if querydepot is True:
                self.at_server = self._parent.query_depot(with_all = False, parent = self.ui_joblist)
            self._parent.do_getjobs(dest = self.at_server)

        self._parent.update_table_model(self.model_jobs, sorted(BaseController.joblist))

    def delete_jobs(self, jobs = []):
        self.logger.debug("Remove selected AT jobs")

        if jobs:
            reply = self._parent.msgbox(translate("schedulerController", "Do you really want to remove the selected job id(s)? This can't be undone!"),
                                        oPB.MsgEnum.MS_QUEST_YESNO)
            if reply is True:
                self.logger.debug("Remove AT jobs")
                self._parent.do_deletejobs(joblist = jobs, dest = self.at_server)
                self.update_model_data_jobs(force = True, querydepot = False)
        else:
            self.logger.debug("Deletion canceled")

    def delete_all_jobs(self):
        self.logger.debug("Remove every AT job")

        if BaseController.joblist:
            reply = self._parent.msgbox(translate("schedulerController", "Do you really want to remove all job(s)? This can't be undone!"),
                                        oPB.MsgEnum.MS_QUEST_YESNO)
            if reply is True:
                self._parent.do_deletealljobs(dest = self.at_server)
                self.update_model_data_jobs(force = True, querydepot = False)
            else:
                self.logger.debug("Deletion canceled")

    def create_jobs(self, clients = [], products = [], ataction = "", dateVal = "", timeVal = "", on_demand = False, wol = False):
        self.logger.debug("Create AT jobs")

        if not clients:
            self.logger.debug("No clients selected")
            self._parent.msgbox(translate("schedulerController", "No opsi client selected."), oPB.MsgEnum.MS_WARN)
            return

        if not products:
            self.logger.debug("No product selected")
            self._parent.msgbox(translate("schedulerController", "No opsi product selected."), oPB.MsgEnum.MS_WARN)
            return

        reply = self._parent.msgbox(translate("schedulerController", "Create AT jobs now?"),
                                    oPB.MsgEnum.MS_QUEST_YESNO)
        if reply is True:
            self._parent.do_createjobs(clIdx = clients, prodIdx = products, ataction = ataction, dateVal = dateVal,
                                       timeVal = timeVal, od_demand = on_demand, wol = wol, dest = self.at_server)

    def retranslateMsg(self):
        self.logger.debug("Retranslating further messages...")
        """Retranslate model headers, will be called via changeEvent of self.ui """
        self.model_jobs.setHorizontalHeaderLabels([translate("schedulerController_joblist", "client"),
                                        translate("schedulerController_joblist", "packet"),
                                        translate("schedulerController_joblist", "action"),
                                        translate("schedulerController_joblist", "date"),
                                        translate("schedulerController_joblist", "time"),
                                        translate("schedulerController_joblist", "AT jobid"),
                                        translate("schedulerController_joblist", "user")]
                                        )
        self.model_clients.setHorizontalHeaderLabels([translate("schedulerController_jobcreator", "client")]
                                        )
        self.model_products.setHorizontalHeaderLabels([translate("quickuninstallController", "product id"),
                                        translate("quickuninstallController", "version"),
                                        translate("quickuninstallController", "description")]
                                        )
