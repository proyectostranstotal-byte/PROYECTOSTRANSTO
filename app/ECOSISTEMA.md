# Ecosistema de scripts / bots / automatizaciones — Nico (Transtotal / Air Liquide)

Inventario armado el 2026-10-21 recorriendo: sesiones anteriores de Claude Code, CLAUDE.md de
distintos proyectos, carpetas de trabajo en C:\, P:\ y K:\, y `schtasks` en la PC NDIFABIO
(usuario `ndifabio`). Alcance: solo trabajo. Se excluyó a propósito lo personal (app de
inversiones CEDEARs en C:\Inversiones puerto 8501, "Nutri sync" / C:\Users\NDiFabio\Proyectos\nutri,
"Billetera de Nico" en C:\SICOP\app\billetera.html, MotoGP, etc.), **el sistema de Gestión de
Compras** (`P:\Archivos compartidos Transtotal\Compras`, Django + wsp-bot de WhatsApp para OC:
tiene su propio `CLAUDE.md`/`BITACORA.md` en esa carpeta y se documenta ahí, no en este inventario)
y **GestyaExcesos** (`C:\GestyaExcesos`, excesos de velocidad de cargas generales): pertenece a
otra operativa, fuera de este alcance.

Convención de rutas: "**edita**" = carpeta donde se modifica el código; "**corre**" = carpeta
desde la que se ejecuta en producción. Cuando no hay confirmación de que existe un paso de
publicación/copia entre ambas, se lo marca como pendiente de confirmar.

---

## 1. SICOP — Vencimientos de documentación de fleteros (WhatsApp)

- **Qué hace**: monitorea el vencimiento de documentación de 3 fleteros (Barrionuevo, Costanzo,
  Wegner) cargados en sicop.com.ar bajo TRANSTOTAL SRL / cliente Cafés La Virginia, y avisa por
  WhatsApp 15 días antes (reenvía cada 5 si no se actualiza). Si un WhatsApp falla, manda un mail.
- **Disparo**: tarea programada **"SICOP Vencimientos"**, diaria 09:00, autor N/A (creada sin
  usuario asociado, revisar quién la creó si hay que tocarla), `Detener en batería / no iniciar
  en batería` activo.
- **Ruta y comando**: se edita y corre en `C:\SICOP`.
  - Comando exacto de la tarea: `cmd.exe /c "C:\SICOP\sicop\whatsapp\ciclo_diario.bat"`
    (`Iniciar en`: `C:\SICOP\sicop\whatsapp`).
  - El `.bat` hace: `python -m sicop.ciclo_diario` (descarga si hace falta + evalúa recordatorios)
    → si hay algo para mandar, `node enviar.js` (WhatsApp) → `python -m sicop.marcar_enviados` →
    `python -m sicop.notificar_fallos`.
  - Para re-vincular WhatsApp si se pierde la sesión: `cd C:\SICOP\sicop\whatsapp && npm run auth`
    (sesión propia en `sicop\whatsapp\.wwebjs_auth`, independiente de la del jornada-bot).
- **Credenciales**: `C:\SICOP\sicop\.env` (no versionado) — variables `SICOP_USER`, `SICOP_PASS`
  (login a sicop.com.ar), `OUTLOOK_USER`, `OUTLOOK_PASS` (aviso por mail de fallos vía Outlook,
  opcional `OUTLOOK_SMTP`/`OUTLOOK_PORT`), `AVISO_DESTINO` (hoy `control@transtotal.com.ar`).
  Confirmado que las 5 variables están completas (el ciclo de hoy se ejecutó con éxito).
- **Endpoints/datos**: `sicop.com.ar` (login + descarga de Estado de Situación por fletero, vía
  HTTP directo replicando el flujo ASP.NET, sin navegador). Teléfonos de choferes en
  `C:\SICOP\sicop\data\contactos.json` (no versionado, datos personales).
- **Logs**: `C:\SICOP\sicop\whatsapp\logs\ciclo_YYYYMMDD.log` (uno por día). Confirmado: el de
  hoy (21/10/2026) corrió a las 09:00, bajó los 3 fleteros, generó 6 avisos y los mandó los 6 sin
  fallos ("Listo. Enviados: 6 docs, fallidos: 0"). Base en `C:\SICOP\sicop\data\vencimientos.db`.
- **Estado actual**: **funciona bien**. Nota: el `README.md` dice como pendiente "vincular la
  sesión de WhatsApp" y "cargar credenciales de Outlook", pero eso ya está resuelto en la
  práctica (el log de hoy lo confirma) — el README quedó desactualizado, conviene refrescarlo.

---

## 2. jornada-bot — Control de jornada de choferes (WhatsApp + Wialon + Google Sheets)

Carpeta con más historia y la más compleja del ecosistema: ~20 choferes de cisternas, controla
horas de manejo/descanso contra Wialon (GPS) y un checklist Pre/Post-Viaje en Google Sheets.

### 2.a Jornada bot Diario — aviso de horario de fin de jornada
- **Qué hace**: a las 14:00 consulta Wialon (sesiones activas de cisternas), cruza con el
  checklist Pre-Viaje (Google Sheets) y manda por WhatsApp a cada chofer su hora de inicio y el
  límite de su jornada (12 h, o 10 h si lleva ≥9 días corridos sin descanso de 36 h).
- **Disparo**: tarea **"Jornada bot Diario"**, diaria 14:00:09, autor `TRANSTOTAL\ndifabio`.
- **Comando**: `C:\jornada-bot\ejecutar.bat` (`Iniciar en` `C:\jornada-bot`) → `node index.js`,
  log en `C:\jornada-bot\logs\ejecutar_YYYYMMDD.log`.
- **Estado hoy**: OK — 13 cisternas con actividad, 11 mensajes enviados, 2 sin chofer logueado
  (570, 672, esperable).

### 2.b Jornada bot Post — recordatorio de checklist Post-Viaje
- **Qué hace**: a las 22:00 busca choferes que completaron el Pre-Viaje pero no el Post-Viaje y
  les manda un recordatorio.
- **Disparo**: tarea **"Jornada bot Post"**, diaria 22:00, sin eliminar tarea si dura >15 min.
- **Comando**: `C:\jornada-bot\recordar-post.bat` → `node recordar-post.js`, log en
  `logs\recordar-post_YYYYMMDD.log`.
- **Estado (último run, 20/10)**: OK — 8 recordatorios enviados.

### 2.c Controlar excesos — control diario de jornada/manejo + reporte por mail
- **Qué hace**: a las 08:00 reconstruye la jornada del día anterior por chofer desde Wialon,
  detecta excesos de jornada/manejo y descansos cortos, actualiza
  `C:\jornada-bot\reportes\Control de jornada YYYY-MM.xlsx`, copia el reporte a
  `\\SISTEMAS\USUARIOS\Flor-Vero\Reporte de jornada` y manda un mail de resumen.
- **Disparo**: tarea **"Controlar excesos"**, diaria 08:00, autor `TRANSTOTAL\ndifabio`.
- **Comando**: `C:\jornada-bot\controlar-excesos.bat` → `node exceso-jornada.js` seguido de
  `powershell ... enviar-mail.ps1`, log en `logs\controlar-excesos_YYYYMMDD.log`.
- **Destinatarios del mail**: definidos en `enviar-mail.ps1` / `mail-destinatarios.txt`
  (hoy: cobranzas@, distribucion@, vpiccolo@transtotal.com.ar).
- **Estado (último run, 20/10)**: OK — 17 jornadas registradas, 1 exceso de jornada, mail enviado.

### Infraestructura común de jornada-bot
- **WhatsApp**: `whatsapp-web.js`, sesión en `C:\jornada-bot\.wwebjs_auth` (~580 MB, no
  versionar). Re-vincular con `C:\jornada-bot\auth-whatsapp.bat` si pide QR (ver
  `GUIA-WHATSAPP.md` en la misma carpeta, es la guía de referencia para cualquier bot nuevo de
  WhatsApp del ecosistema).
- **Wialon (GPS)**: token en `C:\jornada-bot\token.js` (no repetir valor). Cisternas operativas
  hardcodeadas en `wialon.js` (lista `CISTERNAS_OPERATIVAS`).
- **Google Sheets (checklist)**: OAuth en `C:\jornada-bot\credentials.json` + token guardado en
  `google-token.json` / `.token`. Re-autenticar con `google-auth.bat`. Si el checklist no se
  puede leer, el bot **aborta el envío entero** (decisión de diseño: evitar falsos negativos).
- **Choferes**: `C:\jornada-bot\choferes.json` (nombre, teléfono, alias Wialon si difiere).
- **Otros scripts en la carpeta**: `rachas.js` (días corridos sin descanso), `checklist.js`
  (lectura del Sheet), `excel-builder.js`/`exportar-jornada12.js` (reportes), y una gran cantidad
  de `debug-*.js` sueltos (herramientas de diagnóstico puntual, no forman parte del flujo
  programado — no hace falta tocarlos).
- **Riesgo conocido** (documentado en `GUIA-WHATSAPP.md`): `whatsapp-web.js` se cuelga seguido;
  el código ya tiene reintentos + watchdogs. Si un día deja de conectar, lo primero es
  `npm update whatsapp-web.js`.

---

## 3. ExcesosVelocidad — Informe semanal Transdat vs SMP (cisternas)

- **Qué hace**: cruza los excesos de velocidad >80 km/h de Transdat (GPS) contra SMP para
  verificarlos, por semana, de la flota de cisternas.
- **Disparo**: tarea **"Excesos velocidad semanal"**, semanal los lunes 07:30.
- **Comando**: `wscript.exe "C:\ExcesosVelocidad\semanal.vbs"` → `semanal.bat` → `node semanal.js`
  (con los `.js` auxiliares `descargar_transdat.js`, `comparar_smp.js`, `excel_smp.js`,
  `analizar_velocidad.js`). Salida de los reportes: `C:\jornada-bot\reportes` (según el comentario
  de la propia tarea programada).
- **Ruta**: se edita y corre en `C:\ExcesosVelocidad`.
- **Credenciales**: `C:\ExcesosVelocidad\transdat.json` (credenciales de la API de Transdat —
  usada también por el script de Auditorías de unidades, ver sección 5) y
  `C:\ExcesosVelocidad\smp_choferes.json` (mapeo de choferes en SMP).
- **Logs**: `C:\ExcesosVelocidad\logs\semanal_YYYYMMDD.log` (uno por lunes).
- **Estado actual**: funciona — último run semanal registrado el lunes 19/10/2026 07:30 con log
  de tamaño normal (~5 KB, run completo). Hay también un `octubre.log` suelto del 20/10 (corrida
  manual, probablemente de prueba) y un `rehacer_semanas.log` grande (recálculo histórico manual).

---

## 4. ControlPesos — Control de pesos M3-KG (cisternas)

- **Qué hace**: reemplaza una planilla Excel de control de pesos/diferencias M3-KG por una app
  Streamlit con base propia; una sola persona carga a la vez, todos consultan y exportan a Excel.
- **Disparo**: dos tareas.
  - **"ControlPesos"** (inicio de sesión): `wscript.exe "C:\ControlPesos\ControlPesos_servicio.vbs"`
    → lanza `ControlPesos_servicio.bat` invisible (probablemente corre `supervisor.py`, que
    relanza la app si se cae).
  - **"ControlPesos"** (segunda entrada, cada 5 min desde las 07:54): mismo `.vbs`, actúa como
    supervisor/keepalive periódico.
- **Ruta**: se edita en `P:\Archivos compartidos Transtotal\NICO\ControlPesos` y corre en
  `C:\ControlPesos` — **no se encontró un script de "publicar" automático** entre ambas copias;
  hay que confirmar con Nico si la sincronización es manual.
- **Base**: `C:\ControlPesos\controlpesos.db` (SQLite, con backups `.bak-FECHA` — **nunca
  borrar**). Respaldo histórico en Excel en `\NICO\Recuperado\` (según `LEEME.txt`).
- **Endpoint**: `http://localhost:8501` según `ControlPesos.bat` — **ojo**: este es el mismo
  puerto que usa la app personal de Inversiones (fuera de alcance); si ambas se ejecutan en la
  misma sesión de Windows puede haber conflicto de puerto. A confirmar.
- **Logs**: `C:\ControlPesos\logs.txt` (con rotación a `.old`).
- **Estado actual**: funciona — logs recientes (20/10) solo muestran warnings de deprecación de
  Streamlit (`use_container_width` → `width`), no errores funcionales.

---

## 5. Auditorías de unidades CP (ALASA / Air Liquide)

- **Qué hace**: reporta qué unidades (tractores) de la operación ALASA están vencidas de
  auditoría (RS-SGI-08, vencen a los 2 meses) y qué tan cerca están de la base (Ibarlucea, Ruta
  34), cruzando PDFs escaneados + Transdat (GPS) + Transoft (con qué semi viaja cada tractor).
- **Disparo**: **manual** (no hay tarea programada con este nombre).
- **Ruta y comando**: `P:\Archivos compartidos Transtotal\NICO\ALASA\AUDITORIAS`, doble clic en
  `Auditorias unidades.bat` → `auditorias.py`.
- **Fuentes de datos**: `unidades_cp.csv` (vigencia + última auditoría), PDFs en
  `ALASA\DOCUMENTOS\<año>\*\NUEVAS`, API de Transdat (`https://clientes.transdat.com.ar`, mismas
  credenciales que ExcesosVelocidad en `C:\ExcesosVelocidad\transdat.json`), y
  `K:\Transoft\Datos\CGRALES\cgviaje1.dbf`.
- **Salida**: reportes Excel en `ALASA\AUDITORIAS\REPORTES`.
- **Unidades excluidas** (hardcoded en el script): AA346VX, AI543TZ, AI543TY (adosados con
  arreglo aparte, según la memoria del proyecto).
- **Estado**: no se pudo confirmar la fecha del último reporte generado sin abrir la carpeta
  `REPORTES` en detalle — pendiente de verificar en persona cuándo se corrió por última vez.

---

## 6. Ordenar HR de ALASA

- **Qué hace**: ordena las hojas de ruta (PDF/foto) de ALASA según estén o no cargadas en
  Transoft (a "general" si están vigentes, a "PENDIENTE" si no tienen carga o está anulada), y
  corre un control mensual (HR cargadas sin archivo, HR duplicadas, cargas en 0 km, HR en más de
  una carpeta).
- **Disparo**: **manual**.
- **Ruta y comando**: `P:\Archivos compartidos Transtotal\NICO\ALASA\DOCUMENTOS`, doble clic en
  `ORDENAR HR.bat` → `ordenar_hr.py`.
- **Estructura de carpetas que usa**: `DOCUMENTOS\<año>\<mes>\` con subcarpetas "general" (con
  carga), "PENDIENTE" (sin carga), "CERRADAS" y "NUEVAS" (no se tocan).
- **Estado**: sin confirmar última corrida (no hay log con fecha visible en esta pasada).

---

## 7. Liquidación ALASA / Air Liquide (transporte, CC-24, Santa Fe)

- **Qué es**: **no es un script automatizado**, es un proceso mensual asistido en Excel: liquida
  el transporte a Air Liquide usando el esquema VAR-FIJO (tarifas 1294/1246), cruza facturas de
  carga contra viajes de Transoft y controla cargas sin facturar.
- **Disparo**: manual, mes a mes, con ayuda de Claude en sesiones puntuales.
- **Ruta de trabajo**: `P:\Archivos compartidos Transtotal\NICO\ALASA\LIQUIDACION\<MES> <AÑO>`
  (carpetas de enero a septiembre 2026 ya generadas) y `P:\Archivos compartidos Transtotal\FACTURACION ALASA`.
  Hay también `P:\Archivos compartidos Transtotal\CITI\LIQUIDACION KM` (planillas de km por
  chofer/mes relacionadas).
- **Fuente de datos de carga/factura**: Transoft vía `K:\Transoft\Datos` (ver sección 10).
- **Estado**: activo y en uso — archivos de septiembre 2026 son los más recientes encontrados.

---

## 8. EstadisticasChoferes (NICO)

- **Qué hace**: cruza HR transcriptas (OCR/manual) + GPS de Transdat (del tractor) + catálogo de
  clientes para ubicar cada parada de un viaje (visita a cliente, parada de combustible, parada
  de descanso) y generar estadísticas/pronósticos por chofer.
- **Disparo**: tiene una app web Flask corriendo (confirmado por `netstat`: puerto **8710**,
  proceso `python.exe app.py` activo al momento de este inventario) — **no se encontró la tarea
  programada que la arranca**; puede estar iniciada manualmente o por un mecanismo no detectado
  en `schtasks`. Pendiente confirmar cómo se levanta tras un reinicio de la PC.
- **Ruta**: `P:\Archivos compartidos Transtotal\NICO\EstadisticasChoferes`
  - App web: subcarpeta `app_choferes\` (`app.py` Flask + `datos.py` + `ejecucion.py` +
    `config.json` + `templates\`).
  - App Android: subcarpeta `app_android\` (proyecto Gradle, `servidor.properties.ejemplo`
    sugiere que necesita apuntar a un servidor — confirmar si es el mismo :8710).
  - Scripts sueltos: `extraer_viajes.py`, `detectar_visitas.py`, `ubicar_clientes_hr.py`,
    `etiquetar_sitios.py`, `pronostico_semana.py`.
- **Datos**: `estadisticas.db` (SQLite), `clientes_coordenadas.csv`, `hr_transcriptas_<mes>_NN.json`
  (muchos archivos, uno por tanda), caché de GPS en `cache\gps_*.json`.
- **Endpoint**: `http://localhost:8710`.
- **Logs**: `corrida.log` en la misma carpeta — última corrida visible: 1780 renglones de HR,
  1530 ubicados por GPS, 273 clientes en catálogo. Parece funcionar correctamente.
- **Estado**: activo y respondiendo en :8710 al momento de este inventario.

---

## 9. Transoft / FoxPro DBF — fuente de datos base

- **Qué es**: no es una automatización en sí, es la base de datos operativa de Transtotal
  (sistema Transoft, FoxPro) de la que casi todos los sistemas anteriores leen (viajes, cargas,
  choferes, facturación).
- **Ubicación**: `K:\Transoft\Datos` (confirmado que existe). Carpeta clave `CGRALES\cgviaje1.dbf`
  (viajes: CAMION + FECVIAJE → CHRESUM/chofer). Se lee con `dbfread`, encoding **latin1**.
  `NROGEN` es la FK interna; `NROCAR`/`NROVIA` son los números visibles. La factura de carga
  sale de `cgvalcar.FACNRO` → `FACCOB`/`comprob`. Proveedores y cuenta corriente de compras en
  `PROVEED`.
- **Herramientas de acceso/automatización de la UI de Transoft** (no de la base, sino de la
  app FoxPro en sí, vía AutoHotkey): `C:\Users\NDiFabio\Documents\transoft-auto\` —
  `cargar_viaje.py`/`viaje.ahk` (carga viajes por UI), `reconciliar.py`/`reconciliar.bat`
  (reconciliación de 5 fuentes: choferes, pesos, Drive AL, carpeta AL, Transoft — carpeta
  `reconcilia\`), `buscar_cliente.py`, `verificar_hr_transoft.py`. **Disparo manual**, no hay
  tarea programada detectada con "reconcilia" o "transoft" en el nombre. Último archivo de
  reconciliación generado: `reconciliacion_2026-05.xlsx` (06/06/2026) — no se encontró evidencia
  de que se haya vuelto a correr desde entonces; confirmar con Nico si sigue en uso.
- **Guía de referencia**: `C:\Users\NDiFabio\Desktop\Transoft_guia_Claude.md` y
  `P:\Archivos compartidos Transtotal\NICO\Transoft - guia de acceso a la base.md`.

---

## 10. Control de km de choferes — NO CONFIRMADO en esta pasada

La memoria previa (`control-km-choferes-cp.md` y `control-km-choferes-generales.md`) describe
dos procesos mensuales: comparar liquidación/pase/firma/recibos con un script `control_km_cp.py`
(CP) y armar la planilla de firma desde "KMS 2026 (CITI)" + recibos para cargas generales.
**No pude localizar `control_km_cp.py` en esta recorrida** (no está en `C:\jornada-bot`,
`C:\ControlPesos`, `C:\ExcesosVelocidad`, `C:\GestyaExcesos`, `C:\SICOP`, `C:\Users\NDiFabio\Documents`
ni en `P:\Archivos compartidos Transtotal\NICO` de primer nivel). Puede estar en una subcarpeta
de `P:\Archivos compartidos Transtotal\NICO\CITI` o en `P:\CITI\LIQUIDACION KM` (carpetas que
existen y no se recorrieron en profundidad por tiempo). **Pendiente**: ubicarlo antes de tocarlo;
no asumir que sigue en la misma ruta que indica la memoria vieja.

---

## 11. Carpetas con planillas .xlsx sin script asociado (mencionadas aparte)

- `P:\Archivos compartidos Transtotal\NICO\IMSEG.xlsx`, `Chasis unidades - Transoft.xlsx`,
  `Estadisticas de exceso.xlsx`, `Indicadores Seguridad Vial Marzo 2026.xlsx` — planillas de
  trabajo manual, no tienen script que las genere/actualice.
- `P:\Archivos compartidos Transtotal\NICO\Programa de incentivos\` — relacionado con
  `C:\jornada-bot\programa-incentivos.js`, confirmar si ese script se usa activamente o quedó de
  prueba (no está en ninguna tarea programada).
- `C:\MiOrg\` (backend/frontend) — carpetas vacías (solo `frontend\icons`), parece un scaffold
  sin desarrollar; no se encontró código. Si no se está usando, no hace falta documentarlo más.

---

## 12. Datos de referencia (carpetas, sin automatización todavía) — Paso 4

| Qué | Dónde |
|---|---|
| HR de choferes ALASA (general/PENDIENTE/CERRADAS/NUEVAS por mes) | `P:\Archivos compartidos Transtotal\NICO\ALASA\DOCUMENTOS\<año>\<mes>\` |
| Auditorías de unidades (PDFs escaneados) | `P:\Archivos compartidos Transtotal\NICO\ALASA\AUDITORIAS\REPORTES` |
| Liquidación mensual Air Liquide | `P:\Archivos compartidos Transtotal\NICO\ALASA\LIQUIDACION\<MES> <AÑO>` |
| Facturación ALASA | `P:\Archivos compartidos Transtotal\FACTURACION ALASA` |
| Km por chofer/mes (CITI) | `P:\Archivos compartidos Transtotal\CITI\LIQUIDACION KM` |
| Planillas de control de pesos / desvíos / excesos (Desktop) | `C:\Users\NDiFabio\Desktop\LOGISTICA - NICO\` |
| Base operativa Transoft (DBF FoxPro) | `K:\Transoft\Datos` (subcarpeta clave `CGRALES`) |
| HR transcriptas / estadísticas choferes | `P:\Archivos compartidos Transtotal\NICO\EstadisticasChoferes` |
| Reportes de jornada (choferes cisterna) | `C:\jornada-bot\reportes\` y copia en `\\SISTEMAS\USUARIOS\Flor-Vero\Reporte de jornada` |
| Scans varios (certificados, HR) sin proceso asociado | `C:\Users\NDiFabio\Desktop\ESCANER\` |

---

## Chequeos de salud

| Sistema | Qué mirar | Dónde | Resultado esperado |
|---|---|---|---|
| SICOP Vencimientos | Último log del día | `C:\SICOP\sicop\whatsapp\logs\ciclo_YYYYMMDD.log` | Termina en "Fin del ciclo" sin "fallidos" > 0 |
| Jornada bot Diario | Log del día, hora ~14:00 | `C:\jornada-bot\logs\ejecutar_YYYYMMDD.log` | Termina con "Resumen: N mensajes enviados" |
| Jornada bot Post | Log del día, hora ~22:00 | `C:\jornada-bot\logs\recordar-post_YYYYMMDD.log` | "Resumen: N recordatorios enviados" |
| Controlar excesos (jornada) | Log del día, hora ~08:00 | `C:\jornada-bot\logs\controlar-excesos_YYYYMMDD.log` | Termina con "MAIL: enviado a ..." |
| ExcesosVelocidad semanal | Log del último lunes | `C:\ExcesosVelocidad\logs\semanal_YYYYMMDD.log` | Archivo de varios KB (no vacío/chico) |
| ControlPesos | App respondiendo | `http://localhost:8501` (¡puede chocar con la app de Inversiones personal!) | Carga la interfaz Streamlit |
| EstadisticasChoferes | App respondiendo | `http://localhost:8710` | Carga la interfaz |
| Scheduled tasks en general | Último resultado = 0 | PowerShell: `schtasks /query /fo LIST /v` y filtrar por el nombre de la tarea | "Último resultado: 0" en cada una |

### Resumen de estado al 21/10/2026
- **Funcionando bien**: SICOP Vencimientos, jornada-bot (las 3 tareas), ExcesosVelocidad semanal,
  ControlPesos, EstadisticasChoferes (proceso corriendo).
- **Sin automatizar / manual**: Liquidación ALASA, Auditorías de unidades, Ordenar HR, Transoft
  reconciliación (transoft-auto).
- **Sin confirmar en esta pasada**: ubicación de `control_km_cp.py`, última corrida de
  Auditorías/Ordenar HR, cómo se levanta EstadisticasChoferes tras un reinicio.
