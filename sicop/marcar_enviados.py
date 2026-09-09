"""Marca en outbox los mensajes efectivamente enviados por WhatsApp.
Lee data/resultado_whatsapp.json (lo escribe enviar.js)."""
import os, json, datetime
from . import db as dbm

DATA = os.path.join(os.path.dirname(__file__), 'data')
RESULTADO = os.path.join(DATA, 'resultado_whatsapp.json')

def main():
    if not os.path.exists(RESULTADO):
        print('No hay resultado_whatsapp.json todavía.'); return
    res = json.load(open(RESULTADO, encoding='utf-8'))
    con = dbm.connect()
    n = 0
    for dk in res.get('enviados', []):
        cur = con.execute("UPDATE outbox SET estado='enviado' WHERE doc_key=? AND estado='pendiente'", (dk,))
        n += cur.rowcount
    con.commit()
    print(f"Marcados como enviados: {n} documentos "
          f"({len(res.get('fallidos', []))} grupos fallidos).")

if __name__ == '__main__':
    main()
