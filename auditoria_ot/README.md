# Auditoría de flota × órdenes de trabajo (OT)

Continuación del handoff del 29/09/2026. Script: `analisis_maestros.py <carpeta_con_xls> [salida.xlsx]`.
Los `.xls` (vehiculos, articulos, clientes) son xlsx renombrados; encabezado en la fila 6 y **sin** desplazamiento de columnas (a diferencia de `ordenes.xls`). Los datos no se versionan (`.gitignore`).

## vehiculos.xls (352 unidades)
- Las **32 patentes** de la flota auditada existen y todas figuran como cliente TRANSTOTAL.
- La columna `Interno` viene siempre en 0. El interno real está en el texto del modelo (`CISTERNA 538`). Los **16 internos** de la lista coinciden todos.
- Hay tres chasis cisterna Atego en la lista sin interno, cuyo número de cisterna está en el modelo: AC646NF → 672, AE460TD → 613, AF378NF → 671.
- Error de dato: AD690OM (568) tiene año **219** (debería ser 2019).
- **Unidades Air Liquide que no están en la lista** (a confirmar si entran en la auditoría):
  CLD321 (703), EDX933 (709), SMZ040 (537, cliente AIR LIQUIDE), STF787 (535), STF791 (534), SVI394 (539).
  También hay otras cisternas de acero inoxidable (BFV367, CJV954, EAH613, EDI326, OGX769).

## articulos.xls (2.257 artículos)
Es el catálogo y el stock de repuestos (código, descripción, precio, stock y ubicación). **No tiene Id OT, número de comprobante ni ninguna clave hacia órdenes**, y en `ordenes.xls` las columnas de producto e importe están en cero.
→ Se confirma que **el cruce OT ↔ ítem no se puede hacer** con estos archivos. Hay que pedir al sistema de taller la exportación de **detalle de OT (ítems por orden)**.

Lo que sí se hizo: clasificar el catálogo por ítem de auditoría con palabras clave, para tener listo el diccionario el día que llegue el detalle:

| Ítem de auditoría | Artículos | Con stock < 0 |
|---|---:|---:|
| Matafuegos (extintor 5/10 kg + soportes) | 5 | 2 |
| Cinturón de seguridad | 4 | 1 |
| Botiquín | 0 | 0 |
| Arrestallamas | 1 | 1 |
| Banda / calcomanía reflectiva | 1 | 0 |
| Calzas y conos | 3 | 0 |
| Luces | 182 | 44 |
| Michelin (cubiertas) | 5 | 2 |
| Botón Imseg / pánico | 0 | 0 |
| Espejos | 19 | 9 |
| Rótulo riesgo / panel ONU | 1 | 1 |
| Mangueras de producto (cisterna) | 0 | 0 |
| Stop-away | 0 | 0 |
| Frenos | 68 | 17 |
| Alarma / luz de retroceso | 1 | 1 |
| Auxiliares (cubiertas/llantas) | 143 | 51 |
| Candado portamanguera | 5 | 0 |
| Chapa patente (faro porta patente) | 3 | 1 |

Un stock negativo indica que el artículo se consumió sin haber registrado la entrada, pero no dice en qué unidad se usó. Botiquín, Imseg, Stop-away y mangueras de producto no aparecen en el catálogo: probablemente se compran o gestionan por fuera del taller.

## clientes.xls (51 clientes)
Es un maestro simple, sin claves útiles para el cruce. AIR LIQUIDE es el código 53.

## Pendiente
1. Pedir la exportación de detalle de OT (Id OT + código de artículo o descripción del trabajo).
2. Con eso, armar la matriz patente × ítem con las OT que respaldan cada punto, más el motivo de las 20 OT en Diagnóstico.
3. Definir si las 6 unidades Air Liquide que quedaron fuera de la lista se suman a la auditoría.

## Reparaciones por OT (`reparaciones_por_ot.py`)
Con los exports buenos de Copérnico (`ordenes_completo.xls`, `tareas_ot.txt`, `items_remitos.txt`), cada OT queda como
"OT N° · patente · qué se le hizo · repuestos que se le pusieron". El vínculo con los repuestos es
`Cbte.Venta` RS-AAAA-N ↔ remito de salida RSM-R-AAAA-N.

    python reparaciones_por_ot.py <carpeta_exports> 2026-08-01 2026-09-30 Reparaciones_flota.xlsx

Agosto y septiembre de 2026 (el export llega al 10/09): 148 OT de la flota. De ellas, 86 tienen repuestos, y las 12 sin tareas son todas OT abiertas en diagnóstico.

## OT relacionadas con el checklist (`ot_vs_checklist.py`)
Clasifica cada tarea y cada repuesto de las OT contra los puntos del checklist de auditoría y deja solo las OT que tocan al menos uno. Muestra únicamente los renglones relacionados.
Criterios: los controles "para VTV" cuentan como R.T.O. En "Auxiliares" entran las ruedas de auxilio, pero no los faros ni los espejos auxiliares. Las mangueras de vigía (sistema de inflado) no cuentan como mangueras de la cisterna.

    python ot_vs_checklist.py <carpeta_exports> 2026-08-01 2026-09-30 OT_checklist.xlsx
