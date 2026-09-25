import sqlite3

def conectar():
    return sqlite3.connect("sistema_erp.db")

get_connection = conectar

def init_db():
    conn = conectar()
    cursor = conn.cursor()

    # REPARACIÓN AUTOMÁTICA: Si la tabla clientes no tiene 'id', la reestructura
    cursor.execute("PRAGMA table_info(clientes)")
    columnas = [col[1] for col in cursor.fetchall()]
    
    if "clientes" in [t[0] for t in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]:
        if "id" not in columnas:
            cursor.execute("DROP TABLE clientes")

    # Recrear tabla clientes con la estructura correcta
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo_documento TEXT,
            documento TEXT,
            sexo TEXT,
            telefono TEXT,
            direccion TEXT,
            email TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            codigo TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            nit TEXT,
            telefono TEXT,
            email TEXT,
            direccion TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            concepto TEXT,
            total REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()

crear_tablas = init_db

def total_productos():
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM productos")
        res = cursor.fetchone()[0]
    except Exception:
        res = 0
    conn.close()
    return res

def total_clientes():
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM clientes")
        res = cursor.fetchone()[0]
    except Exception:
        res = 0
    conn.close()
    return res

def total_proveedores():
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM proveedores")
        res = cursor.fetchone()[0]
    except Exception:
        res = 0
    conn.close()
    return res

def total_ventas():
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM ventas")
        res = cursor.fetchone()[0]
    except Exception:
        res = 0
    conn.close()
    return res