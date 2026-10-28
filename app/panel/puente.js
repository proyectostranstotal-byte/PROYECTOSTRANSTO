// Puente del Panel de distribución: servidor MCP local (stdio) que corre en la PC NDIFABIO.
// Lo lanza la app de Claude de escritorio; la pestaña "Distribución en vivo" del Tablero lo llama
// con la capability mcp ("host:transtotal"). Sin dependencias: solo Node 18+ (fetch incluido).
//
// Herramientas:
//   flota_ahora      posiciones de Transdat + chofer (iButton) por cisterna        (solo lectura)
//   estado_bots      tareas de Windows y logs de los bots                          (solo lectura)
//   novedades        HR recibidas hoy por WhatsApp                                 (solo lectura)
//   ejecutar_tarea   corre una tarea de la lista "tareas" de puente-config.json con ejecutar:true
//
// La salida estándar es SOLO para el protocolo; los mensajes de diagnóstico van a stderr.

const fs = require("fs");
const path = require("path");
const { execFile, spawn } = require("child_process");

const CONFIG = JSON.parse(fs.readFileSync(path.join(__dirname, "puente-config.json"), "utf8"));
const log = (...a) => console.error("[puente]", ...a);

/* ---------- utilidades ---------- */
const pad = n => String(n).padStart(2, "0");
const hoyISO = (d = new Date()) => d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
const leerJSON = (f, def) => { try { return JSON.parse(fs.readFileSync(f, "utf8").replace(/^\uFEFF/, "")); } catch { return def; } };

function distanciaKm(lat1, lon1, lat2, lon2) {
  const R = 6371, r = x => x * Math.PI / 180;
  const a = Math.sin(r(lat2 - lat1) / 2) ** 2 + Math.cos(r(lat1)) * Math.cos(r(lat2)) * Math.sin(r(lon2 - lon1) / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(a));
}

function ps(script) {
  return new Promise(res => execFile("powershell.exe", ["-NoProfile", "-NonInteractive", "-Command", script],
    { windowsHide: true, timeout: 30000, maxBuffer: 4 << 20 },
    (err, out, errOut) => res({ ok: !err, out: String(out || ""), err: String(errOut || (err && err.message) || "") })));
}

// Último archivo de una carpeta cuyo nombre empieza con un prefijo (los logs son "<prefijo>AAAAMMDD...").
function ultimoLog(carpeta, prefijo) {
  try {
    const fs_ = fs.readdirSync(carpeta).filter(n => n.toLowerCase().startsWith(prefijo.toLowerCase()))
      .map(n => ({ n, f: path.join(carpeta, n), t: fs.statSync(path.join(carpeta, n)).mtimeMs }))
      .sort((a, b) => b.t - a.t);
    return fs_[0] || null;
  } catch { return null; }
}
function colaArchivo(f, lineas = 40) {
  try { return fs.readFileSync(f, "utf8").split(/\r?\n/).filter(Boolean).slice(-lineas); } catch { return []; }
}
const RX_ERROR = /\b(error|fall[óo]|fallid[oa]s? [1-9]|exception|no se pudo|timeout)\b/i;

/* ---------- Transdat ---------- */
let token = null;
async function transdatLogin() {
  const cred = leerJSON(CONFIG.transdat.credenciales, null);
  if (!cred) throw new Error("No se pudo leer el archivo de credenciales de Transdat");
  const r = await fetch(CONFIG.transdat.url + "/auth", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user: cred.user ?? cred.usuario, pass: cred.pass ?? cred.password ?? cred.clave }),
  });
  if (!r.ok) throw new Error("Transdat rechazó el login (" + r.status + ")");
  token = (await r.json()).token;
}
async function transdatObjetos() {
  for (let intento = 0; intento < 2; intento++) {
    if (!token) await transdatLogin();
    const r = await fetch(CONFIG.transdat.url + "/v1/objects/", { headers: { Authorization: "Bearer " + token } });
    if (r.status === 401 || r.status === 403) { token = null; continue; }
    if (!r.ok) throw new Error("Transdat respondió " + r.status);
    return r.json();
  }
  throw new Error("Transdat no aceptó el token");
}

/* ---------- Choferes (iButton) ----------
   El iButton solo viaja por Wialon (SMP). exportar_flota.js ya lo lee con C:\jornada-bot\wialon.js;
   esta función devuelve {"<cisterna>": "<drvr_code>"} y se completa en la PC siguiendo ese script.
   Si falla, la flota sale igual, sin chofer. */
async function codigosChofer() {
  try {
    const w = require(CONFIG.wialon.modulo);
    if (typeof w.codigosChoferPorCisterna === "function") return await w.codigosChoferPorCisterna();
  } catch (e) { log("wialon:", e.message); }
  return {};
}
// drvr_code de Wialon tiene los bytes al revés que las claves de estado-choferes.json.
const invertir = hex => (String(hex).match(/../g) || []).reverse().join("").toUpperCase();
function nombreChofer(codigo) {
  if (!codigo) return "";
  const estado = leerJSON(CONFIG.archivos.estado_choferes, {});
  const lista = leerJSON(CONFIG.archivos.choferes, []);
  for (const k of [String(codigo).toUpperCase(), invertir(codigo)]) {
    if (estado[k]?.nombre) return estado[k].nombre;
    const c = (Array.isArray(lista) ? lista : Object.values(lista)).find(x => String(x.wialon || "").toUpperCase() === k);
    if (c?.nombre) return c.nombre;
  }
  return "";
}

async function flotaAhora() {
  const B = CONFIG.base;
  const [objs, codigos] = await Promise.all([transdatObjetos(), codigosChofer()]);
  const ahora = Date.now();
  const unidades = [];
  for (const o of objs) {
    const nombre = String(o.name || "");
    const cis = (/^\s*(\d{3})/.exec(nombre) || [])[1];
    if (!cis || CONFIG.excluir.includes(cis)) continue;
    const g = o.gps || {};
    const tractor = (nombre.split("/")[1] || o.plate || "").replace(/\s+/g, "").toUpperCase();
    const fecha = g.date ? new Date(g.date * 1000) : null;
    const edadMin = fecha ? Math.max(0, Math.round((ahora - fecha) / 60000)) : null; // la PC va ~3 min atrasada respecto de Transdat
    const dist = g.lat != null ? distanciaKm(g.lat, g.lng, B.lat, B.lng) : null;
    const vel = Math.round(+g.speed || 0);
    let estado = "sin_senal";
    if (edadMin != null && edadMin <= CONFIG.umbrales.sin_senal_min) {
      estado = dist != null && dist <= B.radio_km ? "en_base" : vel >= CONFIG.umbrales.mov_kmh ? "en_viaje" : "detenida";
    }
    unidades.push({
      cis, tractor, lat: g.lat ?? null, lng: g.lng ?? null, vel, rumbo: g.heading ?? null,
      encendido: !!g.engOn, fecha: fecha ? fecha.toISOString() : null, edad_min: edadMin,
      dir: g.dir || "", dist_base_km: dist != null ? Math.round(dist * 10) / 10 : null,
      estado, chofer: nombreChofer(codigos[cis]),
    });
  }
  unidades.sort((a, b) => a.cis.localeCompare(b.cis));
  return { generado: new Date().toISOString(), base: B, unidades };
}

/* ---------- Bots ---------- */
async function tareasWindows() {
  const nombres = CONFIG.tareas.filter(t => t.tipo === "windows").map(t => t.tarea);
  if (!nombres.length) return {};
  const lista = nombres.map(n => "'" + n.replace(/'/g, "''") + "'").join(",");
  const r = await ps(
    `$n=@(${lista});$o=foreach($t in Get-ScheduledTask -TaskPath '\\' -ErrorAction SilentlyContinue){if($n -contains $t.TaskName){` +
    `$i=$t|Get-ScheduledTaskInfo;[pscustomobject]@{n=$t.TaskName;s=[string]$t.State;r=$i.LastTaskResult;` +
    `u=if($i.LastRunTime -and $i.LastRunTime.Year -gt 2000){$i.LastRunTime.ToString('o')}else{''};` +
    `p=if($i.NextRunTime){$i.NextRunTime.ToString('o')}else{''}}}};ConvertTo-Json @($o) -Compress`);
  if (!r.ok) { log("tareas:", r.err); return {}; }
  const out = {};
  for (const t of [].concat(JSON.parse(r.out || "[]"))) out[t.n] = t;
  return out;
}

async function estadoBots() {
  const win = await tareasWindows();
  const items = [];
  for (const t of CONFIG.tareas) {
    const it = { id: t.id, nombre: t.nombre, ejecutar: !!t.ejecutar, aviso: t.aviso || "", estado: "ok", detalle: "", ultima: "", proxima: "" };
    if (t.tipo === "windows") {
      const w = win[t.tarea];
      if (!w) { it.estado = "warn"; it.detalle = "No encuentro la tarea en Windows"; }
      else {
        it.ultima = w.u; it.proxima = w.p;
        if (w.s === "Disabled") { it.estado = "warn"; it.detalle = "Tarea deshabilitada"; }
        else if (w.s === "Running") { it.estado = "ok"; it.detalle = "Corriendo ahora"; it.corriendo = true; }
        else if (w.r !== 0 && w.r !== 267011) { it.estado = "fail"; it.detalle = "Última corrida terminó con error (código " + w.r + ")"; }
      }
    }
    if (t.log) {
      const l = ultimoLog(t.log.carpeta, t.log.prefijo);
      if (!l) { if (it.estado === "ok") { it.estado = "warn"; it.detalle = "Sin log"; } }
      else {
        const cola = colaArchivo(l.f, 15);
        it.log = { archivo: l.n, modificado: new Date(l.t).toISOString(), ultimas: cola.slice(-5) };
        if (!it.ultima) it.ultima = it.log.modificado;
        const horas = (Date.now() - l.t) / 36e5;
        if (t.log.max_horas && horas > t.log.max_horas && it.estado === "ok") { it.estado = "warn"; it.detalle = "Sin corridas hace " + Math.round(horas) + " h"; }
        const err = cola.find(x => RX_ERROR.test(x));
        if (err && it.estado === "ok") { it.estado = "warn"; it.detalle = err.slice(0, 160); }
      }
    }
    if (!it.detalle) it.detalle = it.ultima ? "OK" : "";
    items.push(it);
  }
  return { chequeado: new Date().toISOString(), items };
}

/* ---------- Novedades ---------- */
async function novedades() {
  const hoy = hoyISO(), out = [];
  const indice = leerJSON(CONFIG.archivos.indice_hr, []);
  for (const h of Array.isArray(indice) ? indice : []) {
    // "fecha" viene en UTC (…Z): se compara con el día local para no pasar HR de la noche al día siguiente.
    const d = new Date(h.fecha);
    if (isNaN(d) || hoyISO(d) !== hoy) continue;
    if ((h.tipo_doc || h.tipo) !== "hr") continue;
    const destino = /^duplicado:/i.test(h.destino || "") ? "" : h.destino;
    out.push({
      hora: d.toISOString(), tipo: "hr",
      texto: "HR " + (h.hr || "s/n") + (h.semi ? " · semi " + h.semi : "") + (destino ? " · " + destino : "") +
        (h.km_recorridos ? " · " + h.km_recorridos + " km" : "") + (h.nombre_contacto ? " · de " + h.nombre_contacto : ""),
      procesado: !!h.procesado, obs: h.observaciones || "",
    });
  }
  return { generado: new Date().toISOString(), items: out };
}

/* ---------- Ejecutar ---------- */
const enCurso = new Set();
async function ejecutarTarea({ id }) {
  const t = CONFIG.tareas.find(x => x.id === id);
  if (!t || !t.ejecutar) throw new Error("Esa tarea no está habilitada para ejecutarse desde el panel");
  if (enCurso.has(id)) return { id, lanzada: false, detalle: "Ya se está ejecutando" };
  if (t.tipo === "windows") {
    const r = await ps(`Start-ScheduledTask -TaskPath '\\' -TaskName '${t.tarea.replace(/'/g, "''")}'`);
    if (!r.ok) throw new Error("Windows no pudo lanzar la tarea: " + r.err.slice(0, 200));
    return { id, lanzada: true, detalle: "Lanzada en Windows a las " + new Date().toLocaleTimeString("es-AR") };
  }
  if (t.tipo === "comando") {
    enCurso.add(id);
    const p = spawn(t.comando, t.args || [], { cwd: t.cwd, windowsHide: true, stdio: "ignore", detached: true });
    p.on("exit", () => enCurso.delete(id));
    p.on("error", e => { enCurso.delete(id); log(id, e.message); });
    p.unref();
    return { id, lanzada: true, detalle: "Lanzada a las " + new Date().toLocaleTimeString("es-AR") };
  }
  throw new Error("Tipo de tarea desconocido");
}

/* ---------- MCP (JSON-RPC 2.0 por stdio, un mensaje por línea) ---------- */
const RO = { readOnlyHint: true, openWorldHint: false };
const TOOLS = [
  { name: "flota_ahora", description: "Posición actual de cada cisterna (Transdat), estado y chofer.", inputSchema: { type: "object", properties: {} }, annotations: RO, run: flotaAhora },
  { name: "estado_bots", description: "Estado de las tareas programadas y los bots de la PC.", inputSchema: { type: "object", properties: {} }, annotations: RO, run: estadoBots },
  { name: "novedades", description: "Novedades del día: HR recibidas por WhatsApp.", inputSchema: { type: "object", properties: {} }, annotations: RO, run: novedades },
  { name: "ejecutar_tarea", description: "Ejecuta ahora una tarea habilitada en puente-config.json.", inputSchema: { type: "object", properties: { id: { type: "string" } }, required: ["id"] }, annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: false, openWorldHint: false }, run: ejecutarTarea },
];

const enviar = m => process.stdout.write(JSON.stringify(m) + "\n");
async function manejar(m) {
  const { id, method, params } = m;
  if (id === undefined) return; // notificaciones
  try {
    if (method === "initialize") return enviar({ jsonrpc: "2.0", id, result: { protocolVersion: params?.protocolVersion || "2025-06-18", capabilities: { tools: {} }, serverInfo: { name: "transtotal", version: "1.0.0" } } });
    if (method === "ping") return enviar({ jsonrpc: "2.0", id, result: {} });
    if (method === "tools/list") return enviar({ jsonrpc: "2.0", id, result: { tools: TOOLS.map(({ run, ...t }) => t) } });
    if (method === "tools/call") {
      const t = TOOLS.find(x => x.name === params?.name);
      if (!t) return enviar({ jsonrpc: "2.0", id, error: { code: -32602, message: "Herramienta desconocida" } });
      try {
        const data = await t.run(params.arguments || {});
        return enviar({ jsonrpc: "2.0", id, result: { content: [{ type: "text", text: JSON.stringify(data) }], structuredContent: data } });
      } catch (e) {
        log(t.name, e.message);
        return enviar({ jsonrpc: "2.0", id, result: { content: [{ type: "text", text: e.message }], isError: true } });
      }
    }
    enviar({ jsonrpc: "2.0", id, error: { code: -32601, message: "Método no soportado: " + method } });
  } catch (e) {
    enviar({ jsonrpc: "2.0", id, error: { code: -32603, message: e.message } });
  }
}

let buf = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", d => {
  buf += d;
  let i;
  while ((i = buf.indexOf("\n")) >= 0) {
    const linea = buf.slice(0, i).trim(); buf = buf.slice(i + 1);
    if (!linea) continue;
    try { manejar(JSON.parse(linea)); } catch (e) { log("mensaje inválido:", e.message); }
  }
});

// Prueba desde la consola: node puente.js --probar
if (process.argv.includes("--probar")) {
  (async () => {
    for (const t of TOOLS.filter(t => t.annotations.readOnlyHint)) {
      try { const r = await t.run({}); console.error("== " + t.name + "\n" + JSON.stringify(r, null, 1).slice(0, 3000)); }
      catch (e) { console.error("== " + t.name + " ERROR: " + e.message); }
    }
    process.exit(0);
  })();
}
