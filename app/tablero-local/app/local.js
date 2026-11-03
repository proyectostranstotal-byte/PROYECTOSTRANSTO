// Reemplaza al runtime de claude.ai cuando el tablero se abre desde el servidor local:
// misma interfaz (claude.use("db") / claude.use("mcp")), pero contra /api de servidor.js.
(function () {
  if (window.claude) return;
  window.TABLERO_LOCAL = true;
  const enc = encodeURIComponent;
  async function api(url, opciones) {
    const r = await fetch(url, opciones);
    const j = await r.json().catch(() => ({}));
    if (!r.ok) { const e = new Error(j.error || r.statusText); e.code = j.code || ""; throw e; }
    return j;
  }
  const post = (url, cuerpo) => api(url, { method: "POST", headers: { "Content-Type": "application/json", "X-Tablero": "1" }, body: JSON.stringify(cuerpo) });

  // onSnapshot: se relee cada 5 s (y al volver a la ventana); solo avisa si algo cambió.
  const subs = new Set();
  async function leerSub(s) {
    try { const j = await api(s.url); const t = JSON.stringify(j); if (t !== s.ultimo) { s.ultimo = t; s.cb(s.armar(j)); } }
    catch (e) { s.err && s.err(e); }
  }
  const refrescar = () => subs.forEach(leerSub);
  setInterval(() => { if (!document.hidden) refrescar(); }, 5000);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) refrescar(); });
  function suscribir(url, armar, cb, err) { const s = { url, armar, cb, err, ultimo: null }; subs.add(s); leerSub(s); return () => subs.delete(s); }

  const fotoDoc = j => ({ id: j.id, exists: !!j.exists, data: () => j.data });
  const fotoCol = l => ({ docs: l.map(d => ({ id: d.id, exists: true, data: () => d.data })), size: l.length, empty: !l.length });
  function doc(ruta) {
    const [c, i] = ruta.split("/"), url = "/api/doc/" + enc(c) + "/" + enc(i);
    return {
      id: i,
      get: () => api(url).then(fotoDoc),
      onSnapshot: (cb, err) => suscribir(url, fotoDoc, cb, err),
      set: d => post(url, { op: "set", data: d }).then(refrescar),
      update: d => post(url, { op: "update", data: d }).then(refrescar),
      delete: () => post(url, { op: "delete" }).then(refrescar),
    };
  }
  function collection(c) {
    const url = "/api/col/" + enc(c);
    return {
      get: () => api(url).then(fotoCol),
      onSnapshot: (cb, err) => suscribir(url, fotoCol, cb, err),
      add: d => post(url, { data: d }).then(j => { refrescar(); return { id: j.id }; }),
      doc: i => doc(c + "/" + i),
    };
  }
  const db = { doc, collection };
  const mcp = {
    callTool: (host, nombre, args) => post("/api/tool/" + enc(nombre), { args: args || {} }).then(j => ({ payload: j.payload })),
    invalidate: async () => { },
  };
  const ia = {
    estado: () => api("/api/ia"),
    preguntar: mensajes => post("/api/ia", { mensajes }).then(j => j.respuesta),
  };
  window.claude = { use: async n => n === "db" ? db : n === "mcp" ? mcp : n === "ia" ? ia : null };
})();
