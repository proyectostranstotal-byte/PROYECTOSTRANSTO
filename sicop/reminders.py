"""Motor de recordatorios de vencimiento.

Reglas:
  - Ventana de aviso: 15 días antes del vencimiento (incluye ya vencidos).
  - Al detectar un documento en ventana y sin aviso vigente: se genera el 1er mensaje.
  - Reenvío: cada 5 días se re-evalúa; si el documento NO se actualizó
    (misma fecha de vencimiento, no resuelto), se reenvía el mensaje.
  - Resolución: si en una importación posterior el vencimiento pasó a una fecha
    más lejana (renovó), el recordatorio se marca 'resuelto' y deja de avisar.
"""
import datetime
from . import db as dbm

DIAS_AVISO = 15
DIAS_REENVIO = 5

# No molestar por estos documentos (coincidencia por texto, sin distinguir may/min).
# Ej.: la patente es un impuesto del vehículo que no se persigue como los papeles de
# cumplimiento (ART, libreta, seguros).
ITEMS_IGNORADOS = ['patente']

# Vencidos "muy viejos": si pasó más de esto desde el vencimiento, se desestima
# (se asume abandonado/gestionado por fuera). Los vencidos recientes siguen avisando.
DIAS_VENCIDO_MAX = 365


def ignorar(item, dias):
    it = (item or '').lower()
    if any(k in it for k in ITEMS_IGNORADOS):
        return True
    if dias is not None and dias < -DIAS_VENCIDO_MAX:
        return True
    return False

def _d(iso):
    return datetime.date.fromisoformat(iso) if iso else None

def marcar_resoluciones(con, cambios):
    """cambios: [(doc_key, fecha_prev, fecha_nueva)]. Si la nueva es más lejana, resolver."""
    for doc_key, prev, nueva in cambios:
        if prev and nueva and _d(nueva) > _d(prev):
            con.execute("UPDATE recordatorios SET estado='resuelto' WHERE doc_key=?", (doc_key,))
    con.commit()

def mensaje(chofer, item, entidad, fecha_iso, dias):
    f = _d(fecha_iso)
    fstr = f.strftime('%d/%m/%Y') if f else 'sin fecha'
    detalle = f"{item}" + (f" ({entidad})" if entidad and entidad != chofer else "")
    if dias is None:
        return f"Hola {chofer}: figura sin fecha el vencimiento de {detalle}. Por favor regularizá la documentación en SICOP."
    if dias < 0:
        return (f"Hola {chofer}: {detalle} está VENCIDO desde el {fstr} (hace {-dias} días). "
                f"Enviá la documentación actualizada con urgencia.")
    return (f"Hola {chofer}: te faltan {dias} días para el vencimiento de {detalle} (vence el {fstr}). "
            f"Enviá la documentación actualizada cuanto antes.")

def evaluar(con, today=None, destino_por_fletero=None):
    """Devuelve lista de recordatorios a enviar hoy y actualiza estado + outbox."""
    today = today or datetime.date.today()
    destino_por_fletero = destino_por_fletero or {}
    a_enviar = []
    docs = con.execute("SELECT * FROM documentos").fetchall()
    for doc in docs:
        fv = _d(doc['fecha_vencimiento'])
        dias = (fv - today).days if fv else None
        # ventana: vencido o vence dentro de DIAS_AVISO. (sin fecha => avisar también)
        en_ventana = (dias is None) or (dias <= DIAS_AVISO)
        if not en_ventana:
            continue
        if ignorar(doc['item'], dias):
            continue
        key = f"{doc['fletero_cuit']}|{doc['recurso']}|{doc['identificador']}|{doc['item']}"
        rec = con.execute("SELECT * FROM recordatorios WHERE doc_key=?", (key,)).fetchone()
        if rec and rec['estado'] == 'resuelto' and rec['fecha_venc_notificada'] == doc['fecha_vencimiento']:
            continue
        # ¿toca enviar?
        enviar = False
        if not rec or rec['veces_enviado'] == 0:
            enviar = True
        else:
            ult = _d(rec['ultimo_envio'])
            venc_cambio = rec['fecha_venc_notificada'] != doc['fecha_vencimiento']
            if venc_cambio and fv and rec['fecha_venc_notificada'] and fv > _d(rec['fecha_venc_notificada']):
                enviar = False  # renovó: no reenviar
            elif ult and (today - ult).days >= DIAS_REENVIO:
                enviar = True
        if not enviar:
            continue
        chofer = doc['fletero']
        msg = mensaje(chofer, doc['item'], doc['entidad'], doc['fecha_vencimiento'], dias)
        destino = destino_por_fletero.get(doc['fletero_cuit'])
        canal = 'pendiente-canal' if not destino else destino.get('canal', 'pendiente-canal')
        dest = '' if not destino else destino.get('destino', '')
        # upsert recordatorio
        con.execute("""
          INSERT INTO recordatorios (doc_key,fletero,item,entidad,fecha_venc_notificada,ultimo_envio,veces_enviado,estado)
          VALUES (?,?,?,?,?,?,1,'avisado')
          ON CONFLICT(doc_key) DO UPDATE SET
            fecha_venc_notificada=excluded.fecha_venc_notificada,
            ultimo_envio=excluded.ultimo_envio,
            veces_enviado=recordatorios.veces_enviado+1,
            estado='avisado'
        """, (key, chofer, doc['item'], doc['entidad'], doc['fecha_vencimiento'], today.isoformat()))
        con.execute("INSERT INTO outbox (creado_en,fletero,doc_key,canal,destino,mensaje,estado) VALUES (?,?,?,?,?,?, 'pendiente')",
                    (datetime.datetime.now().isoformat(timespec='seconds'), chofer, key, canal, dest, msg))
        a_enviar.append({'fletero': chofer, 'item': doc['item'], 'entidad': doc['entidad'],
                         'vence': doc['fecha_vencimiento'], 'dias': dias, 'mensaje': msg})
    con.commit()
    return a_enviar
