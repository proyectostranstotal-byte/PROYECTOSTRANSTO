@echo off
chcp 65001 >nul
title SICOP - Prueba (un solo chofer)
echo Prueba: manda SOLO a Wegner, para verificar antes del envio completo.
echo.
cd /d "%~dp0\..\.."
python -m sicop.actualizar
python -m sicop.generar_cola
cd /d "%~dp0"
set CHOFER_TEST=wegner
node enviar.js
echo.
echo (No marca como enviado ni avisa fallos: es solo una prueba.)
pause
