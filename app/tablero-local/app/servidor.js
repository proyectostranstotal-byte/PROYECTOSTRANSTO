// Tablero Transtotal local.
// Sirve la página en http://<esta PC>:8090 para cualquiera de la red de la oficina y guarda los datos
// en datos\<colección>\<id>.json (un archivo por documento, el mismo formato que usaba el tablero de claude.ai).
// Lo en vivo (flota, bots, novedades, mapa, ejecutar tareas) se le pide al puente de C:\jornada-bot\panel\puente.js.
// Sin dependencias: solo Node.
const http = require("http");
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { spawn } = require("child_process");

const PUERTO = +process.env.TABLERO_PUERTO || 8090;
const DIR = __dirname;
const DATOS = path.join(DIR, "datos");
const PUENTE = path.join(DIR, "..", "panel", "puente.js");
const NOMBRE = /^[A-Za-z0-9_.~:@+-]{1,120}$/;
const HERRAMIENTAS = new Set(["flota_ahora", "estado_bots", "novedades", "mapa_tile", "ejecutar_tarea"]);
const SOLO_ESTA_PC = new Set(["ejecutar_tarea"]);
const ESTATICOS = { "/": "index.html", "/index.html": "index.html", "/local.js": "local.js", "/basemap.json": "basemap.json", "/leaflet.js": "leaflet.js" };
const TIPOS = { ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".json": "application/json; charset=utf-8" };

// Imágenes de la marca: el sitio de Transtotal no deja usarlas desde otra página, así que el servidor las baja
// una vez (sin Referer) y las guarda en marca\.
const MARCA = {
  "logo-blanco.png": "https://www.transtotal.com.ar/wp-content/uploads/2026/09/transtotal-group-blanco.png",
  "logo-color.png": "https://www.transtotal.com.ar/wp-content/uploads/2026/09/trantotal-group.png",
  "trama.png": "https://www.transtotal.com.ar/wp-content/uploads/2025/07/tramaflecha-1.png",
};
async function imagenMarca(nombre) {
  const f = path.join(DIR, "marca", nombre);
  if (fs.existsSync(f)) return fs.readFileSync(f);
  const r = await fetch(MARCA[nombre], { signal: AbortSignal.timeout(10000) });
  if (!r.ok) throw new Error("HTTP " + r.status);
  const b = Buffer.from(await r.arrayBuffer());
  fs.mkdirSync(path.dirname(f), { recursive: true });
  fs.writeFileSync(f, b);
  return b;
}

// Choferes asignados a mano (el mismo archivo que usan exceso-jornada.js y sin-gps.js para el reporte de jornada).
const BOT = path.join(DIR, "..");
const ASIGNACIONES = path.join(BOT, "asignaciones-manuales.json");
const ESTADO_CHOFERES = path.join(BOT, "estado-choferes.json");
const pad2 = n => String(n).padStart(2, "0");
const fechaHoy = () => { const d = new Date(); return d.getFullYear() + "-" + pad2(d.getMonth() + 1) + "-" + pad2(d.getDate()); };
const sinAcentos = s => String(s || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
function listaChoferes() {
  const e = leer(ESTADO_CHOFERES) || {}, vistos = new Map();
  for (const [code, v] of Object.entries(e)) if (v?.nombre && !vistos.has(sinAcentos(v.nombre))) vistos.set(sinAcentos(v.nombre), { nombre: v.nombre, code });
  return [...vistos.values()].sort((a, b) => a.nombre.localeCompare(b.nombre));
}
// Chofer asignado a mano a una cisterna para hoy y esta hora (respeta los tramos desde/hasta).
function choferManual(asig, cis) {
  const tramos = (asig[fechaHoy()] || {})[cis];
  if (!Array.isArray(tramos)) return null;
  const d = new Date(), ahora = pad2(d.getHours()) + ":" + pad2(d.getMinutes());
  return tramos.find(t => (!t.desde || t.desde <= ahora) && (!t.hasta || ahora < t.hasta)) || null;
}

function guardarAsignaciones(asig) {
  try { fs.copyFileSync(ASIGNACIONES, ASIGNACIONES + ".bak"); } catch { }
  const tmp = ASIGNACIONES + ".tmp";
  fs.writeFileSync(tmp, JSON.stringify(asig, null, 2), "utf8");
  fs.renameSync(tmp, ASIGNACIONES);
}
// Checklist Pre-Viaje (Google Sheet, el mismo que usa sin-gps.js): se relee cada 10 min.
let cacheChecklist = { t: 0, entradas: [] };
async function entradasChecklist() {
  if (Date.now() - cacheChecklist.t < 10 * 60e3) return cacheChecklist.entradas;
  cacheChecklist.t = Date.now();
  try { cacheChecklist.entradas = await require(path.join(BOT, "checklist.js")).loadChecklist(); }
  catch (e) { log("Checklist:", e.message); }
  return cacheChecklist.entradas;
}
// Cisterna en movimiento sin chofer: si hoy hay un Pre-Viaje con la patente del tractor, se le asigna ese chofer
// (como hace sin-gps.js) y queda guardado en asignaciones-manuales.json con fuente "checklist <patente>".
async function asignarPorChecklist(unidades, asig) {
  const sin = unidades.filter(u => !u.chofer && u.tractor && (u.estado === "en_viaje" || u.vel > 5));
  if (!sin.length) return;
  const entradas = await entradasChecklist();
  if (!entradas.length) return;
  const ck = require(path.join(BOT, "checklist.js"));
  const ahora = Math.floor(Date.now() / 1000), d = new Date();
  const desde = Math.floor(new Date(d.getFullYear(), d.getMonth(), d.getDate()).getTime() / 1000);
  const patentes = unidades.map(x => x.tractor).filter(Boolean);
  const lista = listaChoferes(), hoy = fechaHoy();
  let cambio = false;
  for (const u of sin) {
    const pre = ck.choferPorPatente(entradas, u.tractor, desde, ahora, ahora, patentes);
    const ch = pre && lista.find(x => ck.namesMatchFuzzy(x.nombre, pre.chofer));
    if (!ch) continue;
    ((asig[hoy] ||= {})[u.cis] = [{ nombre: ch.nombre, code: ch.code, fuente: "checklist " + pre.patente }]);
    u.chofer = ch.nombre; u.chofer_manual = true; u.chofer_checklist = true;
    cambio = true;
    log("Checklist: asignado", ch.nombre, "a la", u.cis, "(Pre-Viaje con " + pre.patente + ")");
  }
  if (cambio) guardarAsignaciones(asig);
}

const log = (...a) => console.log(new Date().toLocaleString("es-AR"), ...a);

/* ---------- Datos ---------- */
const carpeta = c => path.join(DATOS, c);
const archivo = (c, i) => path.join(DATOS, c, i + ".json");
function leer(f) {
  try { return JSON.parse(fs.readFileSync(f, "utf8").replace(/^\uFEFF/, "")); }
  catch (e) { if (e.code !== "ENOENT") log("No se pudo leer", f, e.message); return undefined; }
}
function leerColeccion(c) {
  let nombres = [];
  try { nombres = fs.readdirSync(carpeta(c)).filter(n => n.endsWith(".json")); } catch { }
  return nombres.sort().map(n => ({ id: n.slice(0, -5), data: leer(path.join(carpeta(c), n)) })).filter(d => d.data !== undefined);
}
function escribir(c, i, data) {
  fs.mkdirSync(carpeta(c), { recursive: true });
  const tmp = archivo(c, i) + "." + process.pid + ".tmp";
  fs.writeFileSync(tmp, JSON.stringify(data, null, 2), "utf8");
  fs.renameSync(tmp, archivo(c, i));
}
const esObjeto = v => v && typeof v === "object" && !Array.isArray(v);
function mezclar(a, b) {
  const r = { ...(esObjeto(a) ? a : {}) };
  for (const [k, v] of Object.entries(b || {})) r[k] = esObjeto(v) && esObjeto(r[k]) ? mezclar(r[k], v) : v;
  return r;
}

/* ---------- Puente (MCP por stdio) ---------- */
let puente = null, sig = 1, buf = "";
const pendientes = new Map();
function arrancarPuente() {
  if (!fs.existsSync(PUENTE)) { log("No encuentro el puente en", PUENTE); return; }
  puente = spawn(process.execPath, [PUENTE], { cwd: path.dirname(PUENTE), stdio: ["pipe", "pipe", "pipe"], windowsHide: true });
  puente.stdout.setEncoding("utf8");
  puente.stdout.on("data", d => {
    buf += d;
    let i;
    while ((i = buf.indexOf("\n")) >= 0) {
      const linea = buf.slice(0, i).trim(); buf = buf.slice(i + 1);
      if (!linea) continue;
      let m; try { m = JSON.parse(linea); } catch { continue; }
      const p = pendientes.get(m.id);
      if (p) { pendientes.delete(m.id); clearTimeout(p.t); p.ok(m); }
    }
  });
  puente.stderr.on("data", d => log(String(d).trim().slice(0, 500)));
  puente.on("exit", c => {
    log("El puente terminó (código " + c + "); se reinicia en 5 s.");
    for (const p of pendientes.values()) { clearTimeout(p.t); p.mal(new Error("el puente se reinició")); }
    pendientes.clear(); puente = null; buf = "";
    setTimeout(arrancarPuente, 5000);
  });
  rpc("initialize", { protocolVersion: "2025-06-18", capabilities: {}, clientInfo: { name: "tablero-local", version: "1.0.0" } }).catch(e => log("initialize:", e.message));
}
function rpc(method, params, ms = 90000) {
  return new Promise((ok, mal) => {
    if (!puente) return mal(Object.assign(new Error("el puente no está corriendo"), { code: "server_not_connected" }));
    const id = sig++;
    const t = setTimeout(() => { pendientes.delete(id); mal(new Error("el puente no respondió a tiempo")); }, ms);
    pendientes.set(id, { ok, mal, t });
    puente.stdin.write(JSON.stringify({ jsonrpc: "2.0", id, method, params }) + "\n");
  });
}

/* ---------- HTTP ---------- */
function responder(res, status, obj, tipo = "application/json; charset=utf-8") {
  res.writeHead(status, { "Content-Type": tipo, "Cache-Control": "no-store" });
  res.end(typeof obj === "string" || Buffer.isBuffer(obj) ? obj : JSON.stringify(obj));
}
function cuerpo(req) {
  return new Promise((ok, mal) => {
    let t = "";
    req.setEncoding("utf8");
    req.on("data", d => { t += d; if (t.length > 2e6) { mal(new Error("pedido demasiado grande")); req.destroy(); } });
    req.on("end", () => { try { ok(t ? JSON.parse(t) : {}); } catch { mal(new Error("JSON inválido")); } });
    req.on("error", mal);
  });
}
const esEstaPC = req => ["127.0.0.1", "::1", "::ffff:127.0.0.1"].includes(req.socket.remoteAddress);

async function manejar(req, res) {
  const url = new URL(req.url, "http://x");
  const partes = url.pathname.split("/").filter(Boolean).map(decodeURIComponent);

  if (req.method === "GET" && ESTATICOS[url.pathname]) {
    const f = path.join(DIR, ESTATICOS[url.pathname]);
    return fs.readFile(f, (e, d) => e ? responder(res, 404, { error: "no existe" }) : responder(res, 200, d, TIPOS[path.extname(f)]));
  }
  if (req.method === "GET" && partes[0] === "marca" && MARCA[partes[1]]) {
    try { res.writeHead(200, { "Content-Type": "image/png", "Cache-Control": "max-age=86400" }); return res.end(await imagenMarca(partes[1])); }
    catch (e) { log("Imagen de marca", partes[1], e.message); return responder(res, 404, { error: "sin imagen" }); }
  }
  // Fondo del mapa: tiles de OpenStreetMap que baja y guarda el puente (herramienta mapa_tile, caché en panel\tiles).
  if (req.method === "GET" && partes[0] === "tile" && partes.length === 4) {
    try {
      const m = await rpc("tools/call", { name: "mapa_tile", arguments: { z: +partes[1], x: +partes[2], y: parseInt(partes[3]) } }, 30000);
      const d = m.result?.structuredContent?.data || "";
      if (m.result?.isError || !d.startsWith("data:image/png;base64,")) return responder(res, 404, { error: "sin tile" });
      res.writeHead(200, { "Content-Type": "image/png", "Cache-Control": "max-age=604800" });
      return res.end(Buffer.from(d.slice(22), "base64"));
    } catch (e) { return responder(res, 503, { error: e.message }); }
  }
  if (partes[0] !== "api") return responder(res, 404, { error: "no existe" });
  // Los POST llevan este encabezado: otra página web no puede mandarlo sin permiso del servidor.
  if (req.method === "POST" && req.headers["x-tablero"] !== "1") return responder(res, 403, { error: "pedido no permitido" });

  const [, tipo, c, i] = partes;
  if ((tipo === "col" || tipo === "doc") && (!NOMBRE.test(c || "") || (tipo === "doc" && !NOMBRE.test(i || ""))))
    return responder(res, 400, { error: "nombre inválido" });

  if (tipo === "col" && req.method === "GET") return responder(res, 200, leerColeccion(c));
  if (tipo === "col" && req.method === "POST") {
    const b = await cuerpo(req);
    const id = crypto.randomBytes(10).toString("hex");
    escribir(c, id, b.data || {});
    return responder(res, 200, { id });
  }
  if (tipo === "doc" && req.method === "GET") {
    const d = leer(archivo(c, i));
    return responder(res, 200, { id: i, exists: d !== undefined, data: d ?? null });
  }
  if (tipo === "doc" && req.method === "POST") {
    const b = await cuerpo(req);
    if (b.op === "delete") { try { fs.unlinkSync(archivo(c, i)); } catch { } return responder(res, 200, { ok: true }); }
    if (b.op === "update") {
      const actual = leer(archivo(c, i));
      if (actual === undefined) return responder(res, 404, { error: "no existe " + c + "/" + i, code: "not_found" });
      escribir(c, i, mezclar(actual, b.data));
      return responder(res, 200, { ok: true });
    }
    escribir(c, i, b.data || {});
    return responder(res, 200, { ok: true });
  }
  if (tipo === "tool" && req.method === "POST") {
    if (!HERRAMIENTAS.has(c)) return responder(res, 404, { error: "herramienta desconocida" });
    if (SOLO_ESTA_PC.has(c) && !esEstaPC(req)) return responder(res, 403, { error: "solo se puede ejecutar desde la PC NDIFABIO", code: "not_granted" });
    const b = await cuerpo(req);
    try {
      const m = await rpc("tools/call", { name: c, arguments: b.args || {} });
      if (m.error) return responder(res, 502, { error: m.error.message, code: "tool_error" });
      if (m.result?.isError) return responder(res, 502, { error: m.result.content?.[0]?.text || "error", code: "tool_error" });
      const payload = m.result?.structuredContent ?? null;
      if (c === "flota_ahora" && payload?.unidades) {
        const asig = leer(ASIGNACIONES) || {};
        for (const u of payload.unidades) {
          if (u.chofer) continue;
          const t = choferManual(asig, u.cis);
          if (t) { u.chofer = t.nombre; u.chofer_manual = true; u.chofer_checklist = /^checklist/.test(t.fuente || ""); }
        }
        try { await asignarPorChecklist(payload.unidades, asig); } catch (e) { log("Checklist:", e.message); }
      }
      return responder(res, 200, { payload });
    } catch (e) { return responder(res, 503, { error: e.message, code: e.code || "server_not_connected" }); }
  }
  if (tipo === "choferes" && req.method === "GET") return responder(res, 200, listaChoferes());
  if (tipo === "asignar" && req.method === "POST") {
    if (!esEstaPC(req)) return responder(res, 403, { error: "La asignación de choferes se hace desde la PC NDIFABIO." });
    const b = await cuerpo(req);
    const cis = String(b.cis || "").trim(), fecha = /^\d{4}-\d{2}-\d{2}$/.test(b.fecha || "") ? b.fecha : fechaHoy();
    const ch = listaChoferes().find(x => sinAcentos(x.nombre) === sinAcentos(b.nombre));
    if (!/^\d{3}$/.test(cis)) return responder(res, 400, { error: "Cisterna inválida" });
    if (!ch) return responder(res, 400, { error: "No encuentro a ese chofer en estado-choferes.json" });
    const hora = /^\d{2}:\d{2}$/.test(b.desde || "") ? b.desde : "";
    const asig = leer(ASIGNACIONES) || {};
    const dia = (asig[fecha] ||= {});
    let tramos = Array.isArray(dia[cis]) ? dia[cis] : [];
    const tramo = { nombre: ch.nombre, code: ch.code, fuente: "tablero" };
    if (hora && tramos.length) {
      // Cambio de chofer a partir de una hora: el tramo anterior termina ahí.
      tramos = tramos.filter(t => !t.desde || t.desde < hora).map(t => (!t.hasta || t.hasta > hora) ? { ...t, hasta: hora } : t);
      tramo.desde = hora;
      tramos.push(tramo);
    } else tramos = [hora ? { ...tramo, desde: hora } : tramo];
    dia[cis] = tramos;
    guardarAsignaciones(asig);
    log("Asignado", ch.nombre, "a la", cis, "el", fecha, hora ? "desde " + hora : "");
    return responder(res, 200, { ok: true, fecha, cis, tramos });
  }
  responder(res, 404, { error: "no existe" });
}

const servidor = http.createServer((req, res) => {
  manejar(req, res).catch(e => { log("Error:", req.method, req.url, e.message); if (!res.headersSent) responder(res, 500, { error: e.message }); });
});
servidor.on("error", e => {
  if (e.code === "EADDRINUSE") { log("El tablero ya está corriendo en el puerto " + PUERTO + "."); process.exit(0); }
  log("Error del servidor:", e.message); process.exit(1);
});
servidor.listen(PUERTO, "0.0.0.0", () => {
  log("Tablero Transtotal en http://localhost:" + PUERTO + " (también desde la red con el nombre de esta PC).");
  arrancarPuente();
});
// Si se actualiza este archivo, el servidor se cierra con código 3 y tablero-loop.bat lo vuelve a arrancar.
fs.watchFile(__filename, { interval: 5000 }, () => {
  log("servidor.js cambió: reinicio.");
  try { puente && puente.kill(); } catch { }
  process.exit(3);
});
// Si se actualiza el puente, se lo cierra y se vuelve a lanzar solo (ver arrancarPuente).
fs.watchFile(PUENTE, { interval: 5000 }, () => { log("puente.js cambió: lo reinicio."); try { puente && puente.kill(); } catch { } });
process.on("uncaughtException", e => log("Error no esperado:", e.stack || e.message));
