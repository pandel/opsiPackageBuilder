import sys
import ctypes
from ctypes.wintypes import LPWSTR
from PyQt5.QtCore import QLibrary

is_64bits = sys.maxsize > 2**32

class MapDrive(object):
    if is_64bits:
        _handle=ctypes.cdll.LoadLibrary("MapDrive_x64.dll")
    else:
        _handle=ctypes.cdll.LoadLibrary("MapDrive.dll")

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

class MapDrive2(object):
    if is_64bits:
        _handle=QLibrary("MapDrive_x64.dll")
    else:
        _handle=QLibrary("MapDrive.dll")

    assert _handle.load()
    assert _handle.isLoaded()
    _mapDrive=ctypes.CFUNCTYPE(
        ctypes.c_int,
        LPWSTR,
        LPWSTR,
        LPWSTR,
        LPWSTR,
        LPWSTR
    )(int(_handle.resolve("mapDrive")))

    _unMapDrive=ctypes.CFUNCTYPE(
        ctypes.c_int,
        LPWSTR,
        LPWSTR
    )(int(_handle.resolve("unMapDrive")))

    @classmethod
    def mapDrive(cls, name, path, username, password):
        m=LPWSTR(" "*80)
        ok=cls._mapDrive(
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
        ok=cls._unMapDrive(
            LPWSTR(name),
            m
        )
        return ok, m.value


if __name__=="__main__":
    print("MapDrive 1:", MapDrive.mapDrive(
        "Y:",
        "\\\\yi7xa19z\\opsi_workbench",
        "opsiadm",
        "vb.1383"
    ))

    print("MapDrive 2:", MapDrive2.mapDrive(
        "Y:",
        "\\\\yi7xa19z\\opsi_workbench",
        "opsiadm",
        "vb.1383"
    ))

    print("unMapDrive 1:", MapDrive.unMapDrive(
        "Y:"
    ))

    print("unMapDrive 2:", MapDrive2.unMapDrive(
        "Y:"
    ))

    '''
    print("MapDrive 2:", MapDrive2.mapDrive(
        "Y:",
        "\\\\path\\to\\be\\mapped",
        "username",
        "password"
    ))
    '''