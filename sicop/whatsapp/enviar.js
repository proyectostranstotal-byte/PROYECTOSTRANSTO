// Envía los recordatorios de vencimiento a los choferes por WhatsApp Web.
// Lee la cola generada por Python (data/cola_whatsapp.json) y escribe el
// resultado (data/resultado_whatsapp.json) para que Python marque los enviados.
//
// Uso:
//   node enviar.js                     -> envío real
//   CHOFER_TEST=costanzo node enviar.js -> modo prueba (solo los que matcheen)
//
// Blindaje (whatsapp-web.js se cuelga seguido): timeout de 'ready' por intento,
// hasta 5 reintentos con cliente nuevo, watchdog global, y 3s entre mensajes.
const fs = require('fs');
const path = require('path');
const { Client, LocalAuth } = require('whatsapp-web.js');
const { matarBrowser, waPhone } = require('./util');

const DATA = path.join(__dirname, '..', 'data');
const COLA = path.join(DATA, 'cola_whatsapp.json');
const RESULTADO = path.join(DATA, 'resultado_whatsapp.json');
const ESPACIADO_MS = 3000;

const filtro = (process.env.CHOFER_TEST || '').trim().toLowerCase();
if (filtro) console.log(`** MODO PRUEBA: solo choferes que matcheen "${filtro}" **`);

if (!fs.existsSync(COLA)) { console.error('No existe ' + COLA + '. Corré: python3 -m sicop.generar_cola'); process.exit(1); }
const cola = JSON.parse(fs.readFileSync(COLA, 'utf8'));
let envios = (cola.envios || []).filter(e => e.telefono && String(e.telefono).replace(/\D/g, '').length >= 8);
const sinTelefono = (cola.envios || []).filter(e => !e.telefono);
if (filtro) envios = envios.filter(e => (e.nombre || '').toLowerCase().includes(filtro));

if (sinTelefono.length) console.log(`  (${sinTelefono.length} choferes sin teléfono cargado, se omiten)`);
if (!envios.length) { console.log('Nada para enviar.'); writeResultado([], []); process.exit(0); }

const enviados = [];   // doc_keys entregados
const fallidos = [];   // { nombre, telefono, doc_keys, motivo, texto }
let sesionInvalida = false;

// Los choferes sin teléfono también se reportan como fallidos (para el aviso por mail).
for (const e of sinTelefono) {
  fallidos.push({ nombre: e.nombre, telefono: '', doc_keys: e.doc_keys, motivo: 'sin teléfono cargado', texto: e.texto });
}

function writeResultado(ok, fail) {
  // Reconciliar: cualquier envío que tenía teléfono y no se entregó ni figura como
  // fallido puntual, se marca como no enviado (p.ej. WhatsApp nunca conectó).
  const okSet = new Set(ok);
  const yaFallado = new Set(fail.flatMap(f => f.doc_keys || []));
  for (const e of envios) {
    const pendientes = (e.doc_keys || []).filter(k => !okSet.has(k) && !yaFallado.has(k));
    if (pendientes.length) {
      fail.push({ nombre: e.nombre, telefono: e.telefono, doc_keys: pendientes,
                  motivo: 'no se pudo conectar a WhatsApp', texto: e.texto });
    }
  }
  fs.writeFileSync(RESULTADO, JSON.stringify({ generado: new Date().toISOString(), enviados: ok, fallidos: fail }, null, 2));
}

async function enviar(client) {
  for (const e of envios) {
    try {
      const id = await client.getNumberId(waPhone(e.telefono));
      if (!id) { console.log(`  ⚠ ${e.nombre}: el número no tiene WhatsApp activo`); fallidos.push({ nombre: e.nombre, telefono: e.telefono, doc_keys: e.doc_keys, motivo: 'el número no tiene WhatsApp activo', texto: e.texto }); continue; }
      await client.sendMessage(id._serialized, e.texto);
      console.log(`  ✓ ${e.nombre}`);
      enviados.push(...(e.doc_keys || []));
    } catch (err) {
      console.log(`  ✗ ${e.nombre}: ${err.message}`);
      fallidos.push({ nombre: e.nombre, telefono: e.telefono, doc_keys: e.doc_keys, motivo: err.message, texto: e.texto });
    }
    await new Promise(r => setTimeout(r, ESPACIADO_MS));
  }
}

function intentar(intento) {
  return new Promise(resolve => {
    const client = new Client({
      authStrategy: new LocalAuth({ dataPath: './.wwebjs_auth' }),
      puppeteer: { headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'], protocolTimeout: 600000 }
    });
    let resuelto = false;
    const finish = ok => { if (resuelto) return; resuelto = true; clearTimeout(readyTimer); resolve(ok); };
    const readyTimer = setTimeout(() => { console.error(`Intento ${intento}: no llegó a 'ready' en 4 min. Reintento.`); matarBrowser(client); finish(false); }, 4 * 60 * 1000);

    client.on('qr', () => { console.error('Sesión perdida: corré  npm run auth  (auth-whatsapp.js).'); sesionInvalida = true; matarBrowser(client); finish(false); });
    client.on('auth_failure', () => { sesionInvalida = true; matarBrowser(client); finish(false); });
    client.on('ready', async () => {
      clearTimeout(readyTimer);
      await new Promise(r => setTimeout(r, 10000)); // si mandás apenas llega 'ready' se pierden mensajes
      try { await enviar(client); } catch (e) { console.error(e.message); }
      try { await client.destroy(); } catch {}
      finish(true);
    });
    client.initialize().catch(e => { console.error(e.message); matarBrowser(client); finish(false); });
  });
}

async function main() {
  setTimeout(() => { console.error('Watchdog global: salida forzada.'); writeResultado(enviados, fallidos); process.exit(1); }, 28 * 60 * 1000).unref();
  for (let intento = 1; intento <= 5; intento++) {
    if (await intentar(intento)) { writeResultado(enviados, fallidos); console.log(`\nListo. Enviados: ${enviados.length} docs, fallidos: ${fallidos.length}.`); process.exit(0); }
    if (sesionInvalida) { console.error('Re-autenticá con  npm run auth.'); writeResultado(enviados, fallidos); process.exit(1); }
    await new Promise(r => setTimeout(r, 5000));
  }
  writeResultado(enviados, fallidos); process.exit(1);
}
main();
