#ifdef MAPDRIVE_EXPORTS
#define MAPDRIVE_API extern "C" __declspec(dllexport)
#define UNMAPDRIVE_API extern "C" __declspec(dllexport)
#else
#define MAPDRIVE_API __declspec(dllimport)
#define UNMAPDRIVE_API __declspec(dllimport)
#endif
 
MAPDRIVE_API int mapDrive(LPWSTR, LPWSTR, LPWSTR, LPWSTR, LPWSTR);
UNMAPDRIVE_API int unMapDrive(LPWSTR, LPWSTR);