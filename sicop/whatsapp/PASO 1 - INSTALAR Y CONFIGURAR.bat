@echo off
chcp 65001 >nul
title SICOP - Paso 1: Instalar y configurar
echo ============================================================
echo   PASO 1 - Instalar, cargar claves y vincular WhatsApp
echo ============================================================
echo.
echo Voy a: (1) instalar lo necesario, (2) pedirte las contrasenas,
echo (3) mostrarte el codigo QR para vincular el WhatsApp.
echo.
pause

cd /d "%~dp0"
echo.
echo --- Instalando (puede tardar unos minutos la primera vez) ---
call npm install
if errorlevel 1 ( echo. & echo ERROR instalando. Revisa que Node.js este instalado. & pause & exit /b 1 )

echo.
echo --- Cargar contrasenas ---
cd /d "%~dp0\..\.."
python -m sicop.configurar
if errorlevel 1 ( echo. & echo ERROR configurando. Revisa que Python este instalado. & pause & exit /b 1 )

echo.
echo --- Vincular WhatsApp: escanea el QR con el telefono de ESE numero ---
echo (WhatsApp - Dispositivos vinculados - Vincular dispositivo)
echo Despues de escanear, ESPERA hasta que diga "Listo".
echo.
cd /d "%~dp0"
call npm run auth

echo.
echo ============================================================
echo   Listo el Paso 1. Ya podes usar "PASO 2 - ENVIAR AHORA".
echo ============================================================
pause
