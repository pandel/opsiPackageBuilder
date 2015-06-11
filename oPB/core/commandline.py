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

import argparse
from pathlib import PurePath
import platform

from PyQt5 import QtCore

import oPB
from oPB.core import *
from oPB.core.tools import Helper

translate = QtCore.QCoreApplication.translate


class CommandLine(object):
    """
    Command line arguments generation and parsing

    Debug from Python command line like:

        import oPB.core.tools; p=oPB.core.tools.CommandLine(); p.getParser().parse_args("-h".split())
        import oPB.core.tools; p=oPB.core.tools.CommandLine(); args = p.getParser().parse_args("--build=new --instsetup -n -r --log=c:\\temp\\log.txt".split());args.__dict__

    """

    def __init__(self):
        prog_name = "opsiPackageBuilder"
        desc = "opsi PackageBuilder (MIT licensed) " + oPB.PROGRAM_VERSION + " Command Line Interface"
        logpath = PurePath(oPB.CONFIG_PATH,"opb-session.log")
        epi = (
                "Processing order, if you specify --build, --install, --uninstall and --set-rights together:\n"
                "1. Set rights -> 2. Build -> 3. Uninstall (existing) -> 4. Install (new)\n"
                "NOTICE: If you don""t specify --no-gui, every action will take place after opening the GUI.\n\n"
                "Suboptions for --build:\n"
                "\tcancel:\tdon't overwrite an existing package\n"
                "\trebuild:\trebuild (overwrite) an existing package\n"
                "\tnew        :\tcreate new package, append timestamp to package version\n"
                "\tinteractive:\tinteractive mode\n"
                "If you don""t specify any suboption, the default value is 'cancel'.\n\n"
                "Default LOG file path: " + str(logpath) + "\n\n")
        if 'Windows' not in platform.system():
            epi += (
                "Example:\n\topsipackagebuilder --path=/home/opsiproducts/testpak --build=new --no-gui --log=/tmp/opb.log\n"
                "\tThis starts opsi PackageBuilder without GUI and builds the package in /home/opsiproducts/testpak.\n"
                "\tLogging messages go into /tmp/opb.log.\n")
        else:
            epi += (
                "Example:\n\topsipackagebuilder.exe --path=W:\opsi\\testpak --build=new --no-gui --log=c:\\temp\opb.log\n"
                "\tThis starts opsi PackageBuilder without GUI and builds the package in W:\opsi\\testpak.\n"
                "\tLogging messages go into c:\\temp\opb.log.\n")

        epi += ( "\tIf the package exists before, the package version gets timestamped and building proceeds.\n\n"
                "Tipp:\n\tIf you just specify --path=<name of packagefolder> it will get expanded\n"
                "\tto the full development folder path. (Don't combine with --no-netdrv!)\n")

        if 'Windows' not in platform.system():
            epi += ( "\tExample: --path=testpak    ==>   --path=/home/opsiproducts/testpak")
        else:
            epi += (
                "\tExample: --path=testpak    ==>   --path=w:\opsi\\testpak")

        self._parser = argparse.ArgumentParser(prog=prog_name, description = desc, epilog=epi,
                                               formatter_class=argparse.RawDescriptionHelpFormatter)

        self._parser.add_argument("--path", "-p", action="store", default = "",
                                  dest="path", help="Path to package root directory")

        self._parser.add_argument("--no-netdrv", "-w", action="store_true", default = False,
                                  dest="nonetdrive", help="Don't mount development drive")

        self._parser.add_argument("--build", "-b", action="store",
                                  choices=["cancel", "rebuild", "add"],
                                  dest="build_mode", help="Build package (see suboptions)")

        groupexclude = self._parser.add_mutually_exclusive_group()

        groupexclude.add_argument("--install", "-i", action="append_const", const="install",
                                  dest="packetaction", help="Install package")

        groupexclude.add_argument("--instsetup", "-s", action="append_const", const="instsetup",
                                  dest="packetaction",
                                  help="Install package and set clients to setup if installed previously")

        groupexclude.add_argument("--uninstall", "-u", action="append_const", const="uninstall",
                                  dest="packetaction", help="Uninstall package")

        self._parser.add_argument("--set-rights", "-r", action="store_true", default = False,
                                  dest="setrights", help="Set rights on server-side package directory")

        self._parser.add_argument("--no-gui", "-n", action="store_true", default = False,
                                  dest="nogui", help="Don't open GUI, log messages to command line")

        self._parser.add_argument("--quiet", "-q", action="store_true", default = False,
                                  dest="quiet", help="Don't show any message (forces --no-gui)")

        self._parser.add_argument("--no-update", "-x", action="store_true", default = False,
                                  dest="noupdate", help="Don't run update check regardless of INI setting")

        self._parser.add_argument("--log", "-l", action="store", nargs="?", const = str(logpath),
                                  dest="log_file", help="Write logfile (optional: specify logfile name)")

        self._parser.add_argument("--log-level", action="store", default='NOTSET',
                                  choices=["CRITICAL", "ERROR", "SSH", "WARNING", "SSHINFO", "INFO", "DEBUG"],
                                  dest="log_level", help="Specify log level")

        # self._parser.add_argument("--debug", "-d", action="store_true", default = argparse.SUPPRESS,
        #                          dest="nonetdrive", help="Write additional debug output (can create very much text!!)")

    def getArgs(self):
        return self._parser.parse_args()

    def getParser(self):
        return self._parser