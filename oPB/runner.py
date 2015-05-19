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
from logging import setLoggerClass
from io import StringIO

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication

import oPB
from oPB.core import confighandler
if sys.platform == 'win32':
    from oPB.core.mapdrive import MapDrive
from oPB.controller import main, console
import oPB.core.logging
import oPB.gui.logging
from oPB.core.tools import CommandLine, Helper

translate = QtCore.QCoreApplication.translate

def get_script_dir(follow_symlinks=True):
    """Get file path of script. Take freezing into account."""
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)

""" We have to set an environment variables to correct paths when freezing the application.
    OPB_BASE   -> to correct paths to *.ui files in corresponding modules
"""
os.environ['OPB_BASE'] = get_script_dir()


class Main(QObject):

    def __init__(self, parent = None):
        """Create a wizard or the mainwindow"""
        super().__init__(parent)

        self.logger = None
        self.args = self.get_args()

        # redirect system exception hook
        sys.excepthook = self.excepthook

        # create new application
        self.app = QApplication(sys.argv)

        # Application name
        self.app.setOrganizationName("opsi Package Builder")
        self.app.setApplicationName("opsi Package Builder " + oPB.PROGRAM_VERSION)

        # save ourselves in main instance property to be easily accessd via qApp
        # i.e.
        # from PyQt5.QtWidgets import qApp
        # main = qApp.property("main")
        self.app.setProperty("main", self)

        # Initialize the logger
        self.logWindow =  oPB.gui.logging.LogDialog(None, self, self.args.log_level.upper())
        self.instantiate_logger(False)

        #self.instantiate_logger_old()

        # instantiate configuration class
        confighandler.ConfigHandler(oPB.CONFIG_INI)

        # log program version and user
        self.logger.info("opsi PackageBuilder (MIT licensed) " + oPB.PROGRAM_VERSION)
        self.logger.info("Current user: " + Helper.get_user())

        # log commandline arguments
        self.logger.info("Command line arguments given:")
        for key, val in vars(self.args).items():
            self.logger.info("  " + key + ": " + str(val))
        if self.args.log_level.upper() not in ["DEBUG", "INFO", "SSHINFO", "WARNING", "ERROR", "CRITICAL", "SSH"]:
            self.logger.error("  Undefined log level: " + self.args.log_file.upper())
            self.logger.error("  Log level has been set to ERROR")

        for elem in self.app.libraryPaths():
            self.logger.debug("QT5 library path: " + elem)

        self.install_translations()
        self.install_stylesheet()

        self.check_online_status()

        # -----------------------------------------------------------------------------------------
        # main ui dispatching

        # startup gui variant
        if not self.args.nogui:

            # startup program window
            self.mainWindow = main.MainWindowController(self.args)
            self.mainWindow.ui.showLogRequested.connect(self.logWindow.show)
            self.mainWindow.closeAppRequested.connect(self.logWindow.close)

            # run main app loop
            self.app.exec_()

        # only process commandline
        else:
            self.logger.info("No-GUI parameter set")

            # startup program window
            self.console = console.ConsoleController(self.args)

        # -----------------------------------------------------------------------------------------

        # unmount drive after end of program
        if oPB.NETDRV is not None:
            ret = MapDrive.unMapDrive(oPB.NETDRV)
            if ret[0] != 0:
                self.logger.error("Error unmounting path: " + str(ret))
            else:
                self.logger.info("Network drive successfully unmounted")

        # exit and set return code
        self.logger.debug("Exit code: " + str(oPB.EXITCODE))

        sys.exit(oPB.EXITCODE)

    def install_stylesheet(self):
        css = get_script_dir()+"/ui/stylesheet.qss"

        try:
            file = open(css, "r", encoding="utf-8", newline="\n")
            self.logger.debug("Stylesheet: " + css)
            style = file.readlines()
            file.close()
        except:
            self.logger.error("Error reading stylesheet")
            return

        self.app.setStyleSheet(("\n").join(style))

    def install_translations(self):
        # get current system language and load translation
        # we need two translators: one for the individual appplication strings
        # and one for the standard qt message texts
        # qm = 'opsiPackageBuilder_en_EN.qm'
        # get files
        qm_app = ':locale/opsiPackageBuilder_%s.qm' % QtCore.QLocale().system().name()
        self.logger.debug("Load application translation: " + qm_app)
        qm_qt = ':locale/qtbase_%s.qm' % QtCore.QLocale().system().name()
        self.logger.debug("Load Qt standard translation: " + qm_qt)

        # create translators
        translator_app = QtCore.QTranslator(self.app)
        translator_app.load(qm_app)
        translator_qt = QtCore.QTranslator(self.app)
        translator_qt.load(qm_qt)

        # install translators to use it later
        self.app.installTranslator(translator_app)
        self.app.installTranslator(translator_qt)

    def check_online_status(self):
        self.logger.debug("Check online status")
        # check if server is generally available
        # use SSH port for connection test
        ret = Helper.test_port(confighandler.ConfigHandler.cfg.opsi_server, confighandler.ConfigHandler.cfg.sshport, 0.5)
        if ret == True:
            # check network access and mount network drive if on linux
            if sys.platform == 'win32':
                self.logger.info("System platform: "+ sys.platform)
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
                self.logger.info("System platform: "+ sys.platform)
                self.logger.warning("This is not a windows based system. No network drive will be associated")
                self.logger.warning("Please take care, if the specified development base path is correct.")
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

        # log level from command line or standard
        self.set_log_level(self.args.log_level.upper(), logger)

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
        self.set_log_level(self.args.log_level.upper(), self.stdout)
        self.stdout.setFormatter(format)

        # Add handlers to logger
        logger.addHandler(self.stdout)

        # Create different log window handler
        if not self.args.nogui:
            # output standard msg into dialog tab "Logging"
            self.dialogHandler = oPB.core.logging.LogStreamHandler(self.logWindow.editLog, self)
            self.set_log_level(self.args.log_level.upper(), self.dialogHandler)
            self.dialogHandler.setFormatter(format)

            logger.addHandler(self.dialogHandler)

            # Create special SSH output log facility, put this into tab "SSH Output"
            self.sshHandler = oPB.core.logging.LogStreamHandler(self.logWindow.editSSH, self)
            self.set_log_level(oPB.core.logging.SSH, self.sshHandler)
            sshformat = logging.Formatter(oPB.LOG_SSH, oPB.LOG_DATETIME)
            self.sshHandler.setFormatter(sshformat)

            logger.addHandler(self.sshHandler)

        # Create log file handler, possible
        try:
            if self.args.log_file is not None:
                self.fileHandler = logging.FileHandler(self.args.log_file)
                self.fileHandler.setFormatter(format)

                logger.addHandler(self.fileHandler)
        except IOError as error:
            logger.error("Log file could not be opened: " + self.args.log_file)
            logger.error(error)

        self.logger = logger

    def excepthook(self, excType, excValue, tracebackobj):
        """
        Global function to catch unhandled exceptions. Writes
        traceback to temporary file.

        Adopted to Python 3 from here:
        http://www.riverbankcomputing.com/pipermail/pyqt/2009-May/022961.html

        :param excType exception type
        :param excValue exception value
        :param tracebackobj traceback object
        """
        self.logger.debug("Entering excepthook")

        separator = '-' * 80
        logFile = tempfile.NamedTemporaryFile(mode = "w+", suffix = ".log", prefix = "opb-error-", delete = False)

        notice = \
            """An unhandled exception occurred. Please report the problem\n"""\
            """using an error reporting email to <%s>.\n\n"""\
            """A log has been written to "%s".\n\nError information:\n""" % \
            (oPB.__email__, logFile.name)

        versionInfo="0.0.1"
        timeString = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")


        tbinfofile = StringIO()
        traceback.print_tb(tracebackobj, None, tbinfofile)
        tbinfofile.seek(0)
        tbinfo = tbinfofile.read()
        errmsg = '%s: \n%s' % (str(excType), str(excValue))
        sections = [separator, timeString, separator, errmsg, separator, tbinfo]
        msg = '\n'.join(sections)
        try:
            logFile.file.write(msg)
            logFile.file.write(versionInfo)
            logFile.close()
        except IOError:
            pass

        if not self.args.nogui:
            errorbox = QtWidgets.QMessageBox()
            errorbox.setText(str(notice) + str(msg) + str(versionInfo))
            errorbox.exec_()
        else:
            print(str(notice) + str(msg) + str(versionInfo))
