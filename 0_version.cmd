set SPATH="C:\Program Files\Git\usr\bin"

set OLDVERSION=8.4.0
set NEWVERSION=8.4.1
set OLDSHORTVERSION=8.4
set NEWSHORTVERSION=8.4

REM Ersetze "foo" mit "bar" NUR in Zeilen die "baz" enthalten

%SPATH%\sed -b --in-place=.sedcopy "/MyAppVersion/s/%OLDVERSION%/%NEWVERSION%/g" innosetup.iss
%SPATH%\sed -b --in-place=.sedcopy "/MyAppVersion/s/%OLDVERSION%/%NEWVERSION%/g" opb+scripted.iss
%SPATH%\sed -b --in-place=.sedcopy "/bundle_version/s/%OLDVERSION%/%NEWVERSION%/g" pyinstaller-mac.spec
%SPATH%\sed -b --in-place=.sedcopy "/version/s/%OLDVERSION%/%NEWVERSION%/g" setup.py
%SPATH%\sed -b --in-place=.sedcopy "/PROGRAM_VERSION/s/%OLDVERSION%/%NEWVERSION%/g" oPB\__init__.py
%SPATH%\sed -b --in-place=.sedcopy "s/%OLDVERSION%/%NEWVERSION%/g" linux\debreate-normal.dbp
%SPATH%\sed -b --in-place=.sedcopy "s/%OLDVERSION%/%NEWVERSION%/g" linux\debreate-self-contained.dbp
%SPATH%\sed -b --in-place=.sedcopy "s/%OLDVERSION%/%NEWVERSION%/g" linux\opb-helpviewer.desktop
%SPATH%\sed -b --in-place=.sedcopy "s/%OLDVERSION%/%NEWVERSION%/g" linux\opsipackagebuilder.desktop
%SPATH%\sed -b --in-place=.sedcopy "/release/s/%OLDVERSION%/%NEWVERSION%/g" docs\source\conf.py
%SPATH%\sed -b --in-place=.sedcopy "/version/s/%OLDSHORTVERSION%/%NEWSHORTVERSION%/g" docs\source\conf.py
%SPATH%\sed -b --in-place=.sedcopy "/opsipackagebuilder.exe/s/%OLDVERSION%.0/%NEWVERSION%.0/g" 4_distrib.cmd
%SPATH%\sed -b --in-place=.sedcopy "/helpviewer.exe/s/%OLDVERSION%.0/%NEWVERSION%.0/g" 4_distrib.cmd
