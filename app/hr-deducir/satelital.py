"""Recorrido de cada cisterna desde Transdat (NO Wialon: decisión del usuario)
y detección de paradas. Sin dependencias.
Transdat: POST /auth {user, pass} -> token; GET /v1/objects/ -> unidades (o.gps.*).
Recorrido: GET /v1/objects/{object}/report?_v=next&type=tracks (como transdat.js y
descargar_transdat.js); la respuesta trae .details[] con date (epoch s), lat, lng, speed."""
import json, re, time, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone
from comun import CONFIG, km, ruta, leer_json, guardar_json

AR = timezone(timedelta(hours=-3))

def _get(url, token=None, data=None):
    h = {"Content-Type": "application/json"}
    if token: h["Authorization"] = "Bearer " + token
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None, headers=h)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

class Transdat:
    """Se usa como `with Transdat() as t:` (mismo login que puente.js del panel)."""
    def __enter__(self):
        cred = json.load(open(CONFIG["transdat_credenciales"], encoding="utf-8"))
        self.url = CONFIG["transdat_url"]
        self.token = _get(self.url + "/auth", data={
            "user": cred.get("user") or cred.get("usuario"),
            "pass": cred.get("pass") or cred.get("password") or cred.get("clave")})["token"]
        return self
    def __exit__(self, *a): pass
    def unidades(self):
        """{'561': (object, type), ...} por los 3 primeros dígitos del nombre (como transdat.js)."""
        objs = _get(self.url + "/v1/objects/", self.token)
        if isinstance(objs, dict): objs = objs.get("objects") or objs.get("data") or list(objs.values())
        out = {}
        for o in objs:
            m = re.match(r"^\s*(\d{3})", str(o.get("name") or o.get("nombre") or o.get("alias") or ""))
            if m: out[m.group(1)] = (o.get("object"), o.get("type"))
        return out
    def posiciones(self, uid, desde, hasta):
        iso = lambda t: datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        obj, tipo = uid
        url = self.url + CONFIG["transdat_historial"].format(
            object=urllib.parse.quote(str(obj)), type=urllib.parse.quote(str(tipo)),
            desde=urllib.parse.quote(iso(desde)), hasta=urllib.parse.quote(iso(hasta)))
        d = _get(url, self.token)
        out = [(float(p["date"]), float(p["lat"]), float(p["lng"]), float(p.get("speed") or 0))
               for p in (d.get("details") or []) if p.get("date") and p.get("lat") and p.get("lng")]
        return sorted(out)

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

def paradas_del_dia(fecha, fuente=None, cache=True):
    """{'561': [paradas]} para la fecha (AAAA-MM-DD, hora Argentina). Días pasados quedan en caché."""
    f = ruta("paradas", fecha + ".json")
    hoy = datetime.now(AR).date().isoformat()
    if cache and fecha < hoy:
        c = leer_json(f, None)
        if c is not None: return c
    d0 = datetime.fromisoformat(fecha).replace(tzinfo=AR)
    desde, hasta = d0.timestamp(), (d0 + timedelta(days=1)).timestamp()
    own = fuente is None
    w = Transdat().__enter__() if own else fuente
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
