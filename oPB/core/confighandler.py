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
import logging
import json
from distutils.version import LooseVersion
from configparser import ConfigParser, NoOptionError
from PyQt5 import QtCore
import oPB
from oPB.core.tools import Helper, LogMixin

translate = QtCore.QCoreApplication.translate

logger = logging.getLogger(__name__)

class ConfigHandler(ConfigParser, LogMixin):
    """
    Handler for configuration file
    """

    _initial_settings = {
        "version": {
            "ini": oPB.PROGRAM_VERSION,
            "firstrun": "True"
        },
        "server": {
            "name": "server.local.net",
            "user": "opsiadmin",
            "pass": "",
            "rootpw": "",
            "age": "True",
            "sudo": "False",
            "usenetdrive": "False",
            "sshport": "22",
            "usekeyfile": "False",
            "keyfilename": "",
            "is_opsi41": "True",
            "wb_new": "True"
    },
        "maintainer": {
            "name": "Package Maintainer",
            "email": "maintainer@server.local.net",
        },
        "package": {
            "dev_dir": "",
            "local_share_base": "/mnt/opsi_dev_share",
            "build": "opsi-makepackage -v --no-md5 --no-zsync",
            "install": "opsi-package-manager -i",
            "instsetup": "opsi-package-manager -i -S",
            "uninstall": "opsi-package-manager -r",
            "upload": "opsi-package-manager -u",
            "showplink": "True",
            "reloadforat": "False",
            "wolleadtime": "15",
            "usedepotfuncs": "False",
            "depotCache": "",
        },
        "tools": {
            "extchlog": "True",
            "scripteditor": "C:/Program Files (x86)/opsi PackageBuilderNG/ScriptEditor.exe",
            "editoroptions": "-x=opsi -s --path=",
            "attachdirect": "True",
            "editintern": "False",
            "editstyle": "True",
            "editfold": "False",
            "chLogRecognition": oPB.CHLOG_BLOCKMARKER,
            "chLogOnBuild": "False",
            "chLogOnSave": "False",
            "predeploycmds": ""
        },
        "messages": {
            "noError": "False",
            "noWarning": "False",
            "noInfo": "False",
            "noATWarn": "False",
        },
        "language": {
            "lang": "System",
        },
        "log": {
            "logalways": "False",
            "logfile": "opb-session.log",
            "loglevel": "INFO",
        },
        "inet": {
            "useproxy": "False",
            "chkupdstartup": "False",
            "srv": "",
            "port": "",
            "user": "",
            "pass": "",
        },
        "window": {
            "posX": "0",
            "posY": "0",
            "width": "745",
            "height": "650",
            "recentfiles": ""
        }
    }

    cfg = None  # class variable to save ConfigHandler instance for later access

    def __init__(self, configfile, nodefaults = False):
        """
        Reads settings from INI file, compares with setup defaults,
        adds missing settings

        :param configfile: path and name of INI file
        :param nodefaults: if true, no defaults are written to the INI file,
                    also, if INI is missing, none will be created
        """

        # parse settings ONLY for first time initialization of
        # configuration object, never read twice unnecessary
        if ConfigHandler.cfg is None:
            ConfigParser.__init__(self, interpolation=None)

            self.configfile = configfile
            self.nodefaults = nodefaults

            # read settings
            self.logger.debug("Trying to read configuration file: " + self.configfile)
            try:
                with open(self.configfile) as file:
                    self.read_file(file)
                    self.logger.info("Configuration file successfully loaded.")
            except IOError:
                self.logger.error("Configuration file could not be loaded.")

            # apply new/missing defaults
            if not self.nodefaults:
                for section, options in self._initial_settings.items():
                    if not self.has_section(section):
                        self.add_section(section)
                    for option, value in options.items():
                        if not self.has_option(section, option):
                            self.set(section, option, str(value))

            # check if INI pre-python
            if LooseVersion(self.prg_version) < "8.0.0":
                self.convert_old_format()

            if LooseVersion(self.prg_version) < "8.2.5":
                self.convert_to_opsi41()

            # check current version to version in INI file
            if LooseVersion(self.get("version", "ini")) < oPB.PROGRAM_VERSION:
                self.logger.debug("Old version: " + self.prg_version)
                self.logger.debug("Current version: " + oPB.PROGRAM_VERSION)
                self.prg_version = oPB.PROGRAM_VERSION

            # get usable passwords, if there are any
            self.passwords('decrypt')

            # after all, save parser in class variabel
            ConfigHandler.cfg = self

    def log_config(self):
        """Dump config to logfile"""
        self.logger.debug("Current configuration values:")
        self.passwords('encrypt')
        for sect in self.sections():
            self.logger.debug("[" + sect + "]")
            for opt in self.options(sect):
                self.logger.debug("\t" + opt + " = " + self.get(sect, opt))
        self.passwords('decrypt')


    def passwords(self, mode):
        """
        (De-)obfuscate passwords

        :param mode: possible values "encrypt", "decrypt"
        """

        func = Helper.encrypt if mode == 'encrypt' else Helper.decrypt

        if self.opsi_pass.strip() != "":
            self.opsi_pass = func(self.opsi_pass)
        if self.root_pass.strip() != "":
            self.root_pass = func(self.root_pass)
        if self.proxy_pass.strip() != "":
            self.proxy_pass = func(self.proxy_pass)

    def save(self):
        """Write INI file"""
        self.passwords('encrypt')
        try:
            os.makedirs(os.path.dirname(self.configfile), exist_ok=True)
            with open(self.configfile, "w") as file:
                self.write(file)
                file.close()
                self.logger.debug("Configuration successfully saved: " + self.configfile)
        except IOError as error:
            self.logger.error("Configuration could not be saved: " + self.configfile)
            self.logger.error(error.name)
        finally:
            self.passwords('decrypt')

    def convert_old_format(self):
        """
        Convert old INI format
        """
        self.logger.debug("Convert old config.ini format...")
        self.usenetdrive = "False" if self.usenetdrive == "4" else "True"
        self.age = "False" if self.age == "0" else "True"
        self.sudo = "False" if self.sudo == "0" else "True"
        self.usekeyfile = "False" if self.usekeyfile == "0" else "True"

        self.showoutput = "False" if self.showoutput == "0" else "True"
        self.reload_for_at = "False" if self.reload_for_at == "0" else "True"
        self.use_depot_funcs = "False" if self.use_depot_funcs == "0" else "True"

        self.use_extended_changelog = "False" if self.use_extended_changelog == "0" else "True"
        self.editor_intern = "False" if self.editor_intern == "0" else "True"
        self.editor_use_styling = "False" if self.editor_use_styling == "0" else "True"
        self.editor_use_folding = "False" if self.editor_use_folding == "0" else "True"

        try:
            a = int(self.sshport)
        except ValueError:
            self.sshport = "22"

        # reset changelog block reconition / individual not needed at the moment
        self.chlog_block_marker = oPB.CHLOG_BLOCKMARKER

        # if internal editor was used before, let's hope for existence of an old standard installation
        # and set parameters accordingly
        if self.editor_intern == "True":
            self.editor_intern = "False"
            self.scripteditor = "C:\\Program Files (x86)\\opsi PackageBuilder\\ScriptEditor.exe"
            self.editor_options = "-x=opsi -s --path="
            self.editor_attachdirect = "True"

        self.chlog_on_build = "False" if self.chlog_on_build == "0" else "True"
        self.chlog_on_save = "False" if self.chlog_on_save == "0" else "True"

        self.no_error_msg = "False" if self.no_error_msg == "0" else "True"
        self.no_warning_msg = "False" if self.no_warning_msg == "0" else "True"
        self.no_info_msg = "False" if self.no_info_msg == "0" else "True"
        self.no_at_warning_msg = "False" if self.no_at_warning_msg == "0" else "True"

        self.language = "de" if self.language == "Deutsch" else "en"

        self.useproxy = "False" if self.useproxy == "0" else "True"
        self.updatecheck = "False" if self.updatecheck == "0" else "True"

        # remove unneeded options
        self.remove_option("recent", "rec0")
        self.remove_option("recent", "rec1")
        self.remove_option("recent", "rec2")
        self.remove_option("recent", "rec3")
        self.remove_option("recent", "rec4")
        self.remove_option("language", "path")
        self.remove_option("package", "noutf8check")
        self.remove_option("package", "depotcache")  # inititates one time reading of all depots

        # reset passwords due to changed obfuscating method
        self.opsi_pass = ""
        self.root_pass = ""
        self.proxy_pass = ""

        self.save()

    def convert_to_opsi41(self):
        """Add additional parameter for opsi 4.1 Support"""
        self.logger.debug("Upgrade config-new.ini to 8.2.5...")

        # self.wb_new = "True" if self.get("server", "is_sles") == "True" else "False"
        try:
            self.wb_new = "True" if self.get("server", "is_sles") == "True" else "False"
            self.remove_option("server", "is_sles")
        except NoOptionError:
            self.wb_new = "True"

        self.is_opsi41 = "False"
        self.save()

    @property
    def prg_version(self):
        return self.get("version", "ini")

    @prg_version.setter
    def prg_version(self, value):
        self.set("version", "ini", value)

    @property
    def firstrun(self):
        return self.get("version", "firstrun")

    @firstrun.setter
    def firstrun(self, value):
        self.set("version", "firstrun", value)

    @property
    def opsi_server(self):
        return self.get("server", "name")

    @opsi_server.setter
    def opsi_server(self, value):
        self.set("server", "name", value)

    @property
    def opsi_user(self):
        return self.get("server", "user")

    @opsi_user.setter
    def opsi_user(self, value):
        self.set("server", "user", value)

    @property
    def opsi_pass(self):
        return self.get("server", "pass")

    @opsi_pass.setter
    def opsi_pass(self, value):
        self.set("server", "pass", value)

    @property
    def root_pass(self):
        return self.get("server", "rootpw")

    @root_pass.setter
    def root_pass(self, value):
        self.set("server", "rootpw", value)

    @property
    def age(self):
        return self.get("server", "age")

    @age.setter
    def age(self, value):
        self.set("server", "age", value)

    @property
    def sudo(self):
        return self.get("server", "sudo")

    @sudo.setter
    def sudo(self, value):
        self.set("server", "sudo", value)

    @property
    def usenetdrive(self):
        return self.get("server", "usenetdrive")

    @usenetdrive.setter
    def usenetdrive(self, value):
        self.set("server", "usenetdrive", value)

    @property
    def sshport(self):
        return self.get("server", "sshport")

    @sshport.setter
    def sshport(self, value):
        self.set("server", "sshport", value)

    @property
    def usekeyfile(self):
        return self.get("server", "usekeyfile")

    @usekeyfile.setter
    def usekeyfile(self, value):
        self.set("server", "usekeyfile", value)

    @property
    def keyfilename(self):
        return self.get("server", "keyfilename")

    @keyfilename.setter
    def keyfilename(self, value):
        self.set("server", "keyfilename", value)

    @property
    def is_opsi41(self):
        return self.get("server", "is_opsi41")

    @is_opsi41.setter
    def is_opsi41(self, value):
        if value == "True":
            com: str = self.buildcommand
            self.buildcommand = com.replace(oPB.OPB_BUILD40, oPB.OPB_BUILD41)
        else:
            com: str = self.buildcommand
            com = com.replace(oPB.OPB_BUILD41, oPB.OPB_BUILD40)
            com = com.replace("--no-md5", "")
            com = com.replace("--no-zsync", "")
            self.buildcommand = com.replace(oPB.OPB_BUILD41, oPB.OPB_BUILD40)

        self.set("server", "is_opsi41", value)

    @property
    def wb_new(self):
        return self.get("server", "wb_new")

    @wb_new.setter
    def wb_new(self, value):
        self.set("server", "wb_new", value)

    @property
    def packagemaintainer(self):
        return self.get("maintainer", "name")

    @packagemaintainer.setter
    def packagemaintainer(self, value):
        self.set("maintainer", "name", value)

    @property
    def mailaddress(self):
        return self.get("maintainer", "email")

    @mailaddress.setter
    def mailaddress(self, value):
        self.set("maintainer", "email", value)

    @property
    def dev_dir(self):
        return self.get("package", "dev_dir")

    @dev_dir.setter
    def dev_dir(self, value):
        if value[-2] != ":":
            if value[-1:] == "/" or value[-1:] == '\\':
                value = value[:-1]
        self.set("package", "dev_dir", value)

    @property
    def local_share_base(self):
        return self.get("package", "local_share_base")

    @local_share_base.setter
    def local_share_base(self, value):
        if value[-2] != ":":
            if value[-1:] == "/" or value[-1:] == '\\':
                value = value[:-1]
        self.set("package", "local_share_base", value)

    @property
    def buildcommand(self):
        return self.get("package", "build")

    @buildcommand.setter
    def buildcommand(self, value):
        self.set("package", "build", value)

    @property
    def installcommand(self):
        return self.get("package", "install")

    @installcommand.setter
    def installcommand(self, value):
        self.set("package", "install", value)

    @property
    def instsetupcommand(self):
        return self.get("package", "instsetup")

    @instsetupcommand.setter
    def instsetupcommand(self, value):
        self.set("package", "instsetup", value)

    @property
    def uninstallcommand(self):
        return self.get("package", "uninstall")

    @uninstallcommand.setter
    def uninstallcommand(self, value):
        self.set("package", "uninstall", value)

    @property
    def uploadcommand(self):
        return self.get("package", "upload")

    @uploadcommand.setter
    def uploadcommand(self, value):
        self.set("package", "upload", value)

    @property
    def showoutput(self):
        return self.get("package", "showplink")

    @showoutput.setter
    def showoutput(self, value):
        self.set("package", "showplink", value)

    @property
    def reload_for_at(self):
        return self.get("package", "reloadforat")

    @reload_for_at.setter
    def reload_for_at(self, value):
        self.set("package", "reloadforat", value)

    @property
    def wol_lead_time(self):
        return self.get("package", "wolleadtime")

    @wol_lead_time.setter
    def wol_lead_time(self, value):
        self.set("package", "wolleadtime", value)

    @property
    def use_depot_funcs(self):
        return self.get("package", "usedepotfuncs")

    @use_depot_funcs.setter
    def use_depot_funcs(self, value):
        if value == "False":
            self.depotcache = ""
        self.set("package", "usedepotfuncs", value)

    @property
    def use_extended_changelog(self):
        return self.get("tools", "extchlog")

    @use_extended_changelog.setter
    def use_extended_changelog(self, value):
        self.set("tools", "extchlog", value)

    @property
    def scripteditor(self):
        return self.get("tools", "scripteditor")

    @scripteditor.setter
    def scripteditor(self, value):
        self.set("tools", "scripteditor", value)

    @property
    def editor_intern(self):
        return self.get("tools", "editintern")

    @editor_intern.setter
    def editor_intern(self, value):
        self.set("tools", "editintern", value)

    @property
    def editor_use_styling(self):
        return self.get("tools", "editstyle")

    @editor_use_styling.setter
    def editor_use_styling(self, value):
        self.set("tools", "editstyle", value)

    @property
    def editor_use_folding(self):
        return self.get("tools", "editfold")

    @editor_use_folding.setter
    def editor_use_folding(self, value):
        self.set("tools", "editfold", value)

    @property
    def editor_attachdirect(self):
        return self.get("tools", "attachdirect")

    @editor_attachdirect.setter
    def editor_attachdirect(self, value):
        self.set("tools", "attachdirect", value)

    @property
    def editor_options(self):
        return self.get("tools", "editoroptions")

    @editor_options.setter
    def editor_options(self, value):
        self.set("tools", "editoroptions", value)

    @property
    def chlog_block_marker(self):
        return self.get("tools", "chLogRecognition")

    @chlog_block_marker.setter
    def chlog_block_marker(self, value):
        self.set("tools", "chLogRecognition", value)

    @property
    def chlog_on_build(self):
        return self.get("tools", "chLogOnBuild")

    @chlog_on_build.setter
    def chlog_on_build(self, value):
        self.set("tools", "chLogOnBuild", value)

    @property
    def chlog_on_save(self):
        return self.get("tools", "chLogOnSave")

    @chlog_on_save.setter
    def chlog_on_save(self, value):
        self.set("tools", "chLogOnSave", value)

    @property
    def no_error_msg(self):
        return self.get("messages", "noError")

    @no_error_msg.setter
    def no_error_msg(self, value):
        self.set("messages", "noError", value)

    @property
    def no_warning_msg(self):
        return self.get("messages", "noWarning")

    @no_warning_msg.setter
    def no_warning_msg(self, value):
        self.set("messages", "noWarning", value)

    @property
    def no_info_msg(self):
        return self.get("messages", "noInfo")

    @no_info_msg.setter
    def no_info_msg(self, value):
        self.set("messages", "noInfo", value)

    @property
    def no_at_warning_msg(self):
        return self.get("messages", "noATWarn")

    @no_at_warning_msg.setter
    def no_at_warning_msg(self, value):
        self.set("messages", "noATWarn", value)

    @property
    def language(self):
        return self.get("language", "lang")

    @language.setter
    def language(self, value):
        self.set("language", "lang", value)

    @property
    def useproxy(self):
        return self.get("inet", "useproxy")

    @useproxy.setter
    def useproxy(self, value):
        self.set("inet", "useproxy", value)

    @property
    def updatecheck(self):
        return self.get("inet", "chkupdstartup")

    @updatecheck.setter
    def updatecheck(self, value):
        self.set("inet", "chkupdstartup", value)

    @property
    def proxy_server(self):
        return self.get("inet", "srv")

    @proxy_server.setter
    def proxy_server(self, value):
        self.set("inet", "srv", value)

    @property
    def proxy_port(self):
        return self.get("inet", "port")

    @proxy_port.setter
    def proxy_port(self, value):
        self.set("inet", "port", value)

    @property
    def proxy_user(self):
        return self.get("inet", "user")

    @proxy_user.setter
    def proxy_user(self, value):
        self.set("inet", "user", value)

    @property
    def proxy_pass(self):
        return self.get("inet", "pass")

    @proxy_pass.setter
    def proxy_pass(self, value):
        self.set("inet", "pass", value)

    @property
    def log_always(self):
        return self.get("log", "logalways")

    @log_always.setter
    def log_always(self, value):
        self.set("log", "logalways", value)

    @property
    def log_file(self):
        return self.get("log", "logfile")

    @log_file.setter
    def log_file(self, value):
        self.set("log", "logfile", value)

    @property
    def log_level(self):
        return self.get("log", "loglevel")

    @log_level.setter
    def log_level(self, value):
        self.set("log", "loglevel", value)

    @property
    def posX(self):
        return int(self.get("window", "posX"))

    @posX.setter
    def posX(self, value):
        self.set("window", "posX", str(value))

    @property
    def posY(self):
        return int(self.get("window", "posY"))

    @posY.setter
    def posY(self, value):
        self.set("window", "posY", str(value))

    @property
    def width(self):
        return int(self.get("window", "width"))

    @width.setter
    def width(self, value):
        self.set("window", "width", str(value))

    @property
    def height(self):
        return int(self.get("window", "height"))

    @height.setter
    def height(self, value):
        self.set("window", "height", str(value))

    @property
    def recent(self):
        val = str(self.get("window", "recentfiles"))
        if val.strip() == "":
            return []
        else:
            return [x for x in val.split(";") if x]

    @recent.setter
    def recent(self, value):
        self.set("window", "recentfiles", (";").join(value))

    @property
    def depotcache(self):
        val = self.get("package", "depotcache")
        if val.strip() == "":
            return {}
        else:
            return json.loads(val)

    @depotcache.setter
    def depotcache(self, value):
        if value == "":
            self.set("package", "depotCache", "")
        else:
            self.set("package", "depotCache", json.dumps(value))

    @property
    def predeploycmds(self):
        val = self.get("tools", "predeploycmds")
        if val.strip() == "":
            return {}
        else:
            return json.loads(val)

    @predeploycmds.setter
    def predeploycmds(self, value):
        if value == "":
            self.set("tools", "predeploycmds", "")
        else:
            self.set("tools", "predeploycmds", json.dumps(value))
