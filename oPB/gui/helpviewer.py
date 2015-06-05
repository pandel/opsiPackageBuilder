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
from PyQt5 import QtCore
from PyQt5.QtHelp import QHelpEngine
from PyQt5.QtWidgets import QApplication, QSplitter, QDialog, QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import QIODevice, QTimer, QObject, QUrl
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

translate = QtCore.QCoreApplication.translate


class HelpDialog(QObject):
    def __init__(self, qthelp_file):
        QObject.__init__(self)

        # instantiate help engine
        helpEngine = QHelpEngine(qthelp_file)
        helpEngine.setupData()
        self._helpEngine = helpEngine

        # base dialog widget
        self.ui = QDialog()

        # webview for help information
        self._wv = QWebView()
        enam = HelpNetworkAccessManager(self, self._helpEngine)
        self._wv.page().setNetworkAccessManager(enam)

        # get help content overview widget
        self._helpContent = self._helpEngine.contentWidget()
        self._helpIndex = self._helpEngine.indexWidget()
        self._helpSearchQuery = self._helpEngine.searchEngine().queryWidget()
        self._helpSearchResult = self._helpEngine.searchEngine().resultWidget()
        self._se = self._helpEngine.searchEngine()
        self._se.reindexDocumentation()

        self._helpSearchQuery.search.connect(self.search)

        # create QSplitter
        self._splitterMain = QSplitter(QtCore.Qt.Vertical)
        self._splitterMain.setOpaqueResize(False)
        self._splitterSearch = QSplitter(QtCore.Qt.Horizontal)
        self._splitterSearch.setOpaqueResize(False)
        self._splitterUpper = QSplitter(QtCore.Qt.Horizontal)
        self._splitterUpper.setOpaqueResize(False)
        self._splitterLower = QSplitter(QtCore.Qt.Horizontal)
        self._splitterLower.setOpaqueResize(False)

        # create horzLayout
        self._horzLayoutSearch = QHBoxLayout()
        self._horzLayoutUpper = QHBoxLayout()
        self._horzLayoutLower = QHBoxLayout()
        # create vertLayout
        self._vertLayout = QVBoxLayout()

        # main widgets
        self._upperWidget = QWidget()
        self._lowerWidget = QWidget()
        self._btnReset = QPushButton()
        self._btnReset.setMaximumHeight(23)
        self._btnReset.setMaximumWidth(70)
        self._btnReset.setText(translate("HelpViewer", "Reset"))

        # build search structure
        self._splitterSearch.insertWidget(0, self._helpSearchQuery)
        self._splitterSearch.insertWidget(1, self._btnReset)

        # build upper inner structure
        self._splitterUpper.insertWidget(0, self._helpContent)
        self._splitterUpper.insertWidget(1, self._wv)
        self._horzLayoutUpper.addWidget(self._splitterUpper)
        self._upperWidget.setLayout(self._horzLayoutUpper)

        # build lower inner structure
        self._splitterLower.insertWidget(0, self._helpIndex)
        self._splitterLower.insertWidget(1, self._helpSearchResult)
        self._horzLayoutLower.addWidget(self._splitterLower)
        self._lowerWidget.setLayout(self._horzLayoutLower)

        # build outer structure
        self._splitterMain.insertWidget(0, self._splitterSearch)
        self._splitterMain.insertWidget(1, self._upperWidget)
        self._splitterMain.insertWidget(2, self._lowerWidget)

        self._helpSearchResult.hide()
        self._btnReset.hide()

        self._vertLayout.addWidget(self._splitterMain)
        self.ui.setLayout(self._vertLayout)

        # set splitter width
        w = self._splitterUpper.geometry().width()
        self._splitterUpper.setSizes([w*(1/4), w*(3/4)])
        w = self._splitterLower.geometry().width()
        self._splitterLower.setSizes([w*(1/5), w*(4/5)])
        h = self._splitterMain.geometry().height()
        self._splitterMain.setSizes([h*(1/9), h*(7/9), h*(1/9)])

        self._helpContent.linkActivated.connect(self._wv.setUrl)
        self._helpIndex.linkActivated.connect(self._wv.setUrl)
        self._helpSearchResult.requestShowLink.connect(self._wv.setUrl)
        self._se.searchingFinished.connect(self.showResults)
        self._btnReset.clicked.connect(self.resetResult)

    def search(self):
        #print("Searching...")
        self._se.search(self._helpSearchQuery.query())

    def showResults(self):
        #print("Hits:", self._se.hitCount())
        if self._se.hitCount() > 0:
            self._helpIndex.hide()
            h = self._splitterMain.geometry().height()
            self._splitterMain.setSizes([h*(1/3), h*(1/3), h*(1/3)])
            self._helpSearchResult.show()
            self._btnReset.show()

    def setUrl(self, urlstring):
        self._wv.setUrl(QUrl(urlstring))

    def resetResult(self):
        self._helpSearchResult.hide()
        self._btnReset.hide()
        self._helpIndex.show()
        h = self._splitterMain.geometry().height()
        self._splitterMain.setSizes([h*(1/9), h*(7/9), h*(1/9)])

class HelpNetworkAccessManager(QNetworkAccessManager):

    def __init__(self, parent = None, helpEngine = None):
        self._parent = parent
        self._helpEngine = helpEngine
        super().__init__(self._parent)

    def createRequest(self, operation, request, device):
        # ONLY react on qthelp://... requests
        if request.url().scheme() == 'qthelp':
            #print(request.url().toString())
            return HelpReply(self, operation, request, device, self._helpEngine)
        return super().createRequest(operation, request, device)


class HelpReply(QNetworkReply):

    def __init__(self, parent, operation, request, device, helpEngine):
        self._parent = parent
        self._helpEngine = helpEngine
        super().__init__(self._parent)
        self.setRequest(request)
        self.setOperation(operation)
        self.setUrl(request.url())
        self.bytes_read = 0
        self.content = b''

        # give webkit time to connect to the finished and readyRead signals
        QTimer.singleShot(200, self.load_content)

    def load_content(self):
        if self.operation() == QNetworkAccessManager.PostOperation:
            # handle post operations ... but not here ;-)
            pass
        # get content from help engine
        self.content = bytes(self._helpEngine.fileData(self.url()))

        self.open(QIODevice.ReadOnly | QIODevice.Unbuffered)
        self.setHeader(QNetworkRequest.ContentLengthHeader, len(self.content))
        self.setHeader(QNetworkRequest.ContentTypeHeader, "text/html")
        self.readyRead.emit()
        self.finished.emit()

    def abort(self):
        pass

    def isSequential(self):
        return True

    def bytesAvailable(self):
        ba = len(self.content) - self.bytes_read + super().bytesAvailable()
        return ba

    def readData(self, size):
        if self.bytes_read >= len(self.content):
            return None
        data = self.content[self.bytes_read:self.bytes_read + size]
        self.bytes_read += len(data)
        return data

    def manager(self):
        return self.parent()

class Help(QObject):
    def __init__(self, helpfile, prefix,short_url = None):
        super().__init__()
        self._help = HelpDialog(helpfile)
        self._helpprefix = prefix

        self.showHelp(short_url)

    def showHelp(self, short_url):
        if type(short_url) is str:
            self._help.setUrl(self._helpprefix + short_url)
        else:
            self._help.setUrl(self._helpprefix + "index.html")
        self._help.ui.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    #help = Help("de/tabPacket.html")
    Help("D:/Pythonprojects/opsipackgebuilder-dropbox/oPB/help/opsiPackageBuilder.qhc", "qthelp://org.sphinx.opsipackagebuilder.8.0/doc/")

    app.exec_()
