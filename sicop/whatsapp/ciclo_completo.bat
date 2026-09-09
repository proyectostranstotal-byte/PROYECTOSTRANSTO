@echo off
REM Ciclo completo: descargar de SICOP, importar, generar cola y enviar por WhatsApp.
REM Ejecutar desde la raíz del repo. Requiere SICOP_USER / SICOP_PASS en el entorno.
cd /d %~dp0\..\..
if not exist sicop\whatsapp\logs mkdir sicop\whatsapp\logs
for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd"') do set DT=%%I

echo [%date% %time%] Descargando de SICOP e importando...
python -m sicop.actualizar        >> "sicop\whatsapp\logs\ciclo_%DT%.log" 2>&1
python -m sicop.generar_cola      >> "sicop\whatsapp\logs\ciclo_%DT%.log" 2>&1

echo [%date% %time%] Enviando WhatsApp...
cd sicop\whatsapp
node enviar.js                    >> "logs\ciclo_%DT%.log" 2>&1
cd ..\..

echo [%date% %time%] Marcando enviados...
python -m sicop.marcar_enviados   >> "sicop\whatsapp\logs\ciclo_%DT%.log" 2>&1
echo Listo. Ver sicop\whatsapp\logs\ciclo_%DT%.log
