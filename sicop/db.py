"""Base de datos SQLite de documentación y vencimientos de fleteros."""
import sqlite3, os, datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'vencimientos.db')

SCHEMA = """
CREATE TABLE IF NOT EXISTS documentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fletero TEXT NOT NULL,
    fletero_cuit TEXT NOT NULL,
    recurso TEXT NOT NULL,          -- Proveedor / Empleado / Vehiculo
    entidad TEXT,                   -- nombre de la persona o del vehículo
    identificador TEXT,             -- CUIT o dominio
    item TEXT NOT NULL,             -- documento/requisito
    fecha_vencimiento TEXT,         -- ISO yyyy-mm-dd (NULL si 'Falta Fecha')
    fecha_texto TEXT,
    motivo TEXT,                    -- A Vencer / Vencido
    actualizado_en TEXT,
    UNIQUE(fletero_cuit, recurso, identificador, item)
);
CREATE TABLE IF NOT EXISTS snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fletero TEXT, fletero_cuit TEXT, fecha_reporte TEXT,
    archivo TEXT, registros INTEGER, importado_en TEXT
);
CREATE TABLE IF NOT EXISTS recordatorios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_key TEXT NOT NULL UNIQUE,   -- fletero_cuit|recurso|identificador|item
    fletero TEXT, item TEXT, entidad TEXT,
    fecha_venc_notificada TEXT,     -- vencimiento vigente cuando se envió el último aviso
    ultimo_envio TEXT,              -- fecha del último mensaje enviado
    veces_enviado INTEGER DEFAULT 0,
    estado TEXT DEFAULT 'pendiente' -- pendiente / avisado / resuelto
);
CREATE TABLE IF NOT EXISTS outbox (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creado_en TEXT, fletero TEXT, doc_key TEXT,
    canal TEXT, destino TEXT, mensaje TEXT,
    estado TEXT DEFAULT 'pendiente'  -- pendiente / enviado / error
);
"""

def connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    return con

def doc_key(r):
    return f"{r['fletero_cuit']}|{r['recurso']}|{r['identificador']}|{r['item']}"

def upsert_documentos(con, registros):
    """Inserta/actualiza documentos. Devuelve lista de cambios de vencimiento (renovaciones)."""
    now = datetime.datetime.now().isoformat(timespec='seconds')
    cambios = []
    for r in registros:
        prev = con.execute(
            "SELECT fecha_vencimiento FROM documentos WHERE fletero_cuit=? AND recurso=? AND identificador=? AND item=?",
            (r['fletero_cuit'], r['recurso'], r['identificador'], r['item'])).fetchone()
        if prev and prev['fecha_vencimiento'] != r['fecha_vencimiento']:
            cambios.append((doc_key(r), prev['fecha_vencimiento'], r['fecha_vencimiento']))
        con.execute("""
            INSERT INTO documentos (fletero,fletero_cuit,recurso,entidad,identificador,item,
                fecha_vencimiento,fecha_texto,motivo,actualizado_en)
            VALUES (:fletero,:fletero_cuit,:recurso,:entidad,:identificador,:item,
                :fecha_vencimiento,:fecha_texto,:motivo,:now)
            ON CONFLICT(fletero_cuit,recurso,identificador,item) DO UPDATE SET
                fecha_vencimiento=excluded.fecha_vencimiento,
                fecha_texto=excluded.fecha_texto,
                motivo=excluded.motivo,
                entidad=excluded.entidad,
                actualizado_en=excluded.actualizado_en
        """, {**r, 'now': now})
    con.commit()
    return cambios

def record_snapshot(con, fletero, cuit, fecha_reporte, archivo, n):
    con.execute("INSERT INTO snapshots (fletero,fletero_cuit,fecha_reporte,archivo,registros,importado_en) VALUES (?,?,?,?,?,?)",
                (fletero, cuit, fecha_reporte, archivo, n, datetime.datetime.now().isoformat(timespec='seconds')))
    con.commit()
