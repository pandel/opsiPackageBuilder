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
from enum import Enum
from pathlib import PurePath

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

# development base folder on server
DEV_BASE = "/home/opsiproducts"

# some constants
OPB_GREEN = '#c4df9b' # green
OPB_YELLOW = '#fff79a' # yellow
OPB_RED = '#f6989d' # red

# validator regex
OPB_PROPERTY_REGEX_NEW = "^[a-zA-Z0-9-_]{1,128}"
OPB_PROPERTY_REGEX_OLD = "^[a-zA-Z0-9-_]{1,32}"
OPB_PRODUCT_ID_REGEX_NEW = "^[a-z0-9-_\.]{1,128}$"
OPB_PRODUCT_ID_REGEX_OLD = "^[a-z0-9-_\.]{1,32}$"
OPB_PRODUCT_VER_REGEX = "^[a-z0-9\.]{1,32}$"
OPB_PACKAGE_VER_REGEX = "^[a-z0-9\.]{1,16}$"

# basic commands
OPB_INSTALL = "opsi-package-manager -i"
OPB_INSTSETUP = "opsi-package-manager -i -S"
OPB_UNINSTALL = "opsi-package-manager -r"
OPB_UPLOAD = "opsi-package-manager -u"
OPB_DEPOT_SWITCH = "-d"

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
MsgEnum = Enum("MsgEnum", "MS_ERR MS_WARN MS_INFO MS_STAT MS_ALWAYS MS_PARSE MS_QUEST_YESNO MS_QUEST_CTC MS_QUEST_OKCANCEL MS_QUEST_PHRASE")

# output type: MsgBox, Console, Nothing
OutEnum = Enum("OutEnum", "MS_IO_BOX MS_IO_CONSOLE MS_IO_NONE")

# Constants for _updater()
UpdEnum = Enum("UpdEnum", "UP_MANU UP_AUTO")

# command line build modes
BModEnum = Enum("BModEnum", "BD_CANCEL BD_REBUILD BD_NEW BD_INTERACTIVE")

# Constants for _validateContent()
ValidEnum = Enum("ValidEnum", "FD_ASCII FD_RESTRICTED_32 FD_RESTRICTED_128 FD_ALPHA FD_ALPHAPLUS FD_FQDN FD_EMPTY")

# Constants for opsi operations
OpEnum = Enum("OpEnum", "DO_BUILD DO_INSTALL DO_UNINSTALL DO_SETRIGHTS DO_GETCLIENTS DO_GETPRODUCTS DO_CREATEJOBS DO_DELETEJOBS DO_GETJOBS "
                        "DO_DELETEALLATJOBS DO_GETREPOCONTENT DO_GETDEPOTS DO_GETPRODUCTSONDEPOTS DO_QUICKINST DO_QUICKREMOVE DO_INSTSETUP DO_UPLOAD "
                        "DO_DELETE DO_REMOVEDEPOT DO_DEPLOY DO_SETRIGHTS_REPO DO_PRODUPDATER DO_REBOOT DO_POWEROFF DO_MD5")

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
RET_PBUILD = 31       # Err 31: SSH - Error while building package on server, check plink output
RET_PINSTALL = 32     # Err 32: SSH - Error while installing package on server, check plink output
RET_PINSTSETUP = 33   # Err 33: SSH - Error while installing package on server or activating for setup, check plink output
RET_PUNINSTALL = 34   # Err 34: SSH - Error while uninstalling package on server, check plink output

RET_SINGLETON = 51    # Err 51: Program already running
RET_NOINI = 52        # Err 52: No INI file available
RET_QICOMB = 53       # Err 53: Mode incompatibility: --quiet and interactive mode combined on command line
RET_CMDLINE = 54      # Err 54: Incorrect commandline parameters
RET_NOWINEXE = 57     # Err 57: Winexe not found
RET_PRODUPDRUN = 58   # Err 58: opsi-product-updater already running
RET_NOREPO = 59       # Err 59: could not get repo content

EXITCODE = RET_OK