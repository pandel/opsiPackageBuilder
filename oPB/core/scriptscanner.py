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
import linecache

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QIcon
from oPB.core.tools import LogMixin

translate = QtCore.QCoreApplication.translate


class ScriptNode(object):
    def __init__(self, value, children = []):
        self.value = value
        self.children = children

    def __str__(self, level=0):
        ret = "\t" * level + repr(self.value) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def __repr__(self):
        return '<script tree node representation>'

class ScriptTree(LogMixin):

    root = ScriptNode("(tree root)", [])
    model = None

    def __init__(self, projectfolder: str, scripts: list):
        self.sub_regex = re.compile('^\s*([Ss][uU][bB]\s+)\"?([a-zA-Z0-9_%\$\.\\\-]*)\"?\s*$')  # two groups, 1 = "Sub ", 2 = scriptname or variable
        self.include_append_regex = re.compile('^\s*([iI][nN][cC][lL][uU][dD][eE]_[aA][pP][pP][eE][nN][dD]\s+)\"?([a-zA-Z0-9_%\$\.\\\-]*)\"?\s*$')
        self.include_insert_regex = re.compile('^\s*([iI][nN][cC][lL][uU][dD][eE]_[iI][nN][sS][eE][rR][tT]\s+)\"?([a-zA-Z0-9_%\$\.\\\-]*)\"?\s*$')

        ScriptTree.model = QStandardItemModel()

        self.projectfolder = projectfolder
        self.scripts = scripts
        self.scriptheader = ["Setup", "Uninstall", "Update", "Always", "Once", "Custom", "UserLogin"]

        self.get_script_structure()

    def get_script_structure(self):
        """
        Scan script files for sub/include_insert/include_append and build tree structure

        :return: tree representation of scripts
        """
        self.logger.debug("Scan script structure recursively")
        # first, find all product properties in every script and return a set
        for i in range(len(self.scripts)):
            scriptname = self.scripts[i]
            if scriptname != "":
                item = QStandardItem(QIcon(':/images/smallIcons_1712.ico'), self.scriptheader[i] + ": " + scriptname)
                item.setEditable(False)
                item2 = QStandardItem(scriptname)
                item2.setEditable(False)
                ScriptTree.model.appendRow([item, item2])
                ScriptTree.root.children.append(ScriptNode(scriptname + "(" + self.scriptheader[i] + ")", []))
                self._scan_script(scriptname, ScriptTree.root.children[len(ScriptTree.root.children) - 1], 0, item)

        ScriptTree.model.setHeaderData(0, QtCore.Qt.Horizontal, translate('ScriptTree', 'Script structure'))


    def _scan_script(self, script, root, level, modelroot):
        """
        Scan script files recursively for included script files

        :param script: script to search through
        :param root: root node
        :param level: level of recursion
        :return:
        """
        currentline = 1
        scriptname = self.projectfolder.replace('\\', '/') + "/CLIENT_DATA/" + script

        self.logger.debug("\t\t" * level + "Scanning script, current recursion level: " + str(level) + "(" + scriptname + ")")
        self.logger.debug("\t\t" * level + "Current script: " + scriptname)

        line = linecache.getline(scriptname, currentline)

        while line != '':
            m1 = self.sub_regex.search(line)
            m2 = self.include_append_regex.search(line)
            m3 = self.include_insert_regex.search(line)

            if m1:
                include = self._clear_script_name(m1.group(2).replace('\\', '/'))
                root.children.append(ScriptNode("Sub: " + include, []))
                item = QStandardItem(QIcon(':/images/smallIcons_1127.ico'), include + " (sub)")
                item.setEditable(False)
                item2 = QStandardItem(include)
                item2.setEditable(False)
                modelroot.appendRow([item, item2])

                self.logger.debug("\t\t" * level + "Found Sub: " + include)

            elif m2:
                include = self._clear_script_name(m2.group(2).replace('\\', '/'))
                root.children.append(ScriptNode("Include_append: " + include, []))
                item = QStandardItem(QIcon(':/images/smallIcons_1453.ico'), include + " (include_append)")
                item2 = QStandardItem(include)
                item2.setEditable(False)
                modelroot.appendRow([item, item2])

                self.logger.debug("\t\t" * level + "Found include_append: " + include)

            elif m3:
                include = self._clear_script_name(m3.group(2).replace('\\', '/'))
                root.children.append(ScriptNode("Include_insert: " + include, []))
                item = QStandardItem(QIcon(':/images/smallIcons_1453.ico'), include + " (include_insert)")
                item2 = QStandardItem(include)
                item2.setEditable(False)
                modelroot.appendRow([item, item2])

                self.logger.debug("\t\t" * level + "Found include_insert: " + include)

            if m1 or m2 or m3:
                if "(" not in include: self._scan_script(include, root.children[len(root.children) - 1], level + 1, item)

            currentline += 1
            line = linecache.getline(scriptname, currentline)

    def _clear_script_name(self, raw):
        """
        Clear raw line string from any unwanted characters and
        annotate externals
        :param raw: unmodified script line
        :return:
        """

        # remove all occurrences of "%ScriptPath%\"
        st = re.sub("%scriptpath%/", "", raw, flags=re.I)

        # return (External) annotation, if necessary
        if ("%opsiscripthelperpath%/lib" in st.lower()) or\
                ("%winstdir%/lib" in st.lower()) or\
                ("%scriptdrive%/" in st.lower()) or\
                ("%/" in st.lower()):
            st = "(External) " + st
        return st
