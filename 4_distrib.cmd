pyinstaller --noconfirm  pyinstaller-windows.spec
copy dist\helpviewer\helpviewer.exe dist\opsipackagebuilder
copy dist\helpviewer\helpviewer.exe.manifest dist\opsipackagebuilder
rmdir /s /q dist\helpviewer

if exist "C:\Program Files (x86)\Inno Setup 5\iscc.exe" "C:\Program Files (x86)\Inno Setup 5\iscc.exe" opb+scripted.iss