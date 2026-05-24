[Setup]
AppName=Ellibria
AppVersion=1.4.0
AppPublisher=NikitaKayakhov
DefaultDirName={autopf}\Ellibria
DefaultGroupName=Ellibria
OutputBaseFilename=Ellibria.v1.4.0
OutputDir=.
Compression=lzma
SolidCompression=yes
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\Ellibria.exe

[Files]
Source: "dist\Ellibria.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "config.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Ellibria"; Filename: "{app}\Ellibria.exe"; WorkingDir: "{app}"; IconFilename: "{app}\Ellibria.exe"
Name: "{commondesktop}\Ellibria"; Filename: "{app}\Ellibria.exe"; WorkingDir: "{app}"; IconFilename: "{app}\Ellibria.exe"

[Run]
Filename: "{app}\Ellibria.exe"; Description: "Launch Ellibria"; Flags: nowait postinstall skipifsilent