[Setup]
AppName=Ellibria
AppVersion=1.0
AppPublisher=NikitaKayakhov
DefaultDirName={autopf}\Echo
DefaultGroupName=Echo
OutputBaseFilename=Ellibria Ai Installer
OutputDir=.
Compression=lzma
SolidCompression=yes
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\Echo.exe
[Files]
Source: "dist\Echo.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "config.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion
[Icons]
Name: "{group}\Echo"; Filename: "{app}\Echo.exe"; IconFilename: "{app}\Echo.exe"
Name: "{commondesktop}\Echo"; Filename: "{app}\Echo.exe"; IconFilename: "{app}\Echo.exe"
[Run]
Filename: "{app}\Echo.exe"; Description: "Launch Echo"; Flags: nowait postinstall skipifsilent 