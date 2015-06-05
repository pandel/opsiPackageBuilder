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
import inspect
import sys
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

# add base path to environement and append ui package to module search path
# necessary for uic to find resource file
os.environ['OPB_BASE'] = get_script_dir()
sys.path.append(os.environ['OPB_BASE'] + "/ui")

# simple print object relationship besides normal logging
# for object hierarchy debugging
#PRINTHIER = True
PRINTHIER = False

# overall program version
PROGRAM_VERSION = "8.0.0"

# network mode, offline/online
NETMODE="online"

# auto-connected drive letter
NETDRV=None

# standard path for config file
if os.name == "nt":
    CONFIG_PATH = PurePath(os.environ["APPDATA"], "opsiPackageBuilder")
elif os.name == "posix":
    CONFIG_PATH = PurePath(os.environ["HOME"], ".opsiPackageBuilder")

# standard INI file full path
CONFIG_INI = str(PurePath(CONFIG_PATH,"config-new.ini"))

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
-----------------

www.rechner.de
.test.net
10.2225.65.13   <- Problem! Matches as HOST :-)
10.226.98.132
www.böse.net
"""

# basic commands
OPB_INSTALL = "opsi-package-manager -i"
OPB_INSTSETUP = "opsi-package-manager -i -S"
OPB_UNINSTALL = "opsi-package-manager -r"
OPB_UPLOAD = "opsi-package-manager -u"
OPB_PROD_UPDATER = "nohup /usr/bin/opsi-product-updater -vv 1>/dev/null 2>&1 </dev/null &" # must be started with nohup
OPB_DEPLOY_COMMAND = "/var/lib/opsi/depot/opsi-client-agent/opsi-deploy-client-agent"
OPB_DEPOT_SWITCH = "-d"
OPB_METHOD_ONDEMAND = "opsi-admin -d method hostControl_fireEvent 'on_demand'"
OPB_METHOD_PRODUCTACTION = "opsi-admin -d method setProductActionRequestWithDependencies"
OPB_METHOD_WOL = "opsi-admin -d method powerOnHost"
OPB_METHOD_GETDEPOTS = "opsi-admin -d method host_getHashes '[]' '{" + '"type":"OpsiDepotserver"}' + "'"
OPB_METHOD_DELETHOST = "opsi-admin -d method host_delete"
OPB_METHOD_GETPRODUCTS = "opsi-admin -r -d method product_getHashes"
OPB_METHOD_GETCLIENTS = "opsi-admin -d method host_getHashes '[]' '{" + '"type":"OpsiClient"}' + "'"
OPB_METHOD_GETCLIENTSONDEPOTS = "opsi-admin -d method configState_getClientToDepotserver" # filter with behind: '["***REMOVED***1hp.sd8106.***REMOVED***"]'
OPB_METHOD_GETPRODUCTSONDEPOTS = "opsi-admin -d method productOnDepot_getIdents"
OPB_METHOD_UNREGISTERDEPOT = "opsi-admin -d method host_delete"

OPB_AT_QUEUE = "atq -q D"
OPB_AT_JOB_DETAIL = "atq -q D | cut -f1 | xargs at -q D -c | grep opsi-admin"
OPB_AT_CREATE = "at -q D -t"
OPB_AT_REMOVE = "atrm"
OPB_AT_REMOVE_ALL = "atrm $(atq -q D | cut -f 1)"
OPB_SETRIGHTS_NOSUDO = "opsi-setup --set-rights"
OPB_SETRIGHTS_SUDO = "opsi-set-rights"
OPB_GETPRODUPD_PID = "VAR=$(pidof -x opsi-product-updater); echo $VAR"
OPB_PRECHECK_MD5 = "md5deep -h"
OPB_PRECHECK_WINEXE = "winexe --help"
# create MD5 file for packet; set in front: 'PACKETS=\"xca_0.9.3-1.opsi\";'
OPB_CALC_MD5 = 'PACKETPATH="' + REPO_PATH + '"; for p in $PACKETS; do MD5=\"`md5deep $PACKETPATH/$p.opsi 2>/dev/null | cut -d \" \" -f 1`\"; echo -n $MD5 >$PACKETPATH/$p.opsi.md5; done'
# get all products from repository directory incl. MD5
OPB_GETREPOCONTENT = 'PACKETPATH="' + REPO_PATH + '"; PACKETS=\"`ls $PACKETPATH/*.opsi 2>/dev/null | cut -d "/" -f 6`\"; ' \
                       'for p in $PACKETS; do MD5=\"`cat $PACKETPATH/$p.md5 2>/dev/null`\"; echo $MD5-@MD5@-$p; done'
# remove files from repository; set in front: 'PACKETS=\"xca_0.9.3-1\";'
OPB_DEPOT_FILE_REMOVE = 'PACKETPATH="' + REPO_PATH + '"; for p in $PACKETS; do ' \
                            'rm -v -f $PACKETPATH/$p.opsi; rm -v -f $PACKETPATH/$p.opsi.md5; rm -v -f $PACKETPATH/$p.opsi.zsync; done'

OPB_REBOOT = "shutdown -r now"
OPB_POWEROFF = "shutdown -h now"

# file extensions for selection dialogs
SCRIPT_EXT = ["opsiscript", "opsiinc", "ins", "py", "*"]
KEYFILE_EXT = ["ppk"]
PRG_EXT = ["exe"]

# log formats
LOG_DATETIME = "%Y-%m-%d %I:%M:%S %p"
LOG_LONG =  "[%(asctime)s] - %(name)-35s - %(levelname)8s - %(message)s (%(module)s: %(funcName)s - line %(lineno)s, process %(process)s)"
LOG_SHORT = "[%(asctime)s] - %(name)-35s - %(levelname)8s - %(message)s"
LOG_SSH = "[%(asctime)s] - %(message)s"

# product types
PRODTYPES = ["localboot", "netboot"]

# changelog relevant parameter
CHLOG_BLOCKMARKER = "urgency="
CHLOG_URGENCIES = ["low", "middle", "high"]
CHLOG_STATI = ["stable", "testing"]

# base folders inside project directory
BASE_FOLDERS = ["OPSI", "CLIENT_DATA"]

# Constants for _msg() - message type
MsgEnum = Enum("MsgEnum", "MS_ERR MS_WARN MS_INFO MS_STAT MS_ALWAYS MS_PARSE MS_QUEST_YESNO MS_QUEST_CTC MS_QUEST_OKCANCEL "
                          "MS_QUEST_PHRASE MS_QUEST_PASS MS_QUEST_DEPOT")

# Constants for _updater()
UpdEnum = Enum("UpdEnum", "UP_MANU UP_AUTO")

# command line build modes
BModEnum = Enum("BModEnum", "BD_CANCEL BD_REBUILD BD_NEW BD_INTERACTIVE")

# Constants for opsi operations
OpEnum = Enum("OpEnum", "DO_BUILD DO_INSTALL DO_UNINSTALL DO_SETRIGHTS DO_GETCLIENTS DO_GETPRODUCTS DO_CREATEJOBS DO_DELETEJOBS DO_GETATJOBS "
                        "DO_DELETEALLJOBS DO_GETREPOCONTENT DO_GETDEPOTS DO_GETPRODUCTSONDEPOTS DO_QUICKINST DO_QUICKUNINST DO_INSTSETUP DO_UPLOAD "
                        "DO_DELETEFILEFROMREPO DO_UNREGISTERDEPOT DO_DEPLOY DO_SETRIGHTS_REPO DO_PRODUPDATER DO_REBOOT DO_POWEROFF DO_GENMD5 DO_GETCLIENTSONDEPOTS")

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

# Help destinations
HLP_FILE = get_script_dir() + "/help/opsipackagebuilder.qhc"
HLP_PREFIX = "qthelp://org.sphinx.opsipackagebuilder.8.0/doc/"
HLP_DST_TABPACKET = QtCore.QLocale().system().name()[:2] + "/tabpacket.html"
HLP_DST_TABDEPEND = QtCore.QLocale().system().name()[:2] + "/tabdepend.html"
HLP_DST_TABPROP = QtCore.QLocale().system().name()[:2] + "/tabprop.html"
HLP_DST_BUNDLE = QtCore.QLocale().system().name()[:2] + "/bundle.html"
HLP_DST_CHLOGEXT = QtCore.QLocale().system().name()[:2] + "/chlog_extended.html"
HLP_DST_CHLOGSIMPLE = QtCore.QLocale().system().name()[:2] + "/chlog_simple.html"
HLP_DST_DEPLOY = QtCore.QLocale().system().name()[:2] + "/deployclientagent.html"
HLP_DST_DEPOTM = QtCore.QLocale().system().name()[:2] + "/depotmanager.html"
HLP_DST_QUINST = QtCore.QLocale().system().name()[:2] + "/"
HLP_DST_JOBCREATOR = QtCore.QLocale().system().name()[:2] + "/scheduler.html#auftrage-anlegen"
HLP_DST_JOBLIST = QtCore.QLocale().system().name()[:2] + "/scheduler.html"
