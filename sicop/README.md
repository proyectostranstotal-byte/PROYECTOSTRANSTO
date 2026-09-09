# SICOP · Vencimientos de fleteros

Sistema para **monitorear la documentación** de los fleteros (choferes/proveedores de
transporte) cargados en SICOP (sicop.com.ar) bajo el contratista **TRANSTOTAL SRL**,
cliente **CAFES LA VIRGINIA S.A.**, y avisar cuando la documentación está por vencer.

Fleteros monitoreados (configurables en `fleteros.py`):
BARRIONUEVO CESAR CEFERINO, COSTANZO MATIAS MANUEL, WEGNER CLAUDIO.

## Cómo funciona

1. **Descarga automatizada** (`sicop_client.py`): entra a SICOP y baja el "Estado de
   Situación" (.xlsx) de cada fletero. No usa navegador (el entorno lo bloquea):
   replica el flujo ASP.NET por HTTP. La sesión de SICOP expira rápido, por eso cada
   corrida vuelve a loguearse.
2. **Parseo** (`estado_parser.py`): convierte cada Excel en registros
   `recurso / entidad / identificador / item / fecha_vencimiento / motivo`.
3. **Base de datos** (`db.py`, SQLite en `data/vencimientos.db`): guarda los documentos,
   detecta renovaciones (cambios de fecha) y lleva el estado de los recordatorios.
4. **Recordatorios** (`reminders.py`): 15 días antes del vencimiento genera el aviso;
   si a los 5 días la documentación no se actualizó, lo reenvía; si el vencimiento pasó
   a una fecha más lejana (renovó), marca el recordatorio como resuelto.

## Uso

```bash
export SICOP_USER=...            # o copiar sicop/.env.example -> sicop/.env
export SICOP_PASS=...

# Ciclo completo (descarga + importa + evalúa):
python3 -m sicop.actualizar

# Solo reimportar los .xlsx ya descargados y ver el reporte:
python3 -m sicop.importar

# Exportar la base a CSV legible:
python3 -m sicop.exportar_csv
```

Salidas: `data/vencimientos.db` (base), `data/vencimientos.csv` (planilla),
`data/estados/*.xlsx` (descargas), y la tabla `outbox` con los mensajes a enviar.

## Estado actual

- ✅ Acceso automatizado a SICOP y descarga del Estado de Situación de los 3 fleteros.
- ✅ Base de datos con 61 documentos y sus vencimientos.
- ✅ Motor de recordatorios (15 días / reenvío a los 5 / resolución por renovación).
- ✅ Mensajes generados en la tabla `outbox`.

## Falta definir (2 cosas) para cerrar el envío automático

1. **Canal de envío al chofer.** Hoy los mensajes quedan en `outbox` con
   `canal = pendiente-canal`. Hay que elegir WhatsApp / email / chat de SICOP y
   conectar un servicio autorizado. No se envían mensajes reales a terceros sin eso.
2. **Contacto de cada chofer.** El Estado de Situación no trae teléfono del chofer;
   en la grilla el email figura como el de la empresa (CONTROL@TRANSTOTAL.COM.AR).
   Hay que cargar teléfono/email por fletero en `fleteros.py`.

## Seguridad

- Credenciales **solo** por variable de entorno / `sicop/.env` (ignorado por git).
- `cookies.txt` de sesión: ignorado por git.
- La base contiene datos personales de terceros (CUIT, vencimientos). Repositorio privado.
