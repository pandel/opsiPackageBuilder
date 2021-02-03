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

import base64
import ctypes
import itertools
import logging
import platform
import socket
import sys
import os
import re
from itertools import cycle

if sys.platform.lower().startswith('win'):
   import winreg
   from msilib import *

from datetime import datetime
from binascii import hexlify, unhexlify
from pathlib import PurePath, PurePosixPath, WindowsPath

from PyQt5 import QtCore

import oPB

translate = QtCore.QCoreApplication.translate

class LogMixin(object):
    """
    Log mixin class

    Inherit from this class to access app-wide logger via

        self.logger

    from own class
    """

    @property
    def logger(self):
        #name = '.'.join([__name__, self.__class__.__name__])
        name = '.'.join([self.__module__, self.__class__.__name__])
        return logging.getLogger(name)


class Helper():
    """
    Simple tool functions

    Every method is defined as ``@classmethod``
    """

    @classmethod
    def extCheck(cls, filename: str) -> bool:
        """File extension check:
        Valid extension: ins, opsiscript, opsiinc

        Helper.extCheck(filename)

        Alternatives
        1) ext = m.rpartition('.')[-1]; if ext == ...
        2) m.lower().endswith(('.png', '.jpg', '.jpeg')) ....

        :param filename: filename to check
        """

        if filename == "": return True

        value = filename.lower() # change everything to lower case
        ext = value.rpartition('.')[-1]  # extract file extension, rpartition returns 3-tuple:  part before the separator, the separator itself, and the part after the separator
        return False if not ext in oPB.SCRIPT_EXT else True

    @classmethod
    def concat_path_native(cls, path: str, file: str) -> str:
        """
        Help function for connecting paths and filenames/foldernames.
        Takes underlying os into account.

        :param path: base path
        :param file: file or folder
        """
        if platform.system() == "Windows": # if path is a ONLY windows drive, add a backslash to the drive letter
            if path[-1:] == ":":
                path = path + "\\"
        value = str(PurePath(path, file))
        return value

    @classmethod
    def concat_path_posix(cls, path: str, file: str) -> str:
        """
        Help function for connecting paths and filenames/foldernames.
        Only POSIX-complient paths.

        :param path: base path
        :param file: file or folder
        """

        return str(PurePosixPath(path, file))

    @classmethod
    def get_file_from_path(cls, complete: str) -> str:
        """
        Return file name from complete path as string

        :param complete: path incl. filename
        :return: filename
        """

        return str(PurePath(complete).name)

    @classmethod
    def parse_text(cls, text: str) -> str:
        """
        Replace individual @TABS and @ (cr+lf) templates within ``text``

        with HTML-based replacement (for QMessageBox messages)

        @TAB -> "&nbsp;&nbsp;&nbsp;&nbsp;"
        @ -> "<br>"

        :param text: text with templates
        :return: display text
        """

        text = text.replace("@TAB", "&nbsp;&nbsp;&nbsp;&nbsp;")
        text = text.replace("@", "<br>")
        return text

    @classmethod
    def str_to_bool(cls, s: str) -> bool:
        """
        Convert string to bool

        :param s: "true" / "false" as string
        :return: boolean expression
        """

        print("str_to_bool called with value: " + s)
        if s.upper() == 'TRUE':
             return True
        elif s.upper() == 'FALSE':
             return False
        else:
             raise ValueError("Cannot covert {} to a bool".format(s))

    @classmethod
    def get_user(cls) -> str:
        """Return current username, if found"""

        for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
            user = os.environ.get(name)
            if user:
                return user
            # If not user from os.environ.get(), works only on UNIX
            #import pwd
            #return pwd.getpwuid(os.getuid())[0]

    @classmethod
    def encrypt(cls, text: str) -> str:
        """
        Wrapper for Hexlify obfuscator

        Uses Helper.get_user() to obtain *cipher* key

        :param text: string to obfuscate
        :return: obfuscated string
        """

        encrypted = (
            hexlify(
                Helper.Cipher.XORencrypt(Helper.get_user(), text)
            )
        )
        return encrypted.decode('utf-8')


    @classmethod
    def decrypt(cls, text: str) -> str:
        """
        Wrapper for Hexlify obfuscator

        Uses Helper.get_user() to obtain *cipher* key

        :param text: obfuscated string
        :return: not obfuscated string
        """

        decrypted = (
            Helper.Cipher.XORdecrypt(
                Helper.get_user(), unhexlify(text)
            )
        )
        return decrypted

    class Cipher:
        """Cipher (wrapper) class"""

        @classmethod
        def XORencrypt(cls, key, plaintext):
            cyphered = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(plaintext, cycle(key)))
            return base64.b64encode(cyphered.encode())

        @classmethod
        def XORdecrypt(cls, key, ciphertext):
            message = ''.join(chr(c ^ ord(k)) for c, k in zip(base64.b64decode(ciphertext), cycle(key)))
            return message

    @classmethod
    def timestamp(cls) -> str:
        """
        Small timestamp

        :return: timestamp string "%Y%m%d-%H%M%S"
        """

        return datetime.now().strftime("%Y%m%d-%H%M%S")

    @classmethod
    def timestamp_changelog(cls) -> str:
        """
        Long changelog timestamp

        :return: Mon, 27 Apr 2015 12:33:04 + 0100
        """

        return datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")

    @classmethod
    def paramlist2list(cls, value) ->list:
        """
        Converts comma-separated ``value``, to correct list format
        and takes into account, that the ``value`` itself could contain commas, but
        enclosed within "...", i. e.:

            "OU=test1,dc=subdomain,dc=domain,dc=de", "OU=test2,dc=subdomain,dc=domain,dc=de"
            -> these are two values, with commas inside the separate values

            Convert to rea list:
            ["\"OU=Member Computers,dc=subdomain,dc=domain,dc=de\"", "\"OU=Member Computers2,dc=subdomain,dc=domain,dc=de\""]

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

    @classmethod
    def get_available_drive_letters(cls) -> list:
        """
        Returns every non-mapped drive letter

        .. see: http://stackoverflow.com/questions/4188326/in-python-how-do-i-check-if-a-drive-exists-w-o-throwing-an-error-for-removable

        :return: list
        """

        if 'Windows' not in platform.system():
            return []
        drive_bitmask = ctypes.cdll.kernel32.GetLogicalDrives()
        return list(itertools.compress(string.ascii_uppercase,
               map(lambda x:ord(x) - ord('1'), bin(drive_bitmask)[:1:-1])))

    @classmethod
    def get_existing_drive_letters(cls) -> list:
        """
        Returns every mapped drive letter

        .. see: http://stackoverflow.com/questions/4188326/in-python-how-do-i-check-if-a-drive-exists-w-o-throwing-an-error-for-removable

        :return: list
        """

        if 'Windows' not in platform.system():
            return []
        drive_bitmask = ctypes.cdll.kernel32.GetLogicalDrives()
        return list(itertools.compress(string.ascii_uppercase,
               map(lambda x:ord(x) - ord('0'), bin(drive_bitmask)[:1:-1])))

    @classmethod
    def test_port(cls, host: str, port: str, timeout: int = 2):
        """
        Test if network port is reachable

        :param host: hostname or ip
        :param port:  port number
        :param timeout: connection timeout
        :return: True or error
        """
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

    @classmethod
    def strip_ansi_codes(cls, s: str) -> str:
        """
        Remove as many ANSI color and control codes from ``s`` as possible

        :param s: raw input string
        :return: cleaned string
        """

        def removebackspaces(text):
            """
            Removes backspaces from ``text``

            :param text:
            :return: cleaned string
            """

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
        # if I missed something, then get rid of it hopefully now
        ansi_escape1 = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
        s = ansi_escape1.sub('', s)
        ansi_escape2 = re.compile(r'\x1b(\[.*?[@-~]|\].*?(\x07|\x1b\\))')
        s = ansi_escape2.sub('', s)
        s = removebackspaces(s)

        return s
        #s = re.sub(r'\x1b\[([0-9,A-Z]{1,2})?(;[0-9]{1,2})?(;[0-9]{1,3})?[m|l|H|K]?', '', s)
        #s = re.sub(r'\x1b\[(>\?)([0-9,A-Z]{1,2})?(;[0-9]{1,2})?(;[0-9]{1,3})?[m|l|H|K|S|u]?', '', s)
        #return s

    #subdirs = get_subdirlist(r'\\file01.acme.local\home$')
    @classmethod
    def get_subdirlist(cls, path: str):
        """
        Return list of subdirectories

        :param path: base pathname as r'string'
        :return: list of subdirectories
        """
        wpath = WindowsPath(path)
        return [f.name for f in wpath.iterdir() if f.is_dir()]

    # WINDOWS ONLY
    if sys.platform.lower().startswith('win'):
        @classmethod
        def regkey_value(cls, path, name="", start_key = None):
            """
            Query windows registry value

            .. see: http://code.activestate.com/recipes/578689-get-a-value-un-windows-registry/

            :Example:

                bios_vendor = regkey_value(r"HKEY_LOCAL_MACHINE\HARDWARE\DESCRIPTION\System\BIOS", "BIOSVendor")

            :param path: registry path
            :param name: value name ("" for default)
            :param start_key: start key
            :return: key value
            """

            if isinstance(path, str):
                path = path.split("\\")
            if start_key is None:
                start_key = getattr(winreg, path[0])
                return Helper.regkey_value(path[1:], name, start_key)
            else:
                subkey = path.pop(0)
            with winreg.OpenKey(start_key, subkey) as handle:
                assert handle
                if path:
                    return Helper.regkey_value(path, name, handle)
                else:
                    desc, i = None, 0
                    while not desc or desc[0] != name:
                        desc = winreg.EnumValue(handle, i)
                        i += 1
                    return desc[1]

        @classmethod
        def get_msi_property(cls, path: str, property="ProductCode"):
            """
            Return the MSI property for a given MSI package file
            Standard: return ProductCode

            :param path: full path of MSI file
            :return:  MSI ProductCode String
            """

            db = OpenDatabase(path, MSIDBOPEN_READONLY)
            view = db.OpenView ("SELECT Value FROM Property WHERE Property='" + property + "'")
            view.Execute(None)
            result = view.Fetch()

            return result.GetString(1)


