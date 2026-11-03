"""De noche: aprende la ubicación de clientes y plantas con las HR confirmadas
(hr.db, las que llegaron por WhatsApp) y mide los aciertos del modo sombra.
Uso: python aprender.py"""
import os, sqlite3
from collections import defaultdict
from datetime import datetime
from comun import CONFIG, km, ruta, leer_json, guardar_json, clave
from satelital import AR, paradas_del_dia, Wialon

def confirmadas():
    """{hr: cisterna} desde hr.db. Busca la tabla que tenga columnas de nº de HR y de cisterna."""
    con = sqlite3.connect(CONFIG["hr_db"])
    try:
        for (t,) in con.execute("select name from sqlite_master where type='table'"):
            cols = [c[1] for c in con.execute(f'pragma table_info("{t}")')]
            c_hr = next((c for c in cols if c.lower() in ("hr", "nro_hr", "numero", "nro", "hr_nro")), None)
            c_un = next((c for c in cols if c.lower() in ("cisterna", "unidad", "semi")), None)
            if c_hr and c_un:
                return {str(h)[-6:]: str(u)[:3] for h, u in con.execute(f'select "{c_hr}", "{c_un}" from "{t}"') if h and u}
    finally:
        con.close()
    raise RuntimeError("No encontré en hr.db una tabla con nº de HR y cisterna: ajustar confirmadas()")

def agrupar(votos, radio):
    """Agrupa votos [(lat,lng,hr,peso)] en lugares; devuelve [(lat,lng,hrs distintas,peso)] de mayor a menor."""
    grupos = []
    for v in votos:
        g = next((g for g in grupos if km(v[:2], g["c"]) <= radio), None)
        if g is None: g = {"c": v[:2], "v": []}; grupos.append(g)
        g["v"].append(v)
        g["c"] = (sum(x[0] for x in g["v"]) / len(g["v"]), sum(x[1] for x in g["v"]) / len(g["v"]))
    res = [(g["c"][0], g["c"][1], len({x[2] for x in g["v"]}), sum(x[3] for x in g["v"])) for g in grupos]
    return sorted(res, key=lambda r: (-r[2], -r[3]))

def aprender():
    rutas = leer_json(ruta("rutas.json"), {})
    conf = confirmadas()
    hoy = datetime.now(AR).date().isoformat()
    por_hr, carga = {}, []          # paradas de la unidad confirmada en los días de cada HR
    with Wialon() as w:
        for hr, unidad in conf.items():
            r = rutas.get(hr)
            if not r: continue
            ps_hr, pares = [], []
            for fecha, dia in sorted(r["dias"].items()):
                if fecha >= hoy: continue
                ps = paradas_del_dia(fecha, w).get(unidad)
                if not isinstance(ps, list): continue
                ps_hr += ps
                pares.append((dia.get("ordenes") or [], ps))
                if dia.get("tipo") == "carga":
                    carga += [(p["lat"], p["lng"], hr, 1) for p in ps]
            if ps_hr: por_hr[hr] = (ps_hr, pares)
    radio = CONFIG["radio_aprender_km"]
    # Lugares comunes (planta, paradores, estaciones): aparecen en 25% o más de las HR.
    todos = [(p["lat"], p["lng"], hr, 1) for hr, (ps, _) in por_hr.items() for p in ps]
    comunes = [g for g in agrupar(todos, radio) if g[2] >= 4 and g[2] >= 0.25 * len(por_hr)]
    es_comun = lambda p: any(km((p["lat"], p["lng"]), g[:2]) <= radio for g in comunes)
    votos = defaultdict(list)
    if carga:
        g = agrupar(carga, radio)[0]
        votos["_PLANTA_CARGA"] = [(g[0], g[1], h, 1) for h in range(g[2])]
    plan_g = agrupar(carga, radio)[0] if carga else None
    es_planta = lambda p: plan_g and km((p["lat"], p["lng"]), plan_g[:2]) <= radio
    for hr, (ps, pares) in por_hr.items():
        clientes = rutas[hr]["clientes"]
        for ordenes, ps_dia in pares:
            propias = sorted([p for p in ps_dia if not es_comun(p) and not es_planta(p)], key=lambda p: p["ini"])
            if ordenes and len(propias) == len(ordenes):
                # mismas paradas que clientes del día: se aparean en orden (voto fuerte)
                for o, p in zip(sorted(ordenes), propias):
                    votos[clave(clientes[str(o)])].append((p["lat"], p["lng"], hr, 2))
            else:
                for o in ordenes:
                    votos[clave(clientes[str(o)])] += [(p["lat"], p["lng"], hr, 1) for p in propias]
    catalogo = leer_json(ruta("clientes.json"), {})
    for nombre, vs in votos.items():
        g = agrupar(vs, radio)
        top = g[0]
        claro = top[2] >= 2 and (len(g) == 1 or top[2] > g[1][2])
        if top[2] == 1 and top[3] >= 2 and len(g) == 1: claro = True     # HR con una sola parada
        if catalogo.get(nombre, {}).get("fijo"): continue                   # cargado a mano
        catalogo[nombre] = {"lat": round(top[0], 5), "lng": round(top[1], 5), "hrs": top[2],
                            "aprendido": bool(claro), "actualizado": hoy}
    guardar_json(ruta("clientes.json"), catalogo)
    guardar_json(ruta("lugares-comunes.json"), [{"lat": round(g[0], 5), "lng": round(g[1], 5), "hrs": g[2]} for g in comunes])
    return conf, catalogo

def evaluar(conf):
    """Compara cada predicción con la HR confirmada de esa unidad."""
    res = defaultdict(lambda: {"total": 0, "aciertos": 0, "por_confianza": defaultdict(lambda: [0, 0])})
    rutas = leer_json(ruta("rutas.json"), {})
    carpeta = ruta("predicciones")
    for f in sorted(os.listdir(carpeta)) if os.path.isdir(carpeta) else []:
        fecha = f[:-5]
        for u, p in leer_json(os.path.join(carpeta, f), {}).items():
            reales = [h for h, un in conf.items() if un == u and fecha in rutas.get(h, {}).get("dias", {})]
            if not reales: continue                # todavía no llegó la HR de ese día
            semana = datetime.fromisoformat(fecha).strftime("%G-S%V")
            ok = p["hr"] in reales
            res[semana]["total"] += 1; res[semana]["aciertos"] += ok
            pc = res[semana]["por_confianza"][p["confianza"]]; pc[0] += 1; pc[1] += ok
    out = {s: {**v, "porcentaje": round(100 * v["aciertos"] / v["total"]) if v["total"] else None,
               "por_confianza": dict(v["por_confianza"])} for s, v in sorted(res.items())}
    guardar_json(ruta("aciertos.json"), out)
    return out

if __name__ == "__main__":
    conf, cat = aprender()
    print(f"HR confirmadas: {len(conf)} | lugares aprendidos: {sum(1 for v in cat.values() if v['aprendido'])} de {len(cat)}")
    for s, v in evaluar(conf).items():
        print(s, f"{v['aciertos']}/{v['total']}", f"{v['porcentaje']}%", v["por_confianza"])
