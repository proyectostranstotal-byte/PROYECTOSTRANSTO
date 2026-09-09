// Utilidades compartidas.
const cp = require('child_process');

// Matar el Chrome de Puppeteer (si no, queda con la sesión bloqueada).
function matarBrowser(client) {
  try {
    const pid = client.pupBrowser?.process()?.pid;
    if (!pid) return;
    if (process.platform === 'win32') cp.execSync(`taskkill /F /T /PID ${pid}`, { stdio: 'ignore' });
    else process.kill(pid, 'SIGKILL');
  } catch {}
}

// Número argentino móvil: 549 + 10 dígitos (sin 0, sin 15), sufijo @c.us.
function waPhone(tel) {
  const d = String(tel || '').replace(/\D/g, '');
  return `549${d}@c.us`;
}

module.exports = { matarBrowser, waPhone };
