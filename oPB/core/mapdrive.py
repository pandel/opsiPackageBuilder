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
import inspect
import ctypes
from ctypes.wintypes import LPWSTR

is_64bits = sys.maxsize > 2**32

def get_script_dir(follow_symlinks=True):
    """Get file path of script. Take freezing into account."""
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)


class MapDrive(object):
    """
    Maps windows network drives.

    See following link for detail and files in src folder

    .. seealso:: `MapDrive <http://www.gulon.co.uk/2014/08/10/mapping-a-network-drive-with-python/>`_
    """
    if is_64bits:
        _handle=ctypes.cdll.LoadLibrary(get_script_dir()+"\\x64\\MapDrive.dll")
    else:
        _handle=ctypes.cdll.LoadLibrary(get_script_dir()+"\\x86\\MapDrive.dll")

    @classmethod
    def mapDrive(cls, name, path, username, password):
        m=LPWSTR(" "*80)
        ok=cls._handle.mapDrive(
            LPWSTR(name),
            LPWSTR(path),
            LPWSTR(username),
            LPWSTR(password),
            m
        )
        return ok, m.value

    @classmethod
    def unMapDrive(cls, name):
        m=LPWSTR(" "*80)
        ok=cls._handle.unMapDrive(
            LPWSTR(name),
            m
        )
        return ok, m.value

if __name__=="__main__":
    print( "MapDrive 1:", MapDrive.mapDrive(
        "Y:",
        "\\\\path\\to\\be\\mapped",
        "username",
        "password"
    ))

