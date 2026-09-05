#!/usr/bin/env python3
"""Mejora el Gestor_de_Gastos.xlsx: Billetera acumulada, Pagos por tarjeta y cuotas marcadas.

Uso: python3 scripts/mejorar_gestor.py entrada.xlsx salida.xlsx

Cambios que aplica sobre la planilla original (conserva todo lo demás):
  * Nueva hoja "Pagos": por mes, cuánto pagar de Crédito / MercadoPago / Otros
    y una celda amarilla "Pagado el" por tarjeta para marcar la fecha de pago.
  * Nueva hoja "Billetera": saldo inicial + ingresos - gastos - ahorro - tarjetas
    pagadas + fondo Aston Birra = plata que deberías tener hoy; pendientes de
    pago, disponible real, control de caja y sobrante acumulado mes a mes.
  * Cuotas: "Pagadas", "Faltan" y "Estado" se calculan con las marcas de Pagos
    (ya no con la fecha de hoy). Se agregan "Restante ($)" y "Próxima a pagar".
  * Tablero: arregla la fórmula faltante de Supermercado (C18), el TOTAL que
    mezclaba ingresos y gastos, y muestra Crédito / MercadoPago del mes y la
    Billetera.
  * Movimientos: borra la fila de ejemplo y corrige los desplegables de Tipo y
    Medio de pago para que lean Configuración completa.
  * Instrucciones: agrega la explicación del nuevo circuito.
"""
import sys
import warnings
from copy import copy
from datetime import date

import openpyxl
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

warnings.filterwarnings("ignore")

# ---- paleta de la planilla original -------------------------------------
AZUL_TITULO = "FF1F3A5F"
AZUL_HEADER = "FF2E5C8A"
VERDE = "FF2E7D32"
ROJO = "FFC0392B"
GRIS = "FF7F8C8D"
CELESTE = "FFDCE6F1"
AMARILLO = "FFFFF2CC"
AZUL_INPUT = "FF0000FF"
BORDE = "FFBFC9D4"
MONEDA = '"$ "#,##0;[Red]"-$ "#,##0'
FECHA = "d/m/yyyy"

thin = Side(style="thin", color=BORDE)
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)


def fill(rgb):
    return PatternFill(fill_type="solid", start_color=rgb, end_color=rgb)


def style(cell, *, bold=False, size=10, color="FF000000", bg=None, fmt=None,
          h=None, v="center", wrap=False, border=True, italic=False):
    cell.font = Font(name="Arial", size=size, bold=bold, color=color, italic=italic)
    if bg:
        cell.fill = fill(bg)
    if fmt:
        cell.number_format = fmt
    cell.alignment = Alignment(horizontal=h, vertical=v, wrap_text=wrap)
    if border:
        cell.border = BORDER


def title(ws, ref, text, size=16):
    ws[ref] = text
    style(ws[ref], bold=True, size=size, color="FFFFFFFF", bg=AZUL_TITULO, h="left", border=False)


def note(ws, ref, text):
    ws[ref] = text
    style(ws[ref], color=GRIS, size=9, italic=True, h="left", wrap=True, border=False)


def header(cell, text, bg=AZUL_HEADER):
    cell.value = text
    style(cell, bold=True, color="FFFFFFFF", bg=bg, h="center", wrap=True)


def money(cell, formula, bold=False, size=10, color="FF000000", bg=None):
    cell.value = formula
    style(cell, fmt=MONEDA, bold=bold, size=size, color=color, bg=bg)


def label(cell, text, bold=False, bg=None, color="FF000000", indent=False):
    cell.value = text
    style(cell, bold=bold, bg=bg, color=color, h="left")
    if indent:
        cell.alignment = Alignment(horizontal="left", vertical="center", indent=2)


def entrada(cell, value=None, fmt=None):
    """Celda amarilla que completa el usuario (convención de la planilla)."""
    cell.value = value
    style(cell, color=AZUL_INPUT, bg=AMARILLO, fmt=fmt)


def idx(y, m):
    return y * 12 + m


# (año, mes), columna de Pagos, valor. D/G/J = "Pagado el"; E/H/K = "Monto real pagado".
PAGOS_REALES = [
    ((2026, 8), "E", 452253),                    # Visa cierre 27/07: pago del 06/08 (436.451,55 + USD 10,43 al 1.515)
    ((2026, 8), "H", 202017.61),                 # Mercado Pago cierre 27/07: débito automático del 06/08
    ((2026, 9), "D", "✔"),                       # Visa cierre 27/08: pagada (1.150.000 + USD 32, sin Anthropic)
    ((2026, 9), "E", "=1150000+32*1514"),        # editá el 1514 por el cambio al que compraste los dólares
    ((2026, 9), "G", date(2026, 9, 2)),          # Mercado Pago cierre 27/08: débito automático del 02/09
    ((2026, 9), "H", 273984.72),
]

MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
         "Septiembre", "Octubre", "Noviembre", "Diciembre"]


# =========================================================================
def main(src, dst):
    wb = openpyxl.load_workbook(src)
    cfg, mov, cuo, tab, ins, ast = (wb["Configuración"], wb["Movimientos"], wb["Cuotas"],
                                    wb["Tablero"], wb["Instrucciones"], wb["Aston Birra"])
    anio = int(cfg["B3"].value)
    hoy = date.today()
    hoy_idx = idx(hoy.year, hoy.month)

    # ------------------------------------------------------------ Movimientos
    if mov["D4"].value and "ejemplo" in str(mov["D4"].value).lower():
        mov.delete_rows(4)
        for r in range(4, 605):
            mov[f"G{r}"] = f'=IF($A{r}="","",TEXT($A{r},"YYYY-MM"))'
        for col in "ABCDEFG":
            mov[f"{col}604"]._style = copy(mov[f"{col}603"]._style)
    for dv in mov.data_validations.dataValidation:
        if "E4" in str(dv.sqref):
            dv.formula1 = "'Configuración'!$E$7:$E$13"
        if "B4" in str(dv.sqref):
            dv.formula1 = "'Configuración'!$F$7:$F$10"

    # ------------------------------------------------------------------ Pagos
    # Columnas: A idx(oculta) | B Mes | C/D/E Crédito: a pagar, pagado el, monto real |
    # F/G/H MercadoPago | I/J/K Otros | L Total | M Pendiente | N Estado | O Diferencia | P auxiliar
    pg = wb.create_sheet("Pagos")
    pg.sheet_view.showGridLines = False
    pg.merge_cells("A1:O1")
    title(pg, "A1", "💳  Pagos  —  qué pagar cada mes, cuándo lo pagaste y cuánto pagaste de verdad")
    pg.row_dimensions[1].height = 30
    pg.merge_cells("A2:O2")
    note(pg, "A2", "Cada fila es un mes. 'A pagar' sale solo de la hoja Cuotas. Cuando pagues el resumen de una tarjeta, "
         "escribí la fecha (o una ✔) en 'Pagado el' y, si el resumen fue distinto a lo calculado (impuestos, comisiones, "
         "dólares al cambio del día), escribí el importe en 'Monto real': la Billetera descuenta ese importe y la columna "
         "'Diferencia' te muestra cuánto quedó sin cargar en Cuotas. Los meses anteriores a la creación de esta hoja ya "
         "quedaron marcados con ✔.")
    pg.row_dimensions[2].height = 60
    pg["P1"] = "=YEAR(TODAY())*12+MONTH(TODAY())"   # índice del mes actual (auxiliar)
    pg["P2"] = "hoy (auxiliar)"
    pg.column_dimensions["P"].hidden = True

    heads = ["idx", "Mes",
             "💳 Crédito\na pagar", "Pagado el\n(fecha o ✔)", "Monto real\npagado (opcional)",
             "🟡 MercadoPago\na pagar", "Pagado el\n(fecha o ✔)", "Monto real\npagado (opcional)",
             "Otros a pagar\n(préstamo, débito…)", "Pagado el\n(fecha o ✔)", "Monto real\npagado (opcional)",
             "Total del mes\n(calculado)", "Pendiente", "Estado", "Diferencia\nreal − calculado"]
    for i, h in enumerate(heads, 1):
        header(pg.cell(4, i), h)
    pg.row_dimensions[4].height = 42
    FIRST, N_MESES = 5, 36
    LAST = FIRST + N_MESES - 1
    y, m = anio - 1, 1
    for r in range(FIRST, LAST + 1):
        pg[f"A{r}"] = idx(y, m)                       # índice del mes (columna oculta)
        pg[f"B{r}"] = f"{MESES[m - 1]} {y}"
        style(pg[f"B{r}"], bold=True, h="left")
        cu = f"(Cuotas!$M$5:$M$102<=$A{r})*(Cuotas!$N$5:$N$102>=$A{r})"
        money(pg[f"C{r}"], f'=SUMPRODUCT({cu}*(Cuotas!$C$5:$C$102="Crédito")*Cuotas!$F$5:$F$102)')
        entrada(pg[f"D{r}"], fmt=FECHA)
        entrada(pg[f"E{r}"], fmt=MONEDA)
        money(pg[f"F{r}"], f'=SUMPRODUCT({cu}*(Cuotas!$C$5:$C$102="MercadoPago")*Cuotas!$F$5:$F$102)')
        entrada(pg[f"G{r}"], fmt=FECHA)
        entrada(pg[f"H{r}"], fmt=MONEDA)
        money(pg[f"I{r}"], f"=SUMPRODUCT({cu}*Cuotas!$F$5:$F$102)-C{r}-F{r}")
        entrada(pg[f"J{r}"], fmt=FECHA)
        entrada(pg[f"K{r}"], fmt=MONEDA)
        money(pg[f"L{r}"], f"=C{r}+F{r}+I{r}", bold=True)
        money(pg[f"M{r}"], f'=IF(D{r}="",C{r},0)+IF(G{r}="",F{r},0)+IF(J{r}="",I{r},0)', color=ROJO)
        pg[f"N{r}"] = (f'=IF(L{r}=0,"—",IF(M{r}=0,"✅ Todo pagado",IF($A{r}<Pagos!$P$1,"⚠️ Atrasado",'
                       f'IF($A{r}=Pagos!$P$1,"⏳ Pagar este mes","📅 Próximo"))))')
        style(pg[f"N{r}"], h="center")
        money(pg[f"O{r}"], (f'=IF(AND(D{r}<>"",E{r}<>""),E{r}-C{r},0)+IF(AND(G{r}<>"",H{r}<>""),H{r}-F{r},0)'
                            f'+IF(AND(J{r}<>"",K{r}<>""),K{r}-I{r},0)'), color=GRIS)
        pg.row_dimensions[r].height = 20
        m += 1
        if m == 13:
            y, m = y + 1, 1
    # Marcar como pagados los meses anteriores al actual (la planilla se creó con esas cuotas ya pagas)
    grupos = {"Crédito": "D", "MercadoPago": "G"}
    for r in range(5, 103):
        d, n, f, medio = cuo[f"D{r}"].value, cuo[f"E{r}"].value, cuo[f"F{r}"].value, cuo[f"C{r}"].value
        if not d or not n:
            continue
        col = grupos.get(medio, "J")
        ini = idx(d.year, d.month)
        for k in range(ini, min(ini + int(n) - 1, hoy_idx - 1) + 1):
            row = FIRST + (k - idx(anio - 1, 1))
            if FIRST <= row <= LAST:
                pg[f"{col}{row}"] = "✔"
                pg[f"{col}{row}"].alignment = Alignment(horizontal="center", vertical="center")
    # Pagos reales informados por el usuario (resúmenes Visa Galicia y Mercado Pago, cierres 27/07 y 27/08/2026)
    for (yy, mm), col, val in PAGOS_REALES:
        row = FIRST + (idx(yy, mm) - idx(anio - 1, 1))
        if FIRST <= row <= LAST:
            pg[f"{col}{row}"] = val
            if isinstance(val, str) and val == "✔":
                pg[f"{col}{row}"].alignment = Alignment(horizontal="center", vertical="center")
    tr = LAST + 2
    for rr in (tr, tr + 1):
        pg.merge_cells(f"B{rr}:K{rr}")
        for col in "CDEFGHIJK":
            style(pg[f"{col}{rr}"], bg=CELESTE)
    label(pg[f"B{tr}"], "Pendiente de pago (meses vencidos y el actual)", bold=True, bg=CELESTE)
    money(pg[f"L{tr}"], f"=SUMPRODUCT(($A${FIRST}:$A${LAST}<=Pagos!$P$1)*$M${FIRST}:$M${LAST})", bold=True, color=ROJO, bg=CELESTE)
    label(pg[f"B{tr+1}"], "Comprometido en meses futuros", bold=True, bg=CELESTE)
    money(pg[f"L{tr+1}"], f"=SUMPRODUCT(($A${FIRST}:$A${LAST}>Pagos!$P$1)*$L${FIRST}:$L${LAST})", bold=True, bg=CELESTE)
    pg.merge_cells(f"B{tr+3}:O{tr+3}")
    pg.row_dimensions[tr + 3].height = 30
    note(pg, f"B{tr+3}", "Cubre desde enero del año anterior hasta diciembre del año siguiente al de Configuración. "
         "Si una compra termina después, agregá filas copiando la última. Los dólares de la Visa se pagan en dólares: "
         "en 'Monto real' poné pesos + dólares al cambio del día que pagaste.")
    pg.conditional_formatting.add(f"B{FIRST}:O{LAST}", FormulaRule(formula=[f"$A{FIRST}=Pagos!$P$1"], fill=fill("FFE8F0FA")))
    pg.conditional_formatting.add(f"N{FIRST}:N{LAST}", FormulaRule(formula=[f'ISNUMBER(SEARCH("Atrasado",N{FIRST}))'], font=Font(color=ROJO, bold=True), fill=fill("FFF8CBAD")))
    pg.conditional_formatting.add(f"N{FIRST}:N{LAST}", FormulaRule(formula=[f'ISNUMBER(SEARCH("Todo pagado",N{FIRST}))'], font=Font(color=VERDE, bold=True)))
    pg.conditional_formatting.add(f"N{FIRST}:N{LAST}", FormulaRule(formula=[f'ISNUMBER(SEARCH("Pagar este mes",N{FIRST}))'], font=Font(color=ROJO, bold=True)))
    pg.conditional_formatting.add(f"O{FIRST}:O{LAST}", CellIsRule(operator="notEqual", formula=["0"], font=Font(color="FFB9770E", bold=True)))
    pg.column_dimensions["A"].hidden = True
    for col, w in zip("BCDEFGHIJKLMNO", [17, 14, 13, 15, 15, 13, 15, 15, 13, 15, 15, 14, 18, 15]):
        pg.column_dimensions[col].width = w
    pg.freeze_panes = "C5"

    # ----------------------------------------------------------------- Cuotas
    # Validaciones heredadas rotas (#REF! y una "custom" sin fórmula): Excel las rechaza.
    from openpyxl.worksheet.datavalidation import DataValidation
    cuo.data_validations.dataValidation = [
        dv for dv in cuo.data_validations.dataValidation
        if not ("B5:C102" in str(dv.sqref) or "F5:G102" in str(dv.sqref))
    ]
    for rng, src in (("B5:B102", "'Configuración'!$A$7:$A$34"), ("C5:C102", "'Configuración'!$E$7:$E$13")):
        dv = DataValidation(type="list", formula1=src, allow_blank=True, showErrorMessage=False)
        dv.add(rng)
        cuo.add_data_validation(dv)
    cuo["A2"] = ("Completá sólo lo amarillo (A–F). El total, el período y el estado se calculan solos y cada cuota "
                 "se suma al Tablero y al Resumen del mes que corresponde. 'Pagadas' y 'Faltan' salen de las marcas "
                 "que hacés en la hoja Pagos cuando pagás cada tarjeta.")
    cuo["K4"] = "Faltan"
    # La "Tabla_1" y el autofiltro que exportó Google Sheets se superponen en A4:L102 y
    # Excel los rechaza al abrir ("Característica quitada: Tabla"). Se dejan como rango común.
    if "Tabla_1" in cuo.tables:
        del cuo.tables["Tabla_1"]
    cuo.auto_filter.ref = None
    cuo["P4"] = "Restante ($)"
    cuo["Q4"] = "Próxima a pagar"
    for c in ("P4", "Q4"):
        cuo[c]._style = copy(cuo["L4"]._style)
    PA = f"Pagos!$A${FIRST}:$A${LAST}"
    for r in range(5, 103):
        pagos_marca = (f'(($C{r}="Crédito")*(Pagos!$D${FIRST}:$D${LAST}<>"")'
                       f'+($C{r}="MercadoPago")*(Pagos!$G${FIRST}:$G${LAST}<>"")'
                       f'+($C{r}<>"Crédito")*($C{r}<>"MercadoPago")*(Pagos!$J${FIRST}:$J${LAST}<>""))')
        cuo[f"J{r}"] = f'=IF($D{r}="","",SUMPRODUCT(({PA}>=$M{r})*({PA}<=$N{r})*{pagos_marca}))'
        cuo[f"K{r}"] = f'=IF($D{r}="","",$E{r}-$J{r})'
        cuo[f"L{r}"] = (f'=IF($D{r}="","",IF($J{r}>=$E{r},"✅ Finalizado",'
                        f'IF(MIN($E{r},Pagos!$P$1-$M{r})>$J{r},"⚠️ Atrasada "&$J{r}&"/"&$E{r},'
                        f'IF($M{r}>Pagos!$P$1,"⏳ Por comenzar","🔵 En curso "&$J{r}&"/"&$E{r}))))')
        cuo[f"P{r}"] = f'=IF($D{r}="","",$K{r}*$F{r})'
        cuo[f"Q{r}"] = f'=IF($D{r}="","",IF($K{r}=0,"—",TEXT(EDATE($D{r},$J{r}),"MM/YYYY")))'
        cuo[f"K{r}"]._style = copy(cuo[f"J{r}"]._style)
        cuo[f"P{r}"]._style = copy(cuo[f"G{r}"]._style)
        cuo[f"Q{r}"]._style = copy(cuo[f"H{r}"]._style)
    cuo.conditional_formatting._cf_rules.clear()
    cuo.conditional_formatting.add("L5:L102", FormulaRule(formula=['ISNUMBER(SEARCH("Finalizado",L5))'], font=Font(color=VERDE, bold=True)))
    cuo.conditional_formatting.add("L5:L102", FormulaRule(formula=['ISNUMBER(SEARCH("Por comenzar",L5))'], font=Font(color=GRIS)))
    cuo.conditional_formatting.add("L5:L102", FormulaRule(formula=['ISNUMBER(SEARCH("Atrasada",L5))'], font=Font(color=ROJO, bold=True), fill=fill("FFF8CBAD")))
    cuo.column_dimensions["L"].width = 20
    cuo.column_dimensions["P"].width = 15
    cuo.column_dimensions["Q"].width = 15

    # ---------------------------------------------------------------- Tablero
    tab["C18"] = tab["C17"].value.replace("$A17", "$A18")
    tab["C18"]._style = copy(tab["C17"]._style)
    tab["A37"] = "TOTAL GASTOS"
    tab["C37"] = '=SUMIF($B$10:$B$36,"Gasto",C10:C36)'
    tab["D37"] = '=SUMIF($B$10:$B$36,"Gasto",D10:D36)'
    tab["E37"] = '=IF(N(D37)=0,"",D37-C37)'
    tab["F37"] = '=IF(N(D37)=0,"",C37/D37)'
    for c in ("E37", "F37"):
        tab[c]._style = copy(tab["C37"]._style)
    tab["F37"].number_format = "0.0%"
    header(tab["E5"], "💳 Crédito del mes", bg=AZUL_HEADER)
    header(tab["F5"], "🟡 MercadoPago del mes", bg=AZUL_HEADER)
    header(tab["G5"], "👛 Billetera hoy", bg=AZUL_HEADER)
    money(tab["E6"], f"=SUMIFS(Pagos!$C${FIRST}:$C${LAST},{PA},$H$2)", bold=True, size=14, color=ROJO, bg=CELESTE)
    money(tab["F6"], f"=SUMIFS(Pagos!$F${FIRST}:$F${LAST},{PA},$H$2)", bold=True, size=14, color=ROJO, bg=CELESTE)
    money(tab["G6"], "=Billetera!$B$15", bold=True, size=14, color=AZUL_TITULO, bg=CELESTE)
    for c in "EFG":
        tab[f"{c}6"].alignment = Alignment(horizontal="center", vertical="center")
    tab["E7"] = (f'=IFERROR(IF(E6=0,"sin cuotas",IF(INDEX(Pagos!$D${FIRST}:$D${LAST},MATCH($H$2,{PA},0))<>"",'
                 f'"✅ pagado","⏳ pendiente")),"")')
    tab["F7"] = (f'=IFERROR(IF(F6=0,"sin cuotas",IF(INDEX(Pagos!$G${FIRST}:$G${LAST},MATCH($H$2,{PA},0))<>"",'
                 f'"✅ pagado","⏳ pendiente")),"")')
    tab["G7"] = "→ detalle en hoja Billetera"
    for c in "EFG":
        style(tab[f"{c}7"], size=9, color=GRIS, h="center", border=False, italic=True)
    tab.column_dimensions["E"].width = 18
    tab.column_dimensions["F"].width = 20
    tab.column_dimensions["G"].width = 20

    # -------------------------------------------------------------- Billetera
    bi = wb.create_sheet("Billetera")
    bi.sheet_view.showGridLines = False
    bi.merge_cells("A1:G1")
    title(bi, "A1", "👛  Billetera  —  cuánta plata deberías tener hoy")
    bi.row_dimensions[1].height = 30
    bi.merge_cells("A2:G2")
    note(bi, "A2", "Suma todos tus ingresos, resta los gastos sueltos, el ahorro que apartaste y las tarjetas que marcaste "
         "como pagadas en Pagos, y le suma el fondo de Aston Birra porque esa plata está en tu poder. "
         "Completá las celdas amarillas: el saldo inicial y, cuando quieras controlar, lo que contaste de verdad.")
    bi.row_dimensions[2].height = 48
    bi["H1"] = "=Pagos!$P$1"                       # mes actual
    bi["H2"] = ("=IF(COUNT(Movimientos!$A:$A)=0,$H$1,YEAR(MIN(Movimientos!$A:$A))*12"
                "+MONTH(MIN(Movimientos!$A:$A)))")  # primer mes cargado
    bi["I1"], bi["I2"] = "hoy (auxiliar)", "primer mes (auxiliar)"

    label(bi["A4"], "Saldo inicial: plata que tenías antes del primer movimiento cargado", bold=True)
    entrada(bi["B4"], 0, fmt=MONEDA)
    label(bi["A5"], "Fecha de hoy")
    bi["B5"] = "=TODAY()"
    style(bi["B5"], fmt=FECHA)
    label(bi["A6"], "Primer mes cargado en Movimientos")
    bi["B6"] = '=TEXT(DATE(INT(($H$2-1)/12),MOD($H$2-1,12)+1,1),"MM/YYYY")'
    style(bi["B6"], h="center")

    header(bi["A8"], "💰  Lo que deberías tener hoy", bg=VERDE)
    header(bi["B8"], "Monto", bg=VERDE)
    HOY = '"<="&TODAY()'
    label(bi["A9"], "Saldo inicial", indent=True)
    money(bi["B9"], "=$B$4")
    label(bi["A10"], "+ Ingresos cargados hasta hoy", indent=True)
    money(bi["B10"], f'=SUMIFS(Movimientos!$F:$F,Movimientos!$B:$B,"Ingreso",Movimientos!$A:$A,{HOY})', color=VERDE)
    label(bi["A11"], "− Gastos sueltos hasta hoy (Movimientos)", indent=True)
    money(bi["B11"], f'=SUMIFS(Movimientos!$F:$F,Movimientos!$B:$B,"Gasto",Movimientos!$A:$A,{HOY})', color=ROJO)
    label(bi["A12"], "− Ahorro apartado (no cuenta como disponible)", indent=True)
    money(bi["B12"], f'=SUMIFS(Movimientos!$F:$F,Movimientos!$B:$B,"Ahorro",Movimientos!$A:$A,{HOY})', color=ROJO)
    label(bi["A13"], "− Tarjetas y cuotas ya pagadas (monto real si lo cargaste en Pagos)", indent=True)
    money(bi["B13"], f'=SUMPRODUCT(({PA}>=$H$2)*((Pagos!$D${FIRST}:$D${LAST}<>"")*(Pagos!$E${FIRST}:$E${LAST}+(Pagos!$E${FIRST}:$E${LAST}="")*Pagos!$C${FIRST}:$C${LAST})'
                     f'+(Pagos!$G${FIRST}:$G${LAST}<>"")*(Pagos!$H${FIRST}:$H${LAST}+(Pagos!$H${FIRST}:$H${LAST}="")*Pagos!$F${FIRST}:$F${LAST})'
                     f'+(Pagos!$J${FIRST}:$J${LAST}<>"")*(Pagos!$K${FIRST}:$K${LAST}+(Pagos!$K${FIRST}:$K${LAST}="")*Pagos!$I${FIRST}:$I${LAST})))', color=ROJO)
    label(bi["A14"], "+ Fondo Aston Birra (está en tu poder)", indent=True)
    money(bi["B14"], "='Aston Birra'!$B$6", color=VERDE)
    label(bi["A15"], "👛 TOTAL: deberías tener hoy", bold=True, bg=CELESTE)
    money(bi["B15"], "=B9+B10-B11-B12-B13+B14", bold=True, size=14, color=AZUL_TITULO, bg=CELESTE)
    bi.row_dimensions[15].height = 30
    label(bi["A16"], "de eso, es plata del club Aston Birra", color=GRIS, indent=True)
    money(bi["B16"], "=B14", color=GRIS)
    label(bi["A17"], "plata propia", color=GRIS, indent=True)
    money(bi["B17"], "=B15-B14", color=GRIS)

    header(bi["A19"], "💳  Lo que todavía tenés que pagar", bg=AZUL_HEADER)
    header(bi["B19"], "Monto", bg=AZUL_HEADER)
    label(bi["A20"], "Crédito pendiente (meses vencidos y actual)", indent=True)
    money(bi["B20"], f'=SUMPRODUCT(({PA}<=$H$1)*(Pagos!$D${FIRST}:$D${LAST}="")*Pagos!$C${FIRST}:$C${LAST})', color=ROJO)
    label(bi["A21"], "MercadoPago pendiente", indent=True)
    money(bi["B21"], f'=SUMPRODUCT(({PA}<=$H$1)*(Pagos!$G${FIRST}:$G${LAST}="")*Pagos!$F${FIRST}:$F${LAST})', color=ROJO)
    label(bi["A22"], "Otros pendientes (préstamo, etc.)", indent=True)
    money(bi["B22"], f'=SUMPRODUCT(({PA}<=$H$1)*(Pagos!$J${FIRST}:$J${LAST}="")*Pagos!$I${FIRST}:$I${LAST})', color=ROJO)
    label(bi["A23"], "✅ DISPONIBLE REAL después de pagar todo", bold=True, bg=CELESTE)
    money(bi["B23"], "=B15-B20-B21-B22", bold=True, size=14, color=VERDE, bg=CELESTE)
    bi.row_dimensions[23].height = 30
    label(bi["A24"], "Comprometido en cuotas de meses futuros (info)", color=GRIS, indent=True)
    money(bi["B24"], f"=SUMPRODUCT(({PA}>$H$1)*Pagos!$L${FIRST}:$L${LAST})", color=GRIS)

    header(bi["A26"], "🔎  Control de caja (opcional): contá lo que tenés y compará", bg=AZUL_HEADER)
    header(bi["B26"], "Monto", bg=AZUL_HEADER)
    for r, t in ((27, "Efectivo que contaste"), (28, "Banco / débito"), (29, "MercadoPago / billeteras")):
        label(bi[f"A{r}"], t, indent=True)
        entrada(bi[f"B{r}"], fmt=MONEDA)
    label(bi["A30"], "Total real contado", bold=True)
    money(bi["B30"], "=SUM(B27:B29)", bold=True)
    label(bi["A31"], "Diferencia real − teórico (negativo = hay gastos sin cargar)", bold=True, bg=CELESTE)
    money(bi["B31"], '=IF(B30=0,"",B30-B15)', bold=True, bg=CELESTE)

    header(bi["A33"], "📅  Sobrante mes a mes (año de Configuración)", bg=VERDE)
    bi.merge_cells("A33:G33")
    for i, h in enumerate(["Mes", "Ingresos", "Gastos sueltos", "Cuotas del mes", "Ahorro",
                           "Sobrante del mes", "Acumulado\n(plata propia)"], 1):
        header(bi.cell(34, i), h)
    bi.row_dimensions[34].height = 30
    for i, nombre in enumerate(MESES, 1):
        r = 34 + i
        bi[f"H{r}"] = f"='Configuración'!$B$3*12+{i}"
        bi[f"I{r}"] = f'=TEXT(DATE(\'Configuración\'!$B$3,{i},1),"YYYY-MM")'
        label(bi[f"A{r}"], nombre, bold=True)
        cond = f'IF(OR($H{r}<$H$2,$H{r}>$H$1),"",'
        money(bi[f"B{r}"], f'={cond}SUMIFS(Movimientos!$F:$F,Movimientos!$G:$G,$I{r},Movimientos!$B:$B,"Ingreso"))')
        money(bi[f"C{r}"], f'={cond}SUMIFS(Movimientos!$F:$F,Movimientos!$G:$G,$I{r},Movimientos!$B:$B,"Gasto"))')
        money(bi[f"D{r}"], f'={cond}SUMIFS(Pagos!$L${FIRST}:$L${LAST},{PA},$H{r}))')
        money(bi[f"E{r}"], f'={cond}SUMIFS(Movimientos!$F:$F,Movimientos!$G:$G,$I{r},Movimientos!$B:$B,"Ahorro"))')
        money(bi[f"F{r}"], f'=IF(B{r}="","",B{r}-C{r}-D{r}-E{r})', bold=True)
        money(bi[f"G{r}"], f'=IF(F{r}="","",$B$4+SUM($F$35:F{r}))', bold=True, color=AZUL_TITULO)
    label(bi["A47"], "TOTAL AÑO", bold=True, bg=CELESTE)
    for c in "BCDEF":
        money(bi[f"{c}47"], f"=SUM({c}35:{c}46)", bold=True, bg=CELESTE)
    style(bi["G47"], bg=CELESTE)
    note(bi, "A48", "Sólo se muestran los meses desde que empezaste a cargar hasta el mes actual. "
         "'Acumulado' = saldo inicial + sobrantes de cada mes: es tu plata propia si pagás todas las cuotas del mes. "
         "Coincide con 'Disponible real' menos el fondo Aston Birra.")
    bi.merge_cells("A48:G48")
    bi.row_dimensions[48].height = 36
    bi.conditional_formatting.add("F35:G46", CellIsRule(operator="lessThan", formula=["0"], font=Font(color=ROJO, bold=True)))
    bi.conditional_formatting.add("B31", CellIsRule(operator="lessThan", formula=["0"], font=Font(color=ROJO, bold=True)))
    bi.column_dimensions["A"].width = 58
    for c in "BCDEFG":
        bi.column_dimensions[c].width = 17
    bi.column_dimensions["H"].hidden = True
    bi.column_dimensions["I"].hidden = True
    bi.freeze_panes = "A4"

    # ------------------------------------------------------------ Aston Birra
    ast["A2"] = ("Hoja independiente: los aportes NO afectan tu Tablero personal, pero el saldo del fondo sí se suma "
                 "en tu Billetera porque la plata está en tu poder. Cargá cada aporte a la derecha; el saldo, la meta "
                 "y el total por persona se calculan solos.")

    # ---------------------------------------------------------- Instrucciones
    r0 = ins.max_row + 2
    ins[f"A{r0}"] = "Novedades: Billetera y Pagos"
    ins[f"A{r0}"]._style = copy(ins["A3"]._style)
    ins.merge_cells(f"A{r0}:B{r0}")
    ins.row_dimensions[r0].height = 24
    lineas = [
        "👛 Billetera → te dice cuánta plata deberías tener hoy: saldo inicial + ingresos − gastos − ahorro − tarjetas pagadas + fondo Aston Birra.",
        "   Cargá una vez el 'Saldo inicial' (lo que tenías antes del primer movimiento). Abajo ves el sobrante de cada mes y cómo se acumula.",
        "   'Control de caja': contá efectivo + banco + MercadoPago y compará con lo teórico. Si da negativo, hay gastos que no cargaste.",
        "💳 Pagos → una fila por mes con lo que debés pagar de Crédito, MercadoPago y Otros (sale solo de Cuotas).",
        "   Cuando pagás el resumen, escribí la fecha (o ✔) en 'Pagado el' y el importe real en 'Monto real' (si fue distinto a lo calculado: impuestos, comisiones, dólares).",
        "   'Diferencia' te muestra cuánto pagaste de más o de menos respecto de lo cargado en Cuotas: es lo que te falta cargar.",
        "💳 Cuotas → 'Pagadas', 'Faltan', 'Restante ($)' y 'Próxima a pagar' ahora salen de las marcas de Pagos. '⚠️ Atrasada' = hay un mes viejo sin marcar.",
        "📊 Tablero → arriba a la derecha ves Crédito y MercadoPago del mes elegido (con ✅/⏳ según lo hayas pagado) y tu Billetera de hoy.",
        "Circuito sugerido: 1) cargás movimientos a diario · 2) cuando cae el resumen, marcás el pago en Pagos · 3) miras Billetera para saber cuánto te queda.",
    ]
    for i, t in enumerate(lineas, 1):
        ins[f"A{r0+i}"] = t
        ins[f"A{r0+i}"]._style = copy(ins["A4"]._style)
        ins.row_dimensions[r0 + i].height = 19.5

    # ---------------------------------------------------------- orden de hojas
    orden = ["Movimientos", "Cuotas", "Pagos", "Tablero", "Billetera", "Resumen Anual",
             "Aston Birra", "Configuración", "Instrucciones"]
    wb._sheets = [wb[n] for n in orden]
    wb.active = orden.index("Tablero")
    wb.calculation.fullCalcOnLoad = True
    wb.save(dst)
    print("Guardado:", dst)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
