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
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QObject
import oPB
from oPB.core.confighandler import ConfigHandler
from oPB.controller.base import BaseController
from oPB.gui.bundle import BundleDialog
from oPB.core.tools import Helper

translate = QtCore.QCoreApplication.translate

class BundleComponent(BaseController, QObject):

    def __init__(self, parent):
        super().__init__(self)

        self._parent = parent
        print("controller/BundleComponent parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None

        self.ui = None
        self.model_products = None

        self.generate_model()

        self.ui = BundleDialog(self)

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
            self.model_products.setHorizontalHeaderLabels([translate("bundleController", "product id"),
                                            translate("bundleController", "version"),
                                            translate("bundleController", "description")]
                                            )


    def update_model_data(self):
        self.logger.debug("Update model data")

        # first time opened after program start?
        if BaseController.productlist_dict == None:
            self._parent.do_getproducts()

        if BaseController.productlist_dict:
            tmplist = []
            for elem in BaseController.productlist_dict:
                tmplist.append([elem["id"], elem["productVersion"] + "-" + elem["packageVersion"], elem["name"]])

            self._parent.update_table_model(self.model_products, sorted(tmplist))


    def create_bundle(self, prods = []):
        self.logger.debug("Create bundle from selection")

        if prods:
            msg = "\n\n" + translate("bundleController", "Chosen products:") + "\n\n" + ("\n").join([p for p in prods])
            reply = self._parent.msgbox(translate("bundleController", "Create product bundle now?") + msg, oPB.MsgEnum.MS_QUEST_YESNO)
            if reply is True:
                self.logger.debug("Selected product(s): " + str(prods))

                comment = ""
                while comment == "" or accept == False:
                    (comment, accept) = self._parent.msgbox(translate("bundleController","Please enter package name (allowed characters: a-z, A-Z, 0-9, ._-):"),
                                                    oPB.MsgEnum.MS_QUEST_PHRASE, parent = self.ui, preload = "meta-")
                    if ConfigHandler.cfg.age == "True":
                        test = re.match(oPB.OPB_PRODUCT_ID_REGEX_NEW, comment)
                    else:
                        test = re.match(oPB.OPB_PRODUCT_ID_REGEX_OLD, comment)
                    if not test:
                        comment = ""

                if accept:
                    directory = Helper.concat_path_and_file(ConfigHandler.cfg.dev_dir, comment)
                    self.logger.info("Chosen directory for new project: " + directory)
                    self._parent.project_create(directory)
                    for p in prods:
                        self._parent.add_setup_before_dependency(p)
                    self._parent.controlData.priority = -100
                    self._parent.save_backend()
                else:
                    self.logger.debug("Dialog aborted.")
        else:
            self.logger.debug("Nothing selected.")
