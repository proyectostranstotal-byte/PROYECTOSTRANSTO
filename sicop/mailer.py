"""Envío de mail por la cuenta de Outlook (SMTP), sin dependencias externas.

Credenciales por entorno:
    OUTLOOK_USER   - dirección de Outlook (remitente)
    OUTLOOK_PASS   - contraseña de aplicación de Outlook/Microsoft 365
    OUTLOOK_SMTP   - host SMTP (default smtp.office365.com)
    OUTLOOK_PORT   - puerto (default 587, STARTTLS)

Nota: Microsoft suele requerir una "contraseña de aplicación" (no la normal) si la
cuenta tiene verificación en dos pasos. Si el tenant tiene el SMTP básico
deshabilitado, hay que habilitarlo o usar otra cuenta de envío.
"""
import os, smtplib, ssl
from email.message import EmailMessage

def enviar_mail(destino, asunto, cuerpo, remitente=None):
    user = os.environ.get('OUTLOOK_USER')
    pwd = os.environ.get('OUTLOOK_PASS')
    host = os.environ.get('OUTLOOK_SMTP', 'smtp.office365.com')
    port = int(os.environ.get('OUTLOOK_PORT', '587'))
    if not user or not pwd:
        raise RuntimeError('Faltan credenciales de mail: definí OUTLOOK_USER y OUTLOOK_PASS')
    msg = EmailMessage()
    msg['From'] = remitente or user
    msg['To'] = destino
    msg['Subject'] = asunto
    msg.set_content(cuerpo)
    ctx = ssl.create_default_context()
    with smtplib.SMTP(host, port, timeout=30) as s:
        s.starttls(context=ctx)
        s.login(user, pwd)
        s.send_message(msg)
    return True
