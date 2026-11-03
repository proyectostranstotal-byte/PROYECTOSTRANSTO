@echo off
rem Reinicia el servidor del Tablero Transtotal (por ejemplo, despues de actualizarlo).
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name=node.exe\" | Where-Object { $_.CommandLine -like *servidor.js* } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"
timeout /t 2 /nobreak >nul
wscript "C:\jornada-bot\tablero\iniciar-tablero.vbs"
echo Tablero reiniciado.
timeout /t 3 >nul
