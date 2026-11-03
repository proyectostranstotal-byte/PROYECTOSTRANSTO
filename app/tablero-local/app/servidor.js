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
const CLAVE_IA = path.join(DIR, "ia-clave.txt");
const MODELO_IA = process.env.TABLERO_MODELO || "claude-sonnet-5-5";
const NOMBRE = /^[A-Za-z0-9_.~:@+-]{1,120}$/;
const HERRAMIENTAS = new Set(["flota_ahora", "estado_bots", "novedades", "mapa_tile", "ejecutar_tarea"]);
const SOLO_ESTA_PC = new Set(["ejecutar_tarea"]);
const ESTATICOS = { "/": "index.html", "/index.html": "index.html", "/local.js": "local.js", "/basemap.json": "basemap.json", "/leaflet.js": "leaflet.js" };
const TIPOS = { ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".json": "application/json; charset=utf-8" };

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

/* ---------- IA ---------- */
function claveIA() {
  if (process.env.ANTHROPIC_API_KEY) return process.env.ANTHROPIC_API_KEY.trim();
  try { return fs.readFileSync(CLAVE_IA, "utf8").trim(); } catch { return ""; }
}
function contextoIA() {
  const hoy = new Date();
  const mes = hoy.getFullYear() + "-" + String(hoy.getMonth() + 1).padStart(2, "0");
  const col = c => leerColeccion(c).map(d => ({ id: d.id, ...d.data }));
  const doc = (c, i) => leer(archivo(c, i)) || null;
  const ctx = {
    hoy: hoy.toLocaleString("es-AR"),
    mes_actual: doc("mes", mes),
    meses: leerColeccion("mes").map(d => ({ mes: d.id, ...d.data })),
    excesos: col("excesos"),
    faltas: col("faltas"),
    tareas_abiertas: col("tareas").filter(t => t.estado !== "hecha"),
    areas: col("areas"),
    auditorias_sugeridas: doc("meta", "auditorias"),
    salud_bots: doc("meta", "salud"),
    flota_en_vivo: doc("meta", "vivo_flota"),
    bots_en_vivo: doc("meta", "vivo_bots"),
    novedades: doc("meta", "vivo_nov"),
  };
  return JSON.stringify(ctx).slice(0, 400000);
}
const SISTEMA = `Sos el asistente del Tablero Transtotal, el panel operativo de Nico (Transtotal Group, transporte de gases en cisternas para Air Liquide, base en Ibarlucea, Santa Fe).
Respondé en español rioplatense, breve y directo, usando solo los datos del tablero que vienen abajo. Si un dato no está, decilo y no lo inventes.
Contexto de trabajo:
- Obligaciones del mes: auditar 4 a 5 unidades (vencen a los 2 meses), comentar cada exceso de jornada o manejo, avisar a cada chofer sus faltas (programa de incentivos desde noviembre 2026: Excelente >=300 puntos $200.000, Muy Bueno 250-299 $100.000, tolerancia cero en desvíos), cargar m3/kg de las HR en ControlPesos, cargar las HR en Transoft, responder el reporte de seguridad vial de Air Liquide y controlar la facturación de Air Liquide (no factura él: controla, actualiza el Excel y lo pasa a facturación).
- Excesos con requiere=false no necesitan justificación (el campo motivo dice por qué).
- Distribuidores de Air Liquide: LOX = oxígeno, LIN = nitrógeno.
- Por ahora no se les avisa a los choferes sus faltas.
Fechas en formato DD/MM. Si te piden una lista, usá viñetas cortas.`;
async function preguntarIA(mensajes) {
  const clave = claveIA();
  if (!clave) throw Object.assign(new Error("Falta la clave de la API de Anthropic: pegala en C:\\jornada-bot\\tablero\\ia-clave.txt y reiniciá el tablero."), { status: 503 });
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "content-type": "application/json", "x-api-key": clave, "anthropic-version": "2023-06-01" },
    body: JSON.stringify({
      model: MODELO_IA, max_tokens: 1500,
      system: [{ type: "text", text: SISTEMA }, { type: "text", text: "Datos del tablero (JSON):\n" + contextoIA() }],
      messages: mensajes.slice(-12).map(m => ({ role: m.role === "assistant" ? "assistant" : "user", content: String(m.content || "").slice(0, 4000) })),
    }),
  });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw Object.assign(new Error("La API respondió " + r.status + ": " + (j.error?.message || "error")), { status: 502 });
  return (j.content || []).filter(b => b.type === "text").map(b => b.text).join("\n").trim();
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
      return responder(res, 200, { payload: m.result?.structuredContent ?? null });
    } catch (e) { return responder(res, 503, { error: e.message, code: e.code || "server_not_connected" }); }
  }
  if (tipo === "ia" && req.method === "GET") return responder(res, 200, { activa: !!claveIA() });
  if (tipo === "ia" && req.method === "POST") {
    const b = await cuerpo(req);
    try { return responder(res, 200, { respuesta: await preguntarIA(Array.isArray(b.mensajes) ? b.mensajes : []) }); }
    catch (e) { log("IA:", e.message); return responder(res, e.status || 500, { error: e.message }); }
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
process.on("uncaughtException", e => log("Error no esperado:", e.stack || e.message));
