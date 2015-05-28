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

from PyQt5 import QtGui, QtCore

class OpsiProductTableModel(QtGui.QStandardItemModel):
    """
    Subclass of QtGui.QStandardItemModel

    Used to color QTableView lines with items with special field content
    """
    def __init__(self, rows, columns, parent):
        super(QtGui.QStandardItemModel, self).__init__(rows, columns, parent)
        self._rows = rows
        self._columns = columns
        self._parent = parent
        self._errorcolor = QtGui.QBrush(QtGui.QColor("#000000"))  # default to black
        self._errormarker = []
        self._errorcolumn = None

    def set_error_color(self, hexcolor):
        """
        Set special marker color for row.

        :param hexcolor: Color in hex, i. e. #ce34da
        """
        self._errorcolor = QtGui.QBrush(QtGui.QColor(hexcolor))

    def append_error_marker(self, marker):
        """
        Append ``marker`` to the list of strings, which cause a row
        to be set to special marker color, see set_error_color().

        :param marker: string
        """
        if not marker in self._errormarker:
            self._errormarker.append(marker)

    def set_error_column(self, col):
        """
        Set column to look for marker strings.

        If not set, every column is searched for the marker strings.

        :param col: column number, 0-based
        """
        self._errorcolumn = col

    def appendRow(self, rowlist):
        """
        Search for the marker strings in the error_column, if set, or in the whole row,
        then, if found, colorize every item with error_color, and finally,
        append list-of-items to the model

        OpsiProductTableModel.appendRow(list-of-QStandardItems)

        :param rowlist: list-of-QStandardItems
        """
        # if we find self._errormarker in item(self._errorcolumn) of the row
        # set foreground color of complete row to self._errorcolor
        # hint: if self._errorcolumn is None, then every item is searched through
        try:
            for m in self._errormarker:
                if self._errorcolumn is not None:
                    if str(m).upper() in str(rowlist[self._errorcolumn].data(QtCore.Qt.DisplayRole)).upper():
                        for elem in rowlist:
                            elem.setData(self._errorcolor, QtCore.Qt.ForegroundRole)
                else:
                    for item in rowlist:
                        if str(m).upper() in str(item.data(QtCore.Qt.DisplayRole)).upper():
                            for elem in rowlist:
                                elem.setData(self._errorcolor, QtCore.Qt.ForegroundRole)

        except:
            pass
        QtGui.QStandardItemModel.appendRow(self, rowlist)