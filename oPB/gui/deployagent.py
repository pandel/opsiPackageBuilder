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
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.Qt import QKeyEvent
import oPB
import oPB.gui.helpviewer
from oPB.core.tools import LogMixin
from oPB.gui.utilities import SpecialOptionButtonGroup
from oPB.ui.ui import DeployAgentDialogUI, DeployAgentDialogBase
from oPB.gui.splash import Splash

translate = QtCore.QCoreApplication.translate


class DeployAgentDialog(DeployAgentDialogBase, DeployAgentDialogUI, LogMixin):

    dialogOpened = pyqtSignal()
    dialogClosed = pyqtSignal()

    def __init__(self, parent):
        """
        Constructor for settings dialog

        :param parent: parent controller instance
        :return:
        """
        self._parent = parent
        self._parentUi = parent._parent.ui

        DeployAgentDialogBase.__init__(self, self._parentUi, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)

        print("\tgui/DeployAgentDialog parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None
        print("\tgui/DeployAgentDialog parentUi: ", self._parentUi, " -> self: ", self) if oPB.PRINTHIER else None

        self.splash = Splash(self, translate("MainWindow", "Please wait..."))
        self.splash.close()  # only for linux

        self.create_optionsgroups()
        self.optionGroupDeploy.setChecked(self.chkDeployToMulti.isChecked())

        self.connect_signals()

    def connect_signals(self):
        self.finished.connect(self.dialogClosed.emit)
        self.btnShowLog.clicked.connect(self._parentUi.showLogRequested)
        self.btnDeploy.clicked.connect(self.deploy)
        self.chkDeployToMulti.clicked.connect(lambda: self.optionGroupDeploy.setChecked(self.chkDeployToMulti.isChecked()))
        self.btnHelp.clicked.connect(lambda: oPB.gui.helpviewer.Help(oPB.HLP_FILE, oPB.HLP_PREFIX, oPB.HLP_DST_DEPLOY))

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
        self.logger.debug("Open product bundle creation dialog")

        self.dialogOpened.emit()

        self.show()
        self.activateWindow()

    def create_optionsgroups(self):
        self.logger.debug("Create option button group")
        # build special button groups for False/True choice
        self.optionGroupDeploy = SpecialOptionButtonGroup(self.chkDeployToMulti, None,
                                                              [self.inpDestMulti],
                                                              [self.inpDestSingle])


    def deploy(self):
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
        options = {
            "pre_action": self.cmbPreExec.currentText().strip(),
            "user": self.inpUser.text().strip().replace("\\", "\\\\"),
            "pass": self.inpPass.text().strip(),
            "usefqdn": self.chkUseFQDN.isChecked(),
            "ignoreping": self.chkIgnorePing.isChecked(),
            "skipexisting": self.chkSkipExisting.isChecked(),
            "post_action": post,
            "proceed": self.chkProceed.isChecked()
        }

        self._parent.start_deploy(destination, options)

        self.splash.close()