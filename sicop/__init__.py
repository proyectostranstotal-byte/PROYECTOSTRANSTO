"""Paquete SICOP. Al importar, carga sicop/.env en el entorno (si existe) para que
los scripts anden con doble clic sin configurar variables a mano."""
import os

def _load_env():
    env = os.path.join(os.path.dirname(__file__), '.env')
    if not os.path.exists(env):
        return
    for line in open(env, encoding='utf-8'):
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        k, v = k.strip(), v.strip()
        os.environ.setdefault(k, v)  # no pisar lo que ya esté en el entorno

_load_env()
