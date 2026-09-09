// Prueba segura: manda UN mensaje de prueba al número que vos indiques
// (por ejemplo, tu propio celular), usando la sesión ya vinculada.
// No toca la base ni le escribe a ningún chofer.
//
// Uso:  set TEL_PRUEBA=3412131664 && node probar.js
const readline = require('readline');
const { Client, LocalAuth } = require('whatsapp-web.js');
const { matarBrowser, waPhone } = require('./util');

function pedirTel() {
  const env = (process.env.TEL_PRUEBA || '').replace(/\D/g, '');
  if (env) return Promise.resolve(env);
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise(res => rl.question('Tu numero para la prueba (10 digitos, sin 0 ni 15): ', a => { rl.close(); res(a.replace(/\D/g, '')); }));
}

(async () => {
  const tel = await pedirTel();
  if (tel.length < 8) { console.error('Numero invalido.'); process.exit(1); }
  const client = new Client({
    authStrategy: new LocalAuth({ dataPath: './.wwebjs_auth' }),
    puppeteer: { headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'], protocolTimeout: 600000 }
  });
  const timer = setTimeout(() => { console.error('No conecto en 4 min. Si aparece un QR, corre primero el PASO 1.'); matarBrowser(client); process.exit(1); }, 4 * 60 * 1000);
  client.on('qr', () => { console.error('\nHay que vincular primero: corre el PASO 1.'); matarBrowser(client); process.exit(1); });
  client.on('ready', async () => {
    clearTimeout(timer);
    await new Promise(r => setTimeout(r, 8000));
    try {
      const id = await client.getNumberId(waPhone(tel));
      if (!id) { console.error('Ese numero no tiene WhatsApp activo.'); }
      else { await client.sendMessage(id._serialized, '✅ Prueba del sistema de vencimientos SICOP. Si ves este mensaje, quedó funcionando.'); console.log('\n✓ Mensaje de prueba enviado. Revisa el WhatsApp de ese numero.'); }
    } catch (e) { console.error('Error:', e.message); }
    try { await client.destroy(); } catch {}
    process.exit(0);
  });
  client.initialize().catch(e => { console.error(e.message); matarBrowser(client); process.exit(1); });
})();
