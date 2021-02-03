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

import datetime
import sys
import os
import inspect
import logging
import tempfile
import traceback
import pathlib
import platform
from logging import setLoggerClass
from io import StringIO

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen

import oPB
from oPB.core import confighandler

if sys.platform.lower().startswith('win'):
    from oPB.core.mapdrive import MapDrive
    import ctypes

    def hideConsole():
        """
        Hides the console window in GUI mode. Necessary for frozen application, because
        this application support both, command line processing AND GUI mode and theirfor
        cannot be run via pythonw.exe.
        """

        whnd = ctypes.windll.kernel32.GetConsoleWindow()
        if whnd != 0:
            ctypes.windll.user32.ShowWindow(whnd, 0)
            #ctypes.windll.kernel32.CloseHandle(whnd)

    def showConsole():
        """Unhides console window"""
        whnd = ctypes.windll.kernel32.GetConsoleWindow()
        if whnd != 0:
            ctypes.windll.user32.ShowWindow(whnd, 1)
            #ctypes.windll.kernel32.CloseHandle(whnd)

from oPB.controller import main, console
import oPB.core.logging
import oPB.gui.logging
from oPB.core.tools import Helper
from oPB.core.commandline import CommandLine
from oPB.gui.utilities import Translator
from oPB.gui.helpviewer import Help

translate = QtCore.QCoreApplication.translate

class Main(QObject):

    def __init__(self, parent = None):
        """Create a wizard or the mainwindow"""
        self._parent = parent

        super().__init__(self._parent)

        print("runner/Main parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None

        self.logger = None
        self.args = self.get_args()
        self._log_level = None
        self._log_file = None
        self.translator = None

        # make it really quiet, part 1
        if self.args.quiet:
            self.args.nogui = True

        # instantiate configuration class
        confighandler.ConfigHandler(oPB.CONFIG_INI)

        # redirect system exception hook
        if not self.args.noexcepthook:
            sys.excepthook = self.excepthook

        # pre-instantiating the application, avoid some nasty OpenGL messages
        QApplication.setAttribute(QtCore.Qt.AA_UseOpenGLES, on = True)
        # create new application and install stylesheet
        self.app = QApplication(sys.argv)
        #self.install_stylesheet()

        # Create and display the splash screen, if in ui mode
        if not self.args.nogui:
            splash_pix = QPixmap(':/images/splash.png')
            self.splash = QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
            self.splash.setMask(splash_pix.mask())
            # splash.showMessage("opsi Package Builder " + oPB.PROGRAM_VERSION + " " + translate("Main", "is loading..."), QtCore.Qt.AlignCenter, QtCore.Qt.white)
            self.splash.show()
            self.app.processEvents()

        # Application name
        self.app.setOrganizationName("opsi PackageBuilder")
        self.app.setApplicationName("opsi PackageBuilder")
        #self.app.setApplicationDisplayName("opsi PackageBuilder")
        self.app.setApplicationVersion(oPB.PROGRAM_VERSION)

        # save ourselves in main instance property to be easily accessd via qApp
        # i.e.
        # from PyQt5.QtWidgets import qApp
        # main = qApp.property("main")
        self.app.setProperty("main", self)

        if confighandler.ConfigHandler.cfg.log_always == "True":
            if self.args.log_file is not None:
                self._log_file = self.args.log_file
            else:
                self._log_file = confighandler.ConfigHandler.cfg.log_file

            if self.args.log_level.upper() != "NOTSET":
                self._log_level = self.args.log_level.upper()
            else:
                self._log_level = confighandler.ConfigHandler.cfg.log_level
        else:
            self._log_file = self.args.log_file
            if self.args.log_level.upper() == "NOTSET":
                self._log_level = "CRITICAL"
            else:
                self._log_level = self.args.log_level.upper()

        if self._log_file is not None:
            if not pathlib.Path(self._log_file).is_absolute():
                if platform.system() == "Windows":
                    self._log_file = str(pathlib.PurePath(oPB.WIN_TMP_PATH, self._log_file))
                if platform.system() in ["Darwin", "Linux"]:
                    self._log_file = str(pathlib.PurePath(oPB.UNIX_TMP_PATH, self._log_file))

        # overwrite development directory from config with command line arg
        if self.args.dev_dir is not None:
                confighandler.ConfigHandler.cfg.dev_dir = self.args.dev_dir

        # Initialize the logger and reroute QtCore messages to it
        self.logWindow = oPB.gui.logging.LogDialog(None, self, self._log_level)
        self.instantiate_logger(False)
        QtCore.qInstallMessageHandler(self.qt_message_handler)

        # log program version and user
        self.logger.info(80 * "-")
        self.logger.info("opsi PackageBuilder (MIT licensed) " + oPB.PROGRAM_VERSION)
        self.logger.info("Current user: " + Helper.get_user())

        # log commandline arguments
        self.logger.info("Command line arguments given:")
        for key, val in vars(self.args).items():
            self.logger.info("  " + key + ": " + str(val))
        if self._log_level not in ["DEBUG", "INFO", "SSHINFO", "WARNING", "ERROR", "CRITICAL", "SSH"]:
            self.logger.error("  Undefined log level: " + self._log_level)
            self.logger.error("  Log level has been set to ERROR")

        for elem in self.app.libraryPaths():
            self.logger.debug("QT5 library path: " + elem)

        # write config to log, if necessary
        confighandler.ConfigHandler.cfg.log_config()

        self.check_online_status()

        # -----------------------------------------------------------------------------------------
        # main ui dispatching

        # startup gui variant
        if not self.args.nogui:
            # install stylesheet
            self.install_stylesheet()

            # hide console window, but only under Windows and only if app is frozen
            if sys.platform.lower().startswith('win'):
                if getattr(sys, 'frozen', False):
                    hideConsole()

            # installing translators
            self.translator = Translator(self.app, "opsipackagebuilder")
            self.translator.install_translations(confighandler.ConfigHandler.cfg.language)

            # retranslate logWindow, as it is loaded before the translations
            self.logWindow.retranslateUi(self.logWindow)

            # create app icon
            app_icon = QtGui.QIcon()
            app_icon.addFile(':images/prog_icons/opb/package_16x16.png', QtCore.QSize(16, 16))
            app_icon.addFile(':images/prog_icons/opb/package_24x24.png', QtCore.QSize(24, 24))
            app_icon.addFile(':images/prog_icons/opb/package_32x32.png', QtCore.QSize(32, 32))
            app_icon.addFile(':images/prog_icons/opb/package_48x48.png', QtCore.QSize(48, 48))
            app_icon.addFile(':images/prog_icons/opb/package_64x64.png', QtCore.QSize(64, 64))
            app_icon.addFile(':images/prog_icons/opb/package_92x92.png', QtCore.QSize(92, 92))
            app_icon.addFile(':images/prog_icons/opb/package_128x128.png', QtCore.QSize(128, 128))
            app_icon.addFile(':images/prog_icons/opb/package_256x256.png', QtCore.QSize(256, 256))
            self.app.setProperty("prog_icon", app_icon)

            # startup program window
            self.mainWindow = main.MainWindowController(self.args)
            self.mainWindow.ui.showLogRequested.connect(self.logWindow.show)
            self.mainWindow.closeAppRequested.connect(self.logWindow.close)

            self.splash.finish(self.mainWindow.ui)

            # check for updates if configured
            if confighandler.ConfigHandler.cfg.updatecheck == "True":
                self.mainWindow.update_check()

            # run main app loop
            self.app.exec_()

        # only process commandline
        else:
            self.logger.info("No-GUI parameter set")

            # startup program window
            self.console = console.ConsoleController(self.args)

        # -----------------------------------------------------------------------------------------

        # unmount drive (if exist) after end of program
        if (oPB.NETDRV is not None) and oPB.NETDRV != "offline":
            ret = MapDrive.unMapDrive(oPB.NETDRV)
            if ret[0] != 0:
                self.logger.error("Error unmounting path: " + str(ret))
            else:
                self.logger.info("Network drive successfully unmounted")

        # exit and set return code
        self.logger.info("Exit code: " + str(oPB.EXITCODE))

        # show console window
        if not self.args.nogui:
            if sys.platform.lower().startswith('win'):
                if getattr(sys, 'frozen', False):
                    showConsole()

        sys.exit(oPB.EXITCODE)

    def qt_message_handler(self, mode, context, message):
        if mode == QtCore.QtInfoMsg:
            mode = 'INFO'
            fun = self.logger.info
        elif mode == QtCore.QtWarningMsg:
            mode = 'WARNING'
            fun = self.logger.warning
        elif mode == QtCore.QtCriticalMsg:
            mode = 'CRITICAL'
            fun = self.logger.critical
        elif mode == QtCore.QtFatalMsg:
            mode = 'FATAL'
            fun = self.logger.error
        else:
            mode = 'DEBUG'
            fun = self.logger.debug
        fun('Qt framework message handler: line: %d, func: %s(), file: %s' % (
            context.line, context.function, context.file))
        fun('Qt framework message handler:   %s: %s' % (mode, message))

    def install_stylesheet(self):
        if platform.system() == "Darwin":
            css = os.environ['OPB_BASE'] + "/ui/stylesheet-mac.qss"
        else:
            css = os.environ['OPB_BASE'] + "\\ui\\stylesheet.qss"

        try:
            with open(css, "r", encoding="utf-8", newline="\n") as file:
                style = file.readlines()
                file.close()
                self.logger.debug("Stylesheet successfully loaded: " + css)
        except:
            self.logger.debug("Stylesheet could not be opened: " + css)
        else:
            self.app.setStyleSheet(("\n").join(style))

    def check_online_status(self):
        self.logger.debug("Check online status")
        # check if server is generally available
        # use SSH port for connection test
        ret = Helper.test_port(confighandler.ConfigHandler.cfg.opsi_server, confighandler.ConfigHandler.cfg.sshport, 0.5)
        if ret is True:
            # check network access and mount network drive if on linux
            if sys.platform == 'win32':
                self.logger.info("System platform: "+ sys.platform)
                if self.args.nonetdrive is False:
                    if confighandler.ConfigHandler.cfg.usenetdrive == "False":

                        drives = Helper.get_available_drive_letters()
                        if not drives:
                            self.logger.error("No free drive letter found")
                        else:
                            self.logger.info("Free drive letter found: " + repr(drives))
                            self.logger.info("Using drive letter: " + drives[::-1][0])
                            path = "\\\\" + confighandler.ConfigHandler.cfg.opsi_server + "\\" + "opsi_workbench"
                            self.logger.info("Trying to mount path: " + path)
                            ret = MapDrive.mapDrive(drives[::-1][0] + ":", path, confighandler.ConfigHandler.cfg.opsi_user, confighandler.ConfigHandler.cfg.opsi_pass)
                            if ret[0] != 0:
                                self.logger.error("Error mounting path: " + str(ret))
                            else:
                                self.logger.info("Network drive successfully mounted")
                                oPB.NETDRV = drives[::-1][0] + ":"
                    else:
                        self.logger.info("Using existing network drive")
                else:
                    self.logger.info("Mounting of network drive via command line disabled")
            else:
                self.logger.info("System platform: "+ sys.platform)
                self.logger.warning("This is not a windows based system. No network drive will be associated")
                self.logger.warning("Please take care, that the specified development base path is correct.")
        else:
            self.logger.warning("opsi server not available. Offline mode activated.")
            self.logger.warning("Return value from connection test: " + str(ret))
            oPB.NETMODE = "offline"

    def get_args(self):
        # get cmdline args
        cmd_params = CommandLine()
        return cmd_params.getArgs()

    def set_log_level(self, level, handler):
        # set log level
        if level == "DEBUG":
            handler.setLevel(logging.DEBUG)
        elif level == "INFO":
            handler.setLevel(logging.INFO)
        elif level == "WARNING":
            handler.setLevel(logging.WARNING)
        elif level == "ERROR":
            handler.setLevel(logging.ERROR)
        elif level == "CRITICAL":
            handler.setLevel(logging.WARNING)
        elif level == "SSH":
            handler.setLevel(oPB.core.logging.SSH)
        elif level == "SSHINFO":
            handler.setLevel(oPB.core.logging.SSHINFO)
        else:
            handler.setLevel(logging.ERROR)

    def instantiate_logger(self, long):
        # for additional log facilities, see
        # http://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility

        # Create logger
        logger = logging.getLogger('oPB')

        # to add a further logging facility, we have to subclass current logger class
        # and set this new one to be the default logger class
        setLoggerClass(oPB.core.logging.SSHLogger)

        # log level for logger(!) - we filter on handler-based log level later
        self.set_log_level("DEBUG", logger)

        # make it really quiet, part 2
        if self.args.quiet:
            self.noop = logging.NullHandler()
            logger.addHandler(self.noop)
        else:
            if long:
                format = logging.Formatter(oPB.LOG_LONG, oPB.LOG_DATETIME)
            else:
                format = logging.Formatter(oPB.LOG_SHORT, oPB.LOG_DATETIME)

            # redirect stdout / stdin if gui
            if not self.args.nogui:
                # Output forwarding
                sys.stdout = oPB.core.logging.LogOutput(self.logWindow.editOutput,  sys.__stdout__,  self.logWindow.editOutput.textColor())
                sys.stderr = oPB.core.logging.LogOutput(self.logWindow.editOutput,  sys.__stderr__,  QtGui.QColor(QtCore.Qt.red))

            # Create standart output handler
            self.stdout = logging.StreamHandler(sys.__stderr__)
            self.set_log_level(self._log_level, self.stdout)
            self.stdout.setFormatter(format)

            # Add handlers to logger
            logger.addHandler(self.stdout)

            # Create different log window handler
            if not self.args.nogui:
                # output standard msg into dialog tab "Logging"
                self.dialogHandler = oPB.core.logging.LogStreamHandler(self.logWindow.editLog, self)
                self.dialogHandler.colors = oPB.OPB_LOG_COLORS
                self.dialogHandler.colorize = True
                self.set_log_level(self._log_level, self.dialogHandler)
                self.dialogHandler.setFormatter(format)

                logger.addHandler(self.dialogHandler)

                # Create special SSH output log facility, put this into tab "SSH Output"
                self.sshHandler = oPB.core.logging.LogStreamHandler(self.logWindow.editSSH, self)
                self.set_log_level("SSHINFO", self.sshHandler)
                sshformat = logging.Formatter(oPB.LOG_SSH, oPB.LOG_DATETIME)
                self.sshHandler.setFormatter(sshformat)

                logger.addHandler(self.sshHandler)

            # Create log file handler, possible
            try:
                if self._log_file is not None:
                    self.fileHandler = logging.FileHandler(self._log_file)
                    self.set_log_level(self._log_level, self.fileHandler)
                    self.fileHandler.setFormatter(format)

                    logger.addHandler(self.fileHandler)
            except IOError as error:
                logger.error("Log file could not be opened: " + self._log_file)
                logger.error(error)

        self.logger = logger

    def excepthook(self, excType, excValue, tracebackobj):
        """
        Global function to catch unhandled exceptions. Writes
        traceback to temporary file.

        Adopted to Python 3 from here:
        http://www.riverbankcomputing.com/pipermail/pyqt/2009-May/022961.html

        :param excType: exception type
        :param excValue: exception value
        :param tracebackobj: traceback object
        """

        try:
            self.splash.close()
        except:
            pass

        self.logger.debug("Entering excepthook")

        separator = '-' * 80
        logFile = tempfile.NamedTemporaryFile(mode = "w+", suffix = ".log", prefix = "opb-error-", delete = False)

        # """If you have any additional, confidential information you can\n""" \
        # """use this mail address: <%s>\n\n""" \

        notice = \
            """An unhandled exception occurred. Please report the problem\n"""\
            """via the official opsi PackageBuilder forum:\n\n"""\
            """https://forum.opsi.org/viewforum.php?f=22\n\n"""\
            """Thank you!\n\n"""\
            """A log has been written to "%s".\n\nError information:\n""" % \
            (logFile.name)

        timeString = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

        vText = "opsi PackageBuilder version: " + oPB.PROGRAM_VERSION

        tbinfofile = StringIO()
        traceback.print_tb(tracebackobj, None, tbinfofile)
        tbinfofile.seek(0)
        tbinfo = tbinfofile.read()
        errmsg = '%s: \n%s' % (str(excType), str(excValue))
        sections = [separator, timeString, vText, separator, errmsg, separator, tbinfo]
        msg = '\n'.join(sections)
        try:
            logFile.file.write(msg)
            logFile.close()
        except IOError:
            pass

        if not self.args.nogui:
            errorbox = QtWidgets.QMessageBox()
            errorbox.setText(str(notice) + str(msg))
            errorbox.exec_()
        else:
            print(str(notice) + str(msg))

class HelpViewerMain(QObject):
    def __init__(self, parent = None):
        """Create a wizard or the mainwindow"""
        self._parent = parent

        super().__init__(self._parent)

        print("runner/HelperTool parent: ", self._parent, " -> self: ", self) if oPB.PRINTHIER else None

        QApplication.setAttribute(QtCore.Qt.AA_UseOpenGLES)
        self.app = QApplication(sys.argv)

        # instantiate configuration class
        confighandler.ConfigHandler(oPB.CONFIG_INI)

        # installing translators
        self.translator = Translator(self.app, "opsipackagebuilder")
        self.translator.install_translations(confighandler.ConfigHandler.cfg.language)

        # instantiate help viewer and translate it, if necessary
        self.helpviewer = Help(oPB.HLP_FILE, oPB.HLP_PREFIX)
        self.helpviewer.showHelp(oPB.HLP_DST_INDEX, False)
        event = QtCore.QEvent(QtCore.QEvent.LanguageChange)
        self.helpviewer._help.ui.changeEvent(event)

        # run main loop
        # return to os
        sys.exit(self.app.exec_())
