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

import os
from pathlib import PurePath, Path

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal

import oPB
from oPB.core.confighandler import ConfigHandler
from oPB.core.datadefinition import changelog_footer, ControlFileData, ChangelogEntry, ProductDependency, ProductProperty
from oPB.core.processing import OpsiProcessing
from oPB.core.tools import Helper, LogMixin

translate = QtCore.QCoreApplication.translate


class BaseController(LogMixin):

    closeAppRequested = pyqtSignal(int)
    msgSend = pyqtSignal(str) # emit message text, params: header and text
    processingStarted = pyqtSignal()
    processingEnded = pyqtSignal()
    dataAboutToBeRequested = pyqtSignal()
    dataRequested = pyqtSignal()

    clientlist_dict = None
    clientsondepotslist_dict = None
    depotlist_dict = None
    productlist_dict = None
    productsondepotslist = None
    joblist = []

    """
    Base class for handling application requests. It contains necessary methods and attributes
    used for GUI and non-GUI (console) operations.
    """
    def __init__(self, args):
        super().__init__()
        self.args = None
        self.ui = None
        self.controlData = None
        self._dataSaved = None            # True = success, False = failure, None = unset
        self._dataLoaded = None            # True = success, False = failure, None = unset

        self.args = args
        self.controlData = ControlFileData()

        self.controlData.dataLoaded.connect(self.check_backend_data_loaded)
        self.controlData.dataSaved.connect(self.check_backend_data_saved)

    @pyqtSlot(bool)
    def check_backend_data_saved(self, retval):
        """Set marker to see if backend data has been saved successfully"""
        self.logger.debug("Retrieved backend data saved status: " + str(retval))
        self._dataSaved = retval

    @pyqtSlot(bool)
    def check_backend_data_loaded(self, retval):
        """Set marker to see if backend data has been saved successfully"""
        self.logger.debug("Retrieved backend data loaded status: " + str(retval))
        self._dataLoaded = retval


    def save_backend(self):
        """Save backend data"""
        # do we have to add a forced build comment?
        if ConfigHandler.cfg.chlog_on_save == "True":
            comment = ""
            if not self.args.nogui:
                while comment == "":
                    (comment, accept) = self.msgbox(translate("baseController","Please enter a short comment:"), oPB.MsgEnum.MS_QUEST_PHRASE)
            else:
                comment = "Auto-save project from command line"

            self.add_changelog_entry(" * SAVE COMMENT: " + comment)

        self.controlData.save_data()

        while self._dataSaved is None:  # _dataSaved has to be True or False
            pass

        if not self._dataSaved:
            oPB.EXITCODE = oPB.RET_BSAVE

    def reset_backend(self):
        """Reset backend data to initial values"""
        self.controlData.init_data()

    def create_backend(self, project_folder):
        path = PurePath(project_folder)

        try:
            self.create_project_paths(project_folder)
            project_name = path.name.replace(" ","_")
            self.controlData.init_data(project_name)
            self.controlData.projectfolder = project_folder
            self.add_changelog_entry("Project created with opsi Package Builder " + oPB.PROGRAM_VERSION)
            self.save_backend()
            self._dataSaved = None
            self._dataSaved = True
        except Exception:
            self.reset_backend()
            raise

    def add_changelog_entry(self, text = ""):
        if text == "":
            text = "Please add a short description."
        newentry = ChangelogEntry(self.controlData.id)
        newentry.version = "(" + self.controlData.productversion + "-" + self.controlData.packageversion + ")"
        newentry.status = oPB.CHLOG_STATI[0]
        newentry.urgency = oPB.CHLOG_BLOCKMARKER + oPB.CHLOG_URGENCIES[0]
        newentry.text = "\n" + text + changelog_footer()
        self.controlData.changelog_append(newentry)

    def create_project_paths(self, base):
        for elem in oPB.BASE_FOLDERS:
            try:
                path = Path(Helper.concat_path_and_file(base, elem))
                if not path.exists():
                    path.mkdir(parents=True)
            except OSError:
                raise

    def load_backend(self, project_name):
        """Load project data."""
        # itemChanged signal has to be disconnected temporarily, because
        # if not, dataChanged would be set after loading
        self.logger.info("Load project: " + project_name)
        self.controlData.load_data(Helper.concat_path_and_file(ConfigHandler.cfg.dev_dir, project_name))
        while self._dataLoaded is None: # _dataLoaded has to be True or False
            pass

        if not self._dataLoaded:
            # reset loading marker back to unsaved state
            self.logger.error("Backend data could not be loaded.")
            self._dataLoaded = None
            self.logger.debug("Set exitcode RET_EOPEN")
            oPB.EXITCODE = oPB.RET_EOPEN
        else:
            self.logger.info("Backend data loaded")

    def _do(self, jobtype, msg, **kwargs):
        proc = OpsiProcessing(self.controlData)
        proc.progressChanged.connect(self.msgSend)

        # run build job
        self.processingStarted.emit()
        self.msgSend.emit(msg)
        result = proc.run(jobtype, **kwargs)
        self.processingEnded.emit()

        oPB.EXITCODE = result[0]
        if result[0] == oPB.RET_OK:
            self.msgbox(translate("baseController", "Action completed successfully!"), oPB.MsgEnum.MS_INFO)
        else:
            self.msgbox(result[2], result[1])

        return result[3]

    @pyqtSlot()
    def do_build(self):
        if os.path.isfile(self.controlData.local_package_path):
            if self.args.build_mode is None:
                self.logger.debug("Package exits. Ask for further step (cancel, rebuild, add version)")
                reply = self.msgbox(translate("BaseController", "This package version already exists! You have three possibilities:@@Rebuild@TAB@TAB= rebuild (overwrite) the existing one@Add version@TAB= auto-correct package version and build new one@Cancel@TAB= cancel build process"),
                                    oPB.MsgEnum.MS_QUEST_CTC)
            else:
                if self.args.build_mode.upper() == "CANCEL":
                    reply = 0
                if self.args.build_mode.upper() == "REBUILD":
                    reply = 1
                if self.args.build_mode.upper() == "ADD":
                    reply = 2

            # cancel
            if reply == 0:
                self.logger.debug("Process choice: cancel")
                oPB.EXITCODE = oPB.RET_BCANCEL
                return

            # rebuild
            if reply == 1:
                self.logger.debug("Process choice: rebuild")
                try:
                    self.logger.debug("Deleting existing package: " + self.controlData.local_package_path)
                    os.unlink(self.controlData.local_package_path)
                except Exception:
                    self.logger.error("Could not delete old package!")
                    self.msgbox(translate("baseController", "Could not delete old package!"), oPB.MsgEnum.MS_ERR)
                    oPB.EXITCODE = oPB.RET_BFILEDEL
                    return

            # add version
            if reply == 2:
                self.logger.debug("Process choice: add version")
                self.controlData.inc_packageversion()
                self.save_backend()

                while self._dataSaved is None: # _dataSaved has to be True or False
                    pass
                if not self._dataSaved:
                    self.logger.error("Backend data could not be saved")
                    self._dataSaved = None
                    oPB.EXITCODE = oPB.RET_BSAVE
                    return

        # do we have to add a forced build comment?
        if ConfigHandler.cfg.chlog_on_build == "True":
            comment = ""
            if self.args.build_mode is None:
                while comment == "":
                    (comment, accept) = self.msgbox(translate("baseController","Please enter a short build comment:"), oPB.MsgEnum.MS_QUEST_PHRASE)
            else:
                comment = "Automatic entry: command line building initiated"
            self.add_changelog_entry(" * BUILD COMMENT: " + comment)
            self.save_backend()

            while self._dataSaved is None: # _dataSaved has to be True or False
                pass
            if not self._dataSaved:
                self.logger.error("Backend data could not be saved")
                self._dataSaved = None
                oPB.EXITCODE = oPB.RET_BSAVE
                return

        # reset any manipulation
        # if we don't do this, normale save operation can not be
        # recognized from outside
        self._dataSaved = None

        self._do(oPB.OpEnum.DO_BUILD, translate("baseController", "Build running..."))

    @pyqtSlot()
    def do_install(self):
        self._do(oPB.OpEnum.DO_INSTALL, translate("baseController", "Installation running..."))

    @pyqtSlot()
    def do_quickinstall(self, param):
        self._do(oPB.OpEnum.DO_QUICKINST, translate("baseController", "Installation running..."), packagefile=param)

    @pyqtSlot()
    def do_quickuninstall(self, param):
        self._do(oPB.OpEnum.DO_QUICKUNINST, translate("baseController", "Deinstallation running..."), productlist=param)

    @pyqtSlot()
    def do_upload(self, param):
        self._do(oPB.OpEnum.DO_UPLOAD, translate("baseController", "Installation running..."), packagefile=param)

    @pyqtSlot()
    def do_installsetup(self):
        self._do(oPB.OpEnum.DO_INSTSETUP, translate("baseController", "Installation + setup running..."))

    @pyqtSlot()
    def do_uninstall(self):
        self._do(oPB.OpEnum.DO_UNINSTALL, translate("baseController", "Deinstallation running..."))

    @pyqtSlot()
    def do_setrights(self):
        self._do(oPB.OpEnum.DO_SETRIGHTS, translate("baseController", "Setting package rights on:") + " " + self.controlData.path_on_server)

    @pyqtSlot()
    def do_getclients(self):
        BaseController.clientlist_dict = self._do(oPB.OpEnum.DO_GETCLIENTS, translate("baseController", "Getting opsi client list..."))
        self.dataRequested.emit()

    @pyqtSlot()
    def do_getproducts(self):
        BaseController.productlist_dict = self._do(oPB.OpEnum.DO_GETPRODUCTS, translate("baseController", "Getting opsi product list..."))
        self.dataRequested.emit()

    @pyqtSlot()
    def do_getproductsondepots(self):
        BaseController.productsondepotslist= self._do(oPB.OpEnum.DO_GETPRODUCTSONDEPOTS, translate("baseController", "Getting opsi products on depots list..."))
        self.dataRequested.emit()

    @pyqtSlot()
    def do_getjobs(self):
        BaseController.joblist = self._do(oPB.OpEnum.DO_GETJOBS, translate("baseController", "Getting AT job list..."))
        self.dataRequested.emit()

    @pyqtSlot()
    def do_getdepots(self):
        tmpdict = {}
        BaseController.depotlist_dict = self._do(oPB.OpEnum.DO_GETDEPOTS, translate("baseController", "Getting opsi depots..."))
        for elem in BaseController.depotlist_dict:
            tmpdict[elem["id"]] = elem["description"]
        ConfigHandler.cfg.depotcache = tmpdict
        self.dataRequested.emit()

    @pyqtSlot()
    def do_getclientsondepots(self):
        BaseController.clientsondepotslist_dict = self._do(oPB.OpEnum.DO_GETCLIENTSONDEPOTS, translate("baseController", "Getting client to depot association..."))
        self.dataRequested.emit()

    @pyqtSlot()
    def do_deletejobs(self, param):
        self._do(oPB.OpEnum.DO_DELETEJOBS, translate("baseController", "Delete AT jobs..."), joblist = param)
        self.dataRequested.emit()

    @pyqtSlot()
    def do_deletealljobs(self):
        self._do(oPB.OpEnum.DO_DELETEALLJOBS, translate("baseController", "Delete every AT job..."))
        self.dataRequested.emit()

    @pyqtSlot()
    def do_createjobs(self, **param):
        self._do(oPB.OpEnum.DO_CREATEJOBS, translate("baseController", "Create AT jobs..."), **param)
        self.dataRequested.emit()

    @pyqtSlot()
    def do_getrepocontent(self, param):
        tmp = self._do(oPB.OpEnum.DO_GETREPOCONTENT, translate("baseController", "Get repository contents..."), alt_destination = param)
        self.dataRequested.emit()
        return tmp

    @pyqtSlot()
    def do_reboot(self, dest, user, password):
        self._do(oPB.OpEnum.DO_REBOOT, translate("baseController", "Reboot depot..."), alt_destination = dest, alt_user = user, alt_pass = password)

    @pyqtSlot()
    def do_poweroff(self, dest, user, password):
        self._do(oPB.OpEnum.DO_POWEROFF, translate("baseController", "Poweroff depot..."), alt_destination = dest, alt_user = user, alt_pass = password)

    @pyqtSlot()
    def do_runproductupdater(self, param):
        self._do(oPB.OpEnum.DO_PRODUPDATER, translate("baseController", "Run opsi-product-updater..."), alt_destination = param)

    def run_command_line(self):
        """Process project action via command line"""
        self.logger.debug("Project via command line: " + self.args.path)
        self.load_backend(self.args.path)

        if self.args.build_mode is not None:
            self.logger.debug("Command line: build")
            self.do_build()
        try:
            self.logger.debug("Command line: " + self.args.packetaction[0])
            if self.args.packetaction[0] == "install":
                self.do_install()
            if self.args.packetaction[0] == "instsetup":
                self.do_installsetup()
            if self.args.packetaction[0] == "uninstall":
                self.do_uninstall()
        except:
            pass

    def msgbox(self, msgtext = "", typ = oPB.MsgEnum.MS_STAT, parent = None):
        """ Messagebox function (virtual)

        ** HAS TO BE RE-IMPLEMENTES **

        Valid values for ``typ``:
            * oPB.MsgEnum.MS_ERR -> Error message (status bar/ popup)
            * oPB.MsgEnum.MS_WARN -> Warning (status bar/ popup)
            * oPB.MsgEnum.MS_INFO -> Information (status bar/ popup)
            * oPB.MsgEnum.MS_STAT -> Information (only status bar)
            * oPB.MsgEnum.MS_ALWAYS -> Display this message ALWAYS, regardless of which message ``typ`` is deactivated via settings
            * oPB.MsgEnum.MS_PARSE -> just parse message text and return it
            * oPB.MsgEnum.MS_QUEST_YESNO -> return True / False
            * oPB.MsgEnum.MS_QUEST_CTC -> build question: cancel (return 0)/ rebuild return(1)/ add return (2)
            * oPB.MsgEnum.MS_QUEST_OKCANCEL -> return True / False
            * oPB.MsgEnum.MS_QUEST_PHRASE -> return text from input box

        :param msgtext: Message text
        :param typ: type of message window, see oPB.core enums
        :return see descriptions for ``typ``
        """
        if parent is None:
            parent = self.ui

        # first parse text
        msgtext = Helper.parse_text(msgtext)
        pass
