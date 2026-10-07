# Búsqueda laboral periódica – Fiama Anfuso

Plantilla para repetir la búsqueda cada 3 o 4 días. Cada vez: (1) pegar este archivo completo en el chat con Claude o en Claude en Chrome, (2) recibir solo los avisos NUEVOS, (3) recibir el mensaje listo para reenviarle a Fiama con los links de postulación, (4) agregar los nuevos al registro de abajo con la fecha.

Última búsqueda: 07/10/2026 (anteriores: 06/10/2026, 05/10/2026, 02/10/2026, 30/09/2026).

---

## 1. Consigna para pegar (copiar desde acá hasta el final del archivo)

Hacé una investigación exhaustiva de ofertas laborales vigentes en el cordón industrial Timbúes–Rosario (Santa Fe, Argentina). Incluye Timbúes, Puerto General San Martín, San Lorenzo, Fray Luis Beltrán, Capitán Bermúdez, Granadero Baigorria, Ricardone, Funes, Roldán, Pérez, Villa Gobernador Gálvez, Alvear, General Lagos, Arroyo Seco y Rosario.

**Perfil de la candidata:** Técnica Mecánica (EETP N°466, 2019), First Certificate in English. Cuatro años en Inspección de Calidad de Recepción en John Deere Argentina (inspección de piezas según planos, gestión de no conformes, análisis de causa raíz, acciones correctivas), dos años de montaje en línea de tractores, experiencia en ARAG (cableados) y pasantía en Arroyito Maquinarias. Maneja SAP, torno y fresadora CNC, soldadura básica. Licencia B1, movilidad propia. Sin título universitario. Mujer, 25 años.

**Puestos afines:** inspector/a o técnico/a de calidad, control de calidad, QA/QC, calidad de proveedores o de recepción, metrología, auxiliar de gestión de calidad, técnico/a mecánico/a, operario/a calificado/a, técnico de producción o procesos, operador o programador CNC, mantenimiento mecánico nivel técnico. Rubros: metalmecánica, maquinaria agrícola, automotriz, agroindustria, terminales portuarias, aceiteras, química, alimentos.

**Palabras clave:** inspector de calidad, control de calidad, técnico de calidad, técnico mecánico, operador CNC, programador CNC, auxiliar de calidad, metrología.

**Fuentes (revisar todas):**
- Portales generales: Computrabajo, Bumeran, ZonaJobs, LinkedIn Empleos, Indeed, Jooble, Talent.com, Glassdoor, Empleos Clarín, OpcionEmpleo.
- Consultoras: Randstad, Adecco, ManpowerGroup, Grupo Gestión, Grupo Servicemen, Consultores de Empresas (jobiis.com), Ceta Capital Humano (cetacapitalhumano.com), Concepto Empresario, Ezequiel Pereyra, Grupo Consultor, Clip Soluciones, NEO-BIZ, Estudio Aún, Estudio Selector, Leiva & Asociados, Empleos&Recursos, RRHH Buro, GGC.
- Portales de empresas: careers.cargill.com, jobs.bunge.com, Viterra, Louis Dreyfus, COFCO, Renova, ACA, SKF, Sika, Minerva, Gemplast, Paladini, John Deere, CLAAS, Metalfor, Acindar.
- Locales: sitioempleos.com.ar, Plataforma de Intermediación Laboral de Rosario (empleo.produccionrosario.gob.ar), Portal de Empleo de Santa Fe.

Notas de acceso (05/10): Bumeran y ZonaJobs comparten la misma base de avisos (alcanza con revisar uno; los listados HTML vienen vacíos, funciona su API interna /api/avisos/searchV2). Computrabajo no se lee con WebFetch pero sí con curl; URLs válidas: `trabajo-de-<palabra>-en-santa-fe-en-rosario` y `empleos-en-santa-fe-en-<localidad>`. Sitio Empleos: el detalle sale de `busquedas_detalle_ajax.php?id=<id>`. Indeed, Glassdoor y OpcionEmpleo bloquean con captcha; Empleos Clarín está discontinuado; el Portal de Empleo de Santa Fe requiere Clave Fiscal.

Notas de acceso (06/10): la API de Bumeran devuelve 0 resultados desde servidores fuera de Argentina; alternativa que funcionó: anteponer `https://r.jina.ai/` a la URL del listado (ej. `https://r.jina.ai/https://www.bumeran.com.ar/en-santa-fe/empleos-busqueda-calidad.html?recientes=true`), que devuelve la página renderizada con fechas y links. Computrabajo acepta `?pubdate=7` (últimos 7 días) y `?p=2` para paginar. Jooble devuelve 403 a curl pero se lee con WebFetch. Sitio Empleos: el listado completo ordenado por fecha sale de `busquedas_ajax.php?page=N&cat=0&tiempo=&q=&ciudad=&recom=0`. Municipalidad de Rosario: el listado no se puede leer; probar IDs consecutivos en `empleos/x_<id>.html` (el slug es indiferente; un aviso cerrado muestra "Búsqueda finalizada" y uno abierto "Quiero postularme"); el 07/10 el último ID con contenido seguía siendo 1159 (el 1158 apareció ese día). Un aviso de Computrabajo dado de baja redirige al listado general (sirve para detectar cerrados).

**Filtros:**
1. Solo avisos vigentes. Priorizar los publicados en los últimos 10 días, pero incluir los más antiguos si siguen abiertos, indicando la fecha.
2. Excluir los que exijan título universitario (ingeniería, licenciatura, universitario completo o en curso). Si lo piden solo como deseable, incluir y aclararlo.
3. Excluir los que pidan sexo masculino o un rango de edad que deje afuera a una mujer de 25 años.
4. **Excluir todo aviso que ya figure en el registro de la sección 3 de este archivo** (mismo título y misma empresa o consultora, aunque el portal lo muestre renovado con fecha nueva). Si un aviso del registro cambió de manera relevante (otra localidad, otros requisitos), incluirlo marcado como "actualizado".

**Formato de respuesta:** devolver TODOS los avisos nuevos, ordenados por afinidad (alta / media / baja) y dentro de cada grupo por fecha, más recientes primero. Para cada uno: título, empresa o consultora, localidad, fuente, fecha de publicación y antigüedad, requisitos de formación y experiencia (aclarar si no pide universitario), por qué encaja con el perfil, y link directo de postulación (o mail/WhatsApp si es la vía de contacto). Al final: descartados con motivo en una línea, avisos del registro que ya no están publicados (para darlos de baja), y fuentes que no se pudieron consultar.

**Mensaje para Fiama (entregar siempre, además del informe):** armar un segundo texto listo para copiar y pegar en WhatsApp, dirigido a Fiama, en tono cercano y en español rioplatense. Estructura: saludo breve; "🔵 PRIORIDAD ALTA (postular ya)" con los avisos de afinidad alta numerados, cada uno con título, empresa, localidad, fecha, dos líneas de requisitos en lenguaje simple y el link directo en una línea aparte (sin formato markdown, URL pelada para que WhatsApp la haga clickeable); "🟡 PRIORIDAD MEDIA (postular esta semana)" con los de afinidad media, solo título, empresa, localidad, fecha y link; "🟢 SIGUEN ABIERTAS DE LA SEMANA PASADA" con los avisos del registro de afinidad alta que siguen vigentes y a los que todavía no se postuló (estado distinto de "postulada"); cierre con consejos cortos y pedido de que avise a cuáles se postuló. No incluir los de afinidad baja ni los descartados. Si un aviso no tiene link, poner el mail o WhatsApp de contacto. Guardar el mensaje como `mensaje-fiama-<fecha>.md`.

---

## 2. Qué hacer después de cada búsqueda

- Reenviar a Fiama el mensaje generado (archivo `mensaje-fiama-<fecha>.md`).
- Copiar los avisos nuevos a la tabla de la sección 3 con la fecha de la búsqueda.
- Marcar en la columna Estado los que ya no aparecen publicados ("cerrado") o a los que Fiama ya se postuló ("postulada"), así no vuelven a salir en el bloque "siguen abiertas" del mensaje.
- Actualizar la línea "Última búsqueda" al principio del archivo.

---

## 3. Registro de avisos ya vistos (excluir en la próxima búsqueda)

Formato: fecha en que se encontró · título · empresa/consultora · localidad · fuente · estado.

### Búsqueda del 30/09/2026

| Encontrado | Título | Empresa / consultora | Localidad | Fuente | Link | Estado |
|---|---|---|---|---|---|---|
| 30/09 | Técnico/a Mecánico/a (planta aceitera) | Cargill | Villa Gobernador Gálvez | careers.cargill.com | https://careers.cargill.com/es/trabajo/galvez/tecnico-a-mecanico-a-villa-gobernador-galvez/31241/100137415744 | postulada 06/10 (antes: abierto) |
| 30/09 | Inspector de Confiabilidad (TFA) | Bunge | Puerto General San Martín | LinkedIn / jobs.bunge.com | https://jobs.bunge.com/job/Puerto-San-Mart%C3%ADn-Inspector-de-Confiabilidad_TFA/1438087233/ | postulada 06/10 (antes: abierto (17/09; técnico mecánico excluyente, ingeniería no obligatoria)) |
| 30/09 | Coordinador de calidad (metalmecánica) | Consultores de Empresas | Rosario | Jobiis | https://www.jobiis.com/jobs-list/151256?country=ARG | descartado 05/10 (ficha Computrabajo: educación mínima universitario) |
| 30/09 | Operario de Calidad (metalúrgica zona suroeste) | Grupo Servicemen | Rosario | Jooble / Computrabajo | https://ar.jooble.org/desc/3659742492026451399 | postulada 06/10 (antes: abierto) |
| 30/09 | Operario de calidad (metalmecánica, inspección dimensional) | Grupo Servicemen | Rosario | Jooble / Computrabajo | https://ar.jooble.org/desc/-4633967293944523733 | postulada 06/10 (antes: abierto) |
| 30/09 | Operario de calidad (turnos rotativos) | Grupo Servicemen | Rosario | Computrabajo | buscar en Computrabajo | baja 05/10 (duplicado de los dos anteriores) |
| 30/09 | Operario para control de calidad (piezas CNC, planos) | Concepto Empresario S.A. | Rosario | Jooble / Computrabajo | https://ar.jooble.org/desc/-589440106169930197 | postulada 06/10 (antes: abierto) |
| 30/09 | Operario de Calidad / Inspector (chapería) | Grupo Gestión | Rosario | Jooble / Computrabajo | https://ar.jooble.org/desc/-839746385492766789 | solo Jooble (hace 2 meses); ya no está en Computrabajo |
| 30/09 | Inspector/a | Grupo Gestión | Rosario | Computrabajo | buscar en Computrabajo | cerrado 05/10 |
| 30/09 | Inspector/a | ManpowerGroup | Rosario | Computrabajo | buscar en Computrabajo | cerrado 05/10 |
| 30/09 | Auxiliar de Gestión de Calidad | Ezequiel Pereyra – Búsqueda y Selección | Rosario | Jooble / Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-auxiliar-de-gestion-de-calidad-en-rosario-03DD1F9C923CFD0B61373E686DCF3405 | cerrado 06/10 (el link redirige al listado; ya no aparece en la búsqueda) |
| 30/09 | Control de calidad en taller metalúrgico (turno mañana) | LOZAMETAL S.R.L. | Rosario | Jooble / Computrabajo | https://ar.jooble.org/desc/-5998574228895155532 | postulada 06/10 (antes: abierto (renovado 01/10, edad desde 25)) |
| 30/09 | Técnico/a en mantenimiento de máquinas (fábrica de botellas) | Randstad | Rosario | Randstad | https://www.randstad.com.ar/trabajos/tecnicoa-en-mantenimiento-de-maquinas_rosario_47496498/ | abierto |
| 30/09 | Técnico/a (título técnico excluyente, turnos rotativos) | Randstad | Rosario | Randstad | https://www.randstad.com.ar/trabajos/tecnicoa_rosario_46026549/ | abierto (búsqueda permanente) |
| 30/09 | Técnicos/as Rosario (turnos rotativos, sin experiencia) | Randstad | Rosario | Randstad | https://www.randstad.com.ar/trabajos/tecnicosas-rosaro-turnos-rotativos_rosario_46243123/ | abierto (búsqueda permanente) |
| 30/09 | Operario/a de producción (Parque Industrial Pérez) | Randstad | Pérez | Randstad | https://www.randstad.com.ar/trabajos/operarioa-de-produccion_perez_47436166/ | abierto |
| 30/09 | Operarios de planta / caladores (cerealera) | Randstad | San Lorenzo | Randstad | https://www.randstad.com.ar/trabajos/operarios-de-planta-industria-cerealera-aceitera_san-lorenzo_46274394/ | abierto |
| 30/09 | Técnico de Mantenimiento Predictivo | SKF | Rosario | Indeed | https://skf.hiringroom.com/jobs/get_vacancy/6a29636fedf135242156e092 | postulada 06/10 (antes: abierto (sin experiencia requerida, movilidad propia, guardias)) |
| 30/09 | Mantenimiento – técnico electromecánico | Flexocolor | Rosario | Indeed | https://ar.indeed.com/q-t%C3%A9cnico-mecanico-l-rosario,-santa-fe-empleos.html | sin verificar (Indeed bloqueado) |
| 30/09 | Operario de Inyección (controles de calidad) | Gemplast | Pérez | Indeed | https://ar.linkedin.com/jobs/view/operario-a-de-inyecci%C3%B3n-de-pl%C3%A1stico-at-gemplast-argentina-4472381882 | postulada 06/10 (antes: abierto (renovado ~01/10)) |
| 30/09 | Técnico o Ingeniero Mecánico (empresa agrícola zona norte) | Ceta Capital Humano | Rosario | Ceta | https://www.cetacapitalhumano.com/ceta/postulantes/oferta2.php?id=609 | postulada 06/10 (antes: abierto (26/06)) |
| 30/09 | Técnico Mecánico (mecanizado de piezas) | Ceta Capital Humano | Rosario | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-tecnico-mecanico-con-experiencia-en-mecanizado-de-piezas-en-rosario-ECC9317B2C0B1BD461373E686DCF3405 | abierto (renovado 01/10; AutoCAD/SolidWorks avanzado excluyente, 2 años) |
| 30/09 | Programador de CNC | Ceta Capital Humano | Santa Fe | Ceta | https://www.cetacapitalhumano.com/ceta/postulantes/oferta2.php?id=608 | abierto (26/06) |
| 30/09 | Técnico de Mantenimiento | Ceta Capital Humano | Rosario | Ceta | https://www.cetacapitalhumano.com/ceta/postulantes/oferta2.php?id=518 | abierto (17/04) |
| 30/09 | Operario de ensamble | Ceta Capital Humano | Rosario | Ceta | https://www.cetacapitalhumano.com/ceta/postulantes/oferta2.php?id=550 | abierto (14/05) |
| 30/09 | Operario De Producción | Ceta Capital Humano | Rosario | Ceta | https://www.cetacapitalhumano.com/ceta/postulantes/oferta2.php?id=525 | abierto (23/04) |
| 30/09 | Operarios/as de producción con secundario técnico (CNC) | Consultores de Empresas | Rosario | Jooble / Computrabajo | https://ar.jooble.org/desc/-8187052557782033660 | abierto |
| 30/09 | Técnico mecánico / electromecánico / químico – tareas generales | Consultores de Empresas / Adecco | Rosario | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-tecnico-mecanico-electromecanico-quimico-tareas-generales-en-rosario-0ba44e8d1f2acaf761373e686dcf3405 | postulada 06/10 (antes: reabierto 05/10 (armado y ensamble, instrumentos de medición, balancín; secundario técnico; afinidad media)) |
| 30/09 | Supervisor de producción | Consultores de Empresas | Rosario | Jobiis | https://www.jobiis.com/jobs-list/150562?country=ARG | abierto |
| 30/09 | Soldador | Consultores de Empresas | Villa Gobernador Gálvez | Jobiis | https://www.jobiis.com/jobs-list/151275?country=ARG | abierto |
| 30/09 | Soldador (estructuras metálicas) | Importante Empresa | Rosario | Sitio Empleos Rosario | https://www.sitioempleos.com.ar/index.php?pagina=busqueda&id=7998 | abierto |
| 30/09 | Programador CNC (turnos rotativos) | Empresa sin nombre | Rosario | Jooble / Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-programador-cnc-turnos-rotativos-en-rosario-234D0B4A468DAE2161373E686DCF3405 | abierto (renovado 05/10; pide 4 años en CNC) |
| 30/09 | Punzonador CNC | EPTA Argentina | Rosario | Jooble / Computrabajo | https://ar.jooble.org/desc/-269593536706441975 | abierto |
| 30/09 | Tornero fresador | GGC Soluciones Integrales | Rosario | Jooble | https://ar.jooble.org/desc/-4076785833937495551 | abierto |
| 30/09 | Operario de alesadora convencional y CNC | RRHH Buro | Villa Gobernador Gálvez | Jooble | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-operario-de-alesadora-villa-gobernador-galvez-full-time-en-rosario-E0D62114D8F4A5A261373E686DCF3405 | abierto (renovado 03/10) |
| 30/09 | Oficial de mecanizado (empresa agrícola zona norte) | Ceta Capital Humano | Rosario | Jooble | https://ar.jooble.org/desc/3291991438513699472 | abierto |
| 30/09 | Técnico de Mantenimiento | Clip Soluciones en RR.HH. | San Lorenzo | Computrabajo | buscar en Computrabajo | cerrado 05/10 |
| 30/09 | Técnico Mecánico (rental de maquinaria: autoelevadores) | Empresa sin nombre | Pérez | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-tecnico-mecanico-en-perez-B68BC19276B88C6161373E686DCF3405 | abierto (renovado 01/10; 2 años, residir en Pérez) |
| 30/09 | Mantenimiento Mecánico | Empresa sin nombre | Rosario | Computrabajo | buscar en Computrabajo | abierto |
| 30/09 | Mecánico para flota pesada | NEO-BIZ Consultores | Rosario | Computrabajo | buscar en Computrabajo | abierto |
| 30/09 | Mecánico de mantenimiento de vehículos pesados | NEO-BIZ Consultores | Granadero Baigorria | Computrabajo | buscar en Computrabajo | abierto |
| 30/09 | Inspector/a de Mantenimiento | Adecco | Ricardone | Computrabajo | buscar en Computrabajo | abierto (renovado 05/10) |
| 30/09 | Técnicos/as de mantenimiento | Adecco | Rosario | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-tecnicosas-de-mantenimiento-rosario-en-rosario-2083552F50C8569161373E686DCF3405 | abierto (renovado 01/10) |
| 30/09 | Técnico Mecánico | Grúas San Blas S.A. | Rosario | Computrabajo | buscar en Computrabajo | abierto |
| 30/09 | Técnico/a de Mantenimiento (hipermercado) | Grupo Gestión | Rosario | Computrabajo | buscar en Computrabajo | abierto |
| 30/09 | Técnico Naval o Mecánico | Confidencial | Rosario | Bumeran | https://www.bumeran.com.ar/empleos/tecnico-naval-o-mecanico-1118426134.html | abierto (02/09; edad 20-35, viajes) |
| 30/09 | Operario técnico de producción (incluye control de calidad) | Estudio Aún & Asociados | Rosario | Computrabajo | buscar en Computrabajo | abierto |
| 30/09 | Dibujante técnico y proyectista | GDM Ingeniería | Rosario | ZonaJobs | https://www.zonajobs.com.ar/empleos/busqueda-de-dibujante-tecnico-y-proyectista-mecanico-solidworks-gdm-ingenieria-2188513.html | abierto (25/08; SolidWorks excluyente) |
| 30/09 | Analista de calidad | CONSULTNNVA | Rosario | Computrabajo | buscar en Computrabajo | abierto (más de 30 días) |
| 30/09 | Técnico Mecánico/Electromecánico (piping, soldadura) | BERTEC S.A. | Rosario | Computrabajo | buscar en Computrabajo | abierto (más de 30 días) |
| 30/09 | Oficial mecánico / técnico mecánico industrial | Estudio Selector | Rosario | Computrabajo | buscar en Computrabajo | abierto (más de 30 días) |
| 30/09 | Técnico/a de Mantenimiento perfil eléctrico | Randstad | Rosario | Randstad | https://www.randstad.com.ar/trabajos/tecnicoa_rosario_47496497/ | abierto (baja afinidad) |
| 30/09 | Técnico/a de Taller Eléctrico | Randstad | Rosario | Randstad | https://www.randstad.com.ar/trabajos/tecnicoa-de-taller-electrico_rosario_47504917/ | abierto (baja afinidad) |
| 30/09 | Mecánico/a de Camiones | Randstad | Rosario | Randstad | https://www.randstad.com.ar/trabajos/mecanicoa-de-camiones_rosario_47513787/ | abierto (baja afinidad) |
| 30/09 | Técnico de Mantenimiento en cadena de supermercados | Randstad | Rosario | Randstad | https://www.randstad.com.ar/trabajos/tecnico-de-mantenimiento-importante-cadena_rosario_46546752/ | abierto (baja afinidad) |
| 30/09 | Supervisor/a de Planta | Randstad | Timbúes | Randstad | https://www.randstad.com.ar/trabajos/supervisora-de-planta_timbues_47421891/ | abierto (formación sin verificar) |

### Búsqueda del 02/10/2026

| Encontrado | Título | Empresa / consultora | Localidad | Fuente | Link | Estado |
|---|---|---|---|---|---|---|
| 02/10 | Técnicos Electromecánicos, Electrónicos, Eléctricos (mediciones, END, mecanizado, armado de equipos) | Importante empresa del sector | Rosario | Jooble | https://ar.jooble.org/desc/-7537091711801165049 | abierto (hace ~1 mes) |
| 02/10 | Operador Mecanizado CNC (secundario técnico, 1 año) | Importante empresa del sector | Rosario | Jooble | buscar "Operador Mecanizado CNC Rosario" en Jooble | cerrado 05/10 (ya no aparece) |
| 02/10 | Operador de Torno Paralelo (planos, instrumentos de medición) | Importante empresa del sector | Rosario | Jooble | https://ar.jooble.org/desc/5775069938729022262 | abierto (hace ~1 mes) |
| 02/10 | Operador y programador de Centro de Mecanizado (control dimensional) | Rinaudo e Hijos SRL | Granadero Baigorria | Jooble | https://ar.jooble.org/desc/-620947535561914584 | abierto (hace ~2 meses) |
| 02/10 | Programador de Centro Mecanizado CNC | RRHH Buro | Villa Gobernador Gálvez | Jooble | https://ar.jooble.org/desc/4225428492771286761 | abierto (hace ~2 meses) |
| 02/10 | Programador de CNC (empresa agrícola) | Ceta Capital Humano | Rosario | Jooble | https://ar.jooble.org/jdp/-6751909237874383308 | abierto (hace ~2 meses) |
| 02/10 | Operario CNC Parque Industrial de Pérez (prensas y plegadoras, calidad de piezas) | Consultores de Empresas | Pérez | Jooble / Computrabajo | buscar en Jooble o Jobiis | cerrado 05/10 |
| 02/10 | Operarios de Fundición y Mecanizado (inspección de piezas, tornos CNC) | Consultores de Empresas | San Lorenzo | Jobiis | https://www.jobiis.com/jobs-list/151464?country=ARG | actualizado 05/10 (republicado 02/10; técnica deseable, 1 año, movilidad propia excluyente) |
| 02/10 | Operador CNC / control de calidad dimensional | DAVID LEON S.A. | Rosario | Jooble | buscar en Jooble | cerrado 05/10 (ya no aparece) |
| 02/10 | Operarios Sector Chapería (plegadora, tornos, fresa, CNC; movilidad propia) | CONCEPTO EMPRESARIO S.A. | Rosario | Jooble / Computrabajo | https://ar.jooble.org/desc/1845976574651496345 | abierto (30/09) |
| 02/10 | Operario de ensamble zona sur (fábrica de hornos) | Grupo Gestión | Rosario | Jooble / Computrabajo | https://www.bumeran.com.ar/empleos/operario-a-de-ensamble-zona-sur-de-rosario-grupo-gestion-1118458273.html | abierto (renovado 28/09) |
| 02/10 | Operarios Metalúrgicos con secundario completo (turnos rotativos) | Grupo Servicemen | Rosario | Jooble / Computrabajo | https://ar.jooble.org/desc/-7184937661077257895 | abierto (hace ~1 mes) |
| 02/10 | Matricero / operador mecanizado (torno, fresa, CNC) | Excelencia Laboral S.A. | Rosario | Jooble | https://ar.jooble.org/desc/8592492109239111997 | abierto (hace ~1 mes) |
| 02/10 | Plegador (plegadoras CNC, planos, control dimensional, acero naval) | Rocktree (astillero) | Alvear / Pueblo Esther | Bumeran / LinkedIn | https://www.bumeran.com.ar/empleos/plegador-rocktree-1118463820.html | actualizado 05/10 (ahora con empresa y link; 2 años como plegador) |
| 02/10 | Tornero / Alesador convencional | I.M.CA Y PER S.A. | Rosario | Jooble | https://ar.jooble.org/jdp/-8602712347450111538 | abierto (hace ~1 mes) |
| 02/10 | Ayudante Metalúrgico / Operario de Montaje | Consultores de Empresas | Rosario | Jooble / Computrabajo | https://ar.jooble.org/desc/-1616598113154528118 | abierto (republicado ~01/10, edad 25-45, baja afinidad) |
| 02/10 | Operarios caldereros (fabricación metalmecánica, planos) | Importante empresa metalmecánica | Rosario | Jooble | https://ar.jooble.org/desc/2688234911349460639 | abierto (~16/09, baja afinidad) |
| 02/10 | Líder de chapería (zona sur) | Ezequiel Pereyra Búsqueda y Selección | Rosario | Jooble / Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-lider-de-chaperia-en-rosario-D3A065C96F668CD961373E686DCF3405 | abierto (verificado: secundario, 5 años en plegado y control de calidad) |
| 02/10 | Supervisor producción turno tarde (CNC, SAP B1, ISO 9001) | PROGLOBAL | Rosario | Jooble | buscar en Jooble | no encontrado el 05/10 (sin confirmar) |
| 02/10 | Analista de Calidad (concesionarios) | Grupo Quijada | Rosario | Jooble | buscar en Jooble | no encontrado el 05/10 (sin confirmar) |

Descartados el 02/10/2026: Operario Técnico de Producción PyME (Estudio Aún, ya en registro como vigente); Jefe de Producción (Importante Empresa Industrial, pide ingeniería); Jefe de Planta Metalúrgica (Clip, pide Ing. Industrial); Proyectista (INDUMEC, oficina técnica/ingeniería); Quality Control Technician II (Advanced Energy, aviso en inglés, localización dudosa, probablemente no es Rosario Argentina).

Cerrados o sin novedades al 02/10/2026: Randstad Rosario, San Lorenzo y Pérez sin avisos nuevos desde el 28/09; todos los de Randstad del registro siguen publicados.

### Búsqueda del 05/10/2026

Informe completo con requisitos y motivos: `informe-busqueda-fiama-2026-10-05.md`.

| Encontrado | Título | Empresa / consultora | Localidad | Fuente | Link | Estado |
|---|---|---|---|---|---|---|
| 05/10 | Operario de torno CNC (calibre, micrómetro, planos, códigos G/M) | Consultores de Empresas | Rosario (sur) | Computrabajo / Jooble | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-operario-de-torno-cnc-en-rosario-96E09778CF92928261373E686DCF3405 | postulada 06/10 (antes: abierto (01/10, alta)) |
| 05/10 | Técnicos Mecánicos/Electromecánicos – Servicio Posventa y Taller (junior, 2 vacantes) | Sullair Argentina | Rosario | Bumeran | https://www.bumeran.com.ar/empleos/tecnicos-mecanicos-electromecanicos-electronicos-o-equivalentes-sullair-rosario-1118462598.html | postulada 06/10 (antes: abierto (30/09, alta)) |
| 05/10 | Operario de producción – Perfiles Técnicos (verificación con calibres/micrómetros) | Consultores de Empresas | Rosario (sudoeste) | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-operario-de-produccion-perfiles-tecnicos-en-rosario-B05F2663C8B5C46561373E686DCF3405 | postulada 06/10 (antes: abierto (29/09, alta)) |
| 05/10 | Operario de máquinas convencionales req212080 (torno, fresa, planos; eventual) | ManpowerGroup | Villa Gobernador Gálvez | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-operario-de-maquinas-req212080-eventual-en-villa-gdor-galvez-819078D69220610261373E686DCF3405 | postulada 06/10 (antes: abierto (04/10, alta)) |
| 05/10 | Técnico de Garantías (inspección, no conformidades, causa de falla; autopartes) | Confidencial | Rosario | Bumeran | https://www.bumeran.com.ar/empleos/tecnico-de-garantias-1118451262.html | postulada 06/10 (antes: abierto (22/09, alta)) |
| 05/10 | Operario de Producción y Montaje (SPRAYtec, pulverización agrícola) | NEO-BIZ Consultores | Rosario (oeste) | Bumeran / Computrabajo / Jooble | https://www.bumeran.com.ar/empleos/operario-de-produccion-y-montaje-neo-biz-1118460996.html | postulada 06/10 (antes: abierto (30/09, alta; 3 años)) |
| 05/10 | Responsable de Calidad – Parque Metropolitano (ISO 9001, IATF, metrología) | Industria plástica sin nombre | Pérez | Jooble | https://ar.jooble.org/desc/1572436928511256232 | postulada 06/10 (antes: abierto (hace 2 meses, alta)) |
| 05/10 | Tornero con conocimientos en CNC (maquinaria agrícola) | Empresa agroindustrial | Rosario | Municipalidad de Rosario | https://empleo.produccionrosario.gob.ar/empleos/tornero_1136.html | postulada 06/10 (antes: abierto (alta; 2 años como tornero)) |
| 05/10 | Técnico Mecánico/Electromecánico (reparaciones, metalúrgica; eventual) | ManpowerGroup | Villa Gobernador Gálvez | Computrabajo / Jooble | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-tecnico-mecanicoelectromecanico-en-villa-gdor-galvez-7C03EDBDD6F192B761373E686DCF3405 | postulada 06/10 (antes: abierto (30/09, alta; 3 años, edad 25-40)) |
| 05/10 | Operarios de Ensamble (metalúrgica zona oeste, control visual) | Grupo Gestión | Rosario | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-operarios-de-ensamble-en-rosario-E5AA2CA59633BC8361373E686DCF3405 | abierto (04/10, media) |
| 05/10 | Operario de ensamble (componentes mecánicos, planos; turnos) | Importante empresa industrial | Rosario | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-operario-de-ensamble-rosario-en-rosario-FAA7A4F97A6A3AF161373E686DCF3405 | abierto (01/10, media) |
| 05/10 | Operario producción (ensamblado metal/vidrio, control visual, UOM) | Grupo Servicemen | Rosario (sudoeste) | Computrabajo / Jooble | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-operario-produccion-en-rosario-6D47042F2C54DC1361373E686DCF3405 | abierto (03/10, media) |
| 05/10 | Operarios de producción (armado y ensamble en línea, instrumentos de medición) | Concepto Empresario S.A. | Rosario (sur) | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-operarios-de-produccion-rosario-en-rosario-D79CCF89BD95844561373E686DCF3405 | abierto (29/09, media) |
| 05/10 | Operadores/as de producción (metalúrgica, puente grúa) | Concepto Empresario S.A. | Pérez / Zavalla | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-operadoresas-de-produccion-perez-zavalla-en-perez-A10961297970E05B61373E686DCF3405 | abierto (01/10, media) |
| 05/10 | Operarios de producción / de Planta (metalúrgica Pérez; título técnico preferente) | Grupo Servicemen | Pérez | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-operarios-de-produccion-perez-santa-fe-en-perez-F62FF284329C4F7061373E686DCF3405 | abierto (27/09, media) |
| 05/10 | Operarios de Producción Técnicos (Pérez, Soldini, Zavalla) | Grupo Gestión | Pérez | Jooble | https://ar.jooble.org/desc/-7612636578757716798 | abierto (hace 2 meses, media) |
| 05/10 | Montaje de máquinas (maquinaria agrícola; 2 años montaje) | Empresa agroindustrial | Rosario | Municipalidad de Rosario | https://empleo.produccionrosario.gob.ar/empleos/montaje-de-maquinas_1145.html | abierto (media) |
| 05/10 | Ajustador Mecánico (verificación dimensional, planos) | I.M.CA Y PER S.A. | Rosario | Jobsora / trabajosdiarios | https://ar.jobsora.com/oferta-52423016016?source=1 | abierto (~01/10, media) |
| 05/10 | Técnico de mantenimiento mecánico (plástica, SAP, turnos) | NOS Soluciones en RRHH | Pérez | Bumeran / ZonaJobs / Jooble | https://www.bumeran.com.ar/empleos/operario-de-mantenimiento-mecanico-nos-soluciones-en-rrhh-1118456572.html | abierto (25/09, media) |
| 05/10 | Mantenimiento Industrial (técnico mecánico preferente) | Consultores de Empresas | Pérez | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-mantenimiento-industrial-en-perez-119A4AAA082D943661373E686DCF3405 | abierto (29/09, media) |
| 05/10 | Mantenimiento Mecánico / Electromecánico | Consultores de Empresas | Rosario | Computrabajo / Jooble / Jobiis 151488 | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-mantenimiento-mecanico-electromecanico-en-rosario-16D75DB8DADFF5EF61373E686DCF3405 | abierto (01/10, media) |
| 05/10 | Analista de Oficina Técnica de Equipos (SAP, planos, instrumentos; ingeniería deseable) | Milicic S.A. | Rosario | Bumeran | https://www.bumeran.com.ar/empleos/analista-de-oficina-tecnica-de-equipos-milicic-s-a-1118397464.html | abierto (11/08, media) |
| 05/10 | Plegador (planos, elementos de medición) | Consultores de Empresas | Villa Gobernador Gálvez | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-plegador-en-villa-gdor-galvez-6C5AAFC5A706994B61373E686DCF3405 | abierto (29/09, media) |
| 05/10 | Plegador (plegadoras con y sin CNC, control dimensional) | sin nombre (metalúrgica oeste) | Rosario | Sitio Empleos | https://www.sitioempleos.com.ar/index.php?pagina=detalle&id=8078 | abierto (02/10, media) |
| 05/10 | Técnico en Mantenimiento (productos de acero, Parque Industrial Alvear) | Taxia Recruitment | Alvear | Bumeran | https://recruitment.taxia.net/busqueda/tecnico-en-mantenimiento-455 | abierto (23/07, media) |
| 05/10 | Operario de Ensamble (electrodomésticos, control visual; eventual) | Adecco | Granadero Baigorria | Computrabajo / Jooble | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-operario-de-ensamble-en-granadero-baigorria-D9C75FB689974B7661373E686DCF3405 | abierto (03/10, media) |
| 05/10 | Operario de Mantenimiento Industrial (secundario técnico excluyente; eléctrico/refrigeración) | Adecco | Rosario | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-operario-de-mantenimiento-industrial-rosario-en-rosario-3F3A6B78E2E755C661373E686DCF3405 | abierto (30/09, media-baja) |
| 05/10 | Técnico electromecánico de mantenimiento (astillero) | Rocktree | Alvear / Pueblo Esther | Bumeran / LinkedIn | https://www.bumeran.com.ar/empleos/tecnico-electromecanico-de-mantenimiento-rocktree-1118462766.html | abierto (30/09, media-baja) |
| 05/10 | Técnico Mecánico para inspección de obras industriales | DETEXA SRL | Rosario | Indeed / Glassdoor (solo snippet) | detexaros@detexasrl.com.ar · WhatsApp +54 341 6167367 | sin verificar (Indeed bloqueado) |
| 05/10 | Operador técnico de planta – aceites y refrigerantes | Importante empresa | Álvarez (Alvear) | Jooble | https://ar.jooble.org/desc/4940924490153612862 | abierto (hace 2 meses, baja) |
| 05/10 | Operadores/as de Planta Industrial (química; técnico químico/eléctrico/electromecánico) | JoffreHR | Gran Rosario | LinkedIn | https://ar.linkedin.com/jobs/view/operadores-as-de-planta-industrial-gran-rosario-at-joffrehr-4471216345 | abierto (~29/09, baja) |
| 05/10 | Pasante Eventual de Maquinaria Agrícola | CLAAS Argentina | Rosario | Talent.com | https://ar.talent.com/view?id=555317574087216500 | abierto (~27/09, baja) |
| 05/10 | Operario de producción con secundario técnico electromecánico (UOM) | Consultores de Empresas | Rosario | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-operario-de-produccion-con-secundario-tecnico-electromecanico-rosario-en-rosario-8F01C452C00A8E9B61373E686DCF3405 | abierto (28/09, baja; edad 20-27) |
| 05/10 | Operario de producción eventual (Pérez, enlozado, chapería, CNC) | Consultores de Empresas | Pérez | Computrabajo / Jooble | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-operario-de-produccion-eventual-en-perez-7895CE675BB08E1161373E686DCF3405 | abierto (02/10, baja) |
| 05/10 | Operarios metalúrgicos Sector Chapería Pérez | Grupo Gestión | Pérez | Jooble | https://ar.jooble.org/desc/-928659962102364934 | abierto (hace 2 meses, baja) |
| 05/10 | Operario/a de Ensamble – Granadero Baigorria (eventual) | Grupo Gestión | Granadero Baigorria | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-operarioa-de-ensamble-granadero-baigorria-en-granadero-baigorria-9EDC6B7D0401B00161373E686DCF3405 | abierto (05/10, baja) |
| 05/10 | Operario eventual en Granadero Baigorria | Ceta Capital Humano | Granadero Baigorria | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-operario-eventual-en-granadero-baigorria-en-granadero-baigorria-54647092832D333361373E686DCF3405 | abierto (01/10, baja) |
| 05/10 | Operario sector Moldeo y Poliuretano | Consultores de Empresas | Rosario | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-operario-para-el-sector-de-moldeo-y-poliuretano-en-rosario-BD2788944F491F5A61373E686DCF3405 | cerrado 07/10 (el link redirige al listado) |
| 05/10 | Operario de producción sector vidrios (CNC de corte) | Consultores de Empresas | Rosario | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-operario-de-produccion-en-sector-vidrios-en-rosario-A90B2D9B5B3B12DB61373E686DCF3405 | abierto (05/10, baja) |
| 05/10 | Operario industrial zona norte | Importante empresa | Rosario | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-operario-industrial-en-ciudad-de-rosario-zona-norte-en-rosario-5F635B1091F9C86C61373E686DCF3405 | abierto (02/10, baja) |
| 05/10 | Operario Metalúrgico Maquinista (corte y flejado de chapas, calibre) | Importante empresa metalúrgica | Rosario | Jooble | https://ar.jooble.org/desc/-1569207266974551687 | abierto (hace 2 meses, baja) |
| 05/10 | Operario y Soldador Técnico (vagones; con y sin experiencia) | TECNO RAIL SERVICE S.R.L. | San Lorenzo | Computrabajo / Jooble | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-operario-y-soldador-tecnico-en-san-lorenzo-AA73BDFE2784BEBF61373E686DCF3405 | abierto (01/10, baja) |
| 05/10 | Oficial Tornero (tornos paralelos; 5 años) | San Diego S.A. | Alvear | Computrabajo / Jooble | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-oficial-tornero-en-estacion-alvear-288CE0D99F5A066561373E686DCF3405 | abierto (30/09, baja) |
| 05/10 | Técnico de Mantenimiento Industrial (metalúrgica) | San Diego S.A. | Alvear | Jooble | https://ar.jooble.org/desc/7742364290211279999 | abierto (hace 2 meses, baja) |
| 05/10 | Inspector de Ensayos No Destructivos | HEFESTO | Rosario | Bumeran | https://www.bumeran.com.ar/empleos/inspector-de-ensayos-no-destructivos-hefesto-1118379243.html | abierto (24/07, baja) |
| 05/10 | Supervisor Industrial Junior | Consultores de Empresas | Rosario | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-supervisor-industrial-junior-rosario-en-rosario-1700BA9E2235291161373E686DCF3405 | abierto (29/09, baja) |
| 05/10 | Supervisor de producción (metalmecánica) | Confidencial | Alvear | ZonaJobs | https://www.zonajobs.com.ar/empleos/supervisor-de-produccion-2191015.html | abierto (30/09, baja) |
| 05/10 | Jefe de Servicio / Técnicos de Servicio (maquinaria agrícola) | Neo-Biz | Rosario | Bumeran | https://www.bumeran.com.ar/empleos/jefe-de-servicio-tecnicos-de-servicio-neo-biz-1118382609.html | abierto (28/07, baja) |
| 05/10 | Técnico Mecánico de Equipos de Grúas o Izaje (3 años) | ManpowerGroup | Rosario | Jooble / LinkedIn | https://ar.jooble.org/desc/-2970563200247874756 | abierto (hace 2 meses, baja) |
| 05/10 | Técnico de Mantenimiento Zona Rosario (ascensores) | AP Soluciones | Rosario | Bumeran | https://www.bumeran.com.ar/empleos/tecnico-de-mantenimiento-zona-rosario-ap-soluciones-1118388319.html | abierto (03/08, baja) |
| 05/10 | Técnico Químico/Electromecánico/Mecánico – planta de pintura | Importante empresa | Álvarez (Alvear) | Jooble | https://ar.jooble.org/desc/-5535705339427032946 | abierto (hace 2 meses, baja) |
| 05/10 | Operario Terminador (PRFV, carrocerías) | Pierandrei | Villa Gobernador Gálvez | Bumeran | https://www.bumeran.com.ar/empleos/operario-terminador-pierandrei-1118378377.html | abierto (28/07, baja) |

Descartados el 05/10/2026 (resumen; detalle en el informe): Analista de Control y Procesos Jr. (Grassi/Nueva Vicentin, universitario); Analista de Mejora Continua y Analista de PCP (B&B, ingeniería); Auxiliar de calidad San Lorenzo (Clip, ingeniería química); Planificación de Mantenimiento (RRHH Buro, ingeniería); Coordinador de producción (Consultores, ingeniería); Supervisor/a de Producción (Pilares, ingeniería); Supervisor Mecánico (Neo-Biz Timbúes, ingeniería; Adecco Terminal 6, supervisión); Jefe/a de Planta y de Oficina Técnica (Randstad, Adecco), Jefe/a de Calidad (Talento Divergente), Jefe de PCP Pérez (ingeniería); Líder Aseguramiento de Calidad (La Virginia, ingeniería alimentos); Coordinador de Calidad (Air Liquide, Farmacia); Inspector de Calidad (Minerva, alimentos); Coordinador de Inspección (YPF, universitario); Inspector de Cargas Portuarias (RH Talentum, universitario); Inspector/a (empresa de transporte, no es calidad); Operario Metalúrgico gastronómico (Grupo Consultor, edad 30-45); Tornero con experiencia VGG (5 años); Auxiliar de Servicio Técnico (Centro Hidráulico, sexo masculino); Técnico Electromecánico refrigeración (edad 27-57); Operario/a aberturas de aluminio (B&B, METRA); perfiles eléctricos/PLC (Terragene, Pagani, Famago, Pivot Adecco, Litoral Gas, Pierandrei, NOS eléctrico, Randstad NH3, Manpower técnico electrónico grúas, Tecno Rail electrónico, Sitio Empleos 8008, Instrumentista Adecco, Generación Mediterránea Timbúes); soldadores profesionales (Pereyra, Manpower, Consultores, Rocktree FCAW, Concepto Empresario); mecánica automotriz/vial (Consultores Timbúes, Autotrol, Milicic, Manpower vial); fuera de zona (Mec Consultores Carcarañá, Servicemen Carcarañá, San Jorge, Randstad Santa Fe/Recreo); Bunge PGSM (Smart Manufacturing Analyst, Planificador Eléctrico, Procurement, Logística Renova: datos/eléctrico/universitario); Soporte IT CNC Jr (Grassi, informática); Pasantías Maincal (universitarios); CLAAS técnico de maquinaria agrícola (9 meses, service a campo); METRA supervisión de limpieza; Startia supervisión plástica; Sika Técnico/a de Mantenimiento (vencido); Timken y Gates (EE.UU.); Asoko Tempo (finalizado); operarios no afines (inyectora, reciclado, rebobinadora, depósito, té, pastas, balanza, logística, montadores en altura, Maincal calzado, STIB hidráulica, tratamiento de agua, Rocktree calderero).

Cerrados o dados de baja al 05/10/2026: Técnico mecánico/electromecánico/químico tareas generales (Consultores/Adecco) · Inspector/a (Grupo Gestión) · Inspector/a (ManpowerGroup) · Operario de calidad turnos rotativos (Servicemen, duplicado) · Técnico de Mantenimiento (Clip, San Lorenzo) · Operario CNC Parque Industrial de Pérez (Consultores) · Operador Mecanizado CNC (Importante empresa) · Operador CNC DAVID LEON · Coordinador de calidad (Consultores, pasa a descartado por universitario). Sin confirmar: PROGLOBAL, Grupo Quijada, Flexocolor.

### Búsqueda del 06/10/2026

Informe completo con requisitos y motivos: `informe-busqueda-fiama-2026-10-06.md`. Mensaje enviado: `mensaje-fiama-2026-10-06.md`.

| Encontrado | Título | Empresa / consultora | Localidad | Fuente | Link | Estado |
|---|---|---|---|---|---|---|
| 06/10 | Analista de Calidad / Full Time / VGG (técnico mecánico; controles dimensionales, no conformidades, causa raíz; L-J 7-16, V 7-14) | Importante empresa del sector (metalúrgica / equipos para aceiteras) | Villa Gobernador Gálvez | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-analista-de-calidad-full-time-vgg-en-villa-gdor-galvez-5630749F4AE9EAF261373E686DCF3405 | postulada 06/10 (antes: abierto (05/10, alta)) |
| 06/10 | Ensamblador (herramientas, elementos de medición, planos de montaje; CV con foto) | sin nombre | Rosario (sur, área Despacho) | Sitio Empleos | https://www.sitioempleos.com.ar/index.php?pagina=busqueda&id=8119 | postulada 06/10 (antes: abierto (05/10, media)) |
| 06/10 | Técnico/a de Oficina Técnica (presupuestos, visitas a clientes, planos; secundario técnico o terciario; plazo fijo) | Consultores de Empresas | Rosario | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-tecnicoa-de-oficina-tecnica-en-rosario-F0D14E0FEB72C34D61373E686DCF3405 | postulada 06/10 (antes: abierto (05/10, media)) |
| 06/10 | Operario de Mantenimiento (mecánico y eléctrico, refrigeración, plomería, soldadura; edad 25-45) | Consultores de Empresas | Rosario | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-operario-de-mantenimiento-en-rosario-6E4273C8D6D3381661373E686DCF3405 | abierto (05/10, baja) |
| 06/10 | Ayudante Metalúrgico / Full Time / VGG (amoladora excluyente; UOM rama 17) | Importante empresa del sector (misma planta que Analista de Calidad) | Villa Gobernador Gálvez | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-ayudante-metalurgico-full-time-vgg-en-villa-gdor-galvez-6BE0DD59A0CE5B6661373E686DCF3405 | abierto (05/10, baja) |
| 06/10 | Mecánico con perfil eléctrico (maquinaria, equipos y vehículos; tableros; 2 años; viajar) | Consultores de Empresas | Rosario y Piñero | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-mecanico-con-perfil-electrico-en-rosario-048F453918C0A24561373E686DCF3405 | abierto (05/10, baja) |

Descartados el 06/10/2026 (detalle en el informe): Responsable de Control de Calidad, maquinaria agrícola (Municipalidad de Rosario 1155: encajaba, pero "Búsqueda finalizada"); Cadista (Grupo Pose, estudiante de Arquitectura); Estudiantes de Ingeniería Industrial o Mecánica (Industria Líder, universitario); Técnico/a Electromecánico/a (Ricardo Venturino, Venado Tuerto); Responsable de Operaciones (Serrat SRL, jefatura); Responsable de Planta VGG (Randstad, ingeniería); Mecánico/a para autoelevadores (Randstad, Fray Luis Beltrán de Mendoza); Mecánico de Camiones Timbúes (Consultores), Mecánico Vial (CIC), Personal de taller oficial de 3ª (Alsa): automotriz; Oficial Soldador VGG (RRHH Buro), Soldador Calificado (Sitio Empleos 8120), Armador/Calderero y Soldador (Rocktree): soldadura; Técnico de campo (CORTEL y Grupo giio, San Lorenzo, telecomunicaciones); Técnico Electrónico (JALP), Ing. Electrónico Jr (NCA), Coordinador de Mantenimiento eléctrico (Grassi), técnico electrónica (Nardi); Analista QA (Rosental, software); Operario Calificado tratamiento de agua (Sitio Empleos 8011); Operario de Producción pastas (Sitio Empleos 7987), Operario de Producción Paladini, charqueo y despostada (Municipalidad 1151, 1154); Personal de mantenimiento mayor de 40 (Sitio Empleos 7980); Plegador (Sitio Empleos 8068, duplicado del 8078); Montadores estructuras metálicas (8002); Operario movimiento de materiales (Jobiis 151590); Operarios de Mantenimiento San Jorge (Municipalidad 1150); Técnico de Mantenimiento sanitarias y gas (Municipalidad 1149); Operario cartón corrugado Carcarañá (Servicemen); Auxiliar de Taller, Inspector/a y chapería automotriz (empresa de transporte); Técnico de ascensores (Talentive); renovados ya descartados: Inspector/a de calidad servicios energéticos (ingeniería), Técnico Electromecánico refrigeración (edad 27-57), Técnico de Mantenimiento Mecánico (Find Me, ingeniería), Operario/a de Producción aberturas (B&B), Analista de PCP (B&B), Machinist (Timken, EE.UU.).

Postulaciones 06/10/2026: Fiama se postuló a los 22 avisos del mensaje del 06/10 (1 alta nuevo, 3 media nuevos y los 18 del bloque "siguen abiertas"); quedan marcados como "postulada" y no deben volver a listarse.

Cerrados o dados de baja al 06/10/2026: Auxiliar de Gestión de Calidad (Ezequiel Pereyra). Reabierto: Técnico mecánico / electromecánico / químico – tareas generales (Consultores). Verificados como abiertos: los 32 avisos restantes de Computrabajo del registro, Cargill, Bunge, Servicemen (ambos), LOZAMETAL, Responsable de Calidad Pérez, Gemplast, Ceta 608 y 609, SKF, Sullair, Técnico de Garantías, NEO-BIZ, Rocktree, Municipalidad 1136 y 1145, todos los Randstad, Taxia, HEFESTO, Pierandrei, NOS Pérez, Grupo Gestión ensamble zona sur. Sin verificar: Milicic Analista de Oficina Técnica, DETEXA, Flexocolor, PROGLOBAL, Grupo Quijada.

### Búsqueda del 07/10/2026

Informe completo con requisitos y motivos: `informe-busqueda-fiama-2026-10-07.md`. Mensaje enviado: `mensaje-fiama-2026-10-07.md`.

| Encontrado | Título | Empresa / consultora | Localidad | Fuente | Link | Estado |
|---|---|---|---|---|---|---|
| 07/10 | Técnico de Servicios (inspecciones END: PT, MT, ultrasonido; técnico mecánico, 2 años, inglés intermedio, viajes) | SKF Argentina | Rosario | HiringRoom SKF / Bumeran | https://skf.hiringroom.com/jobs/get_vacancy/6ac64a910bc162c70cb1663c | abierto (07/10, alta) |
| 07/10 | Operarios de Chapería: Plegado y Corte Láser (planos, calibre, goniómetro; hasta 35) | LAUGE EQUIPAMIENTOS SRL | Rosario | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-operarios-de-chaperia-plegado-y-corte-laser-rosario-chaperia-en-rosario-2C8781511C16CEC761373E686DCF3405 | abierto (06/10, media) |
| 07/10 | Líder de Producción (planos, instrumentos de precisión, coordinar equipos; plazo fijo) | Consultores de Empresas | Villa Gobernador Gálvez (a definir) | Computrabajo | https://ar.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-lider-de-produccion-en-villa-gdor-galvez-600A0350B616267E61373E686DCF3405 | abierto (06/10, media) |
| 07/10 | Técnico de mantenimiento mecánico (título técnico excluyente; hidráulica, rodamientos, SAP; turnos) | Gemplast Argentina | Pérez | LinkedIn | https://ar.linkedin.com/jobs/view/t%C3%A9cnico-de-mantenimiento-mec%C3%A1nico-at-gemplast-argentina-4475125886 | abierto (06/10, media; probablemente misma vacante que NOS Pérez) |
| 07/10 | Operador(a) de Preparación eventual (secundario técnico; muestreo, laboratorio, equipos; turnos) | Cargill | Villa Gobernador Gálvez | careers.cargill.com | https://careers.cargill.com/es/trabajo/galvez/operador-a-de-preparacion-eventual-villa-gobernador-galvez/31241/101624501472 | abierto (06/10, media) |
| 07/10 | Técnico Mecánico (diseño de piezas a medida; SolidWorks excluyente; ingreso febrero) | Consultores de Empresas | Villa Gobernador Gálvez (a definir) | Jobiis 151667 | https://www.jobiis.com/jobs-list/151667?country=ARG | abierto (~06/10, baja) |
| 07/10 | Técnico en lectura y realización de planos (3D, SolidWorks; dibujante excluyente) | fábrica de aberturas | Rosario | Municipalidad de Rosario 1158 | https://empleo.produccionrosario.gob.ar/empleos/tecnico-en-lectura-y-realizacion-de-planos_1158.html | abierto (07/10, baja) |
| 07/10 | Ayudantes metalúrgicos (turnos tarde/noche, contrato por proyecto) | Consultores de Empresas | Rosario (a definir) | Jobiis 151673 | https://www.jobiis.com/jobs-list/151673?country=ARG | abierto (~06/10, baja) |

Descartados el 07/10/2026 (detalle en el informe): Ingeniero de Confiabilidad (SKF, ingeniería y 10 años); Ingeniero/a de Confiabilidad Jr (Louis Dreyfus General Lagos, ingeniería mecánica); Técnico de Mantenimiento Eléctrico Industrial (San Lorenzo, eléctrico/PLC); Jefe de Planta (Amarilla Gas, jefatura); Montadores de Estructuras Metálicas (FLEXIO, obra en altura); Operario producción (Funcional Foods, alimentos); Operario de recepción y expedición (RRHH Buro), Operarios de depósito (Grupo Gestión), Empleado de depósito (NOS), Operario de Logística (Sitio Empleos 8138): logística; Operador(a) de Limpieza Industrial (Cargill VGG); Supervisor de Producción y Planificador de Confiabilidad (Bunge, Buenos Aires); Electricista de Vehículos (Alsa); Diseñador de Producto Mecánico (Uplin HR, ciudad de Santa Fe); Ingeniero Mecánico (Paladini); Plegador (Sitio Empleos 8079, mismo texto que el 8078).

Cerrados o dados de baja al 07/10/2026: Operario sector Moldeo y Poliuretano (Consultores de Empresas). Verificados como abiertos: los otros 37 avisos de Computrabajo del registro, Municipalidad 1136 y 1145, los 10 de Randstad (Operario/a de producción Pérez vence el 13/10). No quedan avisos de prioridad alta sin postular de búsquedas anteriores.

### Descartados el 30/09/2026 (no volver a listar salvo que cambien los requisitos)

| Título | Empresa / consultora | Motivo |
|---|---|---|
| Analista de Calidad de Planta | Arneg Argentina | pide ingeniería |
| Inspector/a de calidad (servicios energéticos) | sin nombre | pide estudiante avanzado o graduado de ingeniería (renovado 05/10, sin cambios) |
| Jefe/a de Producción | Randstad (Capitán Bermúdez) | pide ingeniería |
| Ingeniero/a de Confiabilidad | Louis Dreyfus (General Lagos) | pide ingeniería |
| Ingeniero/a de Gestión Industrial | Leiva & Asociados | pide ingeniería |
| Técnico de Mantenimiento Mecánico | Findme | pide estudiante o graduado de ingeniería mecánica |
| Inspector de Calidad (industria alimentaria) | Grupo Consultor | pide técnico en alimentos |
| Inspector de Control de Calidad | Paladini (VGG) | pide técnico en alimentos o bromatología |
| Analista de Laboratorio / Asistente de muestras | SGS | pide técnico químico |
| Búsqueda masiva de técnicos (industria alimenticia zona norte) | Empleos&Recursos | pide sexo masculino |
| Técnicos para mantenimiento mecánico (metalmecánica zona sur) | Empleos&Recursos | pide sexo masculino |
| Operario general siderúrgica | Consultores de Empresas (Jobiis 150688) | carga y descarga, no afín |

### Cerrados o vencidos al 30/09/2026

Inspector/a de Calidad en línea de terminación (Randstad, refrigeración) · Soldador/a MIG/MAG (Randstad) · Técnico/a Químico/a de laboratorio (Randstad) · Operador CNC ref. 104031 (Randstad) · Técnico/a de campo en confiabilidad (Randstad, San Lorenzo) · Técnico o Ingeniero Mecánico (Ceta, en Talent.com) · Gerente de Integridad de Activos (Bunge, PGSM).

---

## 4. Próximas búsquedas

| Fecha | Nuevos encontrados | Notas |
|---|---|---|
| 02/10/2026 | 20 | Solo Jooble y Randstad legibles; Computrabajo/Bumeran/LinkedIn pendientes con Claude en Chrome |
| 05/10/2026 | 52 (9 alta, 20 media, 23 baja) | Cubiertos Computrabajo, Bumeran/ZonaJobs, LinkedIn, Jooble, Talent, Jobiis, Randstad, Ceta, Cargill, Bunge, Sitio Empleos, Municipalidad de Rosario. Pendientes con Claude en Chrome: Indeed y Glassdoor (verificar Flexocolor, DETEXA, Minerva, YPF) |
| 06/10/2026 | 7 (1 alta, 3 media incl. 1 reabierto, 3 baja) | Un solo día desde la anterior. Cubiertos Computrabajo, Bumeran/ZonaJobs (vía r.jina.ai), Jooble, LinkedIn, Randstad, Ceta, Jobiis, Sitio Empleos, Municipalidad de Rosario, Cargill, Bunge, SKF, Neo-Biz. Pendientes con Claude en Chrome: Indeed y Glassdoor (DETEXA, Flexocolor, Minerva, YPF); portales Viterra, LDC, COFCO, ACA, Sika, John Deere, CLAAS, Metalfor sin revisar |
| 07/10/2026 | 8 (1 alta, 4 media, 3 baja) | Un día desde la anterior. Cubiertos Computrabajo, Bumeran/ZonaJobs (vía r.jina.ai), Jooble, LinkedIn, Randstad, Ceta, Jobiis, Sitio Empleos, Municipalidad, Cargill, Bunge, SKF. Pendientes: Indeed, Glassdoor, Talent; portales Viterra, COFCO, ACA, Sika, Minerva, John Deere, CLAAS, Metalfor, Acindar |
| 09/10/2026 o 10/10/2026 | | |
| | | |
