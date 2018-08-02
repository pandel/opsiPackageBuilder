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
from oPB.gui.lockedproducts import LockedProductsDialog

translate = QtCore.QCoreApplication.translate

class LockedProductsComponent(BaseController, QObject):
    def __init__(self, parent):
        super().__init__(self)

        self._parent = parent
        print("controller/LockedProductsComponent parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None

        self.ui = None
        self.model_products = None
        self.selected_depot = None

        self.generate_model()

        self.ui = LockedProductsDialog(self)

        self.connect_signals()

    def connect_signals(self):
        self.ui.dialogOpened.connect(self._parent.startup.hide_)
        self.ui.dialogClosed.connect(self._parent.startup.show_)
        self.ui.dialogClosed.connect(self.reset)

    def generate_model(self):
        # create model from data and assign, if not done before
        if self.model_products == None:
            self.logger.debug("Generate product table model")
            self.model_products = QtGui.QStandardItemModel(0, 2, self)
            self.model_products.setObjectName("model_products")

            self.retranslateMsg()

    def reset(self):
        self.selected_depot = None
        BaseController.lockedproductlist_dict = None

    def update_model_data(self, force = False):
        self.logger.debug("Update model data")
        tmplist = []

        # if force, empty depot selection (user clicked on refresh)
        if force == True or self.selected_depot == None:
            self.selected_depot = None
            BaseController.lockedproductlist_dict = None
            self._parent.update_table_model(self.model_products, sorted(tmplist))
            self.selected_depot = self._parent.query_depot(with_all = False, parent = self.ui, with_repo = False)

        self._parent.do_getlockedproducts(depot = self.selected_depot)

        if BaseController.lockedproductlist_dict:
            for elem in BaseController.lockedproductlist_dict:
                tmplist.append([elem["productId"], elem["productVersion"] + "-" + elem["packageVersion"]])

        self._parent.update_table_model(self.model_products, sorted(tmplist))

    def unlock_selection(self, prods = []):
        self.logger.debug("Unlock selection")

        if prods:
            msg = "\n\n" + translate("LockedProductsController", "Selected depot:") + " " + self.selected_depot
            msg = msg + "\n\n" + translate("LockedProductsController", "Chosen products:") + "\n\n" + ("\n").join([p for p in prods])
            reply = self._parent.msgbox(translate("LockedProductsController", "Do you really want to unlock selected product(s) now?") + msg, oPB.MsgEnum.MS_QUEST_YESNO)
            if reply is True:
                self.logger.debug("Selected depot: " + self.selected_depot)
                self.logger.debug("Selected product(s): " + str(prods))
                self._parent.do_unlockproducts(packs = prods, depot = self.selected_depot)
                self.update_model_data()
        else:
            self.logger.debug("Nothing selected.")

    def retranslateMsg(self):
        self.logger.debug("Retranslating further messages...")
        """Retranslate model headers, will be called via changeEvent of self.ui """
        self.model_products.setHorizontalHeaderLabels([translate("LockedProductsController", "product id"),
                                        translate("LockedProductsController", "version")]
                                        )
