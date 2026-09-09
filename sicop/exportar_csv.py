"""Exporta la tabla de documentos/vencimientos a CSV legible."""
import csv, os, datetime
from . import db as dbm

OUT = os.path.join(os.path.dirname(__file__), 'data', 'vencimientos.csv')

def main(today=None):
    today = today or datetime.date.today()
    con = dbm.connect()
    rows = con.execute("SELECT * FROM documentos ORDER BY fletero, fecha_vencimiento").fetchall()
    with open(OUT, 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['fletero', 'cuit_fletero', 'recurso', 'entidad', 'identificador',
                    'item', 'fecha_vencimiento', 'motivo', 'dias_para_vencer'])
        for r in rows:
            dias = ''
            if r['fecha_vencimiento']:
                dias = (datetime.date.fromisoformat(r['fecha_vencimiento']) - today).days
            w.writerow([r['fletero'], r['fletero_cuit'], r['recurso'], r['entidad'],
                        r['identificador'], r['item'], r['fecha_texto'], r['motivo'], dias])
    print('CSV ->', OUT, f'({len(rows)} filas)')

if __name__ == '__main__':
    main(datetime.date(2026, 9, 9))
