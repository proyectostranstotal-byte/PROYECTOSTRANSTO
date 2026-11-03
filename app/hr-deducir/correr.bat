@echo off
rem Uso: correr.bat mails | deducir | noche
cd /d C:\jornada-bot\hr-deducir
if not exist C:\jornada-bot\logs mkdir C:\jornada-bot\logs
set LOG=C:\jornada-bot\logs\hr-deducir_%date:~-4%%date:~3,2%%date:~0,2%.log
echo ==== %date% %time% %1 >> "%LOG%"
if /i "%1"=="mails" (
  powershell -NoProfile -ExecutionPolicy Bypass -File leer-cargas.ps1 >> "%LOG%" 2>&1
  python leer_cargas.py --rutas >> "%LOG%" 2>&1
)
if /i "%1"=="deducir" python deducir_hr.py >> "%LOG%" 2>&1
if /i "%1"=="noche" (
  powershell -NoProfile -ExecutionPolicy Bypass -File leer-cargas.ps1 >> "%LOG%" 2>&1
  python leer_cargas.py --rutas >> "%LOG%" 2>&1
  python deducir_hr.py %2 >> "%LOG%" 2>&1
  python aprender.py >> "%LOG%" 2>&1
)
