; Inno Setup Script for LIQ Invoice

[Setup]
AppName=LIQ Invoice
AppVersion=1.0
AppPublisher=LIQ
AppPublisherURL=https://example.com/
AppSupportURL=https://example.com/
AppUpdatesURL=https://example.com/
DefaultDirName={localappdata}\Programs\LIQ Invoice
DefaultGroupName=LIQ Invoice
OutputDir={#SourcePath}\Output
OutputBaseFilename=LIQ Invoice Installer
Compression=lzma2
SolidCompression=yes
SetupIconFile={#SourcePath}\icon.ico
UninstallDisplayIcon={app}\LIQ Invoice.exe
AppId={{8F44D7D0-10E2-4DAE-9A31-1A7A4B4D4C6C}}
PrivilegesRequired=lowest
WizardStyle=modern
DisableWelcomePage=no
DisableDirPage=no
DisableProgramGroupPage=no
DisableReadyPage=no
DisableReadyMemo=no
ArchitecturesInstallIn64BitMode=x64
UsePreviousAppDir=no
UsePreviousGroup=no
WizardImageFile={#SourcePath}\installer_banner.bmp
WizardSmallImageFile={#SourcePath}\installer_small.bmp
LicenseFile={#SourcePath}\EULA.txt

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Messages]
WelcomeLabel1=Welcome to the LIQ Invoice Setup Wizard
WelcomeLabel2=This installer will guide you through installing LIQ Invoice on your computer.
FinishedHeadingLabel=Installation complete
FinishedLabel=LIQ Invoice has been installed successfully.

[Files]
Source: "{#SourcePath}\dist\LIQ Invoice.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourcePath}\fonts\*"; DestDir: "{app}\fonts"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{userprograms}\LIQ Invoice"; Filename: "{app}\LIQ Invoice.exe"
Name: "{userdesktop}\LIQ Invoice"; Filename: "{app}\LIQ Invoice.exe"

[Run]
Filename: "{app}\LIQ Invoice.exe"; Description: "Launch LIQ Invoice"; Flags: nowait postinstall skipifsilent
