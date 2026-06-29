LIQ Invoice — Public Download Folder

Files included:
- LIQ Invoice Installer.exe  — the signed installer
- EULA.txt — End User License Agreement
- LIQ_Invoice_Installer.sha256 — SHA256 checksum for integrity verification

Verify integrity (Windows PowerShell):
Get-FileHash -Algorithm SHA256 "LIQ Invoice Installer.exe"
# Compare the printed hash with the contents of LIQ_Invoice_Installer.sha256

Verify digital signature (Windows):
# Requires signtool from Windows SDK
signtool verify /pa /v "LIQ Invoice Installer.exe"

Notes:
- This build was signed with a locally-generated code-signing certificate for testing. For public distribution, obtain a CA-issued code signing certificate and re-sign the installer to avoid SmartScreen warnings.
- Keep the PFX file secure. Do not publish it in public repositories.

Ko-fi support:
https://ko-fi.com/liqapps
