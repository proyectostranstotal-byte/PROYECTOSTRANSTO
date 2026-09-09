"""Ciclo completo: descarga el Estado de Situación de todos los fleteros,
lo importa a la base y evalúa los recordatorios.

Uso:
    export SICOP_USER=...   SICOP_PASS=...
    python3 -m sicop.actualizar [YYYY-MM-DD]
"""
import os, sys, datetime
from .sicop_client import SicopClient
from .fleteros import FLETEROS, EMPRESA_ID, CONTRATISTA_CUIT
from . import importar

ESTADOS_DIR = os.path.join(os.path.dirname(__file__), 'data', 'estados')

def descargar_todos():
    os.makedirs(ESTADOS_DIR, exist_ok=True)
    c = SicopClient(EMPRESA_ID)
    c.login()
    for f in FLETEROS:
        out = os.path.join(ESTADOS_DIR, f['nombre'].replace(' ', '_') + '.xlsx')
        try:
            c.descargar_estado(CONTRATISTA_CUIT, f['cuit'], out)
            print(f"  descargado: {f['nombre']}")
        except Exception as e:
            print(f"  [!] {f['nombre']}: {e}")

def main(today=None):
    print("== Descargando estados de situación ==")
    descargar_todos()
    print("\n== Importando y evaluando ==")
    importar.main(today)

if __name__ == '__main__':
    d = datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.date.today()
    main(d)
