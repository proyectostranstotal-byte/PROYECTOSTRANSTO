# Tablero Transtotal

Artefacto: https://claude.ai/artifact/CKkGt8UCiNGHGtLGCwfAMs (publicado el 22/10/2026 con `capabilities: {db: {}}`).

- `tablero.html`: la página. Se republica con el Artifact tool pasando esa URL.
- `tablero-datos/`: respaldo de la base del artefacto (`areas/`, `tareas/`, `meta/`), un JSON por documento, tal como se cargó el 22/10/2026. Para recargarla en otro artefacto: `ArtifactData` batch de `set` con el id igual al nombre del archivo.

## Tarea programada "Chequeo bots Transtotal"

Se crea desde la app de escritorio en la PC `NDIFABIO` (necesita `device_bash` y las carpetas `C:\jornada-bot`, `C:\SICOP\sicop\whatsapp\logs` y `C:\ExcesosVelocidad\logs` conectadas). Lunes a sábado 14:37 (America/Argentina/Buenos_Aires), modo automático, aviso por push. Prompt:

```
Chequeo diario de los bots y de la flota de Transtotal. Respondé en español y en forma breve.

1. BOTS. Con device_bash, leé las últimas líneas de estos logs (fechas en formato YYYYMMDD):
   - C:\jornada-bot\logs\controlar-excesos_<HOY>.log → OK si contiene "MAIL: enviado". Anotá los excesos de jornada y de manejo.
   - C:\SICOP\sicop\whatsapp\logs\ciclo_<HOY>.log → OK si contiene "Fin del ciclo" y 0 fallidos.
   - C:\jornada-bot\logs\ejecutar_<HOY>.log → OK si contiene "Resumen: N mensajes enviados". Anotá N y la línea "Sin chofer logeado".
   - C:\jornada-bot\logs\recordar-post_<AYER>.log → OK si contiene "Resumen: N recordatorios enviados".
   - El semanal_*.log más reciente en C:\ExcesosVelocidad\logs → OK si es del último lunes y pesa más de 1 KB.
   - C:\ExcesosVelocidad\logs\flota_hoy.json → OK si "generado" tiene menos de 2 horas y "errores" está vacío. Su nombre en la lista es "Export flota (cada hora)".
   Si un log no existe, el estado es "fail". Si existe pero el resultado no es el esperado, el estado es "warn".

2. FLOTA. Con flota_hoy.json y C:\jornada-bot\estado-choferes.json armá una fila por cada unidad de "wialon":
   - cis = los 3 primeros caracteres del nombre.
   - tractor = la patente del objeto de "transdat" cuyo nombre empieza con ese número de cisterna.
   - chofer = nombre en estado-choferes.json buscando por el código iButton con los pares de bytes invertidos (ej. 012C7B0F010000DA → DA0000010F7B2C01). Si el código es todo ceros, va vacío.
   - vel = velocidad.
   - hs = horas desde "ultimo", con un decimal.
   - alerta = "en movimiento sin iButton" si vel > 5 y no hay chofer.
   Ordená: primero las unidades que reportan, al final las de hs > 24.

3. TABLERO. En https://claude.ai/artifact/CKkGt8UCiNGHGtLGCwfAMs, con ArtifactData:
   - set meta/salud: {chequeado: "DD/MM/AAAA HH:MM", items: [{nombre, estado: "ok"|"warn"|"fail", detalle (1 línea)}]}
   - set meta/flota: {generado: "DD/MM/AAAA HH:MM", unidades: [...]}
   - Por cada alerta nueva, creá una tarea en "tareas" con area "operacion", prioridad 1, estado "pendiente" y un "siguiente" concreto. Antes listá las tareas y no dupliques una que ya esté abierta.
   Leé cada documento antes de escribirlo para obtener if_version.

4. AVISO. Si hay algún bot en warn o fail, o alguna alerta de flota, avisá con PushNotification en una línea por problema. Si todo está OK, no avises.
```
