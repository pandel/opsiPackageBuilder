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

import os
import subprocess
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import QKeyEvent
import oPB
from oPB.core.confighandler import ConfigHandler
from oPB.core.tools import Helper, LogMixin
from oPB.gui.utilities import EventMixin
from oPB.ui.ui import ScriptTreeDialogBase, ScriptTreeDialogUI


translate = QtCore.QCoreApplication.translate


class ScriptTreeDialog(ScriptTreeDialogBase, ScriptTreeDialogUI, LogMixin, EventMixin):

    def __init__(self, parent):
        """
        Constructor for settings dialog

        :param parent: parent controller instance
        :return:
        """
        self._parent = parent
        self._parentUi = parent.ui

        ScriptTreeDialogBase.__init__(self, self._parentUi, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)
        self.setWindowIcon(self._parentUi.windowIcon())

        print("\tgui/ScriptTreeDialog parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None
        print("\tgui/ScriptTreeDialog parentUi: ", self._parentUi, " -> self: ", self) if oPB.PRINTHIER else None

        self.model = None
        self.connect_signals()

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
        self.treeView.setModel(self.model)
        self.treeView.setColumnHidden(1, True)
        self.treeView.expandAll()

    def connect_signals(self):
        self.treeView.doubleClicked.connect(self.open_scripteditor)

    @pyqtSlot()
    def open_scripteditor(self):
        """Open script editor after double click on tree view item"""

        self.logger.debug("Start scripteditor")

        idx = self.treeView.currentIndex()
        if idx.isValid():
            sibling = idx.sibling(idx.row(), idx.column() + 1)
            item = self.model.itemFromIndex(sibling)
            script = item.text()

        if "(External)" in script:
            self._parent.msgbox(translate("MainWindow", "Sorry! You cannot edit a script outside the project folder!"), oPB.MsgEnum.MS_ERR, self)
            return

        if ConfigHandler.cfg.editor_intern == "True":
            self._parent.msgbox(translate("MainWindow", "Internal editor not available at the moment. Use external editor instead!"), oPB.MsgEnum.MS_ALWAYS, self)
            self._parentUi.actionSettings.trigger()
            return

        if os.path.exists(ConfigHandler.cfg.scripteditor):
            path = Helper.concat_path_native(self._parentUi.lblPacketFolder.text(), "CLIENT_DATA")

            path = Helper.concat_path_native(path, script)

            self.logger.debug("Opening script: " + path)
            cmd = [ConfigHandler.cfg.scripteditor]
            if (ConfigHandler.cfg.editor_options).strip() != "":
                for part in (ConfigHandler.cfg.editor_options).split():
                    cmd.append(part)
                if ConfigHandler.cfg.editor_attachdirect == "True":
                    cmd[-1] = cmd[-1] + path
                else:
                    cmd.append(path)
            else:
                cmd.append(path)

            self.logger.debug("Executing subprocess: " + str(cmd))
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            outs, errs = proc.communicate()
            self.logger.info(outs)
            self.logger.error(errs)
            if proc.returncode != 0:
                self._parent.msgbox(translate("MainWindow", "Editor startup did not cleanup correctly.\n\nThe following message(s) returned:") +
                                    "\n\nStandard Out:\n" + outs +
                                    "\n\nStandard Err:\n" + errs,
                                    oPB.MsgEnum.MS_WARN, self)

        else:
            self._parent.msgbox(translate("MainWindow", "Editor not found:" + " " + ConfigHandler.cfg.scripteditor), oPB.MsgEnum.MS_ERR, self)
