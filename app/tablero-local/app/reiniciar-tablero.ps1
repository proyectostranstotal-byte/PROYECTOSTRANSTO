# Reinicia el servidor del Tablero Transtotal (por ejemplo, después de actualizarlo).
$p = Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine -like '*servidor.js*' }
$p | ForEach-Object { Stop-Process -Id $_.ProcessId -Force; Write-Host "Detenido el proceso $($_.ProcessId)" }
Start-Sleep 2
Start-Process "$env:WINDIR\System32\wscript.exe" -ArgumentList '"C:\jornada-bot\tablero\iniciar-tablero.vbs"'
Write-Host "Tablero reiniciado."
Start-Sleep 3
