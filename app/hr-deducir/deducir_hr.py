"""Para cada cisterna y día propone qué HR está haciendo, cruzando el plan del
distribuidor (rutas.json) con las paradas satelitales y el catálogo de clientes.
Modo sombra: guarda la predicción en predicciones/ y NO toca el tablero.
Uso: python deducir_hr.py [AAAA-MM-DD]"""
import sys
from datetime import date, datetime, timedelta
from comun import CONFIG, km, ruta, leer_json, guardar_json, mismo_cliente
from satelital import AR, paradas_del_dia

def ubicacion(nombre, catalogo):
    for k, v in catalogo.items():
        if v.get("aprendido") and mismo_cliente(nombre, k):
            return (v["lat"], v["lng"])
    return None

def plantas(catalogo):
    return [(v["lat"], v["lng"]) for k, v in catalogo.items() if v.get("aprendido") and k == "_PLANTA_CARGA"]

def candidatas(rutas, fecha):
    d = date.fromisoformat(fecha)
    ventana = {(d + timedelta(days=i)).isoformat() for i in (-1, 0, 1)}
    return [r for r in rutas.values() if ventana & set(r["dias"])]

def puntuar(unidad, fecha, ps, ruta_hr, catalogo, otras):
    plan_hoy = ruta_hr["dias"].get(fecha, {})
    planificada = plan_hoy.get("cisterna") == unidad
    visitados, ajenos, carga = [], [], False
    for p in ps:
        punto = (p["lat"], p["lng"])
        hit = None
        for orden, nombre in ruta_hr["clientes"].items():
            u = ubicacion(nombre, catalogo)
            if u and km(punto, u) <= CONFIG["radio_cliente_km"]:
                hit = (int(orden), nombre, p); break
        if hit: visitados.append(hit); continue
        if any(km(punto, u) <= CONFIG["radio_cliente_km"] for u in plantas(catalogo)):
            carga = True; continue
        for o in otras:
            if o["hr"] == ruta_hr["hr"]: continue
            if any((u := ubicacion(n, catalogo)) and km(punto, u) <= CONFIG["radio_cliente_km"]
                   for n in o["clientes"].values()):
                ajenos.append(o["hr"]); break
    en_orden = [v[0] for v in visitados] == sorted(v[0] for v in visitados)
    puntos = 2 * len(visitados) + (0.5 if en_orden and len(visitados) > 1 else 0) \
             + (1 if carga and planificada and plan_hoy.get("tipo") == "carga" else 0) \
             + (1 if planificada else 0) - 1.5 * len(ajenos)
    if not planificada and not visitados:
        puntos = 0                       # otra unidad: solo cuenta si visitó a sus clientes
    return {"hr": ruta_hr["hr"], "puntos": puntos, "planificada": planificada,
            "visitados": [{"orden": o, "cliente": n, "hora": datetime.fromtimestamp(p["ini"], AR).strftime("%H:%M"), "min": p["min"]} for o, n, p in visitados],
            "carga": carga, "ajenos": sorted(set(ajenos))}

def deducir(fecha):
    rutas = leer_json(ruta("rutas.json"), {})
    catalogo = leer_json(ruta("clientes.json"), {})
    todas = paradas_del_dia(fecha)
    cands = candidatas(rutas, fecha)
    salida = {}
    for unidad, ps in sorted(todas.items()):
        if isinstance(ps, dict): continue
        notas = [puntuar(unidad, fecha, ps, r, catalogo, cands) for r in cands]
        notas = [n for n in notas if n["puntos"] > 0]
        if not notas: continue
        notas.sort(key=lambda n: -n["puntos"])
        m = notas[0]
        if m["visitados"] and not m["ajenos"]: conf = "alta" if m["planificada"] else "revisar"
        elif m["carga"] or m["visitados"]: conf = "media"
        else: conf = "baja"
        if conf != "revisar" and not m["planificada"]: conf = "revisar"
        salida[unidad] = {"fecha": fecha, "unidad": unidad, "hr": m["hr"], "confianza": conf,
                          "visitados": m["visitados"], "carga": m["carga"],
                          "plan": next((r["hr"] for r in cands if r["dias"].get(fecha, {}).get("cisterna") == unidad), None),
                          "alternativas": [n["hr"] for n in notas[1:3]],
                          "calculado": datetime.now(AR).isoformat(timespec="minutes")}
    guardar_json(ruta("predicciones", fecha + ".json"), salida)
    if CONFIG.get("escribir_hr_en_curso", True) and fecha == datetime.now(AR).date().isoformat():
        hr_en_curso(salida, cands, fecha)
        hr_cerradas(rutas, fecha)
    if CONFIG["mostrar_en_tablero"]:
        for u, s in salida.items():
            guardar_json(f'{CONFIG["tablero_datos"]}\\{fecha}-{u}.json', s)
    return salida

CONF_NUM = {"alta": 0.9, "media": 0.6, "revisar": 0.5, "baja": 0.3}

def hr_en_curso(salida, cands, fecha):
    """Para la tabla "Distribución en vivo" del tablero: HR en curso por cisterna según
    el plan del mail (Tomás LIN / Daniel LOX) y según el recorrido."""
    unidades = {}
    for r in cands:                                 # todo lo planificado para hoy
        d = r["dias"].get(fecha)
        if not d: continue
        clientes = [r["clientes"][k] for k in sorted(r["clientes"], key=int)]
        u = unidades.setdefault(d["cisterna"], {"hr": r["hr"], "fuente": "plan", "confianza": 0.3,
            "clientes": clientes, "visitados": [], "producto": r.get("producto"),
            "detalle": "Planta Acindar (carga)" if d.get("tipo") == "carga" else "Según el plan del mail"})
        if u["hr"] != r["hr"]:
            u.setdefault("otras_plan", []).append(r["hr"])
    rutas = {r["hr"]: r for r in cands}
    for unidad, p in salida.items():
        r = rutas.get(p["hr"], {"clientes": {}})
        vis = [v["cliente"] for v in p["visitados"]]
        del_plan = {r2["hr"] for r2 in cands if r2["dias"].get(fecha, {}).get("cisterna") == unidad}
        if p["hr"] in del_plan:
            fuente = "ambos" if (vis or p["carga"]) else "plan"
        else:
            fuente = "recorrido"
        det = ("Visitó " + ", ".join(f'{v["cliente"]} {v["hora"]}' for v in p["visitados"])) if vis \
            else ("Pasó por Planta Acindar" if p["carga"] else "Según el plan del mail")
        if fuente == "recorrido" and del_plan:
            det += " (el plan decía " + ", ".join(sorted(del_plan)) + ")"
        unidades[unidad] = {"hr": p["hr"], "fuente": fuente, "confianza": CONF_NUM.get(p["confianza"], 0.3),
                            "clientes": [r["clientes"][k] for k in sorted(r["clientes"], key=int)],
                            "visitados": vis, "producto": r.get("producto"), "detalle": det}
    destino = CONFIG.get("hr_en_curso", r"C:\jornada-bot\tablero\datos\meta\hr_en_curso.json")
    guardar_json(destino, {"generado": datetime.now(AR).isoformat(timespec="seconds"), "fecha": fecha,
                           "unidades": dict(sorted(unidades.items()))})

def hr_cerradas(rutas, fecha):
    """HR que ya terminaron (la unidad empezó otra HR, o pasó su último día del plan)
    y cuyo PDF todavía no está en hr.db: para Novedades del tablero ("falta recibirla")."""
    import os, sqlite3
    try:
        con = sqlite3.connect(CONFIG["hr_db"])
        recibidas = {str(h)[-6:] for (h,) in con.execute("select hr from hr")}
        con.close()
    except Exception:
        return                                       # sin base no se puede decir qué falta
    desde = CONFIG.get("cerradas_desde", "2026-10-28")
    por_unidad = {}                                  # unidad -> [(primer_dia, ultimo_dia, hr)]
    for r in rutas.values():
        for d, info in r["dias"].items():
            por_unidad.setdefault(info["cisterna"], {}).setdefault(r["hr"], []).append(d)
    pred = {}
    carpeta = ruta("predicciones")
    for f in os.listdir(carpeta) if os.path.isdir(carpeta) else []:
        for u, p in leer_json(os.path.join(carpeta, f), {}).items():
            if p.get("visitados") or p.get("carga"):
                pred.setdefault((u, p["hr"]), []).append(f[:-5])
    lista = []
    for unidad, hrs in por_unidad.items():
        # en orden de inicio (mismo día: la de número menor va primero, como en el mail)
        tramos = sorted((min(ds), int(hr), max(ds), hr) for hr, ds in hrs.items())
        tramos = [(a, c, d) for a, _, c, d in tramos]
        for i, (ini, fin, hr) in enumerate(tramos):
            siguiente = tramos[i + 1] if i + 1 < len(tramos) and tramos[i + 1][0] <= fecha else None
            if fin < desde or hr in recibidas or (fin >= fecha and not siguiente):
                continue
            if siguiente:
                motivo = f"La {unidad} empezó la HR {siguiente[2]} el {siguiente[0][8:10]}/{siguiente[0][5:7]}"
            else:
                motivo = f"Último día en el plan: {fin[8:10]}/{fin[5:7]}"
            lista.append({"hr": hr, "cisterna": unidad, "cerrada": siguiente[0] if siguiente else fin,
                          "motivo": motivo, "producto": rutas[hr].get("producto"),
                          "evidencia": "recorrido" if (unidad, hr) in pred else "plan",
                          "nota": None if (unidad, hr) in pred else "Sin recorrido que lo confirme: puede estar anulada"})
    lista.sort(key=lambda x: (x["cerrada"], x["cisterna"]))
    guardar_json(CONFIG.get("hr_cerradas", r"C:\jornada-bot\tablero\datos\meta\hr_cerradas.json"),
                 {"generado": datetime.now(AR).isoformat(timespec="seconds"), "fecha": fecha,
                  "faltan_recibir": lista})

if __name__ == "__main__":
    fecha = sys.argv[1] if len(sys.argv) > 1 else datetime.now(AR).date().isoformat()
    for u, s in deducir(fecha).items():
        print(u, s["hr"], s["confianza"], "plan:", s["plan"], [v["cliente"] for v in s["visitados"]])
