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
from oPB.gui.mainwindow import Splash

translate = QtCore.QCoreApplication.translate

class SchedulerComponent(BaseController, QObject):

    def __init__(self, parent):
        super().__init__(self)

        self._parent = parent
        self.model_clients = None
        self.model_products = None
        self.model_jobs = None

        # create ui and assign models, signals
        self.ui_joblist = JobListDialog(self._parent.ui)
        self.ui_jobcreator = JobCreatorDialog(self._parent.ui)

        self.splash = Splash(None, translate("MainWindow", "Please wait..."), True)
        self.splash.close()  # only for linux

        self.joblist_generate_model()
        self.jobcreator_generate_model()

        self.joblist_connect_signals()
        self.jobcreator_connect_signals()

    def show_joblist(self):
        self.logger.debug("Show job list")

        if ConfigHandler.cfg.no_at_warning_msg == "False":
            self.usage_hint()

        self._parent.startup.hide_me()
        self.ui_joblist.show()

        # first time opened after program start?
        if not BaseController.joblist:
            self.update_model_data_jobs(50)

        self.ui_joblist.activateWindow()

    def show_jobcreator(self):
        self.logger.debug("Show job creator")

        # set splitter posision
        self.ui_jobcreator.show()
        w = self.ui_jobcreator.splitter.geometry().width()
        self.ui_jobcreator.splitter.setSizes([w*(2/5), w*(3/5)])

        # first time opened after program start?
        if BaseController.clientlist_dict == None:
            self.update_model_data_clients(0)

        # first time opened after program start?
        if BaseController.productlist_dict == None:
            self.update_model_data_products(50)

        self.ui_jobcreator.activateWindow()

    def joblist_connect_signals(self):
        self.logger.debug("Connect signals: job list")
        self.ui_joblist.finished.connect(self._parent.startup.show_me)
        self.ui_joblist.btnRefresh.clicked.connect(self.update_model_data_jobs)
        self.ui_joblist.btnCreate.clicked.connect(self.show_jobcreator)
        self.ui_joblist.btnRemove.clicked.connect(self.joblist_delete_jobs)
        self.ui_joblist.btnClearAll.clicked.connect(self.joblist_delete_all_jobs)
        self.ui_joblist.btnHelp.clicked.connect(self._parent.ui.not_working)

    def jobcreator_connect_signals(self):
        self.logger.debug("Connect signals: job creator")
        self.ui_jobcreator.finished.connect(self.update_model_data_jobs)
        self.ui_jobcreator.btnCreate.clicked.connect(self.jobcreator_create_jobs)

    def joblist_generate_model(self):
        if self.model_jobs == None:
            self.logger.debug("Generate job table model")
            self.model_jobs = QtGui.QStandardItemModel(0, 7, self)
            self.model_jobs.setObjectName("model_jobs")
            self.model_jobs.setHorizontalHeaderLabels([translate("schedulerController_joblist", "client"),
                                            translate("schedulerController_joblist", "packet"),
                                            translate("schedulerController_joblist", "action"),
                                            translate("schedulerController_joblist", "date"),
                                            translate("schedulerController_joblist", "time"),
                                            translate("schedulerController_joblist", "AT jobid"),
                                            translate("schedulerController_joblist", "user")]
                                            )
            self.ui_joblist.assign_model(self.model_jobs)

    def jobcreator_generate_model(self):
        # create model from data and assign, if not done before
        if self.model_clients == None:
            self.logger.debug("Generate client table model")
            self.model_clients = QtGui.QStandardItemModel(0, 1, self)
            self.model_clients.setObjectName("model_clients")
            self.model_clients.setHorizontalHeaderLabels([translate("schedulerController_jobcreator", "client")]
                                            )

        if self.model_products == None:
            self.logger.debug("Generate product table model")
            self.model_products = QtGui.QStandardItemModel(0, 3, self)
            self.model_products.setObjectName("model_products")
            self.model_products.setHorizontalHeaderLabels([translate("quickuninstallController", "product id"),
                                            translate("quickuninstallController", "version"),
                                            translate("quickuninstallController", "description")]
                                            )

            self.ui_jobcreator.assign_model(self.model_clients, self.model_products)

    def update_model_data_clients(self, progress = 0):
        self.logger.debug("Update model data: clients")

        self.splash_show(self.ui_jobcreator)
        self.splash.setProgress(progress)

        self._parent.do_getclients()

        if BaseController.clientlist_dict:
            tmplist = []
            for elem in BaseController.clientlist_dict:
                tmplist.append([elem["id"] + " (" + elem["description"] + ")"])

            self._parent.update_table_model(self.model_clients, sorted(tmplist))

        self.ui_jobcreator.resizeTableClients()

        self.splash.close()

    def update_model_data_products(self, progress = 0):
        self.logger.debug("Update model data: products")

        self.splash_show(self.ui_jobcreator)
        self.splash.setProgress(progress)

        self._parent.do_getproducts()

        if BaseController.productlist_dict:
            tmplist = []
            for elem in BaseController.productlist_dict:
                tmplist.append([elem["id"], elem["productVersion"] + "-" + elem["packageVersion"], elem["name"]])

            self._parent.update_table_model(self.model_products, sorted(tmplist))

        self.ui_jobcreator.resizeTableProducts()

        self.splash.close()

    def update_model_data_jobs(self, progress = 0):
        self.logger.debug("Update model data: jobs")

        self.splash_show(self.ui_joblist)
        self.splash.setProgress(progress)

        self._parent.do_getjobs()

        self._parent.update_table_model(self.model_jobs, sorted(BaseController.joblist))

        self.ui_joblist.resizeTable()

        self.splash.close()

    def splash_show(self, parent):
        self.splash.setParent(parent)
        self.splash.show_()

    def joblist_delete_jobs(self):
        self.logger.debug("Remove selected AT jobs")

        if self.ui_joblist.tblJobs.selectionModel().hasSelection():
            reply = self._parent.msgbox(translate("schedulerController", "Do you really want to remove the selected job id(s)? This can't be undone!"),
                                        oPB.MsgEnum.MS_QUEST_YESNO)
            if reply is True:
                self.logger.debug("Remove AT jobs")

                self.splash_show(self.ui_joblist)
                self.splash.setProgress(0)

                selection = self.ui_joblist.tblJobs.selectionModel().selectedRows()
                remIdx = []
                for row in selection:
                    remIdx.append(self.model_jobs.item(row.row(),5).text())

                self._parent.do_deletejobs(remIdx)
                self.update_model_data_jobs(50)
        else:
            self.logger.debug("Deletion canceled")

    def joblist_delete_all_jobs(self):
        self.logger.debug("Remove every AT job")

        if BaseController.joblist:
            reply = self._parent.msgbox(translate("schedulerController", "Do you really want to remove all job(s)? This can't be undone!"),
                                        oPB.MsgEnum.MS_QUEST_YESNO)
            if reply is True:
                self.splash_show(self.ui_joblist)
                self.splash.setProgress(0)

                self._parent.do_deletealljobs()

                self.update_model_data_jobs(50)
            else:
                self.logger.debug("Deletion canceled")

    def jobcreator_create_jobs(self):
        self.logger.debug("Create AT jobs")

        if not self.ui_jobcreator.tblClients.selectionModel().hasSelection():
            self.logger.debug("No clients selected")
            self._parent.msgbox(translate("schedulerController", "No opsi client selected."), oPB.MsgEnum.MS_WARN)
            return

        if not self.ui_jobcreator.tblProducts.selectionModel().hasSelection():
            self.logger.debug("No product selected")
            self._parent.msgbox(translate("schedulerController", "No opsi product selected."), oPB.MsgEnum.MS_WARN)
            return

        reply = self._parent.msgbox(translate("schedulerController", "Create AT jobs now?"),
                                    oPB.MsgEnum.MS_QUEST_YESNO)
        if reply is True:
            self.splash_show(self.ui_jobcreator)
            self.splash.setProgress(0)

            # get selected clients
            selection = self.ui_jobcreator.tblClients.selectionModel().selectedRows()
            clIdx = []
            for row in selection:
                clIdx.append(self.model_clients.item(row.row(),0).text().split()[0])

            # get selected products
            selection = self.ui_jobcreator.tblProducts.selectionModel().selectedRows()
            prodIdx = []
            for row in selection:
                prodIdx.append(self.model_products.item(row.row(),0).text())

            # get date/time
            dateVal = self.ui_jobcreator.dateSelector.selectedDate().toString("yyyyMMdd")
            timeVal = self.ui_jobcreator.timeSelector.time().toString("hhmm")

            # get action
            if self.ui_jobcreator.rdInstall.isChecked():
                action = "setup"
            if self.ui_jobcreator.rdUninstall.isChecked():
                action = "uninstall"
            if self.ui_jobcreator.rdUpdate.isChecked():
                action = "update"
            if self.ui_jobcreator.rdCustom.isChecked():
                action = "custom"

            # get options
            od = False
            if self.ui_jobcreator.chkOnDemand.isChecked():
                od = True
            wol = False
            if self.ui_jobcreator.chkWOL.isChecked():
                wol = True

            self._parent.do_createjobs(clients = clIdx, products = prodIdx, ataction = action, dateVal = dateVal, timeVal = timeVal, on_demand = od, wol = wol)

            self.ui_jobcreator.close()

    def usage_hint(self):
        msg = translate("infoMessages", "infoAT")
        self._parent.msgbox(msg, oPB.MsgEnum.MS_ALWAYS)
