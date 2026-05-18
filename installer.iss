[Setup]
AppName=Echo
AppVersion=1.0
AppPublisher=WiredScars
DefaultDirName={autopf}\Echo
DefaultGroupName=Echo
OutputBaseFilename=EchoInstaller
OutputDir=.
Compression=lzma
SolidCompression=yes
; Своя иконка для установщика (положи icon.ico рядом с installer.iss)
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\Echo.exe

[Files]
Source: "dist\Echo.exe"; DestDir: "{app}"; Flags: ignoreversion
; Если у тебя есть icon.ico — раскомментируй строку ниже:
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Echo"; Filename: "{app}\Echo.exe"; IconFilename: "{app}\Echo.exe"
Name: "{commondesktop}\Echo"; Filename: "{app}\Echo.exe"; IconFilename: "{app}\Echo.exe"

[Run]
Filename: "{app}\Echo.exe"; Description: "Launch Echo"; Flags: nowait postinstall skipifsilent
