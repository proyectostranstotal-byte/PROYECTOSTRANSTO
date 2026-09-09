"""Arma la cola de mensajes de WhatsApp a partir de la tabla outbox.

Agrupa los recordatorios pendientes por chofer en UN mensaje (menos spam, menos
riesgo de baneo) y le suma el teléfono desde contactos.json. Escribe
data/cola_whatsapp.json, que consume sicop/whatsapp/enviar.js.

Contactos: data/contactos.json (no versionado). Estructura:
    [{ "cuit": "...", "nombre": "...", "telefono": "3415551234" }]
"""
import os, json, datetime
from . import db as dbm

DATA = os.path.join(os.path.dirname(__file__), 'data')
CONTACTOS = os.path.join(DATA, 'contactos.json')
COLA = os.path.join(DATA, 'cola_whatsapp.json')

def _contactos():
    if not os.path.exists(CONTACTOS):
        return {}
    data = json.load(open(CONTACTOS, encoding='utf-8'))
    return {c['cuit']: c for c in data if c.get('cuit')}

def _linea(item, entidad, fecha_iso, today):
    detalle = item + (f" ({entidad})" if entidad and entidad not in item else "")
    if not fecha_iso:
        return f"• {detalle}: sin fecha de vencimiento"
    f = datetime.date.fromisoformat(fecha_iso)
    dias = (f - today).days
    if dias < 0:
        return f"• {detalle}: VENCIDO el {f.strftime('%d/%m/%Y')} (hace {-dias} días)"
    return f"• {detalle}: vence el {f.strftime('%d/%m/%Y')} (en {dias} días)"

def main(today=None):
    today = today or datetime.date.today()
    con = dbm.connect()
    contactos = _contactos()
    pend = con.execute("SELECT * FROM outbox WHERE estado='pendiente'").fetchall()
    # agrupar por cuit (primer segmento del doc_key)
    grupos = {}
    for row in pend:
        cuit = row['doc_key'].split('|')[0]
        grupos.setdefault(cuit, {'nombre': row['fletero'], 'rows': []}).setdefault('rows', []).append(row)
    envios = []
    for cuit, g in grupos.items():
        lineas = []
        doc_keys = []
        for row in g['rows']:
            doc = con.execute("SELECT item, entidad, fecha_vencimiento FROM documentos WHERE (fletero_cuit||'|'||recurso||'|'||identificador||'|'||item)=?", (row['doc_key'],)).fetchone()
            if doc:
                lineas.append(_linea(doc['item'], doc['entidad'], doc['fecha_vencimiento'], today))
                doc_keys.append(row['doc_key'])
        nombre = contactos.get(cuit, {}).get('nombre', g['nombre'])
        tel = contactos.get(cuit, {}).get('telefono', '')
        texto = (f"Hola {nombre}, recordatorio de documentación en SICOP:\n\n"
                 + "\n".join(lineas)
                 + "\n\nPor favor enviá la documentación actualizada cuanto antes. Gracias.")
        envios.append({'cuit': cuit, 'nombre': nombre, 'telefono': tel, 'doc_keys': doc_keys, 'texto': texto})
    out = {'generado': datetime.datetime.now().isoformat(timespec='seconds'), 'envios': envios}
    os.makedirs(DATA, exist_ok=True)
    json.dump(out, open(COLA, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    sin_tel = [e['nombre'] for e in envios if not e['telefono']]
    print(f"Cola -> {COLA}: {len(envios)} choferes, "
          f"{sum(len(e['doc_keys']) for e in envios)} documentos.")
    if sin_tel:
        print("  [!] Sin teléfono (no se enviarán hasta cargarlo en data/contactos.json): " + ", ".join(sin_tel))
    return out

if __name__ == '__main__':
    import sys
    d = datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.date.today()
    main(d)
