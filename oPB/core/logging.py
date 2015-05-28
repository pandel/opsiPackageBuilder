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
from logging import getLoggerClass, addLevelName, setLoggerClass, NOTSET
from PyQt5.QtCore import *
from PyQt5.QtGui import *

"""
Level 	Numeric value
CRITICAL 	50
ERROR 	40
WARNING 	30
INFO 	20
DEBUG 	10
NOTSET 	0
"""

SSH = 35
SSHINFO = 25

class LogStreamHandler(logging.Handler):
    def __init__(self,  parent,  main):
        logging.Handler.__init__(self)
        self.parent = parent
        self.main = main

        self.textWidget = parent
        self.formatter = logging.Formatter("%(message)s")

        self.colorize = False
        self.colors = {
            "DEBUG": Qt.darkGreen,
            "INFO": Qt.black,
            "WARNING": Qt.darkYellow,
            "ERROR": Qt.darkRed,
            "CRITICAL": Qt.red
        }

        self.standardtc = self.textWidget.textColor()

    def setFormatter(self,  format):
        self.formatter = format

    def createLock(self):
        self.mutex = QMutex()

    def acquire(self):
        self.mutex.lock()

    def release(self):
        self.mutex.unlock()

    def emit(self, record):

        if self.colorize:
            for level in self.colors:
                if record.levelname == level:
                    self.textWidget.setTextColor(self.colors[level])

        self.textWidget.insertPlainText(self.formatter.format(record) + "\n")
        self.textWidget.moveCursor(QTextCursor.End)
        self.textWidget.moveCursor(QTextCursor.StartOfLine)
        self.textWidget.ensureCursorVisible()

class LogOutput(object):
    def __init__(self, parent, out=None, color=None):
        self.textWidget = parent
        self.out = out
        self.color = color

    def write(self, m):
        self.textWidget.moveCursor(QTextCursor.End)

        if self.color:
            tc = self.textWidget.textColor()
            self.textWidget.setTextColor(self.color)

        try:
            if type(m) == bytes:
                m = m.decode('utf-8')
            self.textWidget.insertPlainText( m )
        except UnicodeDecodeError:
            pass

        if self.color:
            self.textWidget.setTextColor(tc)

        if self.out:
            try:
                if type(m) == bytes:
                    m = m.decode('utf-8')
                self.out.write(m)
            except UnicodeDecodeError:
                pass

    def flush(self):
        pass

class SSHLogger(getLoggerClass()):
    def __init__(self, name, level=NOTSET):
        super().__init__(name, level)

        addLevelName(SSH, "SSH")
        addLevelName(SSHINFO, "SSHINFO")

    def ssh(self, msg, *args, **kwargs):
        if self.isEnabledFor(SSH):
            self._log(SSH, msg, args, **kwargs)

    def sshinfo(self, msg, *args, **kwargs):
        if self.isEnabledFor(SSHINFO):
            self._log(SSHINFO, msg, args, **kwargs)
