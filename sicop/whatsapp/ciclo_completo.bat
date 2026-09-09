@echo off
REM Ciclo completo: descargar de SICOP, importar, generar cola, enviar WhatsApp,
REM marcar enviados y avisar por mail los que fallaron.
REM Ejecutar desde cualquier lado (usa rutas relativas al .bat).
REM Requiere en el entorno: SICOP_USER, SICOP_PASS, OUTLOOK_USER, OUTLOOK_PASS.
cd /d %~dp0\..\..
if not exist sicop\whatsapp\logs mkdir sicop\whatsapp\logs
for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd"') do set DT=%%I
set LOG=sicop\whatsapp\logs\ciclo_%DT%.log

echo [%date% %time%] Descargando de SICOP e importando...    >> "%LOG%" 2>&1
python -m sicop.actualizar        >> "%LOG%" 2>&1
python -m sicop.generar_cola      >> "%LOG%" 2>&1

echo [%date% %time%] Enviando WhatsApp...                    >> "%LOG%" 2>&1
cd sicop\whatsapp
node enviar.js                    >> "logs\ciclo_%DT%.log" 2>&1
cd ..\..

echo [%date% %time%] Marcando enviados y avisando fallos...  >> "%LOG%" 2>&1
python -m sicop.marcar_enviados   >> "%LOG%" 2>&1
python -m sicop.notificar_fallos  >> "%LOG%" 2>&1
echo Listo. Ver %LOG%
