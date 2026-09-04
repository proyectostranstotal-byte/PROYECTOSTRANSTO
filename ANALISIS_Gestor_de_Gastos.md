# Análisis a fondo — `Gestor_de_Gastos.xlsx`

Archivo analizado: `Gestor_de_Gastos.xlsx` (Google Drive, 73 KB, modificado 04/09/2026).
Fecha del análisis: 04/09/2026. Todos los importes en pesos argentinos.

---

## 1. Qué es y cómo está armado

Es un gestor de gastos personales de 7 hojas. Los datos entran por dos hojas y el resto son cálculos:

| Hoja | Rol | Filas útiles |
|---|---|---|
| **Movimientos** | Entrada: cada ingreso/gasto/ahorro de un solo pago. Columna G (Período) se autocalcula con `TEXT(fecha,"YYYY-MM")`. | 83 movimientos (06/08/2026 → 04/09/2026) |
| **Cuotas** | Entrada: compras financiadas. Cargás fecha de 1ª cuota, cantidad y valor; el resto es automático. | 31 compras |
| **Tablero** | Salida: elegís el mes (B3) y muestra Ingresos / Gastos / Ahorro / Disponible y el detalle por categoría contra presupuesto. | — |
| **Resumen Anual** | Salida: los 12 meses del año + total anual por categoría. | — |
| **Aston Birra** | Fondo del club de fútbol. Hoja aislada: **no** afecta el Tablero. | 2 aportes ($ 11.500) |
| **Configuración** | Listas maestras: 28 categorías con su Tipo, 7 medios de pago, 4 tipos, presupuesto mensual por categoría (todos vacíos). | — |
| **Instrucciones** | Texto de ayuda. | — |

### Mecánica de las fórmulas (lo importante para entender los números)

- **Índice de mes**: todo el libro identifica un mes como `año*12 + mes` (ej. sep-2026 = 24321). En `Cuotas` las columnas ocultas **M** (mes inicio) y **N** (mes fin) guardan ese índice.
- **Gasto de un mes** = `SUMIFS` de Movimientos con Tipo "Gasto" y Período igual al mes **+** `SUMPRODUCT` de todas las cuotas cuya ventana M..N contiene el mes. Así una compra en 12 cuotas suma su valor de cuota en cada uno de los 12 meses.
- **Total anual por categoría** (Resumen Anual col B) = 12 `SUMIFS` encadenados (uno por mes) + columna **O** de Cuotas, que calcula cuántas cuotas caen dentro del año configurado.
- **Pagadas / Restante / Estado** en Cuotas dependen de `TODAY()`, no del mes elegido en el Tablero. Cambian solos con el paso de los días.
- **Disponible** = Ingresos − Gastos − Ahorro. **Tasa de ahorro** = Ahorro / Ingresos.

Verifiqué recalculando desde cero: los totales de agosto y septiembre que muestra la planilla cierran exactamente con Movimientos + Cuotas. Las fórmulas están bien, con las excepciones de la sección 3.

---

## 2. Radiografía financiera

### Agosto 2026 (único mes completo cargado)

| Concepto | Monto |
|---|---|
| Ingresos | 2.344.180 |
| Gastos sueltos (Movimientos) | 1.516.037 |
| Gastos en cuotas / tarjeta | 726.461 |
| **Gastos totales** | **2.242.498** |
| Ahorro registrado | 0 |
| **Disponible** | **101.682 (4,3 % del ingreso)** |

Composición del ingreso de agosto: sueldo 1.587.180 + ajuste por aumento 414.000 + **adelanto de sueldo 100.000** + reintegro 100.000 + **"Ajuste Caja" 113.000** + otros 30.000.
Si se quitan el adelanto (es deuda, no ingreso) y el ajuste de caja (es un cuadre, no plata nueva), el ingreso genuino es 2.131.180 y agosto cierra en **−111.318**. Es decir: agosto se gastó todo el sueldo y un poco más.

Gasto de agosto por categoría (sueltos + cuotas):

| Categoría | Monto | % |
|---|---|---|
| Supermercado | 450.750 | 20,1 |
| Expensas / Servicios | 319.487 | 14,2 |
| Auto | 218.000 | 9,7 |
| Salud / Farmacia | 215.230 | 9,6 |
| Ropa / Cuidado personal | 205.504 | 9,2 |
| Ocio / Salidas | 180.400 | 8,0 |
| Gimnasio / Deporte | 150.614 | 6,7 |
| Transporte / Nafta | 130.000 | 5,8 |
| Música / Producción (notebook) | 120.666 | 5,4 |
| Otros gastos (devolución adelanto + HBO) | 101.547 | 4,5 |
| Regalos / Eventos | 75.300 | 3,4 |
| Comida / Delivery | 45.000 | 2,0 |
| Mascota | 22.000 | 1,0 |
| Internet / Celular | 8.000 | 0,4 |

Observaciones de agosto:

- **Supermercado son 35 compras chicas** (promedio 12.900). Es la categoría más grande y la más fragmentada: verdulería, pollería, carnicería casi día por medio.
- **El 75 % del gasto suelto es en efectivo** (1.144.250 de 1.516.037). El "Ajuste Caja" de 113.000 cargado como ingreso es el síntoma: hubo plata que no cuadró y se corrigió con un ingreso ficticio.
- Un solo gasto de ocio ("Viejo Balcón", 133.000) es el 74 % de toda la categoría del mes.
- Peluquería aparece dos veces en 3 días (16/8 y 19/8, 20.000 cada una). Verificar.

### Septiembre 2026 (4 días cargados)

| Concepto | Monto |
|---|---|
| Ingresos | 2.542.586 (dos filas "Sueldo" el 4/9: 1.034.000 + 1.458.586, más adelanto 50.000) |
| Gastos sueltos (4 días) | 75.250 (incluye la fila de ejemplo de 45.000, ver §3) |
| Cuotas / tarjeta ya comprometidas | **1.380.376** |
| Disponible hoy | 1.086.960 |

**Alerta principal**: las cuotas y el resumen de tarjeta de septiembre ya consumen el **54 % del ingreso** antes de cargar un solo gasto del día a día. Si el gasto suelto se repite como en agosto (~1,5 M), septiembre cerraría cerca de **−340.000**.

Lo que más pesa en septiembre:

| Categoría | Monto | Detalle |
|---|---|---|
| Ropa / Cuidado personal | 239.813 | Adidas Sport + Adidas Urban + zapas + ojotas + crema + balanza + reloj |
| Internet / Celular | 233.093 | Celular en 9 cuotas (total 2.097.837) |
| Auto | 159.000 | Seguro |
| Suplementos / Nutrición | 139.420 | Proteína 112.420 + creatina |
| Supermercado | 128.057 | 75.250 sueltos + 52.807 tarjeta |
| Música / Producción | 116.666 | Notebook (cuota 11 de 12) |
| Regalos / Eventos | 111.050 | Regalo Fiama (2 compras en cuotas) + regalo Benja |

Dos filas "Sueldo" el mismo día (4/9) suman 2.492.586, un 57 % más que el cobro de agosto (1.587.180). Puede ser banco + efectivo, pero conviene confirmar que no esté duplicado, porque infla el "Disponible" del Tablero.

### Compromisos futuros (cuotas ya tomadas)

Total financiado en Cuotas: 7.239.175. Falta pagar: **3.868.867**.

| Mes | Cuotas activas | Monto comprometido |
|---|---|---|
| 2026-10 | 19 | 873.462 |
| 2026-11 | 12 | 553.301 |
| 2026-12 | 10 | 485.039 |
| 2027-01 | 10 | 485.039 |
| 2027-02 | 9 | 471.739 |
| 2027-03 | 6 | 340.106 |
| 2027-04 | 5 | 271.892 |
| 2027-05 | 5 | 271.892 |
| 2027-06 a 08 | 4 | 38.799 (solo suscripciones) |

Por medio de pago: Crédito 6.414.819 (89 %), MercadoPago 606.868, Préstamo (adelanto de sueldo) 217.488.

El celular es el compromiso más grande: 233.093 por mes hasta mayo 2027, el 9 % del sueldo cada mes.

### Lo que la planilla todavía no aprovecha

- **Ahorro: 0**. No hay ningún movimiento de tipo "Ahorro", así que la tasa de ahorro es 0 % y el bloque de Ahorro del Tablero está vacío.
- **Presupuestos: ninguno cargado**. La columna amarilla de Configuración está en blanco, por lo que el semáforo rojo del Tablero (columna "% usado") nunca se activa.
- Enero a julio muestran gastos pero ingreso 0 (solo se ven las cuotas viejas de la notebook, el regalo y el Garmin). El Resumen Anual da un "Disponible" anual de −1.753.299 que no es real: es un artefacto de haber empezado a cargar en agosto.

---

## 3. Errores encontrados en la planilla (ordenados por impacto)

1. **Tablero!C18 (Supermercado) tiene un espacio en vez de la fórmula.** La celda "Movido en el mes" de Supermercado está vacía en todos los meses. Debería mostrar 128.057 para septiembre. Hay que copiar la fórmula de C17 hacia abajo.
2. **Tablero!C37 "TOTAL" suma ingresos + gastos + ahorro juntos** (3.870.155). No significa nada. Debería sumar solo las filas de Tipo "Gasto", o separarse en tres subtotales.
3. **Fila de ejemplo sin borrar**: Movimientos fila 4 ("Compra semanal (ejemplo, borrable)", 45.000, 04/09/2026) está sumando en septiembre. Borrarla.
4. **Cuotas: los desplegables de Categoría y Medio de pago están rotos.** La validación de B5:C102 apunta a `#REF!`. Hay que volver a apuntarla a `Configuración!$A$7:$A$34` y `Configuración!$E$7:$E$13`.
5. **"Prestamo" no aparece en el desplegable de Movimientos.** Está en Configuración!E13 pero la lista de Movimientos llega solo hasta E12.
6. **La categoría "ASTON BIRRA F.C" (Configuración fila 34) no existe en Tablero ni en Resumen Anual**: ambos leen hasta la fila 33. Además hay un Tipo y una Categoría con el mismo nombre, y el Tipo no entra en ningún total. Si la idea es que el club vaya solo por su hoja, conviene sacar ambos de Configuración para evitar confusión.
7. **El desplegable de Tipo está escrito a mano** (`"Ingreso,Gasto,Ahorro,ASTON BIRRA F.C"`) en lugar de leer Configuración!F7:F10. Si agregás un tipo en Configuración no se refleja.
8. **Aston Birra: la lista de nombres (A16:A27) está vacía**, así que el desplegable de "Nombre" no ofrece nada y el bloque "Aporte por persona" no muestra a nadie. Además "Saldo del fondo" es simplemente `=Total aportado`: no hay forma de registrar un gasto del fondo.
9. **Resumen Anual!B23:B49 usa 12 SUMIFS encadenados** por categoría. Funciona, pero se reemplaza por uno solo con comodín: `SUMIFS(Movimientos!$F:$F, Movimientos!$G:$G, $B$3&"-*", Movimientos!$C:$C, $A23) + SUMIFS(Cuotas!$O$5:$O$102, Cuotas!$B$5:$B$102, $A23)`.
10. **"Pagadas" y "Restante" en Cuotas usan `TODAY()`**, no el mes del Tablero. Si mirás un mes pasado, el Tablero muestra el gasto correcto pero el Estado de la cuota es el de hoy.
11. **La hoja Cuotas se usa también como resumen de tarjeta**: 9 de 31 filas tienen 1 sola cuota (718.801 en total). Es un uso válido (agrupa el cierre del 6 de cada mes), pero contradice las Instrucciones y abre el riesgo de cargar lo mismo dos veces (una vez suelto y otra en el resumen de tarjeta). Hoy no detecté duplicados.

## 4. Problemas de datos (categorización)

- "Comida laburo" (27/8, 22.000) está en **Mascota**. Debería ser Comida / Delivery.
- "Fulbo" (3/9) y "Compra Gym" (10/8) están en **Supermercado**. Deberían ser Gimnasio / Deporte.
- "Suplementos" (3 compras en cuotas) y "Omega 3" están en **Salud / Farmacia**, mientras "Creatina-D3" y "Proteína" están en **Suplementos / Nutrición**. Unificar en una sola.
- "Reintegro" (17/8, 100.000) está en **Otros ingresos** habiendo una categoría "Reintegros / Reembolsos".
- Comidas caseras (cena, ravioles, guiso de lentejas, almuerzo sábado) se reparten entre Supermercado, Ocio y Comida sin criterio fijo.
- "Adelanto de sueldo" se carga como **Ingreso** (100.000 en agosto, 50.000 en septiembre) y su devolución (3 × 72.496 = 217.488) como **gasto** en Cuotas. Contablemente infla ingresos y gastos; la alternativa neutra es no cargar el adelanto como ingreso y tampoco su devolución.
- "Ajuste Caja" (113.000) como ingreso es un cuadre de efectivo, no ingreso real.
- "Regalo fiama" aparece dos veces en Cuotas (junio 6 × 50.300 y septiembre 6 × 43.300). Si son dos regalos distintos está bien; si no, hay 259.800 de más.
- "Boxer calvin " tiene un espacio al final (afecta filtros y búsquedas).

## 5. Recomendaciones (en orden)

1. **Arreglar los 4 errores mecánicos**: fórmula en Tablero!C18, TOTAL del Tablero, fila de ejemplo, validaciones de Cuotas.
2. **Cargar presupuestos mensuales** para activar el semáforo. Valores de partida basados en agosto: Supermercado 400.000, Servicios 320.000, Ropa 120.000, Ocio 120.000, Salud 150.000, Nafta 120.000, Gym 100.000, Comida/Delivery 60.000, Suscripciones 40.000.
3. **Reclasificar** los movimientos listados en §4 y elegir una regla: "todo lo que se cocina en casa = Supermercado; todo lo que se come afuera o pedido = Comida / Delivery; salidas sociales = Ocio".
4. **Frenar nuevas cuotas hasta diciembre**: con 873.462 ya comprometidos para octubre y 553.301 para noviembre, cualquier compra financiada nueva se apila encima.
5. **Empezar a registrar Ahorro** aunque sea chico, para que el Tablero mida la tasa de ahorro. Con el ingreso de septiembre y sin nuevos gastos financiados, hay margen para apartar entre 200.000 y 300.000.
6. **Reducir efectivo o anotarlo el mismo día**: el 75 % de los gastos sueltos en efectivo es lo que obligó al "Ajuste Caja". Un "cierre de caja" semanal evita el ajuste mensual.
7. Cargar los nombres de los jugadores en Aston Birra!A16:A27 y agregar una columna de egresos del fondo si van a gastar de ahí.

---

## Reproducir el análisis

```bash
pip install openpyxl pandas
python3 scripts/analizar_gestor.py /ruta/a/Gestor_de_Gastos.xlsx
```

El script recalcula todo desde Movimientos y Cuotas (sin depender de los valores cacheados del Tablero) e imprime las tablas de este informe. El archivo `.xlsx` está excluido del repo por `.gitignore` porque contiene datos personales.
