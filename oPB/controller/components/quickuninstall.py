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
from oPB.gui.quickuninstall import UninstallDialog

translate = QtCore.QCoreApplication.translate

class QuickUninstallComponent(BaseController, QObject):
    def __init__(self, parent):
        super().__init__(self)

        self._parent = parent
        print("controller/QuickUninstallComponent parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None

        self.ui = None
        self.model_products = None

        self.generate_model()

        self.ui = UninstallDialog(self)

        self.connect_signals()

    def connect_signals(self):
        self.ui.dialogOpened.connect(self._parent.startup.hide_)
        self.ui.dialogClosed.connect(self._parent.startup.show_)

    def generate_model(self):
        # create model from data and assign, if not done before
        if self.model_products == None:
            self.logger.debug("Generate product table model")
            self.model_products = QtGui.QStandardItemModel(0, 3, self)
            self.model_products.setObjectName("model_products")

            self.retranslateMsg()



    def update_model_data(self, force = False):
        self.logger.debug("Update model data")

        # first time opened after program start?
        if BaseController.productlist_dict == None or force == True:
            self._parent.do_getproducts()

        if BaseController.productlist_dict:
            tmplist = []
            for elem in BaseController.productlist_dict:
                tmplist.append([elem["id"], elem["productVersion"] + "-" + elem["packageVersion"], elem["name"]])

            self._parent.update_table_model(self.model_products, sorted(tmplist))

    def uninstall_selection(self, prods = []):
        self.logger.debug("Uninstall selection")

        if prods:
            msg = "\n\n" + translate("quickuninstallController", "Chosen products:") + "\n\n" + ("\n").join([p for p in prods])
            reply = self._parent.msgbox(translate("quickuninstallController", "Do you really want to remove the selected product(s)? This can't be undone!") + msg, oPB.MsgEnum.MS_QUEST_YESNO)
            if reply is True:
                self.logger.debug("Selected product(s): " + str(prods))
                self._parent.do_quickuninstall(packs = prods, depot = self._parent.query_depot(parent = self.ui))
        else:
            self.logger.debug("Nothing selected.")

    def retranslateMsg(self):
        self.logger.debug("Retranslating further messages...")
        """Retranslate model headers, will be called via changeEvent of self.ui """
        self.model_products.setHorizontalHeaderLabels([translate("quickuninstallController", "product id"),
                                        translate("quickuninstallController", "version"),
                                        translate("quickuninstallController", "description")]
                                        )
