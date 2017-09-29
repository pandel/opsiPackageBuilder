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
import mimetypes
import os
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtHelp import QHelpEngine
from PyQt5.QtWidgets import QApplication, QSplitter, QDialog, QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import QObject, QUrl, pyqtSignal, pyqtSlot, QByteArray, QIODevice, QBuffer
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebEngineCore import QWebEngineUrlSchemeHandler, QWebEngineUrlRequestJob


from oPB.core.tools import LogMixin

translate = QtCore.QCoreApplication.translate

QtHelp_DOCROOT = "qthelp://org.qt-project."

ExtensionMap = {
    ".bmp": "image/bmp",
    ".css": "text/css",
    ".gif": "image/gif",
    ".html": "text/html",
    ".htm": "text/html",
    ".ico": "image/x-icon",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".js": "application/x-javascript",
    ".mng": "video/x-mng",
    ".pbm": "image/x-portable-bitmap",
    ".pgm": "image/x-portable-graymap",
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".ppm": "image/x-portable-pixmap",
    ".rss": "application/rss+xml",
    ".svg": "image/svg+xml",
    ".svgz": "image/svg+xml",
    ".text": "text/plain",
    ".tif": "image/tiff",
    ".tiff": "image/tiff",
    ".txt": "text/plain",
    ".xbm": "image/x-xbitmap",
    ".xml": "text/xml",
    ".xpm": "image/x-xpm",
    ".xsl": "text/xsl",
    ".xhtml": "application/xhtml+xml",
    ".wml": "text/vnd.wap.wml",
    ".wmlc": "application/vnd.wap.wmlc",
}


# https://fossies.org/linux/eric6/eric/WebBrowser/Network/QtHelpSchemeHandler.py
class HelpSchemeHandler(QWebEngineUrlSchemeHandler):
    """
    Class implementing a scheme handler for the qthelp: scheme.

    see: https://fossies.org/linux/eric6/eric/WebBrowser/Network/QtHelpSchemeHandler.py
    All credits for this class go to:
    Detlev Offenbach, the developer of The Eric Python IDE (https://eric-ide.python-projects.org)

    """

    def __init__(self, engine, parent=None):
        """
        Constructor

        @param engine reference to the help engine
        @type QHelpEngine
        @param parent reference to the parent object
        @type QObject
        """
        super(HelpSchemeHandler, self).__init__(parent)

        self._engine = engine

        self._replies = []

    def requestStarted(self, job):
        """
        Public method handling the URL request.

        @param job URL request job
        @type QWebEngineUrlRequestJob
        """
        if job.requestUrl().scheme() == "qthelp":
            reply = HelpSchemeReply(job, self._engine)
            reply.closed.connect(self.__replyClosed)
            self._replies.append(reply)
            job.reply(reply.mimeType(), reply)
        else:
            job.fail(QWebEngineUrlRequestJob.UrlInvalid)

    @pyqtSlot()
    def __replyClosed(self):
        """
        Private slot handling the closed signal of a reply.
        """
        reply = self.sender()
        if reply and reply in self._replies:
            self._replies.remove(reply)


class HelpSchemeReply(QIODevice):
    """
    Class implementing a reply for a requested qthelp: page.

    @signal closed emitted to signal that the web engine has read
        the data

    see: https://fossies.org/linux/eric6/eric/WebBrowser/Network/QtHelpSchemeHandler.py
    All credits for this class go to:
    Detlev Offenbach, the developer of The Eric Python IDE(https://eric-ide.python-projects.org)

    """
    closed = pyqtSignal()

    def __init__(self, job, engine, parent=None):
        """
        Constructor

        @param job reference to the URL request
        @type QWebEngineUrlRequestJob
        @param engine reference to the help engine
        @type QHelpEngine
        @param parent reference to the parent object
        @type QObject
        """
        super(HelpSchemeReply, self).__init__(parent)

        url = job.requestUrl()
        strUrl = url.toString()

        self.__buffer = QBuffer()

        # For some reason the url to load maybe wrong (passed from web engine)
        # though the css file and the references inside should work that way.
        # One possible problem might be that the css is loaded at the same
        # level as the html, thus a path inside the css like
        # (../images/foo.png) might cd out of the virtual folder
        if not engine.findFile(url).isValid():
            if strUrl.startswith(QtHelp_DOCROOT):
                newUrl = job.requestUrl()
                if not newUrl.path().startswith("/qdoc/"):
                    newUrl.setPath("/qdoc" + newUrl.path())
                    url = newUrl
                    strUrl = url.toString()

        self.__mimeType = mimetypes.guess_type(strUrl)[0]
        if self.__mimeType is None:
            # do our own (limited) guessing
            self.__mimeType = self.__mimeFromUrl(url)

        if engine.findFile(url).isValid():
            data = engine.fileData(url)
        else:
            data = QByteArray(self.tr(
                """<html>"""
                """<head><title>Error 404...</title></head>"""
                """<body><div align="center"><br><br>"""
                """<h1>The page could not be found</h1><br>"""
                """<h3>'{0}'</h3></div></body>"""
                """</html>""").format(strUrl)
                              .encode("utf-8"))

        self.__buffer.setData(data)
        self.__buffer.open(QIODevice.ReadOnly)
        self.open(QIODevice.ReadOnly)

    def bytesAvailable(self):
        """
        Public method to get the number of available bytes.

        @return number of available bytes
        @rtype int
        """
        return self.__buffer.bytesAvailable()

    def readData(self, maxlen):
        """
        Public method to retrieve data from the reply object.

        @param maxlen maximum number of bytes to read (integer)
        @return string containing the data (bytes)
        """
        return self.__buffer.read(maxlen)

    def close(self):
        """
        Public method used to cloase the reply.
        """
        super(HelpSchemeReply, self).close()
        self.closed.emit()

    def __mimeFromUrl(self, url):
        """
        Private method to guess the mime type given an URL.

        @param url URL to guess the mime type from (QUrl)
        @return mime type for the given URL (string)
        """
        path = url.path()
        ext = os.path.splitext(path)[1].lower()
        if ext in ExtensionMap:
            return ExtensionMap[ext]
        else:
            return "application/octet-stream"

    def mimeType(self):
        """
        Public method to get the reply mime type.

        @return mime type of the reply
        @rtype bytes
        """
        return self.__mimeType.encode("utf-8")

class HelpDialog(QObject, LogMixin):
    """Class implementing qthelp viewer dialog"""

    def __init__(self, qthelp_file, parent = None):
        """
        Constructor of HelpDialog

        :param qthelp_file: full path to qthelp helpfile

        """
        super(HelpDialog,self).__init__(parent)

        # instantiate help engine

        helpEngine = QHelpEngine(qthelp_file)
        helpEngine.setupData()
        self._helpEngine = helpEngine

        # base dialog widget
        self.ui = QDialog(None, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCloseButtonHint )

        self.ui.setWindowTitle("HelpViewer")
        self.ui.setWindowIcon(QIcon(":/images/prog_icons/help/help.ico"))

        # Create webview for help information
        # and assign a custom URL scheme handler for scheme "qthelp)
        self._wv = QWebEngineView(self.ui)
        self._urlschemehandler = HelpSchemeHandler(self._helpEngine, self._wv.page().profile())
        self._wv.page().profile().installUrlSchemeHandler(b'qthelp', self._urlschemehandler)

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
        self._btnReset.setMaximumWidth(100)

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

        self.retranslateMsg()

    def retranslateMsg(self):
        self.logger.debug("Retranslating further messages...")
        self._btnReset.setText(translate("HelpViewer", "Reset"))
        self._btnReset.setText(translate("HelpViewer", "Search"))

    def search(self):
        """Initiate qthelp search"""
        self._se.search(self._helpSearchQuery.query())

    def showResults(self):
        """Show search results, if any"""
        if self._se.hitCount() > 0:
            self._helpIndex.hide()
            h = self._splitterMain.geometry().height()
            self._splitterMain.setSizes([h*(1/3), h*(1/3), h*(1/3)])
            self._helpSearchResult.show()
            self._btnReset.show()

    def resetResult(self):
        """Reset search result widget"""

        self._helpSearchResult.hide()
        self._btnReset.hide()
        self._helpIndex.show()
        h = self._splitterMain.geometry().height()
        self._splitterMain.setSizes([h*(1/9), h*(7/9), h*(1/9)])


class Help(QObject):
    """Main HelpViewer class"""

    def __init__(self, helpfile, prefix, parent=None):
        """
        Constructor of Help
        :param helpfile: full path to qthelp file
        :param prefix: url prefix, like qthelp://org.sphinx...
        :param short_url: shortcut url to help content, omits ``prefix``
        :param max: show helpviewer maximized (True), or not (False)
        """
        super().__init__(parent)
        self._help = HelpDialog(helpfile, self)
        self._helpprefix = prefix

        #self.showHelp(short_url, max)

    def showHelp(self, short_url = None, max = True):
        """Find short ``short_url`` in help file and open (maximized) viewer"""

        if type(short_url) is str:
            self._help._wv.setUrl(QUrl(self._helpprefix + short_url))
        else:
            self._help._wv.setUrl(QUrl(self._helpprefix + "index.html"))

        if max:
            self._help.ui.showMaximized()
        else:
            self._help.ui.show()

    def close(self):
        self._help.ui.close()

    def isVisible(self):
        return self._help.ui.isVisible()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    #help = Help("de/tabPacket.html")

    Help("D:/Pythonprojects/opsipackgebuilder-dropbox/oPB/help/opsiPackageBuilder.qhc", "qthelp://org.sphinx.opsipackagebuilder.8.0/doc/")

    sys.exit(app.exec_())

