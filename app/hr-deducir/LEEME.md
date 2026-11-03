# hr-deducir: qué HR está haciendo cada cisterna

Cruza el plan del distribuidor (mails de Air Liquide) con las paradas satelitales y propone
"unidad → HR probable". Sin IA ni API de pago. Corre en la PC NDIFABIO en `C:\jornada-bot\hr-deducir`.

**Modo sombra** (desde 03/11/2026): calcula y mide aciertos. Única salida al tablero (pedido del usuario 03/11): `C:\jornada-bot\tablero\datos\meta\hr_en_curso.json` con la HR en curso por cisterna (columna HR de "Distribución en vivo"); se apaga con `"escribir_hr_en_curso": false`.

Formato: `{generado, fecha, unidades: {"536": {hr, fuente: plan|recorrido|ambos, confianza 0-1, clientes[], visitados[], producto, detalle, otras_plan?}}}`.
Para mostrarlo: `config.json` → `{"mostrar_en_tablero": true}` (escribe `tablero\datos\hr-probable\<fecha>-<unidad>.json`).

| Archivo | Qué hace |
| --- | --- |
| `leer-cargas.ps1` | Outlook → `mails\AAAAMMDD-HHMMSS_LIN|LOX.txt`. LIN: Tomás Moya, "Hojas de Ruta LIN Transtotal DD-MM-AAAA". LOX: Daniel Castillo, "LOX - TTT …" y "LOX - SEMIS TTT …". Solo lee. |
| `leer_cargas.py` | Grilla del mail → `rutas.json` (por HR: clientes por nº de orden juntando todos los mails, y unidad/tipo por día; el mail más nuevo manda para cada día). "Planta Acindar" = carga para esa HR. |
| `satelital.py` | Transdat (credenciales de `C:\ExcesosVelocidad\transdat.json`, como el panel; NO Wialon) → paradas de 15 min o más fuera de la base → `paradas\<fecha>.json`. |
| `deducir_hr.py` | Puntaje por HR candidata (día anterior, mismo y siguiente; también HR de otras unidades) → `predicciones\<fecha>.json`. |
| `aprender.py` | HR confirmadas en `hr.db` + paradas → `clientes.json` (ubicaciones), `lugares-comunes.json` (planta, paradores) y `aciertos.json` (por semana y confianza). |

Tareas de Windows (`crear-tareas.ps1`): mails cada hora 14:10–20:10; recorrido cada hora 08:20–21:20; noche 22:40.
Log: `C:\jornada-bot\logs\hr-deducir_AAAAMMDD.log`.

Una ubicación se puede fijar a mano en `clientes.json` con `"fijo": true` (aprender no la toca).

Nota (03/11/2026): la copia de la PC tiene su propia versión de satelital.py y en config.json
"transdat_historial" con {id} y {tipo}. La del repo usa {object} y {type}: si se reemplaza
satelital.py por la del repo, borrar "transdat_historial" de config.json.

## HR cerradas que faltan recibir (pedido del usuario 03/11/2026)
`deducir_hr.py` también escribe `C:\jornada-bot\tablero\datos\meta\hr_cerradas.json` cada hora:
`{generado, fecha, faltan_recibir: [{hr, cisterna, cerrada, motivo, producto, evidencia: recorrido|plan, nota}]}`.
Una HR se da por cerrada cuando ya no tiene días en el plan (hoy puede seguir con clientes aunque la
siguiente arranque hoy con la carga) y además la cisterna siguió con otra HR o hay mails más nuevos del
mismo producto que ya no la nombran. Si el plan la pasó de una unidad a otra, vale la del mail más nuevo.
Figura solo si su PDF no está en hr.db. Solo HR desde `cerradas_desde` (28/10/2026). Con evidencia
"plan" (sin recorrido que la confirme) puede ser una HR anulada por Air Liquide. El tablero la muestra en
Novedades para que el usuario se la pida al chofer; el bot no escribe a nadie.
