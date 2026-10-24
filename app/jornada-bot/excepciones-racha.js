// Excepciones manuales a la racha de días corridos sin descanso.
//
// Uso en rachas.js (o donde se calcule "días acumulados" por chofer):
//
//   const { aplicarExcepcion } = require('./excepciones-racha');
//   dias = aplicarExcepcion(nombreChofer, dias);          // fecha = hoy
//   dias = aplicarExcepcion(nombreChofer, dias, fecha);   // fecha: Date o 'YYYY-MM-DD'
//
// Devuelve el menor valor entre lo que calculó el bot y los días transcurridos desde
// 'inicioRacha' (inclusive). Así la excepción nunca sube la cuenta y deja de tener efecto
// sola cuando el chofer hace un descanso real y el bot vuelve a contar desde 1.
//
// Las excepciones se leen de excepciones-racha.json, en la misma carpeta.

const fs = require('fs');
const path = require('path');

const ARCHIVO = path.join(__dirname, 'excepciones-racha.json');

function normalizar(nombre) {
  return String(nombre || '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .split(/[\s,]+/)
    .filter(Boolean)
    .sort()
    .join(' ');
}

function aFechaLocal(valor) {
  if (valor instanceof Date) {
    return new Date(valor.getFullYear(), valor.getMonth(), valor.getDate());
  }
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(String(valor || ''));
  if (!m) return null;
  return new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3]));
}

function diasEntre(desde, hasta) {
  const MS_DIA = 24 * 60 * 60 * 1000;
  return Math.round((hasta - desde) / MS_DIA);
}

function cargarExcepciones() {
  try {
    const data = JSON.parse(fs.readFileSync(ARCHIVO, 'utf8'));
    return Array.isArray(data.excepciones) ? data.excepciones : [];
  } catch (e) {
    if (e.code !== 'ENOENT') {
      console.warn(`[excepciones-racha] no se pudo leer ${ARCHIVO}: ${e.message}`);
    }
    return [];
  }
}

function buscarExcepcion(nombreChofer, fecha) {
  const hoy = aFechaLocal(fecha || new Date());
  const clave = normalizar(nombreChofer);
  if (!hoy || !clave) return null;
  for (const ex of cargarExcepciones()) {
    if (normalizar(ex.chofer) !== clave) continue;
    const inicio = aFechaLocal(ex.inicioRacha);
    if (!inicio || inicio > hoy) continue;
    const vence = ex.vence ? aFechaLocal(ex.vence) : null;
    if (vence && hoy > vence) continue;
    return { ...ex, diasDesdeInicio: diasEntre(inicio, hoy) + 1 };
  }
  return null;
}

function aplicarExcepcion(nombreChofer, diasCalculados, fecha) {
  const ex = buscarExcepcion(nombreChofer, fecha);
  if (!ex) return diasCalculados;
  const calc = Number(diasCalculados);
  const dias = Number.isFinite(calc) ? Math.min(calc, ex.diasDesdeInicio) : ex.diasDesdeInicio;
  if (dias !== calc) {
    console.log(`[excepciones-racha] ${nombreChofer}: ${calc} -> ${dias} días (desde ${ex.inicioRacha}${ex.motivo ? ': ' + ex.motivo : ''})`);
  }
  return dias;
}

module.exports = { aplicarExcepcion, buscarExcepcion, normalizar };
