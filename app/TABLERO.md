# Tablero Transtotal

Artefacto: https://claude.ai/artifact/CKkGt8UCiNGHGtLGCwfAMs (publicado el 22/10/2026 con `capabilities: {db: {}}`).

- `tablero.html`: la página. Se republica con el Artifact tool pasando esa URL.
- `tablero-datos/`: respaldo de la base del artefacto (`areas/`, `tareas/`, `meta/`), un JSON por documento, tal como se cargó el 22/10/2026. Para recargarla en otro artefacto: `ArtifactData` batch de `set` con el id igual al nombre del archivo.

## Panel "Mis obligaciones" (23/10/2026)

Colecciones nuevas en la base del artefacto:

- `mes/<AAAA-MM>`: `auditorias` [{cis, fecha}], `hr_m3` y `hr_transoft` {cargadas, total}, `seguridad` {respondido, fecha}, `facturacion` {coincide, excel, enviado, <paso>_fecha}. La página crea el documento del mes la primera vez que se registra algo.
- `excesos/<id>`: {fecha AAAA-MM-DD, chofer, cis, tipo, detalle, comentario, origen}. Un exceso sin comentario queda pendiente; si es de un día anterior, la tarjeta pasa a "Atrasado".
- `faltas/<id>`: {fecha, chofer, falta, avisado, avisado_fecha}. Programa de incentivos desde el 1/11/2026.

Metas: 4 a 5 auditorías por mes. El reporte de seguridad vial no tiene vencimiento. La facturación la hace el sector de facturación; acá solo se controla lo que pasa Air Liquide, se actualiza el Excel con la macro y se envía.

## Tarea programada "Chequeo bots Transtotal"

Se crea desde la app de escritorio en la PC `NDIFABIO` (necesita `device_bash` y las carpetas `C:\jornada-bot`, `C:\SICOP\sicop\whatsapp\logs` y `C:\ExcesosVelocidad\logs` conectadas). Lunes a sábado, cada hora de 08:37 a 15:37 (America/Argentina/Buenos_Aires, cron `37 8-15 * * 1-6`), modo automático, aviso por push. Prompt:

```
Chequeo de los bots y de la flota de Transtotal (corre cada hora, de 08:37 a 15:37). Respondé en español y en forma breve.

1. BOTS. Con device_bash, leé las últimas líneas de estos logs (fechas en formato YYYYMMDD):
   - C:\jornada-bot\logs\controlar-excesos_<HOY>.log → OK si contiene "MAIL: enviado". Anotá los excesos de jornada y de manejo.
   - C:\SICOP\sicop\whatsapp\logs\ciclo_<HOY>.log → OK si contiene "Fin del ciclo" y 0 fallidos.
   - C:\jornada-bot\logs\ejecutar_<HOY>.log → OK si contiene "Resumen: N mensajes enviados". Anotá N y la línea "Sin chofer logeado".
   - C:\jornada-bot\logs\recordar-post_<AYER>.log → OK si contiene "Resumen: N recordatorios enviados".
   - El semanal_*.log más reciente en C:\ExcesosVelocidad\logs → OK si es del último lunes y pesa más de 1 KB.
   - C:\ExcesosVelocidad\logs\flota_hoy.json → OK si "generado" tiene menos de 2 horas y "errores" está vacío. Su nombre en la lista es "Export flota (cada hora)".
   Si un log no existe, el estado es "fail". Si existe pero el resultado no es el esperado, el estado es "warn".
   Excepción: si la hora programada del bot todavía no pasó hoy (Controlar excesos 08:00, SICOP 09:00, Jornada bot Diario 14:00), o pasó hace menos de 30 minutos y el log existe pero no terminó, el estado es "ok" con detalle "todavía no corrió hoy" / "en ejecución", y no cuenta como problema.

2. FLOTA. Con flota_hoy.json y C:\jornada-bot\estado-choferes.json armá una fila por cada unidad de "wialon":
   - cis = los 3 primeros caracteres del nombre.
   - tractor = la patente del objeto de "transdat" cuyo nombre empieza con ese número de cisterna.
   - chofer = nombre en estado-choferes.json buscando por el código iButton con los pares de bytes invertidos (ej. 012C7B0F010000DA → DA0000010F7B2C01). Si el código es todo ceros, va vacío.
   - vel = velocidad.
   - hs = horas desde "ultimo", con un decimal.
   - alerta = "en movimiento sin iButton" si vel > 5 y no hay chofer.
   Ordená: primero las unidades que reportan, al final las de hs > 24.

3. TABLERO. En https://claude.ai/artifact/CKkGt8UCiNGHGtLGCwfAMs, con ArtifactData:
   - Leé primero meta/salud (es el resultado del chequeo anterior; lo necesitás para el paso 4).
   - set meta/salud: {chequeado: "DD/MM/AAAA HH:MM", items: [{nombre, estado: "ok"|"warn"|"fail", detalle (1 línea)}]}
   - set meta/flota: {generado: "DD/MM/AAAA HH:MM", unidades: [...]}
   - Por cada alerta nueva, creá una tarea en "tareas" con area "operacion", prioridad 1, estado "pendiente" y un "siguiente" concreto. Antes listá las tareas y no dupliques una que ya esté abierta.
   Leé cada documento antes de escribirlo para obtener if_version.

4. AVISO. Si hay algún bot en warn o fail, o alguna alerta de flota, avisá con PushNotification en una línea por problema, pero solo si es nuevo: no repitas un problema que ya figuraba con el mismo estado en el meta/salud anterior ni una alerta de flota que ya tiene tarea abierta. Si todo está OK o nada cambió, no avises.
```
