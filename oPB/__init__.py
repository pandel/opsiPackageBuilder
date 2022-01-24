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

if sys.version_info.major != 3 and sys.version_info.minor < 4:
    print("Current Python interpreter version is not supported. You need at least Python 3.4. Exiting...")
    print("Installed Version: " + sys.version_info.major + "." + sys.version_info.major)
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

if int(QtCore.qVersion().split('.')[0]) < 5 or int(QtCore.qVersion().split('.')[1]) < 6:
    print("This version of PyQt5 ist not supported! Please upgrade to a PyQt5 version based on Qt 5.6 or newer!")
    print("Current Qt version: " + QtCore.qVersion())
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

PROGRAM_VERSION = "8.5.0"
"""Overall program version"""

UPDATER_URL="https://s3.eu-central-1.amazonaws.com/opsipackagebuilder/opsiPackageBuilder"
"""Updater base URL"""

NETMODE="online"
"""Current network mode, offline/online"""

NETDRV=None
"""Auto-connected drive letter"""

APP_ICON=None

CONFIG_PATH = ""
"""Standard path for config file"""
if os.name == "nt":
    CONFIG_PATH = PurePath(os.environ["APPDATA"], "opsiPackageBuilder")
elif os.name == "posix":
    CONFIG_PATH = PurePath(os.environ["HOME"], ".opsiPackageBuilder")


CONFIG_INI = str(PurePath(CONFIG_PATH,"config-new.ini"))
"""Standard INI file full path"""

# base folders
DEV_BASE_OPSI40 = "/home/opsiproducts"
"""Development base folder under most os"""
DEV_BASE_OPSI41 = "/var/lib/opsi/workbench"
"""Development base folder under SLES"""
DEV_BASE = DEV_BASE_OPSI41
REPO_PATH = "/var/lib/opsi/repository"
"""Standard repository folder"""
DEPOTSHARE_BASE = "opsi_depot"
"""Standard share name for depot"""

# temp folders
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
OPB_BUILD40 = "opsi-makeproductfile -v"
"""opsi 4.0 package creation command"""
OPB_BUILD41 = "opsi-makepackage -v --no-md5 --no-zsync"
"""opsi 4.1 package creation command"""
OPB_INSTALL = "opsi-package-manager -v -i"
"""opsi basic install command"""
OPB_INSTSETUP = "opsi-package-manager -v -i -S"
"""opsi basic install + setup command"""
OPB_UNINSTALL = "opsi-package-manager -v -r"
"""opsi basic uninstall command"""
OPB_UPLOAD = "opsi-package-manager -v -u"
"""opsi basic upload command"""
OPB_EXTRACT = "opsi-package-manager -v -x"
"""opsi package extract command"""
OPB_PROD_UPDATER_40 = "nohup /usr/bin/opsi-product-updater -vv 1>/dev/null 2>&1 </dev/null &"  # must be started with nohup
"""opsi 4.0 product updater command"""
OPB_PROD_UPDATER_41 = "nohup /usr/bin/opsi-package-updater update &"  # must be started with nohup
"""opsi 4.1 package updater command"""
OPB_PROD_UPDATER = OPB_PROD_UPDATER_40
"""used product updater command"""
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
OPB_METHOD_GETCLIENTSONDEPOTS = "opsi-admin -d method configState_getClientToDepotserver" # filter with added: '["host.domain.de"]'
"""opsi 4.0 API method: get client<->depot list, filter with added: '["<hostname>"]' """
OPB_METHOD_GETPRODUCTSONDEPOTS = "opsi-admin -d method productOnDepot_getIdents"
"""opsi 4.0 API method: long / get all products"""
OPB_METHOD_UNREGISTERDEPOT = "opsi-admin -d method host_delete"
"""opsi 4.0 API method: unregister depot server host"""
OPB_METHOD_GETLOCKEDPRODUCTS = "opsi-admin -d method  productOnDepot_getObjects '[]'" # filter for all with added: '{"depotId":"host.domain.de", "locked":true}' /  # filter for single with added: '{"depotId":"host.domain.de", "productId":"testdummy"}'
"""opsi 4.0 API method: get locked products on depot"""
# full command like so: opsi-admin -d method  productOnDepot_getObjects
# '[]' '{"depotId":"host.domain.de", "locked":true}'
OPB_METHOD_UNLOCKPRODUCTS = " | sed  -e 's/\"locked\": true/\"locked\": false/' > /tmp/update_objects.json"
# full  method: opsi-admin -d method productOnDepot_getObjects '[]'
# '{"productId":"opsi-smartmontools", "depotId":"yi7xa19z.sd8106.gad.de"}'
#  | sed  -e 's/\"locked\": true/\"locked\": false/' > /tmp/update_objects.json
"""opsi 4.0 API method: unlock specified product"""
OPB_METHOD_UPDATEOBJECTS = "opsi-admin -d method productOnDepot_updateObjects < /tmp/update_objects.json"
"""opsi 4.0 API method: update object(s) properties via json import"""
OPB_METHOD_GETGROUPS = "opsi-admin -r -d method group_getHashes"
"""opsi 4.0 API method: get group tree"""
OPB_METHOD_GETCLIENTGROUPS = "opsi-admin -r -d method objectToGroup_getHashes '[]' '{" + '"groupType":"HostGroup"}' + "'"
"""opsi 4.0 API method: get client <-> group association"""
OPB_SETRIGHTS_NOSUDO = "opsi-setup --set-rights"
"""opsi set rights without sudo command"""
OPB_SETRIGHTS_SUDO = "opsi-set-rights"
"""opsi set rights with sudo command"""
OPB_GETPRODUPD40_PID = "VAR=$(ps -elf | grep opsi-product-updater | grep -v grep | awk '{print $4}'); echo $VAR"
"""get pid of running opsi-product-updater"""
OPB_GETPRODUPD41_PID = "VAR=$(ps -elf | grep opsi-package-updater | grep -v grep | awk '{print $4}'); echo $VAR"
"""get pid of running opsi-package-updater"""
OPB_GETPRODUPD_PID = OPB_GETPRODUPD40_PID
"""get pid of currently used opsi package updating command"""

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
OPB_PRECHECK_MD5 = "md5sum -h"
"""md5deep command accessibility check"""
OPB_PRECHECK_WINEXE = "winexe --help"
"""winexe command accessibility check"""
OPB_CALC_MD5 = 'PACKETPATH="' + REPO_PATH + '"; for p in $PACKETS; do MD5=\"`md5sum $PACKETPATH/$p.opsi 2>/dev/null | cut -d \" \" -f 1`\"; echo -n $MD5 >$PACKETPATH/$p.opsi.md5; done'
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
SCRIPT_EXT = ["opsiscript", "opsiinc", "ins", "py"]
"""opsi script file extensions"""
KEYFILE_EXT = ["ppk"]
"""SSH keyfile extension"""
PRG_EXT = ["exe"]
"""Program executable extension (Windows)"""

# log formats
LOG_DATETIME = "%Y-%m-%d %I:%M:%S %p"
"""Log entry: datetime format"""
LOG_LONG =  "[%(asctime)s] - %(name)-45s - %(levelname)8s - %(message)s (%(module)s: %(funcName)s - line %(lineno)s, process %(process)s)"
"""Log entry: long format"""
LOG_SHORT = "[%(asctime)s] - %(name)-45s - %(levelname)8s - %(message)s"
"""Log entry: short format"""
LOG_SSH = "[%(asctime)s] - %(message)s"
"""Log entry (only SSH): format"""

PRODTYPES = ["localboot", "netboot"]
"""opsi product types"""

CHLOG_BLOCKMARKER = "urgency="
"""Changelog block marker"""
CHLOG_URGENCIES = ["low", "middle", "high"]
"""Changelog urgencies"""
CHLOG_STATI = ["stable", "testing", "experimental"]
"""Changelog status"""

BASE_FOLDERS = ["OPSI", "CLIENT_DATA"]
"""Base folders inside project directory"""

MsgEnum = Enum("MsgEnum", "MS_ERR MS_WARN MS_INFO MS_STAT MS_ALWAYS MS_PARSE MS_QUEST_YESNO MS_QUEST_CTC MS_QUEST_OKCANCEL "
                          "MS_QUEST_PHRASE MS_QUEST_PASS MS_QUEST_DEPOT MS_ABOUTQT")
"""Constants for _msg() - message type"""

UpdEnum = Enum("UpdEnum", "UP_MANU UP_AUTO")
"""Constants for _updater()"""

BModEnum = Enum("BModEnum", "BD_CANCEL BD_REBUILD BD_NEW BD_INTERACTIVE")
"""Command line build modes"""

OpEnum = Enum("OpEnum", "DO_BUILD DO_INSTALL DO_UNINSTALL DO_SETRIGHTS DO_GETCLIENTS DO_GETPRODUCTS DO_CREATEJOBS DO_DELETEJOBS DO_GETATJOBS "
                        "DO_DELETEALLJOBS DO_GETREPOCONTENT DO_GETDEPOTS DO_GETPRODUCTSONDEPOTS DO_QUICKINST DO_QUICKUNINST DO_INSTSETUP DO_UPLOAD "
                        "DO_DELETEFILEFROMREPO DO_UNREGISTERDEPOT DO_DEPLOY DO_SETRIGHTS_REPO DO_PRODUPDATER DO_REBOOT DO_POWEROFF DO_GENMD5 DO_GETCLIENTSONDEPOTS "
                        "DO_IMPORT DO_UNLOCKPRODUCTS DO_GETLOCKEDPRODUCTS DO_GETCLIENTGROUPS DO_GETGROUPS")
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
RET_PUPLOAD = 35      # Err 34: SSH - Error while uploading package on server
RET_PUNLOCK = 36      # Err 34: SSH - Error while unlocking product on server

RET_SINGLETON = 51    # Err 51: Program already running * NOT USED *
RET_NOINI = 52        # Err 52: No INI file available * NOT USED *
RET_QICOMB = 53       # Err 53: Mode incompatibility: --quiet and interactive mode combined on command line * NOT USED *
RET_CMDLINE = 54      # Err 54: Incorrect commandline parameters
RET_NOWINEXE = 57     # Err 57: Winexe not found
RET_PRODUPDRUN = 58   # Err 58: opsi-product-updater already running * NOT USED *
RET_NOREPO = 59       # Err 59: could not get repo content

EXITCODE = RET_OK
"""Standard program exitcode"""

# Help destinations
HLP_LANG_DST = "de"
HLP_FILE = get_script_dir() + "/help/opsipackagebuilder.qhc"
HLP_PREFIX = "qthelp://org.sphinx.opsipackagebuilder.8.0/doc/"
HLP_DST_INDEX = "index.html"
HLP_DST_CHANGELOG = "changelog.html"
HLP_DST_TABPACKET = HLP_LANG_DST + "/tabpacket.html"
HLP_DST_TABDEPEND = HLP_LANG_DST + "/tabdepend.html"
HLP_DST_TABPROP = HLP_LANG_DST + "/tabprop.html"
HLP_DST_BUNDLE = HLP_LANG_DST + "/bundle.html"
HLP_DST_CHLOGEXT = HLP_LANG_DST + "/chlog_extended.html"
HLP_DST_CHLOGSIMPLE = HLP_LANG_DST + "/chlog_simple.html"
HLP_DST_DEPLOY = HLP_LANG_DST + "/deployclientagent.html"
HLP_DST_DEPOTM = HLP_LANG_DST + "/depotmanager.html"
HLP_DST_QUNINST = HLP_LANG_DST + "/start.html"
HLP_DST_UNLOCK = HLP_LANG_DST + "/lockedproducts.html"
HLP_DST_JOBCREATOR = HLP_LANG_DST + "/scheduler.html#auftrage-anlegen"
HLP_DST_JOBLIST = HLP_LANG_DST + "/scheduler.html"
HLP_DST_SETTINGS = HLP_LANG_DST + "/settings.html"
