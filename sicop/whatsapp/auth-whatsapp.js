// Autenticación única de WhatsApp Web. Escaneá el QR una sola vez.
// La sesión queda en ./.wwebjs_auth y después enviar.js arranca solo.
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const { matarBrowser } = require('./util');

const client = new Client({
  authStrategy: new LocalAuth({ dataPath: './.wwebjs_auth' }),
  puppeteer: { headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'], protocolTimeout: 600000 }
});

const watchdog = setTimeout(() => {
  console.error('\nNo sincronizó en 15 min. Cerrá y volvé a intentar.');
  matarBrowser(client); process.exit(1);
}, 15 * 60 * 1000);

client.on('qr', qr => {
  console.log('\n=== Escaneá con WhatsApp -> Dispositivos vinculados -> Vincular dispositivo ===\n');
  qrcode.generate(qr, { small: true });
  console.log('\nDespués de escanear, ESPERÁ. La primera sincronización puede tardar varios minutos.\n');
});
client.on('loading_screen', (pct, msg) => console.log(`Sincronizando... ${pct}% ${msg || ''}`));
client.on('authenticated', () => console.log('Autenticado. Sincronizando (esperá)...'));
client.on('auth_failure', () => { console.error('Fallo de autenticación.'); process.exit(1); });
client.on('ready', () => {
  clearTimeout(watchdog);
  console.log('\n✓ Listo. Sesión guardada en ./.wwebjs_auth');
  setTimeout(() => client.destroy().finally(() => process.exit(0)), 5000);
});
client.initialize();
