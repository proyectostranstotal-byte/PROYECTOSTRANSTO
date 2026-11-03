@echo off
rem Corre el servidor del tablero. Si servidor.js se actualiza, el servidor sale con codigo 3 y se vuelve a arrancar solo.
cd /d C:\jornada-bot\tablero
:otra
node servidor.js >> C:\jornada-bot\logs\tablero.log 2>&1
if %errorlevel%==3 goto otra
