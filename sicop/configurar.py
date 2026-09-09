"""Configurador interactivo: crea sicop/.env sin que tengas que editar archivos.
Pregunta las contraseñas (ocultas) y arma el archivo solo.

Uso:  python -m sicop.configurar
"""
import os, getpass

ENV = os.path.join(os.path.dirname(__file__), '.env')
SICOP_USER_DEFAULT = 'control.transtotal@gmail.com'
AVISO_DESTINO_DEFAULT = 'control@transtotal.com.ar'

def _pedir(texto, default=None, oculto=False):
    extra = f' [{default}]' if default else ''
    while True:
        val = (getpass.getpass(texto + extra + ': ') if oculto else input(texto + extra + ': ')).strip()
        if not val and default is not None:
            return default
        if val:
            return val
        print('  (no puede quedar vacío)')

def main():
    print('\n=== Configuración de claves (se guarda en sicop/.env) ===\n')
    if os.path.exists(ENV):
        if input('Ya existe sicop/.env. ¿Sobrescribir? (s/n): ').strip().lower() not in ('s', 'si', 'sí'):
            print('Cancelado. No se tocó nada.'); return
    sicop_user = _pedir('Usuario de SICOP', SICOP_USER_DEFAULT)
    sicop_pass = _pedir('Contraseña de SICOP', oculto=True)
    print('\n-- Aviso por mail cuando un WhatsApp no se pueda enviar --')
    ol_user = _pedir('Tu cuenta de Outlook (email)')
    ol_pass = _pedir('Contraseña de Outlook (o contraseña de aplicación si tenés 2FA)', oculto=True)
    destino = _pedir('Mail donde avisar los fallos', AVISO_DESTINO_DEFAULT)
    with open(ENV, 'w', encoding='utf-8') as f:
        f.write('# Generado por configurar.py. No compartir.\n')
        f.write(f'SICOP_USER={sicop_user}\n')
        f.write(f'SICOP_PASS={sicop_pass}\n')
        f.write(f'OUTLOOK_USER={ol_user}\n')
        f.write(f'OUTLOOK_PASS={ol_pass}\n')
        f.write(f'AVISO_DESTINO={destino}\n')
    print('\n✓ Listo. Guardado en sicop/.env (no se sube a internet ni al repositorio).')

if __name__ == '__main__':
    main()
