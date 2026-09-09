# SICOP · Vencimientos de fleteros + aviso por WhatsApp

Sistema para **monitorear la documentación** de los fleteros (choferes/proveedores de
transporte) cargados en SICOP (sicop.com.ar) bajo el contratista **TRANSTOTAL SRL**,
cliente **CAFES LA VIRGINIA S.A.**, y **avisar por WhatsApp** cuando la documentación
está por vencer.

Fleteros monitoreados (configurables en `fleteros.py`):
BARRIONUEVO CESAR CEFERINO, COSTANZO MATIAS MANUEL, WEGNER CLAUDIO.

## Cómo funciona

1. **Descarga automatizada** (`sicop_client.py`): entra a SICOP y baja el "Estado de
   Situación" (.xlsx) de cada fletero. No usa navegador: replica el flujo ASP.NET por
   HTTP. La sesión de SICOP expira rápido, por eso reintenta con re-login.
2. **Parseo** (`estado_parser.py`): convierte cada Excel en registros
   `recurso / entidad / identificador / item / fecha_vencimiento / motivo`.
3. **Base de datos** (`db.py`, SQLite en `data/vencimientos.db`): documentos, snapshots,
   recordatorios y `outbox`. Detecta renovaciones (cambios de fecha).
4. **Recordatorios** (`reminders.py`): 15 días antes del vencimiento genera el aviso;
   si a los 5 días no se actualizó, lo reenvía; si el documento se renovó, lo resuelve.
5. **Envío por WhatsApp** (`whatsapp/`, Node + `whatsapp-web.js`): agrupa los avisos
   pendientes por chofer en un solo mensaje y los manda por WhatsApp Web.
6. **Aviso por mail de fallos** (`notificar_fallos.py` + `mailer.py`): si un WhatsApp
   no se pudo enviar (número sin WhatsApp, sesión caída, sin teléfono), manda un mail
   a `control@transtotal.com.ar` desde la cuenta de Outlook avisando, con el texto
   que debía enviarse, para contactar al chofer por otro medio.

## Arquitectura de dos partes

- **Python** (descarga + base + recordatorios): corre donde haya red. Produce
  `data/cola_whatsapp.json` con los mensajes a enviar.
- **Node/WhatsApp** (`whatsapp/enviar.js`): **corre en la PC que tiene la sesión de
  WhatsApp vinculada** (igual que el bot de jornada). Lee la cola, envía, y escribe
  `data/resultado_whatsapp.json`. Después Python marca los enviados.

> El envío NO puede correr en el contenedor de Claude: `whatsapp-web.js` necesita un
> Chrome con la sesión del teléfono (QR escaneado una vez) y una PC prendida.

## Puesta en marcha (una vez)

```bash
# 1. Credenciales de SICOP
cp sicop/.env.example sicop/.env          # y completar SICOP_USER / SICOP_PASS
#    (o export SICOP_USER=... ; export SICOP_PASS=...)

# 2. Teléfonos de los choferes
cp sicop/whatsapp/contactos.example.json sicop/data/contactos.json   # y cargar teléfonos

# 3. WhatsApp: instalar y vincular (escanear QR una sola vez)
cd sicop/whatsapp
npm install
npm run auth                              # escanear el QR con el teléfono
```

La sesión de WhatsApp de este proyecto es **independiente** (vive en
`sicop/whatsapp/.wwebjs_auth`), así que podés vincular un número distinto al del bot
de jornada sin que se pisen.

Para el aviso por mail, configurar además `OUTLOOK_USER` / `OUTLOOK_PASS` en
`sicop/.env` (ver `.env.example`).

Formato de teléfono en `contactos.json`: solo los **10 dígitos** (sin 0, sin 15).
El `549` y el sufijo `@c.us` los arma el código.

## Uso diario

```bash
export SICOP_USER=... ; export SICOP_PASS=...

python3 -m sicop.actualizar        # descarga de SICOP + importa + evalúa recordatorios
python3 -m sicop.generar_cola      # arma data/cola_whatsapp.json (agrupado por chofer)

cd sicop/whatsapp
CHOFER_TEST=costanzo node enviar.js  # PRUEBA: solo a los que matcheen (obligatorio la 1ra vez)
node enviar.js                       # envío real
cd ../..

python3 -m sicop.marcar_enviados   # marca en la base los efectivamente enviados
python3 -m sicop.notificar_fallos  # avisa por mail los que no se pudieron enviar
```

En Windows, `sicop/whatsapp/ciclo_completo.bat` hace todo el ciclo; agendalo en el
Programador de tareas (una vez por día), con "ejecutar aunque el usuario no inicie
sesión" y "ejecutar lo antes posible si se perdió una ejecución".

Reportes: `python3 -m sicop.importar` (resumen en pantalla) y
`python3 -m sicop.exportar_csv` (`data/vencimientos.csv`).

## Estado actual

- ✅ Acceso automatizado a SICOP y descarga del Estado de Situación de los 3 fleteros.
- ✅ Base con 61 documentos y sus vencimientos.
- ✅ Motor de recordatorios (15 días / reenvío a los 5 / resolución por renovación).
- ✅ Envío por WhatsApp integrado (whatsapp-web.js, con reintentos y modo prueba).
- ✅ Teléfonos de los 3 choferes cargados en `data/contactos.json` (local, no versionado).
- ✅ Aviso por mail a `control@transtotal.com.ar` cuando un WhatsApp falla.
- ⏳ **Falta** vincular la sesión de WhatsApp en la PC (`npm run auth`) y cargar las
  credenciales de Outlook para el aviso por mail.

## Seguridad y datos

- Credenciales SICOP: solo por entorno / `sicop/.env` (ignorado por git).
- Sesión de WhatsApp (`.wwebjs_auth`, ~580 MB) y `node_modules`: ignorados por git.
- `data/` (base, planillas, contactos, cookies) no se versiona: tiene datos personales
  de terceros y es regenerable. El repo ya tenía esa política para `*.xlsx`/`*.csv`.

## Anti-baneo (WhatsApp)

Ver la guía original. En resumen: 3 s entre mensajes, volumen bajo (una vez por día),
solo contactos reales, mensajes distintos por destinatario, y usar un número dedicado
(no el personal). Un ban cae sobre el número, no sobre el código.
