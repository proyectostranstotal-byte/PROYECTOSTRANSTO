"""Parser del Excel 'Estado de Situación' de SICOP.

Cada archivo tiene columnas:
  Recurso | Descripcion | Nro Proveedor | Identificador | Item | Fecha | Motivo
La fila 1 es el título ('Estado de situación al día: d/m/aaaa'), la fila 2 el encabezado.
Las celdas son inline strings dentro del XLSX.
"""
import re, zipfile, datetime
from xml.etree import ElementTree as ET

NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'


def _cell_text(c):
    t = c.get('t')
    if t == 'inlineStr':
        is_ = c.find(NS + 'is')
        return ''.join(x.text or '' for x in is_.iter(NS + 't')) if is_ is not None else ''
    v = c.find(NS + 'v')
    return v.text if v is not None else ''


def _rows(xlsx_path):
    z = zipfile.ZipFile(xlsx_path)
    root = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
    rows = {}
    for c in root.iter(NS + 'c'):
        ref = c.get('r'); m = re.match(r'([A-Z]+)(\d+)', ref)
        col, rw = m.group(1), int(m.group(2))
        rows.setdefault(rw, {})[col] = (_cell_text(c) or '').strip()
    out = []
    for rw in sorted(rows):
        cells = rows[rw]
        out.append([cells.get(col, '') for col in ['A', 'B', 'C', 'D', 'E', 'F', 'G']])
    return out


def _parse_date(s):
    s = (s or '').strip()
    for fmt in ('%d/%m/%Y', '%d/%m/%y', '%Y-%m-%d'):
        try:
            return datetime.datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            continue
    return None  # e.g. 'Falta Fecha'


def parse(xlsx_path, fletero, fletero_cuit):
    """Devuelve (fecha_reporte_iso, [registros])."""
    rows = _rows(xlsx_path)
    fecha_reporte = None
    if rows and rows[0] and rows[0][0]:
        m = re.search(r'(\d{1,2}/\d{1,2}/\d{2,4})', rows[0][0])
        if m:
            fecha_reporte = _parse_date(m.group(1))
    registros = []
    for r in rows[2:]:
        recurso, descripcion, _nro, identificador, item, fecha, motivo = (r + [''] * 7)[:7]
        if not recurso.strip():
            continue
        registros.append({
            'fletero': fletero,
            'fletero_cuit': fletero_cuit,
            'recurso': recurso.strip(),
            'entidad': descripcion.strip(),
            'identificador': identificador.strip(),
            'item': item.strip(),
            'fecha_vencimiento': _parse_date(fecha),
            'fecha_texto': fecha.strip(),
            'motivo': motivo.strip(),
        })
    return fecha_reporte, registros


if __name__ == '__main__':
    import sys, json
    fr, regs = parse(sys.argv[1], 'TEST', '0')
    print('fecha_reporte', fr, 'registros', len(regs))
    print(json.dumps(regs[:3], ensure_ascii=False, indent=2))
