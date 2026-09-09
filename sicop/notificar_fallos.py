"""Si algún recordatorio de WhatsApp no se pudo enviar, avisa por mail a la operación.

Lee data/resultado_whatsapp.json (lo escribe whatsapp/enviar.js). Por cada chofer
cuyo mensaje falló, manda UN mail a AVISO_DESTINO desde la cuenta de Outlook,
detallando el motivo y el mensaje que debía enviarse.

Uso:
    python3 -m sicop.notificar_fallos            # envía el/los mail(s)
    python3 -m sicop.notificar_fallos --dry-run  # solo muestra lo que enviaría
"""
import os, sys, json, datetime
from . import mailer

DATA = os.path.join(os.path.dirname(__file__), 'data')
RESULTADO = os.path.join(DATA, 'resultado_whatsapp.json')
DESTINO = os.environ.get('AVISO_DESTINO', 'control@transtotal.com.ar')

def _mail_de_fallo(f):
    chofer = f.get('nombre', '(sin nombre)')
    tel = f.get('telefono') or 's/d'
    motivo = f.get('motivo', 'desconocido')
    asunto = f"[SICOP] No se pudo avisar a {chofer} por WhatsApp"
    cuerpo = (
        f"No se pudo enviar el recordatorio de vencimientos por WhatsApp.\n\n"
        f"Chofer: {chofer}\n"
        f"Teléfono: {tel}\n"
        f"Motivo: {motivo}\n"
        f"Fecha: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        f"El mensaje que debía enviarse era:\n"
        f"------------------------------------------------------------\n"
        f"{f.get('texto', '(sin texto)')}\n"
        f"------------------------------------------------------------\n\n"
        f"Por favor contactar al chofer por otro medio.\n"
    )
    return asunto, cuerpo

def main(dry_run=False):
    if not os.path.exists(RESULTADO):
        print('No hay resultado_whatsapp.json.'); return
    res = json.load(open(RESULTADO, encoding='utf-8'))
    fallidos = res.get('fallidos', [])
    if not fallidos:
        print('Sin fallos: no hace falta avisar.'); return
    print(f"{len(fallidos)} fallo(s). Avisando a {DESTINO}...")
    for f in fallidos:
        asunto, cuerpo = _mail_de_fallo(f)
        if dry_run:
            print(f"\n--- MAIL (dry-run) ---\nPara: {DESTINO}\nAsunto: {asunto}\n\n{cuerpo}")
            continue
        try:
            mailer.enviar_mail(DESTINO, asunto, cuerpo)
            print(f"  ✓ aviso enviado por {f.get('nombre')}")
        except Exception as e:
            print(f"  ✗ no se pudo mandar el aviso por {f.get('nombre')}: {e}")

if __name__ == '__main__':
    main(dry_run=('--dry-run' in sys.argv))
