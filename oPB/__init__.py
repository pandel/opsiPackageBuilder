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
if sys.version_info[0] != 3 and sys.version_info[0] != 4:
    print("Current Python interpreter version is not supported. You need at least Python 3.4. Exiting...")
    sys.exit(1)

import os
import inspect
import tempfile
from enum import Enum
from pathlib import PurePath

try:
    from PyQt5 import QtCore
    from PyQt5.QtCore import Qt
except:
    print("PyQt5 language bindings could not be loaded. Are they installed? Existing...")
    sys.exit(1)

def get_script_dir(follow_symlinks=True):
    """Get file path of script. Take freezing into account."""
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)

"""
We have to set an environment variables to correct paths when freezing the application.
OPB_BASE   -> to correct paths to *.ui files in corresponding modules

- add base path to environement and append ui package to module search path
- necessary for uic to find resource file
"""

os.environ['OPB_BASE'] = get_script_dir()
sys.path.append(os.environ['OPB_BASE'] + "/ui")

#PRINTHIER = True
PRINTHIER = False
"""Simple printing of object hierarchie / relationship besides normal logging"""

PROGRAM_VERSION = "8.0.0"
"""Overall program version"""

NETMODE="online"
"""Current network mode, offline/online"""

NETDRV=None
"""Auto-connected drive letter"""

CONFIG_PATH = ""
"""Standard path for config file"""
if os.name == "nt":
    CONFIG_PATH = PurePath(os.environ["APPDATA"], "opsiPackageBuilder")
elif os.name == "posix":
    CONFIG_PATH = PurePath(os.environ["HOME"], ".opsiPackageBuilder")


CONFIG_INI = str(PurePath(CONFIG_PATH,"config-new.ini"))
"""Standard INI file full path"""

# base folders
DEV_BASE = "/home/opsiproducts"
REPO_PATH = "/var/lib/opsi/repository"
WIN_TMP_PATH = tempfile.gettempdir()
UNIX_TMP_PATH = "/tmp"

# some constants
OPB_GREEN = '#c4df9b' # green
OPB_YELLOW = '#fff79a' # yellow
OPB_RED = '#f6989d' # red
OPB_COLOR_ERROR = Qt.red
OPB_LOG_COLORS =  {
            "DEBUG": Qt.darkGreen,
            "INFO": Qt.black,
            "WARNING": Qt.darkYellow,
            "ERROR": Qt.darkRed,
            "CRITICAL": Qt.red,
            "SSH": Qt.darkBlue,
            "SSHINFO": Qt.blue
        }

# validator regex
OPB_PROPERTY_REGEX_NEW = "^[a-zA-Z0-9-_]{1,128}"
OPB_PROPERTY_REGEX_OLD = "^[a-zA-Z0-9-_]{1,32}"
OPB_PRODUCT_ID_REGEX_NEW = "^[a-z0-9-_\.]{1,128}$"
OPB_PRODUCT_ID_REGEX_OLD = "^[a-z0-9-_\.]{1,32}$"
OPB_PRODUCT_VER_REGEX = "^[a-z0-9\.]{1,32}$"
OPB_PACKAGE_VER_REGEX = "^[a-z0-9\.]{1,16}$"
OPB_VALID_IP_ADDRESS_REGEX = r"(?<!\S)(?:(?:\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\b|.\b){7}(?!\S)"
OPB_VALID_HOSTNAME_REGEX = "^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])(\.([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9]))*$"
"""
Host/IP regex examples:
    * www.rechner.de
    * .test.net
    * 10.2225.65.13   <- Problem! Matches as HOST :-)
    * 10.226.98.132
    * www.böse.net
"""

# basic commands
OPB_INSTALL = "opsi-package-manager -i"
"""opsi basic install command"""
OPB_INSTSETUP = "opsi-package-manager -i -S"
"""opsi basic install + setup command"""
OPB_UNINSTALL = "opsi-package-manager -r"
"""opsi basic uninstall command"""
OPB_UPLOAD = "opsi-package-manager -u"
"""opsi basic upload command"""
OPB_PROD_UPDATER = "nohup /usr/bin/opsi-product-updater -vv 1>/dev/null 2>&1 </dev/null &" # must be started with nohup
"""product updater command"""
OPB_DEPLOY_COMMAND = "/var/lib/opsi/depot/opsi-client-agent/opsi-deploy-client-agent"
"""opsi client agent deploy command"""
OPB_DEPOT_SWITCH = "-d"
"""opsi command line switch for depot operations"""
OPB_METHOD_ONDEMAND = "opsi-admin -d method hostControl_fireEvent 'on_demand'"
"""opsi 4.0 API method: on demand"""
OPB_METHOD_PRODUCTACTION = "opsi-admin -d method setProductActionRequestWithDependencies"
"""opsi 4.0 API method: product installation"""
OPB_METHOD_WOL = "opsi-admin -d method powerOnHost"
"""opsi 4.0 API method: wake on lan"""
OPB_METHOD_GETDEPOTS = "opsi-admin -d method host_getHashes '[]' '{" + '"type":"OpsiDepotserver"}' + "'"
"""opsi 4.0 API method: get depot server list"""
OPB_METHOD_GETPRODUCTS = "opsi-admin -r -d method product_getHashes"
"""opsi 4.0 API method: short / get all products"""
OPB_METHOD_GETCLIENTS = "opsi-admin -d method host_getHashes '[]' '{" + '"type":"OpsiClient"}' + "'"
"""opsi 4.0 API method: get client list"""
OPB_METHOD_GETCLIENTSONDEPOTS = "opsi-admin -d method configState_getClientToDepotserver" # filter with added: '["***REMOVED***1hp.sd8106.***REMOVED***"]'
"""opsi 4.0 API method: get client<->depot list, filter with added: '["<hostname>"]' """
OPB_METHOD_GETPRODUCTSONDEPOTS = "opsi-admin -d method productOnDepot_getIdents"
"""opsi 4.0 API method: long / get all products"""
OPB_METHOD_UNREGISTERDEPOT = "opsi-admin -d method host_delete"
"""opsi 4.0 API method: unregister depot server host"""
OPB_SETRIGHTS_NOSUDO = "opsi-setup --set-rights"
"""opsi set rights without sudo command"""
OPB_SETRIGHTS_SUDO = "opsi-set-rights"
"""opsi set rights with sudo command"""
OPB_GETPRODUPD_PID = "VAR=$(pidof -x opsi-product-updater); echo $VAR"
"""get pid of running opsi-product-updater"""

# additional commands
OPB_AT_QUEUE = "atq -q D"
"""AT command: get content of queue 'D'"""
OPB_AT_JOB_DETAIL = "atq -q D | cut -f1 | xargs at -q D -c | grep opsi-admin"
"""AT command: get job details for queue 'D' and user opsi-admin"""
OPB_AT_CREATE = "at -q D -t"
"""AT command: create AT job"""
OPB_AT_REMOVE = "atrm"
"""AT command: remove single AT job"""
OPB_AT_REMOVE_ALL = "atrm $(atq -q D | cut -f 1)"
"""AT command: remove all AT jobs at once"""
OPB_PRECHECK_MD5 = "md5deep -h"
"""md5deep command accessibility check"""
OPB_PRECHECK_WINEXE = "winexe --help"
"""winexe command accessibility check"""
OPB_CALC_MD5 = 'PACKETPATH="' + REPO_PATH + '"; for p in $PACKETS; do MD5=\"`md5deep $PACKETPATH/$p.opsi 2>/dev/null | cut -d \" \" -f 1`\"; echo -n $MD5 >$PACKETPATH/$p.opsi.md5; done'
"""Create MD5 file for packet; add in front: 'PACKETS=\"xca_0.9.3-1.opsi\";'"""
OPB_GETREPOCONTENT = 'PACKETPATH="' + REPO_PATH + '"; PACKETS=\"`ls $PACKETPATH/*.opsi 2>/dev/null | cut -d "/" -f 6`\"; ' \
                       'for p in $PACKETS; do MD5=\"`cat $PACKETPATH/$p.md5 2>/dev/null`\"; echo $MD5-@MD5@-$p; done'
"""Get all products from repository directory incl. MD5"""
OPB_DEPOT_FILE_REMOVE = 'PACKETPATH="' + REPO_PATH + '"; for p in $PACKETS; do ' \
                            'rm -v -f $PACKETPATH/$p.opsi; rm -v -f $PACKETPATH/$p.opsi.md5; rm -v -f $PACKETPATH/$p.opsi.zsync; done'
"""Remove files from repository; add in front: 'PACKETS=\"xca_0.9.3-1\";'"""
OPB_REBOOT = "shutdown -r now"
"""Reboot machine command"""
OPB_POWEROFF = "shutdown -h now"
"""Poweroff machine command"""
OPB_WINST_NT = "C:\\Program Files (x86)\\opsi.org\\opsi-client-agent\\opsi-winst\\winst32.exe"
"""winst32.exe path on windows client"""
OPB_WINST_LINUX = ""
"""winst32 path on linux client"""

# file extensions for selection dialogs
SCRIPT_EXT = ["opsiscript", "opsiinc", "ins", "py", "*"]
"""opsi script file extensions"""
KEYFILE_EXT = ["ppk"]
"""SSH keyfile extension"""
PRG_EXT = ["exe"]
"""Program executable extension (Windows)"""

# log formats
LOG_DATETIME = "%Y-%m-%d %I:%M:%S %p"
"""Log entry: datetime format"""
LOG_LONG =  "[%(asctime)s] - %(name)-35s - %(levelname)8s - %(message)s (%(module)s: %(funcName)s - line %(lineno)s, process %(process)s)"
"""Log entry: long format"""
LOG_SHORT = "[%(asctime)s] - %(name)-35s - %(levelname)8s - %(message)s"
"""Log entry: short format"""
LOG_SSH = "[%(asctime)s] - %(message)s"
"""Log entry (only SSH): format"""

PRODTYPES = ["localboot", "netboot"]
"""opsi product types"""

CHLOG_BLOCKMARKER = "urgency="
"""Changelog block marker"""
CHLOG_URGENCIES = ["low", "middle", "high"]
"""Changelog urgencies"""
CHLOG_STATI = ["stable", "testing"]
"""Changelog status"""

BASE_FOLDERS = ["OPSI", "CLIENT_DATA"]
"""Base folders inside project directory"""

MsgEnum = Enum("MsgEnum", "MS_ERR MS_WARN MS_INFO MS_STAT MS_ALWAYS MS_PARSE MS_QUEST_YESNO MS_QUEST_CTC MS_QUEST_OKCANCEL "
                          "MS_QUEST_PHRASE MS_QUEST_PASS MS_QUEST_DEPOT")
"""Constants for _msg() - message type"""

UpdEnum = Enum("UpdEnum", "UP_MANU UP_AUTO")
"""Constants for _updater()"""

BModEnum = Enum("BModEnum", "BD_CANCEL BD_REBUILD BD_NEW BD_INTERACTIVE")
"""Command line build modes"""

OpEnum = Enum("OpEnum", "DO_BUILD DO_INSTALL DO_UNINSTALL DO_SETRIGHTS DO_GETCLIENTS DO_GETPRODUCTS DO_CREATEJOBS DO_DELETEJOBS DO_GETATJOBS "
                        "DO_DELETEALLJOBS DO_GETREPOCONTENT DO_GETDEPOTS DO_GETPRODUCTSONDEPOTS DO_QUICKINST DO_QUICKUNINST DO_INSTSETUP DO_UPLOAD "
                        "DO_DELETEFILEFROMREPO DO_UNREGISTERDEPOT DO_DEPLOY DO_SETRIGHTS_REPO DO_PRODUPDATER DO_REBOOT DO_POWEROFF DO_GENMD5 DO_GETCLIENTSONDEPOTS")
"""Constants for opsi operations"""

# return codes
RET_OK = 0            # Err  0: OK
RET_EOPEN = 10        # Err 10: Can't open project
RET_BCANCEL = 20      # Err 20: Package file already exists, build canceled automatically
RET_BFILEDEL = 21     # Err 21: Package could not be deleted before re-building
RET_BSAVE = 22        # Err 22: Package could not be saved before building
RET_BUNDEF = 23       # Err 23: Undefined error in build routine

RET_SSHCONNERR = 25   # Err 25: Can't establish SSH connection
RET_SSHCMDERR = 26    # Err 26: Error during command execution via SSH
RET_PEXISTS = 30      # Err 30: SSH - Package exists already
RET_PBUILD = 31       # Err 31: SSH - Error while building package on server
RET_PINSTALL = 32     # Err 32: SSH - Error while installing package on server
RET_PINSTSETUP = 33   # Err 33: SSH - Error while installing package on server or activating for setup
RET_PUNINSTALL = 34   # Err 34: SSH - Error while uninstalling package on server
RET_PUPLOAD = 35   # Err 34: SSH - Error while uploading package on server

RET_SINGLETON = 51    # Err 51: Program already running
RET_NOINI = 52        # Err 52: No INI file available
RET_QICOMB = 53       # Err 53: Mode incompatibility: --quiet and interactive mode combined on command line
RET_CMDLINE = 54      # Err 54: Incorrect commandline parameters
RET_NOWINEXE = 57     # Err 57: Winexe not found
RET_PRODUPDRUN = 58   # Err 58: opsi-product-updater already running
RET_NOREPO = 59       # Err 59: could not get repo content

EXITCODE = RET_OK
"""Standard program exitcode"""

# Help destinations
HLP_LANG_DST = "de"
HLP_FILE = get_script_dir() + "/help/opsipackagebuilder.qhc"
HLP_PREFIX = "qthelp://org.sphinx.opsipackagebuilder.8.0/doc/"
HLP_DST_INDEX = "index.html"
HLP_DST_TABPACKET = HLP_LANG_DST + "/tabpacket.html"
HLP_DST_TABDEPEND = HLP_LANG_DST + "/tabdepend.html"
HLP_DST_TABPROP = HLP_LANG_DST + "/tabprop.html"
HLP_DST_BUNDLE = HLP_LANG_DST + "/bundle.html"
HLP_DST_CHLOGEXT = HLP_LANG_DST + "/chlog_extended.html"
HLP_DST_CHLOGSIMPLE = HLP_LANG_DST + "/chlog_simple.html"
HLP_DST_DEPLOY = HLP_LANG_DST + "/deployclientagent.html"
HLP_DST_DEPOTM = HLP_LANG_DST + "/depotmanager.html"
HLP_DST_QUNINST = HLP_LANG_DST + "/start.html"
HLP_DST_JOBCREATOR = HLP_LANG_DST + "/scheduler.html#auftrage-anlegen"
HLP_DST_JOBLIST = HLP_LANG_DST + "/scheduler.html"
HLP_DST_SETTINGS = HLP_LANG_DST + "/settings.html"
