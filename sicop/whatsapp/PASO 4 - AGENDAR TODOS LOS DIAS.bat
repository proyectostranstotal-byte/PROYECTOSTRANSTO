@echo off
chcp 65001 >nul
title SICOP - Agendar envio diario
echo Voy a agendar el envio automatico TODOS LOS DIAS a las 09:00.
echo (La PC tiene que estar prendida y con internet a esa hora.)
echo.
pause
schtasks /Create /F /TN "SICOP Vencimientos" /TR "cmd /c \"%~dp0ciclo_completo.bat\"" /SC DAILY /ST 09:00
if errorlevel 1 ( echo. & echo No se pudo agendar. Proba abrir este archivo como administrador. & pause & exit /b 1 )
echo.
echo Listo. Quedo agendado como "SICOP Vencimientos" a las 09:00.
echo Para cambiar la hora o sacarlo, busca "Programador de tareas" en Windows.
pause
