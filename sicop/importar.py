"""Importa los Excel 'Estado de Situación' descargados a la base y corre los recordatorios.

Uso:
  python3 -m sicop.importar [YYYY-MM-DD]   # fecha de referencia (default: hoy)
"""
import os, sys, glob, datetime
from . import estado_parser, db as dbm, reminders
from .fleteros import FLETEROS

ESTADOS_DIR = os.path.join(os.path.dirname(__file__), 'data', 'estados')

def _archivo_de(cuit, nombre):
    # match por nombre normalizado
    base = nombre.replace(' ', '_')
    cands = glob.glob(os.path.join(ESTADOS_DIR, '*.xlsx'))
    for c in cands:
        if base.split('_')[0].upper() in os.path.basename(c).upper():
            return c
    return None

def main(today=None):
    today = today or datetime.date.today()
    con = dbm.connect()
    total = 0
    for f in FLETEROS:
        arch = _archivo_de(f['cuit'], f['nombre'])
        if not arch:
            print(f"[!] sin archivo para {f['nombre']}")
            continue
        fecha_rep, regs = estado_parser.parse(arch, f['nombre'], f['cuit'])
        cambios = dbm.upsert_documentos(con, regs)
        reminders.marcar_resoluciones(con, cambios)
        dbm.record_snapshot(con, f['nombre'], f['cuit'], fecha_rep, os.path.basename(arch), len(regs))
        total += len(regs)
        print(f"  {f['nombre']:28s} {len(regs):3d} docs  (reporte {fecha_rep})"
              + (f"  {len(cambios)} cambios de vencimiento" if cambios else ""))
    print(f"Total documentos en base: {total}")

    # Reporte de vencimientos
    print("\n=== Vencimientos por fletero (ref " + today.isoformat() + ") ===")
    for f in FLETEROS:
        rows = con.execute(
            "SELECT * FROM documentos WHERE fletero_cuit=? ORDER BY fecha_vencimiento", (f['cuit'],)).fetchall()
        venc = [r for r in rows if r['motivo'] == 'Vencido' or (r['fecha_vencimiento'] and datetime.date.fromisoformat(r['fecha_vencimiento']) < today)]
        prox = [r for r in rows if r['fecha_vencimiento'] and 0 <= (datetime.date.fromisoformat(r['fecha_vencimiento']) - today).days <= 15]
        print(f"\n{f['nombre']} ({f['cuit']}): {len(rows)} docs | {len(venc)} vencidos | {len(prox)} vencen en <=15 días")
        for r in venc:
            print(f"   VENCIDO  {r['fecha_texto']:11s} {r['recurso']:9s} {r['item'][:52]}")
        for r in prox:
            d = (datetime.date.fromisoformat(r['fecha_vencimiento']) - today).days
            print(f"   en {d:2d}d   {r['fecha_texto']:11s} {r['recurso']:9s} {r['item'][:52]}")

    # Recordatorios que se enviarían hoy
    print("\n=== Recordatorios a enviar hoy ===")
    envs = reminders.evaluar(con, today=today)
    print(f"{len(envs)} mensajes generados (quedan en outbox, canal pendiente):")
    for e in envs:
        print(f"\n  -> {e['fletero']}")
        print(f"     {e['mensaje']}")
    return con

if __name__ == '__main__':
    d = datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.date(2026, 9, 9)
    main(d)
