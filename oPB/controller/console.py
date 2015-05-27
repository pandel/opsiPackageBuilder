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

from PyQt5 import QtCore
from PyQt5.QtWidgets import qApp
from oPB.core.datadefinition import *
from oPB.core.confighandler import ConfigHandler
from oPB.core.tools import Helper
from oPB.controller.base import BaseController

translate = QtCore.QCoreApplication.translate

class ConsoleController(BaseController, QObject):

    def __init__(self, cmd_line):
        super().__init__(cmd_line)
        print("controller/ConsoleController self: ", self) if oPB.PRINTHIER else None

        self.logger.debug("Initialize console")

        # if --path defined, try to load project
        if not self.args.path == "":
            self.run_command_line()
        else:
            self.logger.info("Nothing to do")

        self.finished()

    def finished(self):
        self.logger.info("Processing finished")
        ConfigHandler.cfg.save()

