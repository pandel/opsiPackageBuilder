call workon oPB

%USERPROFILE%\Envs\oPB\Scripts\pyinstaller --noconfirm  --version-file version.txt pyinstaller-windows.spec

copy dist\helpviewer\helpviewer.exe dist\opsipackagebuilder
copy dist\helpviewer\helpviewer.exe.manifest dist\opsipackagebuilder

rmdir /s /q dist\helpviewer

if exist verpatch\verpatch.exe verpatch\verpatch dist\opsipackagebuilder\opsipackagebuilder.exe 8.4.5.0 /pv 8.4.5.0 /va /s description "opsi Package Building Tool" /s company "hp" /s copyright "(c) 2018" /s product "opsi PackageBuilder"
if exist verpatch\verpatch.exe verpatch\verpatch dist\opsipackagebuilder\helpviewer.exe 8.4.5.0 /pv 8.4.5.0 /va /s description "Help viewer for opsi Package Building Tool" /s company "hp" /s copyright "(c) 2018" /s product "Helpviewer"

if exist "C:\Program Files (x86)\Inno Setup 5\iscc.exe" "C:\Program Files (x86)\Inno Setup 5\iscc.exe" opb+scripted.iss