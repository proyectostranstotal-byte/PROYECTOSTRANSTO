# Panel de distribución en vivo

Pestaña "Distribución en vivo" del Tablero Transtotal (`app/tablero.html`): mapa de las cisternas,
novedades del día y botones para ejecutar tareas de la PC.

- `puente.js` (flota_ahora, estado_bots, novedades, mapa_tile, ejecutar_tarea): servidor MCP local (stdio, sin dependencias, Node 18+). Corre en la PC NDIFABIO en
  `C:\jornada-bot\panel\` y lo lanza la app de Claude de escritorio con el nombre `transtotal`.
  La página lo llama como `host:transtotal` (capability `mcp`): solo funciona cuando el dueño abre
  el tablero en esa app. Cada lectura se guarda en la base del tablero (`meta/vivo_flota`,
  `meta/vivo_bots`, `meta/vivo_nov`) para ver la última foto desde el celular.
- `puente-config.json`: URL de Transdat y ruta de las credenciales (no se copian), base de Ibarlucea,
  umbrales y la lista de tareas. Solo las que tienen `"ejecutar": true` se pueden lanzar desde el panel;
  las que mandan mensajes a choferes quedan en `false`.
- `choferes-wialon.js` (vive solo en la PC): exporta `codigosChoferPorCisterna()` →
  `{"534": "<drvr_code>"}`, armado como en `C:\ExcesosVelocidad\exportar_flota.js`.

Registro en la app (claude_desktop_config.json):

```json
{ "mcpServers": { "transtotal": { "command": "node", "args": ["C:\\jornada-bot\\panel\\puente.js"] } } }
```

Prueba en consola: `node C:\jornada-bot\panel\puente.js --probar`.

Estados de unidad: `sin_senal` si el último reporte tiene más de 30 min; `en_base` a 1 km o menos de la base;
`en_viaje` a 5 km/h o más; si no, `detenida`. La posición viene en `o.gps.*` de `/v1/objects/`
(exportar_flota.js la busca en el nivel de arriba y por eso sale vacía).
