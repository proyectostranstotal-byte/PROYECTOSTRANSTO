@echo off
rem Corre el servidor del tablero y lo vuelve a arrancar si se corta por cualquier motivo.
rem Solo termina con codigo 0 (otro servidor ya usa el puerto 8090).
cd /d C:\jornada-bot\tablero
:otra
node servidor.js >> C:\jornada-bot\logs\tablero.log 2>&1
set cod=%errorlevel%
if "%cod%"=="0" goto fin
if "%cod%"=="3" goto otra
echo %date% %time% El servidor se corto [codigo %cod%], se vuelve a arrancar en 10 s. >> C:\jornada-bot\logs\tablero.log
ping -n 11 127.0.0.1 >nul
goto otra
:fin
