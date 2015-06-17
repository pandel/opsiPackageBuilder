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
from oPB.controller.base import BaseController
from oPB.gui.deployagent import DeployAgentDialog

translate = QtCore.QCoreApplication.translate

class DeployAgentComponent(BaseController, QObject):
    def __init__(self, parent):
        super().__init__(self)

        self._parent = parent
        print("controller/DeployAgentComponent parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None

        self.ui = None

        self.ui = DeployAgentDialog(self)

        self.connect_signals()

    def connect_signals(self):
        self.ui.dialogOpened.connect(self._parent.startup.hide_)
        self.ui.dialogClosed.connect(self._parent.startup.show_)

    def start_deploy(self, destination: list, options: dict):
        self._parent.do_deploy(clientlist = destination, options = options, dest = self._parent.query_depot(parent = self.ui, with_all=False))

