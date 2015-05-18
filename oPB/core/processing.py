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
import sys
import json
import os
import socket
import spur
import shutil
from io import StringIO
from pathlib import Path, PurePath, PurePosixPath

from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSignal

import oPB
from oPB.core.confighandler import ConfigHandler
from oPB.core.tools import Helper, LogMixin

translate = QtCore.QCoreApplication.translate

class OpsiProcessing(QObject, LogMixin):

    progressChanged = pyqtSignal(str)

    """
    opsi server job handler
    """
    # def __init__(self, project, project_folder, server="127.0.0.1", port=22, username = None, password = None, keyfile = None, cfg = None):
    def __init__(self, control = None):
        """
        Initialises job processing.

        :param control: backend controlData object
        :return:
        """
        super().__init__()
        self._shell = None
        self._ip = None
        self._hide_secret_in_output = False
        self._sshuser = None
        self._sshpass = None
        self._sshkey = None

        self.control = control

        self.ret = oPB.RET_OK
        self.rettype = oPB.MsgEnum.MS_INFO
        self.retmsg = translate("OpsiProcessing", "Command executed.")

    def run(self, action, **kwargs):
        """
        Starts job processing.

        :param action: job to run (see oPB.OpEnum for job types)
        :param kwargs: optional arguments depending on job type, see below
        :return: tuple(3): (return code(see oPB.RET_*), msg type (see oPB.MsgEnum), msg text)
        """

        #options = {
        #    'prodver' : '1.0',
        #    'packver' : '1',}
        #options.update(kwargs)
        #packname = self.control.name + "_" + options['prodver'] + "-" + options['packver'] + ".opsi"

        # individual user / pass for shell
        # if not set, ConfigHandler.cfg.opsi_user + ConfigHandler.cfg.opsi_pass are used

        # reset ssh user / pass
        self._hide_secret_in_output = []
        self._sshuser = ConfigHandler.cfg.opsi_user
        self._sshpass = ConfigHandler.cfg.opsi_pass
        self._sshkey = ConfigHandler.cfg.keyfilename

        self._env = {"PYTHONIOENCODING" : "'utf-8'", "POSIXLY_CORRECT" : "1"}

        self.logger.debug("Executing action: " + str(oPB.OpEnum(action)))
        if not self.control is None:
            self.logger.sshinfo("Local path: " + self.control.local_package_path)
            self.logger.sshinfo("Path on server: " + self.control.path_on_server + "/" + self.control.packagename)


        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_BUILD:
            ret = oPB.RET_PEXISTS
            self.logger.ssh(20 * "-" + "ACTION: BUILD" + 20 * "-")
            if os.path.isfile(self.control.local_package_path):
                self.logger.ssh("Package already build.")
                self.logger.warning("Set return code to RET_PEXISTS")
                self.ret = ret
                self.retmsg = oPB.MsgEnum.MS_WARN
                self.retmsg = translate("OpsiProcessing", "Package has been build before. It will not be overwritten!")
            else:
                cmd = ConfigHandler.cfg.buildcommand

            result = self._processAction(cmd, action, ret)

        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_INSTALL:
            ret = oPB.RET_PINSTALL
            self.logger.ssh(20 * "-" + "ACTION: INSTALL" + 20 * "-")
            if not os.path.isfile(self.control.local_package_path):
                self.logger.ssh("Package not available: " + self.control.packagename)
                self.logger.warning("Set return code to RET_PINSTALL")
                self.ret = ret
                self.retmsg = oPB.MsgEnum.MS_ERR
                self.retmsg = translate("OpsiProcessing", "Package file could not be found!")
            else:
                if ConfigHandler.cfg.use_depot_funcs == "False":
                    cmd = ConfigHandler.cfg.installcommand + " " + self.control.packagename
                else:
                    cmd = oPB.OPB_INSTALL + " " + oPB.OPB_DEPOT_SWITCH + " " + ConfigHandler.cfg.opsi_server + " " + self.control.packagename

            result = self._processAction(cmd, action, ret)

        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_INSTSETUP:
            ret = oPB.RET_PINSTSETUP
            self.logger.ssh(20 * "-" + "ACTION: INSTALLSETUP" + 20 * "-")
            if not os.path.isfile(self.control.local_package_path):
                self.logger.ssh("Package not available.")
                self.logger.warning("Set return code to RET_PINSTALL")
                self.ret = ret
                self.retmsg = oPB.MsgEnum.MS_ERR
                self.retmsg = translate("OpsiProcessing", "Package file could not be found!")
            else:
                if ConfigHandler.cfg.use_depot_funcs == "False":
                    cmd = ConfigHandler.cfg.instsetupcommand + " " + self.control.packagename
                else:
                    cmd = oPB.OPB_INSTSETUP + " " + oPB.OPB_DEPOT_SWITCH + " " + ConfigHandler.cfg.opsi_server + " " + self.control.packagename

            result = self._processAction(cmd, action, ret)

        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_UNINSTALL:
            ret = oPB.RET_PUNINSTALL
            self.logger.ssh(20 * "-" + "ACTION: UNINSTALL" + 20 * "-")
            if ConfigHandler.cfg.use_depot_funcs == "False":
                cmd = ConfigHandler.cfg.uninstallcommand + " " + self.control.id
            else:
                cmd = oPB.OPB_UNINSTALL + " " + oPB.OPB_DEPOT_SWITCH + " " + ConfigHandler.cfg.opsi_server + " " + self.control.id

            result = self._processAction(cmd, action, ret)

        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_SETRIGHTS:
            ret = oPB.RET_SSHCMDERR
            self.logger.ssh(20 * "-" + "ACTION: SET RIGHTS" + 20 * "-")
            if ConfigHandler.cfg.age == "True":
                cmd = "opsi-set-rights '" + self.control.path_on_server + "'"
                if ConfigHandler.cfg.sudo == "True":
                    cmd = "echo '" + ConfigHandler.cfg.opsi_pass + "' | sudo -s " + cmd
                else:
                    cmd = "sudo " + cmd
            else:
                self._sshuser = "root"
                self._sshpass = ConfigHandler.cfg.root_pass
                cmd = "opsi-setup --set-rights '" + self.control.path_on_server + "'"

            result = self._processAction(cmd, action, ret)

        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_QUICKINST:
            ret = oPB.RET_PINSTALL

            package = kwargs.get("packagefile", "")

            # check if temporary install folder exists and create if not
            tmppath = "/tmp"
            destfile = str(PurePosixPath(tmppath, PurePath(package).name))

            self.logger.ssh(20 * "-" + "ACTION: QUICKINSTALL" + 20 * "-")
            # copy file to temporary location
            try:
                self.logger.ssh("Copy file: " + package + " --> " + destfile)
                self.copyToRemote(package, destfile)
            except Exception as error:
                self.logger.ssh("Could not copy file to remote destination.")
                self.logger.error(repr(error).replace("\\n"," --> "))
                self.logger.error("Set return code to RET_SSHCONNERR")
                self.ret = oPB.RET_SSHCONNERR
                self.rettype = oPB.MsgEnum.MS_ERR
                self.retmsg = translate("OpsiProcessing", "Error establishing SSH connection. See Log for details.")

            if ConfigHandler.cfg.use_depot_funcs == "False":
                cmd = ConfigHandler.cfg.installcommand + " " + destfile
            else:
                cmd = oPB.OPB_INSTALL + " " + oPB.OPB_DEPOT_SWITCH + " " + ConfigHandler.cfg.opsi_server + " " + destfile

            result = self._processAction(cmd, action, ret)

        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_UPLOAD:
            ret = oPB.RET_PUPLOAD

            package = kwargs.get("packagefile", "")

            # check if temporary install folder exists and create if not
            tmppath = "/tmp"
            destfile = str(PurePosixPath(tmppath, PurePath(package).name))

            self.logger.ssh(20 * "-" + "ACTION: UPLOAD" + 20 * "-")
            # copy file to temporary location
            try:
                self.logger.ssh("Copy file: " + package + " --> " + destfile)
                self.copyToRemote(package, destfile)
            except Exception as error:
                self.logger.ssh("Could not copy file to remote destination.")
                self.logger.error(repr(error).replace("\\n"," --> "))
                self.logger.error("Set return code to RET_SSHCONNERR")
                self.ret = oPB.RET_SSHCONNERR
                self.rettype = oPB.MsgEnum.MS_ERR
                self.retmsg = translate("OpsiProcessing", "Error establishing SSH connection. See Log for details.")

            if ConfigHandler.cfg.use_depot_funcs == "False":
                cmd = ConfigHandler.cfg.uploadcommand + " " + destfile
            else:
                cmd = oPB.OPB_UPLOAD + " " + oPB.OPB_DEPOT_SWITCH + " " + ConfigHandler.cfg.opsi_server + " " + destfile

            result = self._processAction(cmd, action, ret)

        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_GETCLIENTS:
            ret = oPB.RET_SSHCMDERR
            self.logger.ssh(20 * "-" + "ACTION: GET CLIENTS" + 20 * "-")
            cmd = "opsi-admin -r -d method host_getHashes"

            result = self._processAction(cmd, action, ret)

            result = json.loads(result)

        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_GETPRODUCTS:
            ret = oPB.RET_SSHCMDERR
            self.logger.ssh(20 * "-" + "ACTION: GET PRODUCTS" + 20 * "-")
            cmd = "opsi-admin -r -d method product_getHashes"

            result = self._processAction(cmd, action, ret)

            result = json.loads(result)

        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_QUICKUNINST:
            ret = oPB.RET_PUNINSTALL
            productlist = kwargs.get("productlist", [])

            self.logger.ssh(20 * "-" + "ACTION: QUICK UNINSTALL" + 20 * "-")
            for p in productlist:
                self.logger.sshinfo("Current selection: " + p)
                if ConfigHandler.cfg.use_depot_funcs == "False":
                    cmd = ConfigHandler.cfg.uninstallcommand + " " + p
                else:
                    cmd = oPB.OPB_UNINSTALL + " " + oPB.OPB_DEPOT_SWITCH + " " + ConfigHandler.cfg.opsi_server + " " + p

                result = self._processAction(cmd, action, ret)

        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_CREATEJOBS:
            self.logger.sshinfo("Executing action: " + str(oPB.OpEnum(action)))

            result = self._processAction(cmd, action, ret)

        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_DELETEJOBS:
            self.logger.sshinfo("Executing action: " + str(oPB.OpEnum(action)))

            result = self._processAction(cmd, action, ret)

        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_GETJOBS:
            self.logger.sshinfo("Executing action: " + str(oPB.OpEnum(action)))

            result = self._processAction(cmd, action, ret)

        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_DELETEALLATJOBS:
            self.logger.sshinfo("Executing action: " + str(oPB.OpEnum(action)))

            result = self._processAction(cmd, action, ret)

        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_GETREPOCONTENT:
            self.logger.sshinfo("Executing action: " + str(oPB.OpEnum(action)))

            result = self._processAction(cmd, action, ret)

        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_GETDEPOTS:
            self.logger.sshinfo("Executing action: " + str(oPB.OpEnum(action)))

            result = self._processAction(cmd, action, ret)

        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_GETPRODUCTSONDEPOTS:
            self.logger.sshinfo("Executing action: " + str(oPB.OpEnum(action)))

            result = self._processAction(cmd, action, ret)

        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_DELETE:
            self.logger.sshinfo("Executing action: " + str(oPB.OpEnum(action)))

            result = self._processAction(cmd, action, ret)

        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_REMOVEDEPOT:
            self.logger.sshinfo("Executing action: " + str(oPB.OpEnum(action)))

            result = self._processAction(cmd, action, ret)

        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_DEPLOY:
            self.logger.sshinfo("Executing action: " + str(oPB.OpEnum(action)))

            result = self._processAction(cmd, action, ret)

        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_SETRIGHTS_REPO:
            self.logger.sshinfo("Executing action: " + str(oPB.OpEnum(action)))

            result = self._processAction(cmd, action, ret)

        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_PRODUPDATER:
            self.logger.sshinfo("Executing action: " + str(oPB.OpEnum(action)))

            result = self._processAction(cmd, action, ret)

        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_REBOOT:
            self.logger.sshinfo("Executing action: " + str(oPB.OpEnum(action)))

            result = self._processAction(cmd, action, ret)

        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_POWEROFF:
            self.logger.sshinfo("Executing action: " + str(oPB.OpEnum(action)))

            result = self._processAction(cmd, action, ret)

        # ------------------------------------------------------------------------------------------------------------------------
        if action == oPB.OpEnum.DO_MD5:
            self.logger.sshinfo("Executing action: " + str(oPB.OpEnum(action)))

            result = self._processAction(cmd, action, ret)

        # return
        return self.ret, self.rettype, self.retmsg, result

    def _processAction(self, cmd, action, retval):
        self.logger.sshinfo("Processing action...")
        # ------------------------------------------------------------------------------------------------------------------------
        if self.ret == oPB.RET_OK:

            # hook into stderr for progress analysing
            old_stderr = sys.stderr
            s = AnalyseProgressHook(self, old_stderr)
            # sys.stdout = s

            try:
                with self.shell:
                    try:
                        self.logger.sshinfo("Trying to execute command: " + self._obscurepass(cmd))

                        if action in [oPB.OpEnum.DO_INSTALL, oPB.OpEnum.DO_QUICKINST, oPB.OpEnum.DO_INSTSETUP,
                                      oPB.OpEnum.DO_UPLOAD, oPB.OpEnum.DO_UNINSTALL, oPB.OpEnum.DO_QUICKUNINST]:
                            result = self.shell.run(cmd.split(),
                                cwd = self.control.path_on_server,
                                update_env = self._env,
                                allow_error = True,
                                stderr = s,
                                use_pty = True
                            )
                        else:
                            result = self.shell.run(cmd.split(),
                                cwd = self.control.path_on_server,
                                update_env = self._env,
                                allow_error = True,
                                stderr = s
                            )

                        # Log standard out
                        out = Helper.strip_ansi_codes(result.output.decode(encoding='UTF-8')).splitlines()
                        for line in out:
                            line = self._obscurepass(line)
                            self.logger.ssh(line)


                        # Log standard error
                        out = Helper.strip_ansi_codes(result.stderr_output.decode(encoding='UTF-8')).splitlines()
                        for line in out:
                            line = self._obscurepass(line)
                            self.logger.sshinfo(line)
                            isErr = self.hasErrors(line)
                            if isErr[0]:
                                self.ret = retval
                                self.rettype = oPB.MsgEnum.MS_ERR
                                self.retmsg = isErr[1]

                    except spur.NoSuchCommandError:
                        self.logger.error("Set return code to RET_SSHCMDERR")
                        self.ret = oPB.RET_SSHCMDERR
                        self.rettype = oPB.MsgEnum.MS_ERR
                        self.retmsg = translate("OpsiProcessing", "Command not found. See Log for details.")

            except ConnectionError as error:
                    self.logger.error(repr(error).replace("\\n"," --> "))
                    self.logger.error("Set return code to RET_SSHCONNERR")
                    self.ret = oPB.RET_SSHCONNERR
                    self.rettype = oPB.MsgEnum.MS_ERR
                    self.retmsg = translate("OpsiProcessing", "Error establishing SSH connection. See Log for details.")

            # reset hook state
            #sys.stdout = old_stderr

            return result.output.decode(encoding='UTF-8')
        else:
            return {}

    def _obscurepass(self, line):
        """
        Try to find current SSH password in string and replace it with ***SECRET***

        Works only for the first found secret at the moment!!!

        :param line: string to scan
        :return: string with password obscured
        """
        if line.find(self._sshpass) != -1:
            try:
                hide = [line.find(self._sshpass), line.find(self._sshpass) + len(self._sshpass)]
                return line[:hide[0]] + "***SECRET***" + line[hide[1]:]
            except:
                return line
        else:
            return line

    def hasErrors(self, text):
        found = False
        msg = ""
        if "ERROR: 'ascii' codec can't encode character".upper() in text.upper():
            found = True
            msg = translate("OpsiProcessing", "There are umlauts in some fields which can't be processed: build failed.")

        elif "Backend error: Failed to install package".upper() in text.upper():
            found = True
            msg = translate("OpsiProcessing", "Backend error: installation failed.")

        elif "ERROR: Failed to process command 'install'".upper() in text.upper():
            found = True
            msg = translate("OpsiProcessing", "Could not process 'install' command.")

        elif "ERROR: Package file".upper() in text.upper():
            found = True
            msg = translate("OpsiProcessing", "Package file error. Check log.")

        elif "ERROR".upper() in text.upper():
            found = True
            msg = translate("OpsiProcessing", "Undefined error occurred. Check log.")

        return (found, msg)

    def copyToRemote(self, localfile, remotefile):
        """
        Copy local file to remote destination viy SSH connection

        :param localfile: local file name
        :param remotefile: destination file name
        """
        self.logger.debug("Copying file: %s (local) to %s (remote)", localfile, remotefile)
        try:
            with open(localfile, "rb") as local_file:
                with self.shell.open(remotefile, "wb") as remote_file:
                    shutil.copyfileobj(local_file, remote_file)
        except Exception as error:
            self.logger.error("Error while copying file: " + repr(error))


    @property
    def shell(self):
        """
        Dispatch ssh shell creation depending on online status and configuration value
        :return: spue shell object
        """
        if self._shell == None:
            if self.ip.startswith("127."):
                self._shell = self._shell_local()
            elif ConfigHandler.cfg.usekeyfile == "True":
                self._shell = self._shell_remote_with_keyfile()
            else:
                self._shell = self._shell_remote_with_password()
        return self._shell

    @property
    def ip(self):
        """
        Check if server ip from configuration is the same as our local ip

        :return: server ip to use
        """

        if self._ip == None:
            local = self._get_local_ip()
            try:
                remote = socket.gethostbyname(ConfigHandler.cfg.opsi_server)
                if local == remote:
                    self._ip = '127.0.0.1'
                else:
                    self._ip = remote
            except:
                self._ip = "0.0.0.0"
        return self._ip

    def _get_local_ip(self):
        """
        Try to get local network ip address.
        :return: current ip address or "127.0.0.1"
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 0))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def _shell_remote_with_keyfile(self):
        """
        Establishing ssh shell via private keyfile authorization

        :return: spur shell object
        """
        self.logger.debug("Establishing ssh shell via private keyfile authorization")
        self.logger.debug("Server IP: " + self.ip)
        self.logger.debug("Username: " + self._sshuser)
        shell = spur.SshShell(hostname=self.ip, username=self._sshuser, private_key_file=self._sshkey, connect_timeout=15,
                              missing_host_key=spur.ssh.MissingHostKey.warn, look_for_private_keys= False)
        return shell

    def _shell_remote_with_password(self):
        """
        Establishing ssh shell via user/password authorization

        :return: spur shell object
        """
        self.logger.debug("Establishing ssh shell via user/password authorization")
        self.logger.debug("Server IP: " + self.ip)
        self.logger.debug("Username: " + self._sshuser)
        shell = spur.SshShell(hostname=self.ip, username=self._sshuser, password=self._sshpass, connect_timeout=15,
                              missing_host_key=spur.ssh.MissingHostKey.warn, look_for_private_keys= False)
        return shell

    def _shell_local(self):
        """
        Establishing local shell

        :return: spur shell object
        """
        self.logger.debug("Establishing local shell")
        shell = spur.LocalShell()
        return shell


class AnalyseProgressHook(StringIO):
    """
    Redirect hook to anaylse stderr from spur.shell.run.

    based on this idea: http://bulkan-evcimen.com/redirecting-stdout-to-stringio-object.html
    """
    def __init__(self, parent, stderr):
        self._match = re.compile('\s*(\d*\.?\d*)')
        self.__stderr = stderr
        self._parent = parent
        self._line = ""
        StringIO.__init__(self)

    # "misuse" write() to capture a whole line and analyse its content
    def write(self, s):
        try:

            # receive single bytes, concert to string and
            # concatenate them to a whole line
            if type(s) == bytes:
                s = s.decode('utf-8')
            if s == '\n':
                self._line = ""
            else:
                self._line += s

            if self._line.strip():  # strip out empty lines
                m = self._match.search(self._line)
                if m:
                    if m.group(0).strip() != "":
                        count = float(m.group(0).strip())
                        self._parent.progressChanged.emit(translate("ProgressHook", "Package building in progress:") + " " +
                                                          '\r[{0}] {1}%'.format('=' * int(count/5), count))
                        #StringIO.write(self, self._line)


        # eol throws a unicode decode error, so simply ignore it
        except UnicodeDecodeError:
            pass

    def read(self):
        self.seek(0)
        self.__stderr.write(StringIO.read(self))

