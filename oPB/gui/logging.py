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

import logging
from PyQt5.QtCore import *
import oPB
from oPB.ui.ui import LogDialogBase, LogDialogUI
from oPB.core.tools import LogMixin
from oPB.gui.utilities import EventMixin


class LogDialog(LogDialogBase, LogDialogUI, LogMixin, EventMixin):
    """Main LogDialog class"""

    def __init__(self, parent, main, level):
        """
        Constructor of LogDialog

        :param parent: dialog parent
        :param main: main logger instance
        :param level: initial log level
        """
        self._parent = parent

        LogDialogBase.__init__(self, self._parent)
        self.setupUi(self)

        print("\tgui/LogDialog parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None

        self.main = main

        if level == "DEBUG":
            self.cmbLogLevel.setCurrentIndex(6)
        elif level == "INFO":
            self.cmbLogLevel.setCurrentIndex(5)
        elif level == "SSHINFO":
            self.cmbLogLevel.setCurrentIndex(4)
        elif level == "WARNING":
            self.cmbLogLevel.setCurrentIndex(3)
        elif level == "SSH":
            self.cmbLogLevel.setCurrentIndex(2)
        elif level == "ERROR":
            self.cmbLogLevel.setCurrentIndex(1)
        elif level == "CRITICAL":
            self.cmbLogLevel.setCurrentIndex(0)
        else:
            self.cmbLogLevel.setCurrentIndex(3)

        self.connect_signals()

    def connect_signals(self):
        self.cmbLogLevel.currentIndexChanged.connect(self.changeLogLevel)
        self.chkFormat.stateChanged.connect(self.changeFormat)

    def changeLogLevel(self,  index):
        """
        Set changelog level

        Possible values are:

            * logging.DEBUG
            * logging.INFO
            * oPB.core.logging.SSHINFO
            * logging.WARNING
            * oPB.core.logging.SSH
            * logging.ERROR
            * logging.CRITICAL

        :param index: log level
        """
        self.cmbLogLevel.setCurrentIndex(index)
        if index == 6:
            self.logger.debug("Set dialog log level to: DEBUG")
            self.setLevel(logging.DEBUG)
        elif index == 5:
            self.logger.debug("Set dialog log level to: INFO")
            self.setLevel(logging.INFO)
        elif index == 4:
            self.logger.debug("Set dialog log level to: SSHINFO")
            self.setLevel(oPB.core.logging.SSHINFO)
        elif index == 3:
            self.logger.debug("Set dialog log level to: WARNING")
            self.setLevel(logging.WARNING)
        elif index == 2:
            self.logger.debug("Set dialog log level to: SSH")
            self.setLevel(oPB.core.logging.SSH)
        elif index == 1:
            self.logger.debug("Set dialog log level to: ERROR")
            self.setLevel(logging.ERROR)
        elif index == 0:
            self.logger.debug("Set dialog log level to: CRITICAL")
            self.setLevel(logging.CRITICAL)
        else:
            self.logger.debug("Set dialog log level to: ERROR")
            self.setLevel(logging.ERROR)

    def setLevel(self, level):
        self.main.dialogHandler.setLevel(level)
        self.main.stdout.setLevel(level)
        try:
            self.main.fileHandler.setLevel(level)
        except:
            pass

    def changeFormat(self,  state):
        """
        Set log format

        Possible values are:

            * oPB.LOG_LONG
            * oPB.LOG_SHORT

        :param state: state constant
        """
        if state == Qt.Checked:
            format = logging.Formatter(oPB.LOG_LONG, oPB.LOG_DATETIME)
            self.logger.debug("Set dialog log format to: LONG")
        else:
            format = logging.Formatter(oPB.LOG_SHORT, oPB.LOG_DATETIME)
            self.logger.debug("Set dialog log format to: SHORT")

        self.main.dialogHandler.setFormatter(format)
