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
import re
import logging
import argparse
import base64
import socket
import ctypes
import itertools
import string
import platform
from datetime import datetime
from binascii import hexlify, unhexlify
from pathlib import PurePath
from Crypto.Cipher import XOR

from PyQt5 import QtCore

import oPB

translate = QtCore.QCoreApplication.translate

# This class could be imported from a utility module
class LogMixin(object):
    @property
    def logger(self):
        name = '.'.join([__name__, self.__class__.__name__])
        return logging.getLogger(name)

class Helper(LogMixin):
    """ Simple tool functions
    """
    @staticmethod
    def extCheck(filename):
        """File extension check:
        Valid extension: ins, opsiscript, opsiinc

        Helper.extCheck(filename)

        Alternatives
        1) ext = m.rpartition('.')[-1]; if ext == ...
        2) m.lower().endswith(('.png', '.jpg', '.jpeg')) ...."""

        if filename == "": return True

        value = filename.lower() # change everything to lower case
        ext = value.rpartition('.')[-1]  # extract file extension, rpartition returns 3-tuple:  part before the separator, the separator itself, and the part after the separator
        return False if not ext in oPB.SCRIPT_EXT else True

    @staticmethod
    def concat_path_and_file(path: str, file: str) -> str:
        """
        Help function for connecting paths and filenames/foldernames.
        Takes underlying os into account.

        :param path: base path
        :param file: file or folder
        """
        return str(PurePath(path, file))

    @staticmethod
    def get_file_from_path(complete: str) -> str:
        """
        Return file name from complete path as string
        :param complete: path incl. filename
        :return: filename
        """
        return str(PurePath(complete).name)

    @staticmethod
    def parse_text(text: str) -> str:
        """
        Replace individual TABS and CRLF templates from message text

        :param text: text with templates
        :return: display text
        """
        text = text.replace("@TAB", "&nbsp;&nbsp;&nbsp;&nbsp;")
        text = text.replace("@", "<br>")
        return text

    @staticmethod
    def str_to_bool(s: str) -> bool:
        print("str_to_bool called with value: " + s)
        if s == 'True':
             return True
        elif s == 'False':
             ret =  False
        else:
             raise ValueError("Cannot covert {} to a bool".format(s))

    @staticmethod
    def get_user():
        for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
            user = os.environ.get(name)
            if user:
                return user
            # If not user from os.environ.get(), works only on UNIX
            #import pwd
            #return pwd.getpwuid(os.getuid())[0]

    @staticmethod
    def encrypt(text):
        encrypted = (
            hexlify(
                Helper.Cipher.XORencrypt(Helper.get_user(), text)
            )
        )
        return encrypted.decode('utf-8')


    @staticmethod
    def decrypt(text):
        decrypted = (
            Helper.Cipher.XORdecrypt(
                Helper.get_user(), unhexlify(text)
            )
        )
        return decrypted.decode('utf-8')

    class Cipher:

        @staticmethod
        def XORencrypt(key, plaintext):
            cipher = XOR.new(key)
            return base64.b64encode(cipher.encrypt(plaintext))

        @staticmethod
        def XORdecrypt(key, ciphertext):
            cipher = XOR.new(key)
            return cipher.decrypt(base64.b64decode(ciphertext))

    @staticmethod
    def timestamp():
        return datetime.now().strftime("%Y%m%d-%H%M%S")

    @staticmethod
    def timestamp_changelog():
        #  Mon, 27 Apr 2015 12:33:04 + 0100
        return datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")

    @staticmethod
    def paramlist2list(value):
        """
        Converts comma-separated parameters from input field, to correct list format
        and takes into account, that the parameter itself could contain commas, but
        enclosed within "...", i. e.:

        "OU=test1,dc=subdomain,dc=domain,dc=de", "OU=test2,dc=subdomain,dc=domain,dc=de"
        -> these are two values, with commas inside the separate values

        :param value: pseudo-list as string
        :return: correctly separated parameters as real list
        """
        quot = 0
        quotpos = []
        retval = []
        sep = "++@KOM@++"

        # find all positions of , WITHIN "...", incl. " char!

        for i in range(0, len(value) - 1, 1):
            if value[i] == chr(34):
                quot = 1 - quot  # find opening/closing double quotes
            if (value[i] == chr(44)) and (quot == 0):
                quotpos.append(i)  # find comma between quoted strings; i.e. quotpos=[0,4,12,56]

        # now separate string into list, exchange every comma OUTSIDE of "..." with ++@KOM@++
        # re-join the string and split it along the new separator, voilà!

        if len(quotpos) > 0:
            list_ = list(value)
            for pos in quotpos:
                list_[pos] = sep

            val = "".join(list_)

            retval = [x.strip() for x in val.split(sep)]

            return retval
        else:
            retval.append(value)
            return retval

    @staticmethod
    def ui_file_path(uifile):
        return Helper.concat_path_and_file(os.environ['OPB_BASE'], "ui/" + uifile)


    # the following two routines are modifications of:
    # see: http://stackoverflow.com/questions/4188326/in-python-how-do-i-check-if-a-drive-exists-w-o-throwing-an-error-for-removable

    @staticmethod
    def get_available_drive_letters():
        """Returns every non-mapped drive letter"""
        if 'Windows' not in platform.system():
            return []
        drive_bitmask = ctypes.cdll.kernel32.GetLogicalDrives()
        return list(itertools.compress(string.ascii_uppercase,
               map(lambda x:ord(x) - ord('1'), bin(drive_bitmask)[:1:-1])))

    @staticmethod
    def get_existing_drive_letters():
        """Returns every mapped drive letter"""
        if 'Windows' not in platform.system():
            return []
        drive_bitmask = ctypes.cdll.kernel32.GetLogicalDrives()
        return list(itertools.compress(string.ascii_uppercase,
               map(lambda x:ord(x) - ord('0'), bin(drive_bitmask)[:1:-1])))

    @staticmethod
    def test_port(host, port, timeout=2):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, int(port)))
            sock.shutdown(socket.SHUT_RDWR)
        except OSError as e:
            return e
        else:
            sock.close()
            return True

    @staticmethod
    def strip_ansi_codes(s):
        def removebackspaces(text):
            backspace_or_eol = r'(.\010)|(\033\[K)'
            n = 1
            while n > 0:
                text, n = re.subn(backspace_or_eol, '', text, 1)
            return text

        s = s.replace(r'\x1b', '\n' + r'\x1b')
        s = re.sub(r'\x1b\[\d*;\d*;\d*m', '', s)
        s = re.sub(r'\x1b\[\d*;\d*[fmHr]', '', s)
        s = re.sub(r'\x1b\[\d*[tGEFDBCAPMnXJKjam@Ldkel]', '', s)
        s = re.sub(r'\x1b\[\?\d*[hl]', '', s)
        s = re.sub(r'\x1b\[\?\w*', '', s)
        s = re.sub(r'\x1b\[>\d*[hl]', '', s)
        s = re.sub(r'\x1b\[[Hsu]', '', s)
        s = re.sub(r'\x1b\(\w*', '', s)
        s = re.sub(r'\x1b\]0;[\w*]', '', s)
        s = re.sub(r'\x1b[=>]', '', s)
        s = re.sub('(\n)+', '\n', s)
        s = re.sub('\A\n|\n\Z', '', s)
        s = re.sub(r'\A\v|\v\Z', '', re.sub(r'(\v)+', '\n', s))
        s = s.replace('\07', '')
        s = removebackspaces(s)
        return s
        #s = re.sub(r'\x1b\[([0-9,A-Z]{1,2})?(;[0-9]{1,2})?(;[0-9]{1,3})?[m|l|H|K]?', '', s)
        #s = re.sub(r'\x1b\[(>\?)([0-9,A-Z]{1,2})?(;[0-9]{1,2})?(;[0-9]{1,3})?[m|l|H|K|S|u]?', '', s)
        #return s

class CommandLine(object):
    """ Command line arguments generation and parsing.
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

# import oPB.core.tools; p=oPB.core.tools.CommandLine(); p.getParser().parse_args("-h".split())
# import oPB.core.tools; p=oPB.core.tools.CommandLine(); args = p.getParser().parse_args("--build=new --instsetup -n -r --log=c:\\temp\\log.txt".split());args.__dict__
