# Instala el Tablero Transtotal local:
#  - acceso directo en Inicio de Windows (arranca el servidor al iniciar sesión, sin ventana)
#  - acceso directo "Tablero Transtotal" en el escritorio (ventana propia de Chrome)
#  - regla del firewall para que la red de la oficina pueda abrirlo (puerto 8090, solo redes privadas y de dominio)
$ErrorActionPreference = "Stop"
$dir = "C:\jornada-bot\tablero"
$admin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $admin) {
  Start-Process powershell -Verb RunAs -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`""
  exit
}

$sh = New-Object -ComObject WScript.Shell
function Acceso($ruta, $vbs, $desc) {
  $l = $sh.CreateShortcut($ruta)
  $l.TargetPath = "$env:WINDIR\System32\wscript.exe"
  $l.Arguments = "`"$dir\$vbs`""
  $l.WorkingDirectory = $dir
  $l.Description = $desc
  $chrome = (Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe" -ErrorAction SilentlyContinue).'(default)'
  if ($chrome) { $l.IconLocation = "$chrome,0" }
  $l.Save()
  Write-Host "Creado: $ruta"
}
# Se instala para el usuario que inició sesión (no para el administrador que elevó).
$usuario = (Get-CimInstance Win32_ComputerSystem).UserName.Split("\")[-1]
$perfil = "C:\Users\$usuario"
$escritorio = [Environment]::GetFolderPath("Desktop")
if ($escritorio -notlike "$perfil*") { $escritorio = "$perfil\Desktop"; if (Test-Path "$perfil\OneDrive\Escritorio") { $escritorio = "$perfil\OneDrive\Escritorio" } elseif (Test-Path "$perfil\OneDrive\Desktop") { $escritorio = "$perfil\OneDrive\Desktop" } }
$inicio = "$perfil\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

Acceso "$inicio\Tablero Transtotal (servidor).lnk" "iniciar-tablero.vbs" "Arranca el servidor del Tablero Transtotal"
Acceso "$escritorio\Tablero Transtotal.lnk" "abrir-tablero.vbs" "Abre el Tablero Transtotal"

if (-not (Get-NetFirewallRule -DisplayName "Tablero Transtotal" -ErrorAction SilentlyContinue)) {
  New-NetFirewallRule -DisplayName "Tablero Transtotal" -Direction Inbound -Protocol TCP -LocalPort 8090 -Action Allow -Profile Private,Domain | Out-Null
  Write-Host "Firewall: puerto 8090 abierto para la red de la oficina."
}

Start-Process "$env:WINDIR\System32\wscript.exe" -ArgumentList "`"$dir\iniciar-tablero.vbs`""
Start-Sleep 3
Write-Host ""
Write-Host "Listo. Desde esta PC: http://localhost:8090"
Write-Host "Desde otra PC de la oficina: http://$env:COMPUTERNAME`:8090"
Read-Host "Enter para cerrar"
