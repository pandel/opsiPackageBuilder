pyinstaller --noconfirm  pyinstaller-windows.spec
copy dist\helpviewer\helpviewer.exe dist\opsipackagebuilder
copy dist\helpviewer\helpviewer.exe.manifest dist\opsipackagebuilder
rmdir /s /q dist\helpviewer