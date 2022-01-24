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

import ctypes
import ctypes.wintypes


class MapDrive(object):
    """
    Maps windows network drives.
    """

    class NETRESOURCEW(ctypes.Structure):
        # https://docs.microsoft.com/en-us/windows/win32/api/winnetwk/ns-winnetwk-netresourcew
        _fields_ = [
            ("dwScope", ctypes.wintypes.DWORD),
            ("dwType",  ctypes.wintypes.DWORD),
            ("dwDisplayType",  ctypes.wintypes.DWORD),
            ("dwUsage",  ctypes.wintypes.DWORD),
            ("lpLocalName", ctypes.wintypes.LPWSTR),
            ("lpRemoteName", ctypes.wintypes.LPWSTR),
            ("lpComment", ctypes.wintypes.LPWSTR),
            ("lpProvider", ctypes.wintypes.LPWSTR)
        ]

    WNetAddConnection2 = ctypes.windll.MPR.WNetAddConnection2W # https://docs.microsoft.com/en-us/windows/win32/api/winnetwk/nf-winnetwk-wnetaddconnection2w
    WNetAddConnection2.argtypes = [ctypes.POINTER(NETRESOURCEW), ctypes.wintypes.LPCWSTR, ctypes.wintypes.LPCWSTR, ctypes.wintypes.BOOL]
    WNetCancelConnection2 = ctypes.windll.MPR.WNetCancelConnection2W # https://docs.microsoft.com/en-us/windows/win32/api/winnetwk/nf-winnetwk-wnetcancelconnection2w
    WNetCancelConnection2.argtypes = [ctypes.wintypes.LPCWSTR, ctypes.wintypes.DWORD, ctypes.wintypes.BOOL]
    RESOURCE_TYPE_DISK = 1
    RESOURCE_USAGE_IGNORED = 0
    FLAG_CONNECT_UPDATE_PROFILE = 1


    @classmethod
    def mapDrive(cls, name, path, username, password):
        nr = cls.NETRESOURCEW()
        nr.dwType = cls.RESOURCE_TYPE_DISK
        nr.lpLocalName = name
        nr.lpRemoteName = path
        nr.lpProvider = None

        flags = cls.FLAG_CONNECT_UPDATE_PROFILE

        retVal = cls.WNetAddConnection2(ctypes.byref(nr), password, username, flags)
        msg = ''
        if retVal != 0:
            msg = ctypes.FormatError(retVal)
        return retVal, msg

    @classmethod
    def unMapDrive(cls, name):
        retVal = cls.WNetCancelConnection2(name, cls.FLAG_CONNECT_UPDATE_PROFILE, False)
        msg = ''
        if retVal != 0:
            msg = ctypes.FormatError(retVal)
        return retVal, msg

if __name__=="__main__":
    print( "MapDrive 1:", MapDrive.mapDrive(
        "Y:",
        "\\\\path\\to\\be\\mapped",
        "username",
        "password"
    ))

