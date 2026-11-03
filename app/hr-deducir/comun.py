"""Configuración y utilidades compartidas de hr-deducir (sin dependencias)."""
import json, math, os, re, unicodedata

BASE = os.path.dirname(os.path.abspath(__file__))
CONFIG = {
    "token_wialon": r"C:\jornada-bot\token.js",   # el mismo token que usa el bot de jornada
    "hr_db": r"C:\jornada-bot\hr.db",
    "base": [-32.8639, -60.7676], "radio_base_km": 1.0,
    "parada_min": 15, "vel_parada": 3, "radio_cliente_km": 2.0, "radio_aprender_km": 1.0,
    "mostrar_en_tablero": False,                   # modo sombra: no escribe en el tablero
    "tablero_datos": r"C:\jornada-bot\tablero\datos\hr-probable",
}
_cfg = os.path.join(BASE, "config.json")
if os.path.exists(_cfg):
    CONFIG.update(json.load(open(_cfg, encoding="utf-8")))

def ruta(*p): return os.path.join(BASE, *p)

def leer_json(f, defecto):
    try:
        with open(f, encoding="utf-8") as h: return json.load(h)
    except Exception: return defecto

def guardar_json(f, datos):
    os.makedirs(os.path.dirname(f), exist_ok=True)
    tmp = f + ".tmp"
    with open(tmp, "w", encoding="utf-8") as h: json.dump(datos, h, ensure_ascii=False, indent=1)
    os.replace(tmp, f)

def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 12742 * math.asin(math.sqrt(h))

def clave(nombre):
    """Nombre de cliente normalizado (los mails lo cortan a 17 letras)."""
    s = unicodedata.normalize("NFKD", nombre.upper()).encode("ascii", "ignore").decode()
    s = re.sub(r"\b(LIN|LOX)\b.*$", "", s)
    return re.sub(r"[^A-Z0-9]+", " ", s).strip()

def mismo_cliente(a, b):
    """Iguales o uno es el comienzo del otro (por el corte a 17 letras)."""
    a, b = clave(a), clave(b)
    if not a or not b: return False
    return a == b or (min(len(a), len(b)) >= 6 and (a.startswith(b) or b.startswith(a)))
