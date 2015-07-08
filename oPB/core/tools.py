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
import sys
import re
import logging
import base64
import socket
import ctypes
import itertools
import string
import platform

if sys.platform.lower().startswith('win'):
    import winreg

from datetime import datetime
from binascii import hexlify, unhexlify
from pathlib import PurePath, PurePosixPath, WindowsPath

from Crypto.Cipher import XOR
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
        name = '.'.join([__name__, self.__class__.__name__])
        return logging.getLogger(name)


class Helper(LogMixin):
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

        return str(PurePath(path, file))

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
        return decrypted.decode('utf-8')

    class Cipher:
        """Cipher (wrapper) class"""

        @classmethod
        def XORencrypt(cls, key, plaintext):
            cipher = XOR.new(key)
            return base64.b64encode(cipher.encrypt(plaintext))

        @classmethod
        def XORdecrypt(cls, key, ciphertext):
            cipher = XOR.new(key)
            return cipher.decrypt(base64.b64decode(ciphertext))

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

class HTMLTools(LogMixin):
    """
    HTMLTools class provides convenient functions to create working HTML pages from simple text

    Every method is defined as ``@classmethod``

    """
    @classmethod
    def HTMLHeader(cls, title = "", bodybgcolor = "#ffffff", highlightbgcolor = "#F0F9FF",
                   headerbgcolor = "#007EE5", bodytxtcolor = "#000000", headertxtcolor = "#ffffff") -> str:
        """
        Return valid HTML page header

        :param title: page title
        :param bodybgcolor: body background color
        :param highlightbgcolor: highlight background color
        :param headerbgcolor: header background color
        :param bodytxtcolor: body text color
        :param headertxtcolor: header text color
        :return: HTML string
        """
        head = ""
        if title != "":
            head = '<center><h2>' + title + '</h2></center>'

        css = "table {margin: 1em; border-collapse: collapse; } \n" \
              "td, th {padding: .3em; border: 1px #ccc solid; }\n" \
              "thead {background: " + headerbgcolor + "; }\n" \
              "thead {color:" + headertxtcolor + ";}\n" \
              "tbody {background: " + bodybgcolor + "; }\n" \
              "tbody {color: " + bodytxtcolor + "; }\n" \
              "#highlight tr.hilight { background: " + highlightbgcolor + "; }\n" \
              "h2 { font-size: 100%; }\n" \
              "@media print { h2 { font-size: 94%; } }\n" \
              "body { font-size: 94%; font-family: Helvetica, Arial, sans-serif; line-height: 100%; }\n"

        javascript = "function tableHighlightRow() {\n" \
              "  if (document.getElementById && document.createTextNode) {\n" \
              '    var tables=document.getElementsByTagName("table");\n' \
              "    for (var i=0;i<tables.length;i++)\n" \
              "    {\n" \
              '      if(tables[i].className=="hilite") {\n' \
              '        var trs=tables[i].getElementsByTagName("tr");\n' \
              "        for(var j=0;j<trs.length;j++)\n" \
              "           {\n" \
              '          if(trs[j].parentNode.nodeName=="TBODY") {\n' \
              '            trs[j].onmouseover=function(){this.className="hilight";return false}\n' \
              "            trs[j].onmouseout=function(){this.className="";return false}\n" \
              "          }\n" \
              "        }\n" \
              "      }\n" \
              "    }\n" \
              "  }\n" \
              "}\n" \
              "window.onload=function(){tableHighlightRow();}\n"

        html = "<!DOCTYPE html><html>\n" + \
              "<head> " + \
              "<title>" + title + "</title>\n" \
              "<Style>\n" + \
              css + \
              "</Style>\n" + \
              "<script>\n" + \
              javascript + \
              "</script>\n" + \
              "</head>\n" + \
              "<body>\n" + head

        return html

    @classmethod
    def HTMLFooter(cls):
        """
        Very simple HTML page footer

        :return: footer string "</body></html>"
        """
        return "</body></html>"

    @classmethod
    def Array2HTMLTable(cls, element_list = [], colspan = 1, title = '', bodybgcolor = "#ffffff", hightlightbgcolor = "#F0F9FF",
        headerbgcolor = "#007EE5", bodytxtcolor = "#000000", headertxtcolor = "#ffffff", headers_on = True, only_table = False) -> str:
        """
        Convert list of lists (2D table) two HTML table

        :param element_list: list of lists
        :param colspan: colspan of header row, only valid if ``headers_on`` is True
        :param title: page title, only valid if ``only_table`` is False
        :param bodybgcolor: body background color, only valid if ``only_table`` is False
        :param highlightbgcolor: highlight background color, only valid if ``only_table`` is False
        :param headerbgcolor: header background color, only valid if ``only_table`` is False
        :param bodytxtcolor: body text color, only valid if ``only_table`` is False
        :param headertxtcolor: header text color, only valid if ``only_table`` is False
        :param headers_on: ``element_list`` contains table headers in first row (True) or not (False)
        :param only_table: generate table only (True), or return complete HTML page (False)
        :return: HTML string
        """

        if not element_list:
            return

        table_rows = ""
        table_header  = ""
        bodystart = 1

        try:
            total_rows = len(element_list)
            if not headers_on:
                total_columns = len(element_list[0]) # first real data row sets column count for whole table
            else:
                total_columns = len(element_list[1]) # first real data row sets column count for whole table
        except:
            return

        if not headers_on:
            bodystart = 0
        else:
            if total_rows < 2:
                return # there need to be at least two rows if headers are on

            for x in range(total_columns):
                try: # fewer header columns than data columns?
                    t = str(element_list[0][x]) if element_list[0][x] is not None else ""
                    table_header = table_header + '   <th colspan=' + str(colspan) + '>' + t + '</th>\n'
                except:
                    pass

        for r in range(bodystart, total_rows):
            table_columns = ""
            for c in range(0, total_columns):
                t = str(element_list[r][c]) if element_list[r][c] is not None else ""
                table_columns = table_columns + '   <td>' + t + '</td>\n'

            table_rows += '<tr>' + table_columns + '</tr>\n'

        if not only_table:
            html = cls.HTMLHeader(title, bodybgcolor, hightlightbgcolor, headerbgcolor, bodytxtcolor, headertxtcolor) + \
                    '<p align="center"><table class="hilite" id="highlight" style="width:80%">\n' + \
                    '<thead>\n' + \
                    '<tr>' + \
                    table_header + \
                    '</tr>\n' + \
                    '</thead>\n' + \
                    '</p><tbody>\n' + \
                    table_rows + \
                    '</tbody>\n' + \
                    '</table>\n' + \
                    cls.HTMLFooter()
        else:
            html = '<p align="center"><table class="hilite" id="highlight" style="width:80%">\n' + \
                    '<thead>\n' + \
                    '<tr>' + \
                    table_header + \
                    '</tr>\n' + \
                    '</thead>\n' + \
                    '</p><tbody>\n' + \
                    table_rows + \
                    '</tbody>\n' + \
                    '</table>\n'

        return html
