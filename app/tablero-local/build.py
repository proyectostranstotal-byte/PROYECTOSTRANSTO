# Arma app/index.html (tablero local) a partir del HTML publicado en claude.ai.
# Uso: python build.py <tablero-publicado.html>
import sys, pathlib

AQUI = pathlib.Path(__file__).parent
src = pathlib.Path(sys.argv[1]).read_text(encoding="utf8")

def cambiar(viejo, nuevo, n=1):
    global src
    c = src.count(viejo)
    if c != n:
        sys.exit(f"Esperaba {n} vez/veces y encontré {c}: {viejo[:70]!r}")
    src = src.replace(viejo, nuevo)

# Fuentes de la marca
cambiar('family=Barlow+Condensed:wght@600;700&family=Source+Sans+3:wght@400;600&family=JetBrains+Mono:wght@500',
        'family=Urbanist:wght@500;700&family=Poppins:wght@400;500;600&family=Archivo:wght@500;700')

# Runtime local antes que el resto
# Leaflet servido por la propia app (no depende de cdnjs)
cambiar('<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"',
        '<script src="local.js"></script>\n<script src="leaflet.js"')

# Colores, tipografías y encabezado de Transtotal (van después del estilo original y lo pisan)
MARCA = (AQUI / "marca.css").read_text(encoding="utf8")
cambiar('</style>\n<script src="local.js">', '</style>\n<style>\n' + MARCA + '</style>\n<script src="local.js">')

cambiar('''  <header>
    <h1>Tablero Transtotal</h1>
    <span class="fecha" id="fecha"></span>
  </header>''', '''  <header class="tt-head">
    <picture class="tt-logo"><source media="(prefers-color-scheme: dark)" srcset="marca/logo-blanco.png"><img src="marca/logo-blanco.png" alt="Transtotal Group" onerror="this.closest('picture').hidden=true"></picture>
    <div class="tt-tit"><span class="tt-etq">Panel operativo · Air Liquide</span><h1>Tablero Transtotal</h1><span class="fecha" id="fecha"></span></div>
  </header>''')


# Mapa: fondo de calles (OpenStreetMap vía el puente) en la app local; si no carga, el mapa vectorial de siempre.
cambiar('''function dibujarBase(){
  if(!mapa||!base)return;''', '''let tilesOk=null,capaTiles=null;
function dibujarBase(){
  if(!mapa||!base||(window.TABLERO_LOCAL&&tilesOk!==false))return;''')
cambiar('''  capaU=L.layerGroup().addTo(mapa);
  dibujarBase();''', '''  capaU=L.layerGroup().addTo(mapa);
  if(window.TABLERO_LOCAL){
    let fallas=0;
    mapa.setMaxZoom(17);
    capaTiles=L.tileLayer("tile/{z}/{x}/{y}.png",{minZoom:3,maxZoom:17,attribution:"© OpenStreetMap"}).addTo(mapa);
    capaTiles.on("tileload",()=>{tilesOk=true});
    capaTiles.on("tileerror",()=>{if(tilesOk||++fallas<4)return;tilesOk=false;mapa.removeLayer(capaTiles);dibujarBase()});
    mapa.attributionControl.removeAttribution("Natural Earth");
  }
  dibujarBase();''')

# Textos que hablaban de la app de Claude
cambiar('"Sin datos todavía. Abrí el tablero en la app de Claude de la PC NDIFABIO."', '"Sin datos todavía. Revisá que el tablero esté corriendo en la PC NDIFABIO."')
cambiar('(vivo.live?"":" · en vivo solo desde la app de Claude de la PC")', '(vivo.live?"":" · sin conexión con el puente de la PC")')
cambiar('"Se renuevan cuando el tablero está abierto en la app de Claude de la PC."', '"Se renuevan cada 2 minutos mientras el tablero está abierto."')
cambiar('" · los botones funcionan solo en la app de Claude de la PC"', '" · sin conexión con el puente de la PC"')

# Asignar chofer desde la alerta "en movimiento sin chofer" (escribe asignaciones-manuales.json)
cambiar('d:`Sin iButton · ${u.tractor||""} · ${u.vel} km/h`};', 'd:`Sin iButton · ${u.tractor||""} · ${u.vel} km/h`,asig:1};')
cambiar('<span class="ad">${esc(a.d)}</span></li>', '<span class="ad">${esc(a.d)}</span>${a.asig&&window.TABLERO_LOCAL?`<button type="button" class="btn sec asig-b" data-asig="${esc(a.cis)}">Asignar chofer</button>`:""}</li>')
cambiar('''<td>${u.chofer?esc(u.chofer):'<span class="sub">—</span>'}</td>''', '''<td>${u.chofer?esc(u.chofer)+(u.chofer_manual?' <span class="sub">(a mano)</span>':''):'<span class="sub">—</span>'}</td>''')
cambiar('</div>\n\n<script>', (AQUI / "asignar.html").read_text(encoding="utf8") + '</div>\n\n<script>')

# Excesos: solo desde noviembre 2026 (los de octubre quedan guardados en datos\excesos, pero no se muestran)
cambiar('db.collection("excesos").onSnapshot(s=>{excesos=s.docs.map(d=>({id:d.id,...d.data()}));', 'db.collection("excesos").onSnapshot(s=>{excesos=s.docs.map(d=>({id:d.id,...d.data()})).filter(e=>(e.fecha||"")>=EXCESOS_DESDE);')
cambiar('const INICIO_INCENTIVOS="2026-11-01";', 'const INICIO_INCENTIVOS="2026-11-01";\nconst EXCESOS_DESDE="2026-11-01";')

# Incentivos: cada exceso desde noviembre que requiere justificación y no fue justificado es una falta automática
# (el "avisado" se guarda en el mismo exceso). Las faltas cargadas a mano (multas, siniestros, etc.) siguen en "faltas".
cambiar('excesos=[],faltas=[],', 'excesos=[],faltas=[],faltasMan=[],')
cambiar('db.collection("faltas").onSnapshot(s=>{faltas=s.docs.map(d=>({id:d.id,...d.data()}));renderOb()},err);',
        'db.collection("faltas").onSnapshot(s=>{faltasMan=s.docs.map(d=>({id:d.id,...d.data()})).filter(f=>!f.exceso_id&&(f.fecha||"")>=EXCESOS_DESDE);armarFaltas();renderOb()},err);')
cambiar('.filter(e=>(e.fecha||"")>=EXCESOS_DESDE);', '.filter(e=>(e.fecha||"")>=EXCESOS_DESDE);armarFaltas();')
cambiar('const EXCESOS_DESDE="2026-11-01";', '''const EXCESOS_DESDE="2026-11-01";
function armarFaltas(){
  const auto=excesos.filter(e=>e.requiere!==false&&e.resultado!=="justificado").map(e=>({id:"ex:"+e.id,fecha:e.fecha,chofer:e.chofer||"Sin chofer",falta:[e.tipo,e.detalle].filter(Boolean).join(": "),avisado:!!e.avisado,avisado_fecha:e.avisado_fecha||"",auto:true}));
  faltas=faltasMan.concat(auto);
}''')
cambiar('try{await db.doc("faltas/"+f.id).update', 'try{await db.doc(f.auto?"excesos/"+f.id.slice(3):"faltas/"+f.id).update')
cambiar('falta:$("fa-d").value.trim(),avisado:false}', 'tipo:$("fa-tipo").value,falta:[$("fa-tipo").value,$("fa-d").value.trim()].filter(Boolean).join(": "),avisado:false}')
cambiar('<input id="fa-d" placeholder="Falta (ej. exceso de velocidad)" aria-label="Falta">', '<select id="fa-tipo" aria-label="Tipo de falta"><option>Multa</option><option>Siniestro</option><option>Documentación</option><option>Checklist</option><option>Otro</option></select><input id="fa-d" placeholder="Detalle (ej. multa en Ruta 34)" aria-label="Detalle">')

# Script de asignar chofer al final
CHAT_JS = (AQUI / "asignar.js").read_text(encoding="utf8")
i = src.rindex("</script>")
src = src[:i] + "\n" + CHAT_JS + "\n" + src[i:]

(AQUI / "app" / "index.html").write_text(src, encoding="utf8")
print("OK", len(src), "bytes")
