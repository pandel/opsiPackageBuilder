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
import os.path
import platform
import PyQt5
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtProperty, QUrl, QObject, QSortFilterProxyModel, QDir
from PyQt5.QtWidgets import QWidget, QDialog, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QPushButton
from PyQt5.QtPrintSupport import QPrintPreviewDialog, QPrinter
from PyQt5.QtWebKitWidgets import QWebView
import oPB
from oPB.core.tools import LogMixin, Helper
from oPB.gui.depotmanager import translate

translate = QtCore.QCoreApplication.translate


class SpecialOptionButtonGroup(QWidget, LogMixin):
    """
    This object takes care of radio buttons and checkboxes, that have a true one-to-one counterpart (like yes/no or true/false)
    and, additionally, activate/deactivate other widgets dependend of their own state.

    Imagine, you have two exclusive radio buttons, a ``left_button`` and a ``right_button`` one.
    This object treats both widgets as one, returning *True* if the *``left_button`` is active and *False*, if the ``right_button`` one is active.
    Additionally, if there are widgets, whose active/inactive states depend on if ``left_button`` is checked or not, this routine takes care of it, too.

    :Example:

        Radio buttons::

            obj = SpecialOptionButtonGroup(win.rdButtonLeft, win.rdButtonRight, [win.fieldA, win.fieldB], [win.fieldC, win.fieldD]

        * if win.rdButtonLeft is checked: obj.getChecked == True
          -> win.FieldA and win.FieldB will be activated, win.FieldC and win.FieldD will be deactivated
        * if win.rdButtonRight is checked: obj.getChecked == False
          -> win.FieldA and win.FieldB will be deactivated, win.FieldC and win.FieldD will be activated


    :Example:

        Checkbox::

            obj = SpecialOptionButtonGroup(win.chkBox, None, [win.fieldA, win.fieldB], [win.fieldC, win.fieldD]

        * if win.chkBox is checked: obj.getChecked == True
          -> win.FieldA and win.FieldB will be activated, win.FieldC and win.FieldD will be deactivated
        * if win.chkBox is not checked: obj.getChecked == False
          -> win.FieldA and win.FieldB will be deactivated, win.FieldC and win.FieldD will be activated

    **Notice:**
    This is really helpful, if you have one boolean variable, with which you want to control a whole set of widgets in your ui,
    and at the same time, map this variable via QDataWidgetMapper to a data model.
    """

    def __init__(self, left_button:QWidget, right_button:QWidget = None, enable_left:list = [], enable_right:list = []):
        """
        Constructor of special option button group:

        :param left_button: in a two-button relationship, left("Answer A") button
        :param right_button: in a two-button relationship, right("Answer B") button (optional)
        :param enable_left: widgets (obj), that should be active for "Answer A" (optional)
        :param enable_right: widgets (obj), that should be active for "Answer B" (optional)
        """
        super().__init__()

        self._checked = True
        self._left_button = left_button
        self._right_button = right_button
        self._enable_left = enable_left
        self._enable_right = enable_right

    def getChecked(self):
        """
        Return main value of this option group

        :return: True/False
        """
        return self._checked

    def setChecked(self, value: bool):
        """
        Sets the overall option group value and activates/deactivtes the dependend widgets.

        :param value: True(=left), False(=right)
        """

        self._checked = value
        if value == True:
            self._left_button.setChecked(True)
            if self._right_button is not None: self._right_button.setChecked(False)
            for widget in self._enable_left:
                widget.setEnabled(True)
            for widget in self._enable_right:
                widget.setEnabled(False)
        else:
            self._left_button.setChecked(False)
            if self._right_button is not None: self._right_button.setChecked(True)
            for widget in self._enable_left:
                widget.setEnabled(False)
            for widget in self._enable_right:
                widget.setEnabled(True)

    checked = pyqtProperty(bool, fget=getChecked, fset=setChecked)


class ScriptFileValidator(QtGui.QValidator):
    """Validator to check for existing files"""

    def __init__(self, parent, field):
        """
        Constructor of ScriptFileValidator

        :param parent: parent window
        :param field: field object to validate
        """
        self._parent = parent

        super().__init__(self._parent)
        print("\tgui/ScriptFileValidator parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None

        self._field = field

    def validate(self, p_str, p_int):
        """
        Validator method

        :param p_str: script full pathname to validate
        :param p_int: (not used)

        :return: tuple(QValidator.state, p_str, p_int)
        """
        if p_str == "":
            return ScriptFileValidator.Intermediate, p_str, p_int
        if os.path.exists(Helper.concat_path_and_file(self._parent.lblPacketFolder.text().replace('\\','/') + "/CLIENT_DATA/", p_str)):
            return ScriptFileValidator.Acceptable, p_str, p_int
        else:
            return ScriptFileValidator.Invalid, p_str, p_int


class HtmlView(QWebView):
    """Subclass QWebView and connect to a QPrintPreviewDialog object"""

    def __init__(self, parent=None, url = ""):
        """
        Constructor of HtmlView

        :param parent: parent of the view
        :param url: url to load, if set, a loadFInished signal is emitted
        """
        super().__init__(parent)
        self.setUrl(QUrl(url))
        self.preview = QPrintPreviewDialog()

        # just for the moment / buf in Qt leads to incorrect printing of tables fomr QWebKit
        self.preview.printer().setOutputFormat(QPrinter.PdfFormat)
        self.preview.printer().setPaperSize(QPrinter.A4)

        self.preview.paintRequested.connect(self.print)
        if url != "":
            self.loadFinished.connect(self.execpreview)

    def execpreview(self, arg):
        """Open QPrintPreviewDialog dialog window"""
        self.preview.exec_()


class HtmlDialog(QDialog):
    """Generate a more complex HTML Viewer dialog window, with Prin/Close Buttons"""

    def __init__(self, parent = None):
        """
        Constructor of HtmlDialog

        :param parent: dialog parent
        :return:
        """
        super().__init__(parent, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCloseButtonHint)

        self.horzLayout = QHBoxLayout()
        self.vertLayout = QVBoxLayout()
        self.spacer = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)

        # print button
        self.btnPrint = QPushButton(self)
        self.btnPrint.setText(translate("ReportDialog", "Print"))
        self.btnPrint.setMaximumWidth(100)
        self.btnClose = QPushButton(self)
        self.btnClose.setText(translate("ReportDialog", "Close"))
        self.btnClose.setMaximumWidth(100)

        # webview for help information
        self.wv = HtmlView(self)

        # build structure
        self.horzLayout.addWidget(self.btnPrint)
        self.horzLayout.addWidget(self.btnClose)
        self.horzLayout.addSpacerItem(self.spacer)
        self.vertLayout.insertLayout(0, self.horzLayout)
        self.vertLayout.addWidget(self.wv)

        self.setLayout(self.vertLayout)

        self.btnPrint.clicked.connect(self.wv.execpreview)
        self.btnClose.clicked.connect(self.close)

    def showHtml(self, html):
        """
        Show rendered value of ``html``

        :param html: raw html data
        """
        self.wv.setHtml(html)
        self.show()

class Translator(QObject, LogMixin):
    """
    Translator class, can only be instantiated once

    To conveniently set ui language on the fly, see :ref:`oPB.core.tools.EventMixin`

    .. code-block:: python

        class EventMixin(object):
        \"""
        Event mixin class

        For reacting on changeEvent, especially language change event
        \"""
            def __init__(self, *args, **kwargs):
                super(EventMixin, self).__init__(*args, **kwargs)

            def changeEvent(self, event):
                if event.type() == QtCore.QEvent.LanguageChange:
                    self.logger.debug("Retranslating ui...")
                    self.retranslateUi(self)

                    super(type(self), self).changeEvent(event)

    """

    cfg = None
    """Class variable holding current Translator instance"""

    def __init__(self, parent = None, applangprefix = ""):
        """
        Constructor of Translator class

        :param parent: parent, mostly qApp
        :param applangprefix: application language file prefix
        """

        if Translator.cfg is None:
            Translator.cfg = self

            Translator.cfg._parent = parent

            super().__init__(Translator.cfg._parent)

            Translator.cfg._qt_local_path = None
            Translator.cfg._app_locale_path = None
            Translator.cfg._syslocale = None
            Translator.cfg._current_lang = "en"
            Translator.cfg.applangprefix = applangprefix

            Translator.cfg._combobox = None
            Translator.cfg._dialog = None

            # different translators
            Translator.cfg.translator_qthelp = None
            Translator.cfg.translator_qtmm = None
            Translator.cfg.translator_qt = None
            Translator.cfg.translator_app = None

            pyqt_path = os.path.dirname(PyQt5.__file__)

            if platform.system() == "Windows":
                Translator.cfg._qt_locale_path = Helper.concat_path_and_file(pyqt_path, "translations")
            else:
                Translator.cfg._qt_locale_path = "/usr/share/qt5/translations/"

            Translator.cfg._app_locale_path = ":locale/"
            Translator.cfg._syslocale = QtCore.QLocale().system().name()[:2]

    @classmethod
    def install_translations(cls, config_lang):
        """
        Get current system language and load translation

        We need more than one translator: one for the individual appplication strings
        and some other for the standard qt message texts.

        :param config_lang: two-character language string, or "System"
        """

        # remove possible existing translators
        if cls.cfg.translator_qthelp is not None:
            cls.cfg._parent.removeTranslator(cls.cfg.translator_qthelp)
            cls.cfg.translator_qthelp = None
        if cls.cfg.translator_qtmm is not None:
            cls.cfg._parent.removeTranslator(cls.cfg.translator_qtmm)
            cls.cfg.translator_qtmm = None
        if cls.cfg.translator_qt is not None:
            cls.cfg._parent.removeTranslator(cls.cfg.translator_qt)
            cls.cfg.translator_qt = None
        if cls.cfg.translator_app is not None:
            cls.cfg._parent.removeTranslator(cls.cfg.translator_app)
            cls.cfg.translator_app = None

        # decide, if we load the system language or specified language from config
        if config_lang == "System":
            use_local = QtCore.QLocale().system()
            qm_qt = "qt_%s" % cls.cfg._syslocale
            qm_app = cls.cfg.applangprefix + '_%s' % cls.cfg._syslocale
            cls.cfg.logger.debug("Installing language: " + use_local.name()[:2])
        else:
            use_local = QtCore.QLocale(config_lang)
            qm_qt = 'qt_%s.qm' % config_lang
            qm_app = cls.cfg.applangprefix + '_%s.qm' % config_lang
            cls.cfg.logger.debug("Installing language: " + config_lang)
        cls.cfg.logger.debug("Load Qt standard translation: " + qm_qt + " from: " + cls.cfg._qt_locale_path)
        cls.cfg.logger.debug("Load application translation: " + qm_app + " from: " + cls.cfg._app_locale_path)

        # create translators

        # translator_qt.load(use_local, "qtquick1", "_", qt_locale_path, ".qm")
        # translator_qt.load(use_local, "qtmultimedia", "_", qt_locale_path, ".qm")
        # translator_qt.load(use_local, "qtxmlpatterns", "_", qt_locale_path, ".qm")

        # qt base
        cls.cfg.translator_qt = QtCore.QTranslator(cls.cfg._parent)
        if cls.cfg.translator_qt.load(use_local, "qtbase", "_", cls.cfg._qt_locale_path, ".qm"):
            cls.cfg.logger.debug("Qtbase translations successfully loaded.")

        # qt help
        cls.cfg.translator_qthelp = QtCore.QTranslator(cls.cfg._parent)
        if cls.cfg.translator_qthelp.load(use_local, "qt_help", "_", cls.cfg._qt_locale_path, ".qm"):
            cls.cfg.logger.debug("Qthelp translations successfully loaded.")

        # qt multimedia
        cls.cfg.translator_qtmm = QtCore.QTranslator(cls.cfg._parent)
        if cls.cfg.translator_qtmm.load(use_local, "qtmultimedia", "_", cls.cfg._qt_locale_path, ".qm"):
            cls.cfg.logger.debug("Qtmultimedia translations successfully loaded.")

        # application
        cls.cfg.translator_app = QtCore.QTranslator(cls.cfg._parent)
        if cls.cfg.translator_app.load(use_local, "opsipackagebuilder", "_", cls.cfg._app_locale_path, ".qm"):
            cls.cfg.logger.debug("Application translations successfully loaded.")

        # install translators to app
        if not cls.cfg.translator_qthelp.isEmpty():
            cls.cfg._parent.installTranslator(cls.cfg.translator_qthelp)
        if not cls.cfg.translator_qtmm.isEmpty():
            cls.cfg._parent.installTranslator(cls.cfg.translator_qtmm)
        if not cls.cfg.translator_qt.isEmpty():
            cls.cfg._parent.installTranslator(cls.cfg.translator_qt)
        if not cls.cfg.translator_app.isEmpty():
            cls.cfg._parent.installTranslator(cls.cfg.translator_app)

        # save current language
        cls.cfg._current_lang = use_local.name()[:2]

    @classmethod
    def setup_language_combobox(cls, dialog: PyQt5.QtWidgets, combobox: PyQt5.QtWidgets.QComboBox):
        """
        Setup language chooser ``combobox`` in ``dialog``
        Makes it very easy to setup a language changer with on-the-fly setup of ui language

        :param dialog: the parent dialog widget of ``combobox``
        :param combobox: the language combobox
        """
        cls.cfg.combobox = combobox
        cls.cfg.dialog = dialog

        cls.cfg.combobox.clear()
        cls.cfg.combobox.addItem("System" , "")

        for filePath in QDir(cls.cfg._app_locale_path).entryList():
            fileName  = os.path.basename(filePath)
            fileMatch = re.match(cls.cfg.applangprefix + "_([a-z]{2,}).qm", fileName)
            if fileMatch:
                cls.cfg.combobox.addItem(fileMatch.group(1), filePath)

        cls.cfg.dialog.sortFilterProxyModelLanguage = QSortFilterProxyModel(cls.cfg.combobox)
        cls.cfg.dialog.sortFilterProxyModelLanguage.setSourceModel(cls.cfg.combobox.model())
        cls.cfg.combobox.model().setParent(cls.cfg.dialog.sortFilterProxyModelLanguage)
        cls.cfg.combobox.setModel(cls.cfg.dialog.sortFilterProxyModelLanguage)

        cls.cfg.combobox.currentIndexChanged.connect(cls.cfg.on_comboBoxLanguage_currentIndexChanged)
        cls.cfg.combobox.model().sort(0)

    @classmethod
    @QtCore.pyqtSlot()
    def on_comboBoxLanguage_currentIndexChanged(cls):
        """
        Convinience method for setting ui language after changing selection
        in combobox.
        """
        cls.cfg.install_translations(cls.cfg.combobox.currentText())

    @classmethod
    def resetLanguage(cls):
        """Reset language to Translator.cfg._current_lang explicitly"""
        index = cls.cfg.combobox.findText(cls.cfg._current_lang)
        cls.cfg.combobox.setCurrentIndex(index)
