# Tablero Transtotal

Artefacto: https://claude.ai/artifact/CKkGt8UCiNGHGtLGCwfAMs (publicado el 22/10/2026 con `capabilities: {db: {}}`).

- `tablero.html`: la página. Se republica con el Artifact tool pasando esa URL.
- `tablero-datos/`: respaldo de la base del artefacto (`areas/`, `tareas/`, `meta/`), un JSON por documento, tal como se cargó el 22/10/2026. Para recargarla en otro artefacto: `ArtifactData` batch de `set` con el id igual al nombre del archivo.

## Panel "Mis obligaciones" (23/10/2026)

Colecciones nuevas en la base del artefacto:

- `meta/auditorias`: lo escribe el chequeo de las 08:37 con las 5 unidades a auditar y si están en la base.

- `mes/<AAAA-MM>`: `auditorias` [{cis, fecha}], `hr_m3` y `hr_transoft` {cargadas, total}, `seguridad` {respondido, fecha}, `facturacion` {coincide, excel, enviado, <paso>_fecha}. La página crea el documento del mes la primera vez que se registra algo.
- `excesos/<id>`: {fecha AAAA-MM-DD, chofer, cis, tipo, detalle, comentario, origen}. Un exceso sin comentario queda pendiente; si es de un día anterior, la tarjeta pasa a "Atrasado". Al comentarlo, Nico elige "Justificado" o "Cuenta como falta"; lo segundo crea el documento en `faltas` (campo `falta_id` en el exceso). A los choferes no se les avisa por ahora.
- `faltas/<id>`: {fecha, chofer, falta, avisado, avisado_fecha}. Programa de incentivos desde el 1/11/2026.

Metas: 4 a 5 auditorías por mes. El reporte de seguridad vial no tiene vencimiento. La facturación la hace el sector de facturación; acá solo se controla lo que pasa Air Liquide, se actualiza el Excel con la macro y se envía.

## Tarea programada "Chequeo bots Transtotal"

Se crea desde la app de escritorio en la PC `NDIFABIO` (necesita `device_bash` y las carpetas `C:\jornada-bot`, `C:\SICOP\sicop\whatsapp\logs`, `C:\ExcesosVelocidad\logs` conectadas, más el conector de Google Drive para la planilla de auditorías). Lunes a sábado, cada hora de 08:37 a 15:37 (America/Argentina/Buenos_Aires, cron `37 8-15 * * 1-6`), modo automático, aviso por push. Prompt:

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

2b. EXCESOS (en cada corrida desde las 08:37; solo agrega lo que falte). Abrí C:\jornada-bot\reportes\Control de jornada <AAAA-MM>.xlsx (si está abierto en Excel, copialo antes a una carpeta temporal y leé la copia) y, en la hoja del día anterior (nombre "DD-MM"), tomá cada fila con la columna "Infracciones" no vacía, salvo "SIN_SENAL". Columnas: Cis, Chofer, Inicio, Fin, Hs Jor, Hs Manejo, Bloque max, Descanso, Infracciones, Chk Pre, Chk Post, Comentarios. Si "Infracciones" es "SIN_CHOFER", el chofer va vacío y el tipo es "Sin chofer logueado". Los lunes sumá los excesos de velocidad >80 km/h del último informe semanal de C:\ExcesosVelocidad (tipo "Velocidad", detalle con km/h y lugar). No se avisa nada a los choferes.

2c. AUDITORÍAS (solo en la corrida de las 08:37). Con el conector de Google Drive leé la planilla "RS-SGI-08 Control auditorias a las unidades.xlsx" (id 1ax8jUvaX3NABVuYjT399YO8eNaXwKG1h), hoja "2026 - CP": una fila por tractor o semi (los semis traen la cisterna entre paréntesis, ej. "SVI 393 (538)") y una columna por mes con la fecha de cada auditoría. La auditoría vence a los 2 meses. Dejá afuera las unidades que no operan: 559, 560, 578, 602 y AG990WM. Armá una entrada por cisterna operativa juntando su tractor (la patente que figura en meta/flota) y su semi; los días son los del más atrasado de los dos. Quedate con todas las que superan 60 días (vencidas), ordenadas de más a menos días. Para cada una buscá la posición actual del tractor en Transdat como lo hace auditorias.py (credenciales en C:\ExcesosVelocidad\transdat.json) y la distancia a la base de Transtotal (Ibarlucea, Ruta 34, mismas coordenadas y radio que usa auditorias.py). en_base = está dentro de ese radio.

3. TABLERO. En https://claude.ai/artifact/CKkGt8UCiNGHGtLGCwfAMs, con ArtifactData:
   - Leé primero meta/salud (es el resultado del chequeo anterior; lo necesitás para el paso 4).
   - set meta/salud: {chequeado: "DD/MM/AAAA HH:MM", items: [{nombre, estado: "ok"|"warn"|"fail", detalle (1 línea)}]}
   - set meta/flota: {generado: "DD/MM/AAAA HH:MM", unidades: [...]}
   - Por cada alerta nueva, creá una tarea en "tareas" con area "operacion", prioridad 1, estado "pendiente" y un "siguiente" concreto. Antes listá las tareas y no dupliques una que ya esté abierta.
   - Excesos: por cada fila de 2b, id "x<AAAAMMDD>-<cis>-<primer palabra del chofer en minúsculas, sin acentos>" ("sinchofer" si no hay chofer). Si no existe, set excesos/<id> con {fecha "AAAA-MM-DD", chofer, cis, tipo (texto de Infracciones), detalle "Jornada H:MM h · manejo H:MM h · bloque H:MM h", comentario (columna Comentarios o ""), origen: "reporte jornada"}. Si ya existe y su comentario está vacío pero el Excel tiene comentario, update solo {comentario}. Nunca pises un comentario cargado en el tablero.
   - Auditorías (solo 08:37): set meta/auditorias: {generado: "DD/MM/AAAA HH:MM", ubicacion: true, sugeridas (todas las vencidas): [{tractor ("<patente tractor> + <patente semi>"), cis, ultima "AAAA-MM-DD" o "", dias, vence "AAAA-MM-DD", en_base true/false, dist_km}]}.
   Leé cada documento antes de escribirlo para obtener if_version.

4. AVISO. Si hay algún bot en warn o fail, o alguna alerta de flota, avisá con PushNotification en una línea por problema, pero solo si es nuevo: no repitas un problema que ya figuraba con el mismo estado en el meta/salud anterior ni una alerta de flota que ya tiene tarea abierta. Auditorías (solo 08:37): por cada vencida con en_base true que no figure auditada este mes en mes/<AAAA-MM>, avisá "Auditoría: la <cis> (<patentes>) está en el transporte, vencida hace <dias> días". Si todo está OK o nada cambió, no avises.
```
