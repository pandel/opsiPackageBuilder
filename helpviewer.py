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

import sys
import oPB
from oPB.core import confighandler
from oPB.gui.helpviewer import Help
from oPB.gui.utilities import Translator
import oPB.ui.opsipackagebuilder_rc
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

translate = QtCore.QCoreApplication.translate

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # instantiate configuration class
    confighandler.ConfigHandler(oPB.CONFIG_INI)

    # installing translators
    translator = Translator(app, "opsipackagebuilder")
    translator.install_translations(confighandler.ConfigHandler.cfg.language)

    # instantiate help viewer and translate it, if necessary
    helpviewer = Help(oPB.HLP_FILE, oPB.HLP_PREFIX, oPB.HLP_DST_INDEX, False)
    event = QtCore.QEvent(QtCore.QEvent.LanguageChange)
    helpviewer._help.ui.changeEvent(event)

    # run main loop
    app.exec_()

