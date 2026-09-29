"""Análisis de maestros (vehiculos / articulos / clientes) para el cruce OT x auditoría de flota.

Uso: python analisis_maestros.py <carpeta_con_xls> [salida.xlsx]
Los .xls del sistema de taller son en realidad xlsx: se leen con openpyxl.
"""
import re
import sys
from pathlib import Path

import pandas as pd

# Flota auditada: patente -> interno (None = tractor/chasis sin interno en la lista)
FLOTA = {
    "AC646NF": None, "AD068KU": None, "AE055XV": None, "AE460TD": None, "AE567CR": None,
    "AE766YQ": None, "AF378NF": None, "AG072ZV": None, "AG153LC": None, "AG549BR": None,
    "AG758LX": None, "AG990WL": None, "AH961KD": None, "AG990WM": None, "AH068SE": None,
    "AH560UF": None, "SVI393": 538, "RFW595": 547, "CHJ554": 555, "IWF382": 558,
    "IWF383": 559, "KXN578": 560, "KXN579": 561, "AD690OM": 568, "AE221MF": 571,
    "AE241RL": 573, "AG118FI": 574, "AG118FH": 575, "AE221MQ": 570, "TWO885": 602,
    "AG283ZT": 578, "SMY932": 536,
}

# Ítem de auditoría -> regex sobre la descripción del artículo (mayúsculas, sin tildes)
ITEMS = {
    "Matafuegos": r"MATAFUEGO|EXTINT",
    "Cinturón de seguridad": r"CINTURON",
    "Botiquín": r"BOTIQUIN",
    "Arrestallamas": r"ARRESTA ?LLAMA",
    "Banda / calcomanía reflectiva": r"REFLECTIV|CALCOMAN|OJO DE GATO|CATADIOPTRIC",
    "Calzas y conos": r"\bCALZAS?\b|CONOS? (?:DE )?SENAL",
    "Luces": r"LAMPARA|\bFAROS?\b|FAROL|OPTICA|\bLED\b|\bLUZ\b|\bLUCES\b|BALIZA|\bBULBO|PLAFON",
    "Michelin (cubiertas)": r"MICHELIN",
    "Botón Imseg / pánico": r"IMSEG|PANICO",
    "Espejos": r"ESPEJO",
    "Rótulo riesgo / panel ONU": r"ROMBO|\bONU\b|PANEL NARANJA|PLACA NARANJA",
    "Mangueras de producto (cisterna)": r"PORTA ?MANGUERA|MANGUERA.*(?:CISTERN|DESCARGA|CRIOG|PRODUCTO)|BRIDA.*CISTERN",
    "Stop-away": r"STOP ?-?AWAY",
    "Frenos": r"FRENO|PASTILLA|ZAPATA|CAMPANA|PULMON|VALVULA RELAY|CHICHARRA DE FRENO",
    "Alarma / luz de retroceso": r"ALARMA|RETROCESO|ZUMBADOR|BUZZER|CHICHARRA(?! DE FRENO)",
    "Auxiliares (cubiertas/llantas)": r"CUBIERTA|NEUMATICO|\bLLANTA|PORTA ?AUXILIO|AUXILIO",
    "Candado portamanguera": r"CANDADO",
    "Chapa patente": r"PATENTE",
}


def norm(s):
    s = str(s).upper()
    return s.translate(str.maketrans("ÁÉÍÓÚÜÑ", "AEIOUUN"))


def leer(path, header=5):
    return pd.read_excel(path, engine="openpyxl", header=header)


def vehiculos(path):
    v = leer(path).iloc[:, :13]
    v.columns = ["pat", "marca", "modelo", "version", "anio", "color", "cliente",
                 "serie", "codprod", "desc", "f_ult_serv", "km", "interno"]
    v = v.dropna(subset=["pat"])
    v["pat"] = v["pat"].astype(str).str.replace(" ", "").str.upper()
    # El campo Interno viene siempre en 0: el interno real está en el texto del modelo
    v["interno_modelo"] = v["modelo"].astype(str).str.extract(r"CISTERNA\s+(\d{3})")[0]
    return v


def main(carpeta, salida):
    carpeta = Path(carpeta)
    v = vehiculos(carpeta / "vehiculos.xls")

    flota = pd.DataFrame({"pat": list(FLOTA), "interno_lista": list(FLOTA.values())})
    flota = flota.merge(v[["pat", "marca", "modelo", "anio", "cliente", "km", "interno_modelo"]],
                        on="pat", how="left")
    flota["en_vehiculos"] = flota["marca"].notna()
    flota["interno_ok"] = flota.apply(
        lambda r: "sin interno" if pd.isna(r.interno_lista)
        else ("OK" if str(int(r.interno_lista)) == str(r.interno_modelo) else "DIFIERE"), axis=1)

    es_al = (v["marca"].astype(str).str.contains("AIR LIQUIDE")
             | v["modelo"].astype(str).str.contains("CISTERNA"))
    fuera = v[es_al & ~v["pat"].isin(FLOTA)][["pat", "marca", "modelo", "anio", "cliente", "km"]]

    a = leer(carpeta / "articulos.xls").dropna(subset=["Artículo"])
    a["_n"] = a["Artículo"].map(norm)
    filas = []
    for item, rx in ITEMS.items():
        m = a[a["_n"].str.contains(rx, regex=True)]
        for _, r in m.iterrows():
            filas.append({"item_auditoria": item, "codigo": r["Código"], "articulo": r["Artículo"],
                          "stock": r["Stock"], "venta": r["Venta"], "ubicacion": r["Ubicación"]})
    art = pd.DataFrame(filas)
    resumen = (art.groupby("item_auditoria")
               .agg(articulos=("codigo", "count"),
                    con_stock_negativo=("stock", lambda s: int((s < 0).sum())))
               .reindex(ITEMS.keys()).fillna(0).astype(int).reset_index())

    c = leer(carpeta / "clientes.xls").dropna(subset=["Razón Social"])
    cli = c[["Código", "Razón Social", "Estado", "Tipo IVA"]]

    with pd.ExcelWriter(salida) as xw:
        flota.to_excel(xw, sheet_name="flota_vs_vehiculos", index=False)
        fuera.to_excel(xw, sheet_name="AL_fuera_de_lista", index=False)
        resumen.to_excel(xw, sheet_name="resumen_items", index=False)
        art.to_excel(xw, sheet_name="articulos_por_item", index=False)
        cli.to_excel(xw, sheet_name="clientes", index=False)
    return flota, fuera, resumen, art, cli


if __name__ == "__main__":
    flota, fuera, resumen, art, cli = main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2
                                           else "maestros_auditoria.xlsx")
    pd.set_option("display.width", 200)
    print(flota.to_string(index=False))
    print(fuera.to_string(index=False))
    print(resumen.to_string(index=False))
