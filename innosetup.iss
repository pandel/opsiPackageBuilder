; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "opsi PackageBuilder"
#define MyAppVersion "8.0.0"
#define MyAppPublisher "opsi community project"
#define MyAppPublisherURL "https://forum.opsi.org/viewforum.php?f=22"
#define MyAppExeName "opsiPackageBuilder.exe"
#define MyAppContact "holger.pandel@googlemail.com"
#define MyAppCopyright "Copyright (C) 2013-2015 Holger Pandel"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{3E74E782-16F6-4CEC-BE71-52476A6EFAA2}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppPublisherURL}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=D:\Pythonprojects\opsipackgebuilder-dropbox\dist
OutputBaseFilename=opsiPackageBuilder-v{#MyAppVersion}
SetupIconFile=D:\Pythonprojects\opsipackgebuilder-dropbox\images\prog.ico
Compression=lzma
SolidCompression=yes
EnableDirDoesntExistWarning=True
AppContact={#MyAppContact}
VersionInfoVersion={#MyAppVersion}
MinVersion=0,5.01
; LicenseFile=LICENSE_EN
VersionInfoProductName=opsi PackageBuilder
AppCopyright={#MyAppCopyright}
ChangesAssociations=True
AppSupportURL={#MyAppPublisherURL}
AppUpdatesURL={#MyAppPublisherURL}
FlatComponentsList=False
ShowTasksTreeLines=True
ShowLanguageDialog=auto

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 0,6.1

[Files]
Source: "D:\Pythonprojects\opsipackgebuilder-dropbox\dist\opsipackagebuilder\opsipackagebuilder.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Pythonprojects\opsipackgebuilder-dropbox\dist\opsipackagebuilder\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
