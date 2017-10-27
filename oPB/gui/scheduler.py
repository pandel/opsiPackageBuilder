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

from datetime import datetime
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QModelIndex
from PyQt5.Qt import QKeyEvent
import oPB
from oPB.gui.helpviewer import Help
from oPB.core.tools import LogMixin
from oPB.gui.utilities import EventMixin
from oPB.core.confighandler import ConfigHandler
from oPB.ui.ui import JobListDialogUI, JobCreatorDialogUI, JobListDialogBase, JobCreatorDialogBase
from oPB.gui.splash import Splash

translate = QtCore.QCoreApplication.translate


class JobListDialog(JobListDialogBase, JobListDialogUI, LogMixin, EventMixin):

    dialogOpened = pyqtSignal()
    dialogClosed = pyqtSignal()

    def __init__(self, parent):
        """
        Constructor for JobList dialog

        :param parent: parent controller instance
        :return:
        """
        self._parent = parent
        self._parentUi = parent._parent.ui

        JobListDialogBase.__init__(self, self._parentUi, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)
        self.setWindowIcon(self._parentUi.windowIcon())

        print("\tgui/JobListDialog parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None
        print("\tgui/JobListDialog parent: ", self._parentUi, " -> self: ", self) if oPB.PRINTHIER else None

        self.splash = Splash(self, translate("MainWindow", "Please wait..."))
        self.splash.close()  # only for linux

        self.helpviewer = Help(oPB.HLP_FILE, oPB.HLP_PREFIX, self)

        self.model = None

        self.assign_model(self._parent.model_jobs)

        self.connect_signals()

    def connect_signals(self):
        self.dialogOpened.connect(self.update_ui)
        self.finished.connect(self.dialogClosed.emit)
        self.btnRefresh.clicked.connect(lambda: self.update_ui(force = True))
        self.btnCreate.clicked.connect(self._parent.ui_jobcreator.show_)
        self.btnRemove.clicked.connect(self.delete_jobs)
        self.btnClearAll.clicked.connect(self._parent.delete_all_jobs)
        self.btnHelp.clicked.connect(lambda: self.helpviewer.showHelp(oPB.HLP_DST_JOBLIST, False))

    def keyPressEvent(self, evt: QKeyEvent):
        """
        Ignore escape key event, because it would close startup window.
        Any other key will be passed to the super class key event handler for further
        processing.

        :param evt: key event
        :return:
        """
        if evt.key() == QtCore.Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(evt)
        pass

    def assign_model(self, model):
        self.model = model
        self.tblJobs.setModel(self.model)
        self.resizeTable()

    def resizeTable(self):
        self.tblJobs.resizeRowsToContents()
        self.tblJobs.resizeColumnsToContents()
        self.tblJobs.sortByColumn(5, QtCore.Qt.AscendingOrder)

    def show_(self):
        self.logger.debug("Show job list dialog")
        if ConfigHandler.cfg.no_at_warning_msg == "False":
            self.usage_hint()

        self.show()
        self.activateWindow()

        self.dialogOpened.emit()

    def usage_hint(self):
        """Show longer AT usage hint message"""

        msg = translate("infoMessages", "infoAT")
        self._parent.msgbox(msg, oPB.MsgEnum.MS_ALWAYS)

    def update_ui(self, force = False):
        """
        Update model data and reset tableview

        See: :meth:`oPB.controller.components.scheduler.SchedulerComponent.update_model_data_jobs`

        :param force: Force ui AND backend data refresh
        """
        self.splash.show_()
        self.splash.setProgress(50)
        self._parent.update_model_data_jobs(force = force)
        self.setWindowTitle(translate("JobListDialog", "Job list") + translate("JobListDialog", " - Current server: ") + self._parent.at_server)
        self.resizeTable()
        self.splash.close()

    def delete_jobs(self):
        """Initiate job deletion via backend

        See: :meth:`oPB.controller.components.scheduler.SchedulerComponent.delete_jobs`
        """
        self.splash.show_()

        selection = self.tblJobs.selectionModel().selectedRows()
        remIdx = []
        for row in selection:
            remIdx.append(self.model.item(row.row(),5).text())

        self._parent.delete_jobs(remIdx)
        self.splash.close()

    def retranslateMsg(self):
        self.logger.debug("Retranslating further messages...")
        self.splash.msg = translate("MainWindow", "Please wait...")

class JobCreatorDialog(JobCreatorDialogBase, JobCreatorDialogUI, LogMixin, EventMixin):

    dialogOpened = pyqtSignal()
    dialogClosed = pyqtSignal()

    def __init__(self, parent):
        """
        Constructor for JobCreator dialog

        :param parent: parent controller instance
        :return:
        """
        self._parent = parent
        self._parentUi = parent._parent.ui

        JobCreatorDialogBase.__init__(self, self._parentUi, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)
        self.setWindowIcon(self._parentUi.windowIcon())

        print("\tgui/JobCreatorDialog parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None
        print("\tgui/JobCreatorDialog parentUi: ", self._parentUi, " -> self: ", self) if oPB.PRINTHIER else None

        self.splash = Splash(self, translate("MainWindow", "Please wait..."))
        self.splash.close()  # only for linux

        self.model_clients = None
        self.model_products = None

        self.assign_model(self._parent.model_clients, self._parent.model_products)

        self.dateSelector.setSelectedDate(datetime.now().date())
        self.timeSelector.setTime(datetime.now().time())

        self.connect_signals()

    def connect_signals(self):
        self.dialogOpened.connect(self.update_ui)
        self.btnCreate.clicked.connect(self.create_jobs)
        self.finished.connect(lambda: self._parent.ui_joblist.update_ui(True))
        self.btnHelp.clicked.connect(lambda: oPB.gui.helpviewer.Help(oPB.HLP_FILE, oPB.HLP_PREFIX, oPB.HLP_DST_JOBCREATOR))

    def keyPressEvent(self, evt: QKeyEvent):
        """
        Ignore escape key event, because it would close startup window.
        Any other key will be passed to the super class key event handler for further
        processing.

        :param evt: key event
        :return:
        """
        if evt.key() == QtCore.Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(evt)
        pass

    def assign_model(self, model_clients, model_products):
        self.model_clients = model_clients
        self.model_products = model_products
        self.tblClients.setModel(self.model_clients)
        self.tblProducts.setModel(self.model_products)

    def show_(self):
        self.logger.debug("Show job creator dialog")

        self.show()

        w = self.splitter.geometry().width()
        self.splitter.setSizes([w*(2/5), w*(3/5)])

        self.activateWindow()

        self.dialogOpened.emit()


    def spanParents(self, model, parent=QModelIndex()):
        """Iterate through the whole Qtreeview model to span to headlines

        see: https://stackoverflow.com/questions/33124903/how-to-iterate-trough-a-qstandarditemmodel-completely

        :param model: data model of the QTreeview
        :param parent: current QModelIndex to inspect for children
        """

        # the first ``parent`` is invalid, so ``childcount`` returns 1 (for root)
        # in any succeeding recursion it returns the actual row count of children
        childcount = model.rowCount(parent)

        for r in range(0, childcount):
            # get the index of the first column item in the topmost row based on  parent
            index = model.index(r, 0, parent)
            name = model.data(index)
            # these two are always there, so span them anyways
            if name == "clientdirectory" or name == "software-on-demand":
                self.tblClients.setFirstColumnSpanned(r, parent, True)

            # if the model has children at the index position, it must be a headline, so span it
            # this possibly leads to spanning clientdirectory and/or sod twice, but who cares...
            if model.hasChildren(index):
                self.tblClients.setFirstColumnSpanned(r, parent, True)
                self.spanParents(model, index)


    def update_ui(self):
        """
        Update model data and reset tableview

        See: :meth:`oPB.controller.components.scheduler.SchedulerComponent.update_model_data_clients`
        See: :meth:`oPB.controller.components.scheduler.SchedulerComponent.update_model_data_products`
        """
        self.splash.show_()
        self.splash.setProgress(10)
        self._parent.update_model_data_clients()

        self.splash.setProgress(80)
        self._parent.update_model_data_products()

        self.tblClients.expand(self.model_clients.item(0).index())
        self.tblProducts.resizeRowsToContents()
        self.tblProducts.resizeColumnsToContents()

        self.tblClients.setSortingEnabled(True)

        self.spanParents(self.tblClients.model())

        self.splash.close()

    def create_jobs(self):
        """
        Initiate AT job creation via backend

        See: :meth:`oPB.controller.components.scheduler.SchedulerComponent.create_jobs`
        """
        self.logger.debug("Create AT jobs")

        self.splash.show_()

        # get selected clients
        selection = self.tblClients.selectedIndexes()
        clIdx = []
        for row in selection:
            clIdx.append(row.model().itemFromIndex(row).text().split()[0])

        # get selected products
        selection = self.tblProducts.selectionModel().selectedRows()
        prodIdx = []
        for row in selection:
            prodIdx.append(self.model_products.item(row.row(), 0).text())

        # get date/time
        dateVal = self.dateSelector.selectedDate().toString("yyyyMMdd")
        timeVal = self.timeSelector.time().toString("hhmm")

        # get action
        if self.rdInstall.isChecked():
            action = "setup"
        if self.rdUninstall.isChecked():
            action = "uninstall"
        if self.rdUpdate.isChecked():
            action = "update"
        if self.rdCustom.isChecked():
            action = "custom"

        # get options
        od = False
        if self.chkOnDemand.isChecked():
            od = True
        wol = False
        if self.chkWOL.isChecked():
            wol = True

        self._parent.create_jobs(clients = clIdx, products = prodIdx, ataction = action, dateVal = dateVal, timeVal = timeVal, on_demand = od, wol = wol)

        self.splash.close()
        self.close()

    def retranslateMsg(self):
        self.logger.debug("Retranslating further messages...")
        self.splash.msg = translate("MainWindow", "Please wait...")