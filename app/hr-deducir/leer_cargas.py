"""Lee el mail "Adjunto las cargas de mañana" (texto de ancho fijo) y devuelve
para cada cisterna y día las HR planificadas con sus clientes.
Sin dependencias. Uso: python leer_cargas.py mail.txt  -> JSON por stdout."""
import json, re, sys
from datetime import datetime

MESES = {"JAN":1,"ENE":1,"FEB":2,"MAR":3,"APR":4,"ABR":4,"MAY":5,"JUN":6,"JUL":7,
         "AUG":8,"AGO":8,"SEP":9,"OCT":10,"NOV":11,"DEC":12,"DIC":12}
RE_FECHA = re.compile(r"(\d{2})-([A-Z]{3})-(\d{2})")
RE_SEP = re.compile(r"^_{10,}(\s+_{10,})+\s*$")

def fecha_iso(m):
    return datetime(2000 + int(m.group(3)), MESES[m.group(2)], int(m.group(1))).date().isoformat()

def leer(texto, producto=None):
    """producto: "LOX" o "LIN" según el asunto del mail (los LOX dicen "LOX - TTT ..." / "LOX - SEMIS TTT ...")."""
    # Outlook convierte "2.LA" en link y en texto plano queda "2.LA<http://2.la/>"
    texto = re.sub(r"<(https?|mailto):[^>]*>", "", texto)
    lineas = texto.replace("\r", "").split("\n")
    fechas_pos, cols = [], []          # posición de cada fecha / inicio de cada columna
    plan, unidad, celdas = [], None, {}
    def cerrar():
        for (col, _), c in sorted(celdas.items()):
            if col < len(fechas_pos):
                plan.append(c)
    for ln in lineas:
        fs = list(RE_FECHA.finditer(ln))
        if fs and (len(fs) >= 2 or not fechas_pos or "Semi" in ln or ln.strip() == fs[0].group(0)):
            fechas_pos = [(m.start(), fecha_iso(m)) for m in fs]
            continue
        if RE_SEP.match(ln):            # separador entre unidades
            cerrar(); celdas, unidad = {}, None
            cols = [m.start() for m in re.finditer(r"_{10,}", ln)][1:]
            continue
        m = re.match(r"^(\d{3})\s", ln)
        if m: unidad = m.group(1)
        if unidad is None or not cols or "|" not in ln:
            continue
        for p in [i for i, ch in enumerate(ln) if ch == "|"]:
            col = min(range(len(cols)), key=lambda k: abs(cols[k] - p))
            txt = re.sub(r"\s*_{5,}.*$", "", ln[p + 1:].split("|")[0]).strip()
            if txt.startswith("HR:"):
                nro = re.sub(r"\D", "", txt)[-6:]
                n = sum(1 for k in celdas if k[0] == col)
                celdas[(col, n)] = {"cisterna": unidad, "fecha": fechas_pos[col][1],
                                    "hr": nro, "tipo": None, "clientes": []}
                continue
            abiertas = [k for k in celdas if k[0] == col]
            if not abiertas or not txt: continue
            c = celdas[max(abiertas)]
            if txt.startswith("Continuaci"): c["tipo"] = "continuacion"
            elif txt.lower().startswith("planta"): c["tipo"] = "carga"; c["planta"] = txt
            else:
                mc = re.match(r"^(\d+)?\.(.*)$", txt)
                if mc and mc.group(1):
                    c["clientes"].append({"orden": int(mc.group(1)), "texto": mc.group(2).strip()})
                elif c["clientes"]:   # renglón partido (".DyP - LIN")
                    c["clientes"][-1]["texto"] += " " + txt
    cerrar()
    for c in plan:
        t = " ".join(x["texto"] for x in c["clientes"])
        c["producto"] = producto or ("LOX" if re.search(r"-\s*LOX\b", t) else None) or ("LIN" if re.search(r"-\s*L(IN)?\b|-LIN", t) else None)
        for x in c["clientes"]:
            x["texto"] = re.sub(r"\s+", " ", x["texto"]).strip()
            x["nombre"] = re.sub(r"\s*-\s*(LIN.*|LOX.*|L|LO|LIN A)?\s*$", "", x["texto"]).strip(" -")
    return plan

def juntar(rutas, plan, recibido):
    """Acumula los mails: cada HR guarda su ruta completa (clientes por número de
    orden, de todos los mails) y por día la unidad/tarea del mail más nuevo."""
    for c in plan:
        r = rutas.setdefault(c["hr"], {"hr": c["hr"], "clientes": {}, "dias": {}})
        if c.get("producto"): r["producto"] = c["producto"]
        for x in c["clientes"]:
            r["clientes"][str(x["orden"])] = x["nombre"]
        r["dias"][c["fecha"]] = {"cisterna": c["cisterna"], "tipo": c["tipo"],
                                 "planta": c.get("planta"), "mail": recibido,
                                 "ordenes": [x["orden"] for x in c["clientes"]]}
    return rutas

def actualizar_rutas():
    """Lee todos los mails bajados (mails/*.txt, del más viejo al más nuevo) y
    arma rutas.json: por HR, sus clientes y en qué unidad/día figura."""
    import os
    from comun import ruta, guardar_json
    rutas = {}
    for f in sorted(os.listdir(ruta("mails"))):
        if not f.endswith(".txt"): continue
        sello, prod = f[:-4].split("_")[:2]
        texto = open(ruta("mails", f), encoding="utf-8-sig").read()
        juntar(rutas, leer(texto, prod), sello)
    guardar_json(ruta("rutas.json"), rutas)
    return rutas

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "--rutas":
        print(json.dumps(leer(open(sys.argv[1], encoding="utf-8").read()), ensure_ascii=False, indent=1))
    else:
        r = actualizar_rutas()
        print(f"rutas.json: {len(r)} HR")
