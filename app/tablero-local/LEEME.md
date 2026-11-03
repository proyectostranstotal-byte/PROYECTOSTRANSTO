# Tablero Transtotal local (desde el 03/11/2026)

El tablero deja de depender de la app de Claude: corre en la PC NDIFABIO como un servidor Node en `C:\jornada-bot\tablero` (puerto 8090) y se abre desde cualquier PC de la oficina en `http://NDIFABIO:8090`.

- `app/servidor.js`: sirve la página, guarda los datos en `datos\<colección>\<id>.json` y le pide lo en vivo (flota, bots, novedades, mapa, ejecutar tareas) al puente `C:\jornada-bot\panel\puente.js`, que lanza como proceso hijo. "Ejecutar tarea" solo se acepta desde la propia PC.
- `app/local.js`: imita `claude.use("db")` / `claude.use("mcp")` del runtime de claude.ai contra `/api`, así la página es la misma.
- `app/index.html`: se arma con `python build.py <html publicado en claude.ai>` (marca Transtotal de `marca.css`, chat de `chat.html`/`chat.js`, mapa de calles CARTO con el mapa vectorial `basemap.json` de respaldo, Leaflet servido localmente).
- Chat con IA: `/api/ia` llama a la API de Anthropic con los datos del tablero como contexto. La clave va en `C:\jornada-bot\tablero\ia-clave.txt` (la pega el usuario; no se sube al repo).
- Instalación: `instalar-tablero.bat` (pide administrador): acceso directo en Inicio (arranca el servidor sin ventana), acceso directo "Tablero Transtotal" en el escritorio (Chrome `--app`) y regla de firewall para el puerto 8090 en redes privadas y de dominio. Log en `C:\jornada-bot\logs\tablero.log`.
- La tarea "Chequeo bots Transtotal" escribe ahora en los archivos de `datos` (prompt en `prompt-chequeo-bots.txt`).
