"""Recorrido de cada cisterna desde Wialon (mismo token que el bot de jornada)
y detección de paradas. Sin dependencias."""
import json, re, time, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone
from comun import CONFIG, km, ruta, leer_json, guardar_json

API = "https://hst-api.wialon.com/wialon/ajax.html"
AR = timezone(timedelta(hours=-3))

def _token():
    txt = open(CONFIG["token_wialon"], encoding="utf-8").read()
    return re.search(r"['\"]([0-9a-fA-F]{40,})['\"]", txt).group(1)

def _call(svc, params, sid=None):
    q = {"svc": svc, "params": json.dumps(params)}
    if sid: q["sid"] = sid
    with urllib.request.urlopen(API + "?" + urllib.parse.urlencode(q), timeout=60) as r:
        d = json.load(r)
    if isinstance(d, dict) and d.get("error"):
        raise RuntimeError(f"Wialon {svc} error {d['error']}")
    return d

class Wialon:
    def __enter__(self):
        self.sid = _call("token/login", {"token": _token()})["eid"]
        return self
    def __exit__(self, *a):
        try: _call("core/logout", {}, self.sid)
        except Exception: pass
    def unidades(self):
        """{'561': id_wialon, ...} por los 3 primeros dígitos del nombre."""
        d = _call("core/search_items", {"spec": {"itemsType": "avl_unit", "propName": "sys_name",
              "propValueMask": "*", "sortType": "sys_name"}, "force": 1, "flags": 1, "from": 0, "to": 0}, self.sid)
        out = {}
        for it in d.get("items", []):
            m = re.match(r"^(\d{3})", it.get("nm", ""))
            if m: out[m.group(1)] = it["id"]
        return out
    def posiciones(self, uid, desde, hasta):
        d = _call("messages/load_interval", {"itemId": uid, "timeFrom": int(desde), "timeTo": int(hasta),
              "flags": 1, "flagsMask": 65281, "loadCount": 0xFFFFFFFF}, self.sid)
        return [(m["t"], m["pos"]["y"], m["pos"]["x"], m["pos"].get("s", 0))
                for m in d.get("messages", []) if m.get("pos") and m["pos"].get("y")]

def paradas(pos):
    """Detenciones de parada_min o más, fuera de la base. [{ini, fin, min, lat, lng}]"""
    out, grupo = [], []
    def cerrar():
        if len(grupo) < 2: return
        dur = (grupo[-1][0] - grupo[0][0]) / 60
        if dur < CONFIG["parada_min"]: return
        lat = sum(p[1] for p in grupo) / len(grupo); lng = sum(p[2] for p in grupo) / len(grupo)
        if km((lat, lng), CONFIG["base"]) <= CONFIG["radio_base_km"]: return
        out.append({"ini": grupo[0][0], "fin": grupo[-1][0], "min": round(dur),
                    "lat": round(lat, 5), "lng": round(lng, 5)})
    for p in pos:
        quieto = p[3] < CONFIG["vel_parada"]
        if quieto and grupo and km(p[1:3], grupo[0][1:3]) > 0.5:
            cerrar(); grupo = []
        if quieto: grupo.append(p)
        else:
            cerrar(); grupo = []
    cerrar()
    return out

def paradas_del_dia(fecha, wialon=None, cache=True):
    """{'561': [paradas]} para la fecha (AAAA-MM-DD, hora Argentina). Días pasados quedan en caché."""
    f = ruta("paradas", fecha + ".json")
    hoy = datetime.now(AR).date().isoformat()
    if cache and fecha < hoy:
        c = leer_json(f, None)
        if c is not None: return c
    d0 = datetime.fromisoformat(fecha).replace(tzinfo=AR)
    desde, hasta = d0.timestamp(), (d0 + timedelta(days=1)).timestamp()
    own = wialon is None
    w = Wialon().__enter__() if own else wialon
    try:
        res = {}
        for u, uid in w.unidades().items():
            try: res[u] = paradas(w.posiciones(uid, desde, min(hasta, time.time())))
            except Exception as e: res[u] = {"error": str(e)}
    finally:
        if own: w.__exit__()
    guardar_json(f, res)
    return res

if __name__ == "__main__":
    import sys
    fecha = sys.argv[1] if len(sys.argv) > 1 else datetime.now(AR).date().isoformat()
    for u, ps in paradas_del_dia(fecha, cache=False).items():
        print(u, ps if isinstance(ps, dict) else [(datetime.fromtimestamp(p["ini"], AR).strftime("%H:%M"), p["min"], p["lat"], p["lng"]) for p in ps])
