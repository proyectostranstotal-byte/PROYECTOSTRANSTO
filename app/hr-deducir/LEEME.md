# hr-deducir: qué HR está haciendo cada cisterna

Cruza el plan del distribuidor (mails de Air Liquide) con las paradas satelitales y propone
"unidad → HR probable". Sin IA ni API de pago. Corre en la PC NDIFABIO en `C:\jornada-bot\hr-deducir`.

**Modo sombra** (desde 03/11/2026): calcula y mide aciertos, no escribe en el tablero.
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
