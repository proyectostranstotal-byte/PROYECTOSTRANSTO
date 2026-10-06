# Búsqueda laboral periódica – Nicolás Di Fabio

Plantilla para repetir la búsqueda cada 3 o 4 días. Cada vez: (1) pegar este archivo completo en el chat con Claude o en Claude en Chrome, (2) recibir solo los avisos NUEVOS, (3) recibir la lista de postulación lista para usar, (4) agregar los nuevos al registro de abajo con la fecha.

Última búsqueda: 06/10/2026 (primera).

---

## 1. Consigna para pegar (copiar desde acá hasta el final del archivo)

Hacé una investigación exhaustiva de ofertas laborales vigentes en el cordón industrial Timbúes–Rosario (Santa Fe, Argentina). Incluye Timbúes, Puerto General San Martín, San Lorenzo, Fray Luis Beltrán, Capitán Bermúdez, Granadero Baigorria, Ricardone, Funes, Roldán, Pérez, Villa Gobernador Gálvez, Alvear, General Lagos, Arroyo Seco y Rosario.

**Perfil del candidato:** Bachiller en Gestión de las Organizaciones (2013). Técnico Superior en Logística incompleto (ISP N°22, Fray Luis Beltrán, 2019–2021). Licenciatura en Tecnologías Aplicadas al Arte Sonoro en curso (no afín). Hombre, 30 años. Licencia B1, movilidad propia, disponibilidad full time. Maneja SAP, Oracle y Excel avanzado (macros, cruces de datos, conciliación de reportes), plataformas satelitales y de tacógrafos (VDO), automatización básica con Python.

Experiencia:
- **Transtotal S.A. – Administrativo de Logística y Control de Flota (servicio para Air Liquide)** (sep. 2025 – actualidad; efectivo desde mar. 2026): planificación diaria de distribución asignando chofer, cisterna, semi y tractor (flota de ~20 cisternas y 25 choferes, tractores Mercedes-Benz Atego/Actros); control de jornada y fatiga de choferes con seguimiento satelital (inicio de turno y límite de 12 h); procesamiento de hojas de ruta (salidas/regresos) y descarga de tacógrafos VDO; liquidaciones de choferes y del cliente Air Liquide en Excel; conciliación de reportes entre IMSEG y Air Liquide; control de asignaciones tractor-semi y gestión del mantenimiento de unidades; automatización de tareas administrativas (scripts de extracción de datos, facturación).
- **John Deere – Operario de Logística y Coordinación** (ago. 2021 – ago. 2025): todos los puestos de recepción y abastecimiento a la línea de tractores; reemplazos en coordinación del área de recepción de materiales; mejora continua.
- **Nouryon Chemicals Argentina – Administrativo de Logística** (sep. 2020 – ago. 2021): logística de entregas nacionales e internacionales, contratación y evaluación de transportes, coordinación de choferes (asignación de cargas, ingreso/salida, pesaje, documentación), movimientos en SAP, interacción con Calidad y Ventas.
- **Louis Dreyfus Company – Operario de Balanza** (mar. – ago. 2020): pesaje de camiones de cereal, verificación de documentación y condiciones de carga.
- **Molinos Agro – Asistente Administrativo de Logística** (ago. 2019 – ene. 2020): carga de Cartas de Porte, verificación de documentación de transportistas.
- **Vicentin SAIC – Responsable de Logística de Obra** (ene. 2018 – abr. 2019): recepción y despacho de materiales de obra, inventario en Oracle.
- **Operador de autoelevador** en depósitos (Wander, Celulosa Argentina, Molino Cañuelas).

**Puestos afines:** administrativo/a o analista de logística, coordinador/a o planificador/a de tráfico o de transporte, controlador/a de flota, monitoreo satelital / telemetría, liquidación de fletes o de choferes, administrativo de transporte, recepción y despacho, balancero/a, analista de stock o inventario, encargado/supervisor de depósito o de playa de camiones, abastecimiento a línea, comprador/a junior de transporte, facturación logística, control de gestión operativa. Rubros: transporte de cargas y cisternas, gases industriales, terminales portuarias y agroexportadoras, aceiteras, química, maquinaria agrícola/metalmecánica, distribución y operadores logísticos.

**Palabras clave:** administrativo de logística, analista de logística, coordinador de tráfico, coordinador de flota, control de flota, monitoreo satelital, planificador de transporte, liquidación de fletes, balancero, recepción y despacho, analista de stock, supervisor de depósito.

**Fuentes (revisar todas):**
- Portales generales: Computrabajo, Bumeran, ZonaJobs, LinkedIn Empleos, Indeed, Jooble, Talent.com, Glassdoor, OpcionEmpleo.
- Consultoras: Randstad, Adecco, ManpowerGroup, Grupo Gestión, Grupo Servicemen, Consultores de Empresas (jobiis.com), Ceta Capital Humano (cetacapitalhumano.com), Concepto Empresario, Ezequiel Pereyra, Grupo Consultor, Clip Soluciones, NEO-BIZ, Estudio Aún, Estudio Selector, Leiva & Asociados, Empleos&Recursos, RRHH Buro, GGC.
- Portales de empresas: careers.cargill.com, jobs.bunge.com, Viterra, Louis Dreyfus, COFCO, Renova, ACA, AGD, Molinos Agro, Nouryon, Air Liquide, Linde/Praxair, John Deere, CLAAS, Acindar; transportistas y operadores logísticos de la zona (Andreani, OCA, Transportes Don Pedro, Lusitania, etc.).
- Locales: sitioempleos.com.ar, Plataforma de Intermediación Laboral de Rosario (empleo.produccionrosario.gob.ar), Portal de Empleo de Santa Fe.

Notas de acceso: Bumeran y ZonaJobs comparten la misma base de avisos (alcanza con revisar uno; los listados HTML vienen vacíos, funciona su API interna /api/avisos/searchV2). Computrabajo no se lee con WebFetch pero sí con curl; URLs válidas: `trabajo-de-<palabra>-en-santa-fe-en-rosario` y `empleos-en-santa-fe-en-<localidad>`. Sitio Empleos: el detalle sale de `busquedas_detalle_ajax.php?id=<id>`. Indeed, Glassdoor y OpcionEmpleo bloquean con captcha; el Portal de Empleo de Santa Fe requiere Clave Fiscal.

Notas de acceso (06/10): la API de Bumeran devuelve 0 resultados desde servidores fuera de Argentina; alternativa que funcionó: anteponer `https://r.jina.ai/` a la URL del listado (ej. `https://r.jina.ai/https://www.bumeran.com.ar/en-santa-fe/empleos-area-abastecimiento-y-logistica.html?recientes=true`, paginar con `&page=2`). Computrabajo acepta `?pubdate=15` y `?p=2`; para toda la provincia usar `trabajo-de-<palabra>-en-santa-fe`. Jooble devuelve 403 a curl pero se lee con WebFetch; sus links `away/` son redirecciones sin contenido. Sitio Empleos: listado por `busquedas_ajax.php?page=N&cat=<id>&tiempo=&q=&ciudad=&recom=0` (cat 157 = Logística/Abastecimiento, 149 = Administración, 164 = Choferes). Municipalidad de Rosario: probar IDs consecutivos en `empleos/x_<id>.html` (aviso cerrado muestra "Búsqueda finalizada"; el 06/10 el último ID con contenido era 1159). Un aviso de Computrabajo dado de baja redirige al listado general. Rosental publica en rosental.hiringroom.com; Minerva Foods en minervafoods-argentina.gupy.io; Suple en huntcore.senderoshr.com.ar.

**Filtros:**
1. Solo avisos vigentes. Priorizar los publicados en los últimos 10 días, pero incluir los más antiguos si siguen abiertos, indicando la fecha.
2. Excluir los que exijan título universitario completo o estudiante de una carrera específica (ingeniería, administración, comercio exterior, contador). Si lo piden solo como deseable, incluir y aclararlo.
3. Excluir los que pidan un rango de edad que deje afuera a alguien de 30 años.
4. Excluir puestos con remuneración o nivel claramente inferiores a su situación actual (ayudante de depósito, repositor, carga y descarga manual), salvo que sean en empresas objetivo (agroexportadoras, aceiteras, química).
5. **Excluir todo aviso que ya figure en el registro de la sección 3 de este archivo** (mismo título y misma empresa o consultora, aunque el portal lo muestre renovado con fecha nueva). Si un aviso del registro cambió de manera relevante, incluirlo marcado como "actualizado".

**Formato de respuesta:** devolver TODOS los avisos nuevos, ordenados por afinidad (alta / media / baja) y dentro de cada grupo por fecha, más recientes primero. Para cada uno: título, empresa o consultora, localidad, fuente, fecha de publicación y antigüedad, requisitos de formación y experiencia (aclarar si no pide universitario), por qué encaja con el perfil, y link directo de postulación (o mail/WhatsApp si es la vía de contacto). Al final: descartados con motivo en una línea, avisos del registro que ya no están publicados (para darlos de baja), y fuentes que no se pudieron consultar.

**Lista de postulación (entregar siempre, además del informe):** texto corto para usar desde el celular. Estructura: "🔵 PRIORIDAD ALTA (postular ya)" con los avisos de afinidad alta numerados, cada uno con título, empresa, localidad, fecha, una línea con qué experiencia destacar en la postulación y el link en una línea aparte (URL pelada); "🟡 PRIORIDAD MEDIA" con título, empresa, localidad, fecha y link; "🟢 SIGUEN ABIERTAS" con los avisos del registro de afinidad alta que siguen vigentes y con estado distinto de "postulado". No incluir los de afinidad baja ni los descartados. Guardar como `postulaciones-nico-<fecha>.md`.

---

## 2. Qué hacer después de cada búsqueda

- Postularse a los de prioridad alta (archivo `postulaciones-nico-<fecha>.md`).
- Copiar los avisos nuevos a la tabla de la sección 3 con la fecha de la búsqueda.
- Marcar en la columna Estado los que ya no aparecen publicados ("cerrado") o a los que ya se postuló ("postulado").
- Actualizar la línea "Última búsqueda" al principio del archivo.

---

## 3. Registro de avisos ya vistos (excluir en la próxima búsqueda)

Formato: fecha en que se encontró · título · empresa/consultora · localidad · fuente · link · estado.

### Búsqueda del 06/10/2026

Informe completo: `informe-busqueda-nico-2026-10-06.md`. Lista de postulación: `postulaciones-nico-2026-10-06.md`.

| Encontrado | Título | Empresa / consultora | Localidad | Fuente | Link | Estado |
|---|---|---|---|---|---|---|
| 06/10 | Supervisor Administrativo de Logística (supervisión de choferes, seguimiento satelital, flota) | ManpowerGroup | Rosario | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-supervisor-administrativo-de-logistica-en-rosario-6E175D31E912956561373E686DCF3405 | abierto (05/10, alta) |
| 06/10 | Coordinador de Operaciones de Logística – CD Rosario (secundario, 2 años; 6-14 + sáb) | Suple Servicio Empresario | Rosario | Computrabajo / Bumeran / Jooble | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-coordinador-de-operaciones-de-logistica-rosario-en-rosario-379368E0DA9C6B4061373E686DCF3405 (postulación: https://huntcore.senderoshr.com.ar/jobs/coordinador-de-operaciones-de-logistica-rosario-d20e1864/apply) | abierto (29/09, renovado 06/10, alta) |
| 06/10 | Analista de Operación Logística (última milla, monitoreo de rutas y flota; 20-40 años) | clicOH | Rosario | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-analista-de-operacion-logistica-en-rosario-00718C61368A29D861373E686DCF3405 | abierto (23/09, alta) |
| 06/10 | Analista de Tráfico (multinacional consumo masivo; formación solo valorada) | Texia RRHH | Rosario | Bumeran | https://www.bumeran.com.ar/empleos/analista-de-trafico-texia-rrhh-1118418779.html | abierto (27/08, alta) |
| 06/10 | Analista de Logística – Sucursal Rosario (secundario, KPIs, Excel avanzado, Power BI) | Establecimiento Las Marías | Rosario | Bumeran | https://www.bumeran.com.ar/empleos/analista-de-logistica-establecimiento-las-marias-1118418276.html | abierto (27/08, actualizado 05/10, alta) |
| 06/10 | Responsable Logístico/a (alimentos fríos; flota, hojas de ruta, fletes; convenio Camioneros) | Randstad (incorporación directa) | Alvear | Randstad | https://www.randstad.com.ar/trabajos/responsable-logistico_alvear_47408853/ | abierto (07/09; VENCE 07/10, alta) |
| 06/10 | Analista Sr. de Planificación Logística (2 vacantes; rutas, costos, satelital; sin título) | Texia RRHH | Rosario | Bumeran | https://www.bumeran.com.ar/empleos/analista-de-planificacion-logistica-texia-rrhh-1118365104.html | abierto (13/07, alta) |
| 06/10 | Administrativo de Logística (recorridos de vehículos, seguimiento de viajes, remitos; 22-35) | FLEXIO SA | Pérez | Computrabajo / Jooble | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-administrativo-logistica-en-perez-11036C62B104FA8461373E686DCF3405 | abierto (más de 30 días, alta) |
| 06/10 | Operario de balanza (terciario declarado, 5 años, hasta 45; part time turnos) | Importante empresa del cordón industrial | San Lorenzo | Computrabajo / Jooble | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-operario-de-balanza-en-san-lorenzo-E481B780A8F468EA61373E686DCF3405 | abierto (04/10, media) |
| 06/10 | Supervisor Operativo turno mañana (depósito; 3 años supervisión excluyente) | Bro Reclutamiento Humano | Rosario | LinkedIn | https://ar.linkedin.com/jobs/view/supervisor-operativo-turno-ma%C3%B1ana-at-bro%E2%80%94-reclutamiento-humano-4462693850 | abierto (~06/09, media) |
| 06/10 | Jefe Logístico (terciario, 2 años, desde 30 años) | Importante empresa del sector | Rosario | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-jefe-logistico-en-rosario-2E8F3DD151743B6761373E686DCF3405 | abierto (28/09, media) |
| 06/10 | Jefe de Despacho (alimenticia; stock, cargas, cámaras de frío) | Confidencial | Rosario | ZonaJobs / Bumeran | https://www.zonajobs.com.ar/empleos/jefe-de-despacho-2190735.html | abierto (24/09, media) |
| 06/10 | Auxiliar de Logística (seguimiento de pedidos, coordinación de choferes, remitos; junior) | Adecco | Rosario | Bumeran | https://www.bumeran.com.ar/empleos/auxiliar-de-logistica-adecco-recursos-humanos-argentina-sa-1118445754.html | abierto (17/09, actualizado 30/09, media) |
| 06/10 | Asistente administrativo de coordinación logística (transporte internacional; 2 años; junior) | Startia Consultores / Transportia | Rosario | Bumeran | https://www.bumeran.com.ar/empleos/asistente-administrativo-de-coordinacion-logistica-startia-consultores-1118388599.html | abierto (03/08, media) |
| 06/10 | Administrativo – Rubro Agro (cartas de porte, stock, conciliaciones; 1 año agro) | Catalano Dupuy | Rosario (Fisherton) | Bumeran | https://www.bumeran.com.ar/empleos/administrativo-rubro-agro-catalano-dupuy-1118393474.html | abierto (06/08, media) |
| 06/10 | Analista de Aplicaciones y Mercaderías (descargas, contratos; 3 años) | SV Matesur | Rosario | LinkedIn | https://ar.linkedin.com/jobs/view/analista-de-aplicaciones-y-mercader%C3%ADas-at-sv-matesur-4462229243 | abierto (~07/09, media) |
| 06/10 | Responsable de Operaciones (depósito instrumental ISO; secundario; 3-5 años supervisión; 12-21) | Adecco | Rosario | Bumeran | https://www.bumeran.com.ar/empleos/responsable-de-operaciones-rosario-adecco-recursos-humanos-argentina-sa-1118386431.html | abierto (31/07, media) |
| 06/10 | Administrativo/a de Ventas y Logística (corralón; rutas de envío, stock; comercio) | Del Castillo & Rossi Advisors | Rosario (centro) | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-administrativoa-de-ventas-y-logisitca-en-rosario-900CBE102D40449161373E686DCF3405 | abierto (01/10, media) |
| 06/10 | Analista de Almacenes SR (estudiante avanzado o profesional de Ing. Industrial / Tec. Logística / Adm.; SAP) | Minerva Foods (Swift) | Villa Gobernador Gálvez | Gupy / Jooble | https://minervafoods-argentina.gupy.io/jobs/12373446?jobBoardSource=gupy_public_page | abierto (1-3 semanas, media) |
| 06/10 | Operario/a de Logística (autoelevador excluyente; inventarios, envíos; química) | Sika | Rosario | LinkedIn | https://ar.linkedin.com/jobs/view/operario-a-de-log%C3%ADstica-at-sika-4456503434 | abierto (~08/09, media) |
| 06/10 | Jefe de Logística – Ciudad Industria (terciario, 4 años jefatura, 30-45, B1) | Pronto Equipamientos S.R.L. | Funes | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-jefe-de-logistica-en-funes-EA31A0C495F78D3961373E686DCF3405 | abierto (30/09, media) |
| 06/10 | Comprador/a (formación universitaria como perfil deseado; SAP, inglés) | COFCO International | Rosario (Puerto Norte) | LinkedIn | https://ar.linkedin.com/jobs/view/comprador-a-at-cofco-international-4476174531 | abierto (06/10, media) |
| 06/10 | Operador Comercial y de procesos logísticos de cereal (5 años, 30-40, comercial) | We Lean | San Lorenzo | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-operador-comercial-y-de-procesos-logisticos-de-cereal-en-san-lorenzo-02DC9DAB236B70DA61373E686DCF3405 | abierto (28/09, baja) |
| 06/10 | Administrativo/a de Operaciones (distribuidora; descripción genérica) | sin nombre | Rosario (centro) | Sitio Empleos | https://www.sitioempleos.com.ar/index.php?pagina=busqueda&id=7965 | abierto (05/10, baja) |
| 06/10 | Responsable de Compras y Logística (constructora) | Ezequiel Pereyra Búsqueda y Selección | Rosario | Jooble / Computrabajo | https://ar.jooble.org/desc/-8557178444750129724 | abierto (hace 2 meses, baja) |
| 06/10 | Administrativo/a General Ssr. (contable; graduado deseable; movilidad propia) | Neo-Biz | Rosario | Bumeran | https://www.bumeran.com.ar/empleos/administrativo-a-general-ssr-neo-biz-1118379993.html | abierto (actualizado 25/09, baja) |
| 06/10 | Administrativo/a de Finanzas y Tesorería (6 h) | Randstad | Rosario | Randstad | https://www.randstad.com.ar/trabajos/administrativao_rosario_47447344/ | abierto (15/09, vence 14/10, baja) |
| 06/10 | Administrativa y Atención al Cliente (edad 30-35; 8-19) | Consultores de Empresas | Rosario (sur) | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-administrativa-y-atencion-al-cliente-en-rosario-2F7599D01820D32661373E686DCF3405 | abierto (29/09, baja) |

### Descartados (no volver a listar salvo que cambien los requisitos)

| Título | Empresa / consultora | Motivo |
|---|---|---|
| Jefe de Logística – CD Rosario | Suple Servicio Empresario | graduados en logística o ingeniería, 3 años en el rol |
| Analista Planificador de Logística y Puerto RENOVA (Timbúes) | Bunge | Ingeniero Industrial excluyente |
| Coordinador de Logística y Operaciones Portuarias | Taxia Recruitment | ingeniería o licenciatura, 6 años de jefatura |
| Jefe de Cadena de Suministros (Pérez) | NOS Soluciones en RRHH | terciario/universitario graduado, 4 años |
| Administrativo/a de Abastecimiento en Obra | Milicic S.A. | Ing. Industrial o Lic. Administración, 3 años |
| Analista de Operaciones (Pluscargo) | B&B Consultores | estudiante o graduado de Comercio Exterior |
| Analista de Planificación y Abastecimiento (y Junior) | Rosental Inversiones | estudiante próximo a graduarse, inglés avanzado excluyente, part time |
| Jr / Ssr Commodity Management Analyst | Louis Dreyfus Company | universitario o en curso, inglés avanzado |
| Comprador/a | Maincal S.A. | universitario, 4 años, inglés |
| Comprador Sr | Briket S.A. | compras no productivas, senior |
| Administrativo/a (Rosario) | Adecco | Tec./Lic. Administración en curso o graduado |
| Coordinador/a de Administración (Superebe, Capitán Bermúdez) | Neo-Biz | graduado de Ciencias Económicas |
| Administrativo/a Jr. (RENS) | Neo-Biz | universitario, cobranzas, 20-35 |
| Administrativa – Abastecimiento | David Rosental e Hijos | educación mínima universitario |
| Administrativos/as rubro Agro (eventual) | Randstad | estudiantes avanzados Cs. Económicas / Comex excluyente |
| Administrativo/a Contable y Operaciones (Roldán) | Grupo Consultor | universitario contable excluyente, inglés |
| Administrativo/a Abastecimiento (Sitio Empleos 7936/7937/7938) | sin nombre | universitario avanzado o graduado excluyente |
| Analista Centro de Operaciones (San Lorenzo) | Securion | terciario/universitario culminado excluyente, turnos 12 h |
| Profesional de logística puerto / Operador logístico marítimo / Operador marítimo (también Municipalidad 1132) | RH Talentum | graduado o próximo, 3 años portuario, inglés |
| Coordinador de Operaciones (San Lorenzo, puertos) | Leiva & Asociados | universitaria, inglés; más de 30 días |
| Administrativo/a de Taller (empresa de logística) | Tuttolomondo Consultores | pide técnico mecánico |
| Operarios de depósito / logístico / carga y descarga / playa | Grupo Gestión, Liqui, Larraya, Comercial CAB, Coca-Cola Andina, Concepto Empresario, Consultores (Jobiis 151590), Confidencial | nivel inferior (filtro 4) |
| Operario de Depósito (Pueblo Esther) | Importante empresa | edad 18-25 |
| Transportista de cereales (San Lorenzo) y choferes varios | Randstad, ADN, Grupo Gestión, Sitio Empleos | puestos de chofer |
| Balancero/a | Randstad | ciudad de Santa Fe, fuera de zona |
| Analista de Logística (613) y Operario de Depósito (667) | Ceta Capital Humano | Cañada de Gómez |
| Administrativo/a | Sinergia | Susana (Rafaela) |
| Analista Sr. Logística y Distribución, Analista Sr. Compras (Venado Tuerto); Analista Sr. Compras (Armstrong); Líder de Logística y Responsable de Tráfico (Adecoagro); Asistente de Logística COFCO (La Pampa); Analista Logístico Adecco (GBA); Expedición Bringeri (San Nicolás) | varias | fuera de zona |
| Analista Senior de Compras Estratégicas; Trade Administrator | Bunge; Jobs2Web | ubicación genérica, perfiles senior/universitarios, no verificables |
| Pasantía en Control y Análisis de Stock (Funes) | L&L Futura | pasantía 20 h |
| Gerente de Negocio Logístico; Gerente de Operaciones; Responsable de Operaciones (Serrat) | Grassi; Startia; Serrat SRL | nivel gerencial |
| Ingeniero/a de Despacho | Litoral Gas | ingeniería |
| Analista de Mantenimiento Mercado Envíos; mecánicos de flota | Mercado Libre; Neo-Biz, Materiales Colombia, Serodino | mantenimiento / mecánica |

---

## 4. Próximas búsquedas

| Fecha | Nuevos encontrados | Notas |
|---|---|---|
| 06/10/2026 | 28 (8 alta, 14 media, 6 baja) | Primera búsqueda. Cubiertos Computrabajo, Bumeran/ZonaJobs (vía r.jina.ai), Jooble, LinkedIn, Randstad, Ceta, Jobiis, Sitio Empleos, Municipalidad de Rosario, Cargill, Bunge, COFCO, LDC, Minerva, Rosental, Sika. Pendientes con Claude en Chrome: Indeed, Glassdoor, Talent; portales Air Liquide, Linde, Viterra, ACA, Andreani, OCA, Molinos Agro, AGD, John Deere sin listado legible |
| 09/10/2026 o 10/10/2026 | | |
