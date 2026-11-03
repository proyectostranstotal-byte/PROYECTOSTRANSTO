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
    if CONFIG["mostrar_en_tablero"]:
        for u, s in salida.items():
            guardar_json(f'{CONFIG["tablero_datos"]}\\{fecha}-{u}.json', s)
    return salida

if __name__ == "__main__":
    fecha = sys.argv[1] if len(sys.argv) > 1 else datetime.now(AR).date().isoformat()
    for u, s in deducir(fecha).items():
        print(u, s["hr"], s["confianza"], "plan:", s["plan"], [v["cliente"] for v in s["visitados"]])
