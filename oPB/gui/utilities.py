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

import os.path
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtWidgets import QWidget
import oPB
from oPB.core.tools import LogMixin, Helper

translate = QtCore.QCoreApplication.translate


class SpecialOptionButtonGroup(QWidget, LogMixin):
    """This object takes care of radio buttons and checkboxes, that have a counterpart (like yes/no or true/false)
    and additionally activate/deactivate other widgets
    """

    def __init__(self, left_button:QWidget, right_button:QWidget = None, enable_left:list = [], enable_right:list = []):
        """
        Constructor of SpecialOptionButtonGroup

        Imagine, you have two exclusive radio buttons. This object treats both widgets as one, returning "True" if the :left: is
        active and "False", if the :right: one is active.
        Additionally, if there are widgets, whose active/inactive states depend on if :left_button: is checked or not,
        this routine takes care of it, too.

        Exp. (radio buttons):

            obj = SpecialOptionButtonGroup(win.rdButtonLeft, win.rdButtonRight, [win.fieldA, win.fieldB], [win.fieldC, win.fieldD]

        a) if win.rdButtonLeft is checked: obj.getChecked == True
        aa) win.FieldA and win.FieldB will be activated, win.FieldC and win.FieldD will be deactivated
        b) if win.rdButtonRight is checked: obj.getChecked == False
        ab) win.FieldA and win.FieldB will be deactivated, win.FieldC and win.FieldD will be activated

        Exp. (checkbox):

            obj = SpecialOptionButtonGroup(win.chkBox, None, [win.fieldA, win.fieldB], [win.fieldC, win.fieldD]

        a) if win.chkBox is checked: obj.getChecked == True
        aa) win.FieldA and win.FieldB will be activated, win.FieldC and win.FieldD will be deactivated
        b) if win.chkBox is not checked: obj.getChecked == False
        bb) win.FieldA and win.FieldB will be deactivated, win.FieldC and win.FieldD will be activated

        Notice:
        This is really helpful, if you have one boolean variable, with which you want to control a whole set of widgets in your ui,
        and at the same time, map this variable via QDataWidgetMapper to a data model.

        :param left_button: in a two-button relationship, left("Answer A") button
        :param right_button: in a two-button relationship, right("Answer B") button (optional)
        :param enable_left: widgets (obj), that should be active for "Answer A" (optional)
        :param enable_right: widgets (obj), that should be active for "Answer B" (optional)
        :return:
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

    def setChecked(self, value):
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
    """
    Validator to check for existing files

    (Constructor has to be called with parent and field,
    because validate() needs to access some values from
    different window elements.)
    """

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
        if p_str == "":
            return ScriptFileValidator.Intermediate, p_str, p_int
        if os.path.exists(Helper.concat_path_and_file(self._parent.lblPacketFolder.text().replace('\\','/') + "/CLIENT_DATA/", p_str)):
            return ScriptFileValidator.Acceptable, p_str, p_int
        else:
            return ScriptFileValidator.Invalid, p_str, p_int