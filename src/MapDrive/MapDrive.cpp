// MapDrive.cpp : Definiert die exportierten Funktionen für die DLL-Anwendung.
//

#include "stdafx.h"
#include "MapDrive.h"
#include <strsafe.h>
 
#define ASCII 20127
 
void formatError(DWORD error, LPWSTR errorStr){
    LPVOID msg, display;
 
    FormatMessage(
        FORMAT_MESSAGE_ALLOCATE_BUFFER|FORMAT_MESSAGE_FROM_SYSTEM|FORMAT_MESSAGE_IGNORE_INSERTS,
        NULL,
        error,
        MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
        (LPTSTR) &msg,
        0,
        NULL
    );
     
    int sizeNeeded=lstrlen((LPCTSTR)msg);
    display=(LPVOID)LocalAlloc(LMEM_ZEROINIT, sizeNeeded*sizeof(TCHAR));
    StringCchPrintf((LPTSTR)display, LocalSize(display)/sizeof(TCHAR), TEXT("%s"), msg);
    StringCbPrintf(errorStr, 80, L"%s", display);
  
    LocalFree(msg);
    LocalFree(display);
}
 
MAPDRIVE_API int mapDrive(LPWSTR name, LPWSTR path, LPWSTR username, LPWSTR password, LPWSTR message){
    NETRESOURCE nr;
    memset(&nr, 0, sizeof(NETRESOURCE));
    nr.dwType=RESOURCETYPE_ANY;
    nr.lpLocalName=name;
    nr.lpRemoteName=path;
    nr.lpProvider=NULL;
 
    DWORD flags=CONNECT_UPDATE_PROFILE;
 
    DWORD retVal=WNetAddConnection2(&nr, password, username, flags);
    if(retVal==NO_ERROR) return 0;
 
    formatError(retVal, message);
    return retVal;
}

UNMAPDRIVE_API int unMapDrive(LPWSTR name, LPWSTR message){

	DWORD flags=CONNECT_UPDATE_PROFILE;

	DWORD retVal=WNetCancelConnection2(name, flags, FALSE);
    if(retVal==NO_ERROR) return 0;
 
    formatError(retVal, message);
    return retVal;
}
