pyinstaller --noconfirm  pyinstaller-windows.spec
copy dist\helpviewer\helpviewer.exe dist\opsipackagebuilder
copy dist\helpviewer\helpviewer.exe.manifest dist\opsipackagebuilder
rmdir /s /q dist\helpviewer

if exist verpatch\verpatch.exe verpatch\verpatch dist\opsipackagebuilder\opsipackagebuilder.exe 8.1.3.0 /pv 8.1.3.0 /va /s description "opsi Package Building Tool" /s company "hpSoft" /s copyright "(c) 2016" /s product "opsi PackageBuilder"
if exist verpatch\verpatch.exe verpatch\verpatch dist\opsipackagebuilder\helpviewer.exe 8.1.3.0 /pv 8.1.3.0 /va /s description "Help viewer for opsi Package Building Tool" /s company "hpSoft" /s copyright "(c) 2016" /s product "Helpviewer"


if exist "C:\Program Files (x86)\Inno Setup 5\iscc.exe" "C:\Program Files (x86)\Inno Setup 5\iscc.exe" opb+scripted.iss