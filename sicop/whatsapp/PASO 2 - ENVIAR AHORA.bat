@echo off
chcp 65001 >nul
title SICOP - Enviar recordatorios ahora
echo ============================================================
echo   Descargando de SICOP y enviando los recordatorios...
echo ============================================================
echo.
cd /d "%~dp0\..\.."
python -m sicop.actualizar
python -m sicop.generar_cola
cd /d "%~dp0"
node enviar.js
cd /d "%~dp0\..\.."
python -m sicop.marcar_enviados
python -m sicop.notificar_fallos
echo.
echo ============================================================
echo   Terminado.
echo ============================================================
pause
