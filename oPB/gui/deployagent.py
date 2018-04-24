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

from collections import deque
import re
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.Qt import QKeyEvent
import oPB
from oPB.gui.helpviewer import Help
from oPB.core.tools import LogMixin
from oPB.core.confighandler import ConfigHandler
from oPB.gui.utilities import SpecialOptionButtonGroup, EventMixin
from oPB.ui.ui import DeployAgentDialogUI, DeployAgentDialogBase
from oPB.gui.splash import Splash

translate = QtCore.QCoreApplication.translate


class DeployAgentDialog(DeployAgentDialogBase, DeployAgentDialogUI, LogMixin, EventMixin):

    dialogOpened = pyqtSignal()
    dialogClosed = pyqtSignal()

    def __init__(self, parent):
        """
        Constructor for deploy opsi client agent dialog

        :param parent: parent controller instance
        :return:
        """
        self._parent = parent
        self._parentUi = parent._parent.ui

        DeployAgentDialogBase.__init__(self, self._parentUi, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)
        self.setWindowIcon(self._parentUi.windowIcon())

        print("\tgui/DeployAgentDialog parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None
        print("\tgui/DeployAgentDialog parentUi: ", self._parentUi, " -> self: ", self) if oPB.PRINTHIER else None

        self.splash = Splash(self, translate("MainWindow", "Please wait..."))
        self.splash.close()  # only for linux

        self.helpviewer = Help(oPB.HLP_FILE, oPB.HLP_PREFIX, self)

        self.create_optionsgroups()
        self.optionGroupDeploy.setChecked(self.chkDeployToMulti.isChecked())

        self.connect_signals()

    def connect_signals(self):
        self.finished.connect(self.dialogClosed.emit)
        self.btnShowLog.clicked.connect(self._parentUi.showLogRequested)
        self.btnDeploy.clicked.connect(self.deploy)
        self.chkDeployToMulti.clicked.connect(lambda: self.optionGroupDeploy.setChecked(self.chkDeployToMulti.isChecked()))
        self.btnHelp.clicked.connect(lambda: self.helpviewer.showHelp(oPB.HLP_DST_DEPLOY, False))

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

    def show_(self):
        self.logger.debug("Open deploy agent dialog")

        self.dialogOpened.emit()

        self.cmbPreExec.clear()
        self.cmbPreExec.addItems([""])
        self.cmbPreExec.addItems(ConfigHandler.cfg.predeploycmds)

        self.show()
        self.activateWindow()

    def closeEvent(self, event):
        self.logger.debug("Closing dialog")
        # Save the 10 last used pre deployment commands

        c = deque('', 10)

        for i in range(self.cmbPreExec.count()):
            if self.cmbPreExec.itemText(i) != "":
                if not self.cmbPreExec.itemText(i) in c:
                    c.append(self.cmbPreExec.itemText(i))

        if self.cmbPreExec.currentText() != "":
            if not self.cmbPreExec.currentText() in c:
                c.append(self.cmbPreExec.currentText())

        ConfigHandler.cfg.predeploycmds = list(c)

        event.accept()
        self.finished.emit(0) # we have to emit this manually, because of subclassing closeEvent

    def create_optionsgroups(self):
        """
        Create group of dependend dialog widgets

        See :class:`oPB.gui.utilities.SpecialOptionButtonGroup`
        """
        self.logger.debug("Create option button group")
        # build special button groups for False/True choice
        self.optionGroupDeploy = SpecialOptionButtonGroup(self.chkDeployToMulti, None,
                                                              [self.inpDestMulti],
                                                              [self.inpDestSingle])

    def deploy(self):
        """
        Get values from dialog widgets and pass them to backend method start_deploy.

        See: :meth:`oPB.controller.components.deployagent.DeployAgentComponent.start_deploy`
        :return:
        """
        self.logger.debug("Deploy client agent")

        check_ip = re.compile(oPB.OPB_VALID_IP_ADDRESS_REGEX)
        check_dns = re.compile(oPB.OPB_VALID_HOSTNAME_REGEX)
        destination = []

        if self.chkDeployToMulti.isChecked():
            text = self.inpDestMulti.toPlainText().splitlines()
            for line in text:
                if line.strip() != "":
                    if check_ip.search(line.strip()) or check_dns.search(line.strip()):
                        destination.append(line.strip())
                    else:
                        self.logger.warning("Obviously, no network name or ip: " + line.strip())
        else:
            if self.inpDestSingle.text().strip() != "":
                destination.append(self.inpDestSingle.text().strip())

        if not destination:
            self.logger.info('No destination.')
            return

        self.splash.show_()

        self.logger.info('Possible destinations: ' + str(destination))

        if self.rdDoNothing.isChecked():
            post = ""
        elif self.rdStartOpsiclientd.isChecked():
            post = "startclient"
        elif self.rdReboot.isChecked():
            post = "reboot"
        elif self.rdShutdown.isChecked():
            post = "shutdown"

        # now build option dict
        # Win10 - removed escaping of baslashes, because smbclient 4.3.11 (opsiVM) handles them correctly:
        # "user": self.inpUser.text().strip().replace("\\", "\\\\"),
        options = {
            "pre_action": self.cmbPreExec.currentText().strip(),
            "user": self.inpUser.text().strip(),
            "pass": self.inpPass.text().strip(),
            "usefqdn": self.chkUseFQDN.isChecked(),
            "ignoreping": self.chkIgnorePing.isChecked(),
            "skipexisting": self.chkSkipExisting.isChecked(),
            "post_action": post,
            "proceed": self.chkProceed.isChecked()
        }

        self._parent.start_deploy(destination, options)

        self.splash.close()

    def retranslateMsg(self):
        self.logger.debug("Retranslating further messages...")
        self.splash.msg = translate("MainWindow", "Please wait...")