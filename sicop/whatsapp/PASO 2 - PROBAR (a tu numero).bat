@echo off
chcp 65001 >nul
title SICOP - Prueba a tu propio numero
echo Esta prueba te manda UN WhatsApp a TU numero (no a un chofer).
echo Asi verificas que quedo bien vinculado, sin molestar a nadie.
echo.
cd /d "%~dp0"
node probar.js
echo.
pause
