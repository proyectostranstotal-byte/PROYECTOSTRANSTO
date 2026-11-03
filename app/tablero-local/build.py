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
    <picture class="tt-logo"><source media="(prefers-color-scheme: dark)" srcset="https://www.transtotal.com.ar/wp-content/uploads/2026/09/transtotal-group-blanco.png"><img src="https://www.transtotal.com.ar/wp-content/uploads/2026/09/transtotal-group-blanco.png" alt="Transtotal Group" onerror="this.closest('picture').hidden=true"></picture>
    <div class="tt-tit"><span class="tt-etq">Panel operativo · Air Liquide</span><h1>Tablero Transtotal</h1><span class="fecha" id="fecha"></span></div>
  </header>''')

# Chat con la IA, después de las alertas
CHAT_HTML = (AQUI / "chat.html").read_text(encoding="utf8")
cambiar('''  <section aria-labelledby="vivo-h">''', CHAT_HTML + '''\n  <section aria-labelledby="vivo-h">''')

# Mapa: fondo de calles (CARTO/OpenStreetMap) en la app local; si no carga, el mapa vectorial de siempre.
cambiar('''function dibujarBase(){
  if(!mapa||!base)return;''', '''let tilesOk=null,capaTiles=null;
function dibujarBase(){
  if(!mapa||!base||(window.TABLERO_LOCAL&&tilesOk!==false))return;''')
cambiar('''  capaU=L.layerGroup().addTo(mapa);
  dibujarBase();''', '''  capaU=L.layerGroup().addTo(mapa);
  if(window.TABLERO_LOCAL){
    const oscuro=matchMedia("(prefers-color-scheme: dark)").matches;
    let fallas=0;
    mapa.setMaxZoom(17);
    capaTiles=L.tileLayer("https://{s}.basemaps.cartocdn.com/rastertiles/"+(oscuro?"dark_all":"voyager")+"/{z}/{x}/{y}{r}.png",{subdomains:"abcd",maxZoom:19,attribution:"© OpenStreetMap · © CARTO"}).addTo(mapa);
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

# Script del chat al final
CHAT_JS = (AQUI / "chat.js").read_text(encoding="utf8")
i = src.rindex("</script>")
src = src[:i] + "\n" + CHAT_JS + "\n" + src[i:]

(AQUI / "app" / "index.html").write_text(src, encoding="utf8")
print("OK", len(src), "bytes")
