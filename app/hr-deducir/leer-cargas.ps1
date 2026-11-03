# Baja de Outlook los mails de cargas de Air Liquide (LIN y LOX) a texto plano.
# Solo LEE el buzón: no mueve, no marca como leído, no responde.
# Uso: powershell -File leer-cargas.ps1 [-Dias 10]   (primera vez: -Dias 100 para traer desde agosto)
param([int]$Dias = 10)
$ErrorActionPreference = 'Stop'
$base = Split-Path -Parent $MyInvocation.MyCommand.Path
$dir = Join-Path $base "mails"
New-Item -ItemType Directory -Force -Path $dir | Out-Null
$ol = New-Object -ComObject Outlook.Application
$ns = $ol.GetNamespace("MAPI")
$desde = (Get-Date).AddDays(-$Dias).ToString("dd/MM/yyyy HH:mm")
$nuevos = 0
# Bandeja de entrada de todas las cuentas del perfil (por si llega a otra casilla).
foreach ($store in $ns.Stores) {
  try { $inbox = $store.GetDefaultFolder(6) } catch { continue }
  $items = $inbox.Items.Restrict("[ReceivedTime] >= '$desde'")
  foreach ($m in $items) {
    if ($m.Class -ne 43) { continue }   # solo mails
    $asunto = [string]$m.Subject
    if ($asunto -match 'Hojas de Ruta LIN Transtotal') { $prod = 'LIN' }
    elseif ($asunto -match '^\s*(RE:|RV:|FW:)?\s*LOX\s*-\s*(SEMIS\s+)?TTT') { $prod = 'LOX' }
    else { continue }
    $sello = $m.ReceivedTime.ToString("yyyyMMdd-HHmmss")
    $f = Join-Path $dir ("{0}_{1}.txt" -f $sello, $prod)
    if (Test-Path $f) { continue }
    $cab = "#ASUNTO: $asunto`r`n#DE: $($m.SenderName)`r`n#RECIBIDO: $($m.ReceivedTime.ToString('s'))`r`n"
    [IO.File]::WriteAllText($f, $cab + [string]$m.Body, [Text.Encoding]::UTF8)
    $nuevos++
  }
}
Write-Output "$(Get-Date -Format s) mails de cargas nuevos: $nuevos"
