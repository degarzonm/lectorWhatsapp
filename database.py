# Contenido del archivo: database.py
import sqlite3
import time

# Nombre de la base de datos
DB_NAME = 'asistente.db'

def inicializar_base_datos():
    """Crea la base de datos y las tablas si no existen."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Crear la tabla 'finanzas' si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS finanzas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE NOT NULL,
            valor REAL NOT NULL, 
            descripcion TEXT,
            categoria TEXT
        );
    ''')
    # Crear la tabla 'mensajes' si no existe, con una columna 'mensaje_preview'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER NOT NULL,
            timestamp DATETIME NOT NULL,
            mensaje TEXT NOT NULL,
            mensaje_preview TEXT NOT NULL,  -- Agregamos esta columna
            tipo TEXT NOT NULL  -- 'user' o 'assistant'
        );
    ''')
    conn.commit()
    conn.close()
    print("Base de datos inicializada.")

def chatsql(sql_statement):
    """Ejecuta la sentencia SQL proporcionada en la base de datos."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(sql_statement)
        if sql_statement.strip().lower().startswith("select"):
            resultados = cursor.fetchall()
            print("Resultados de la consulta:", sql_statement, "\n", resultados)
            conn.close()
            return resultados
        else:
            conn.commit()
            print("Resultados de la consulta:", sql_statement, "\n", "Operación realizada con éxito.")
            conn.close()
            return "Operación realizada con éxito."
    except sqlite3.Error as e:
        conn.close()
        return f"Error al ejecutar la consulta: {e}"

def guardar_mensaje(message_id, timestamp, mensaje, tipo):
    """Guarda un mensaje en la tabla 'mensajes'."""
    mensaje_preview = mensaje[:20]  # Tomamos los primeros 20 caracteres
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO mensajes (message_id, timestamp, mensaje, mensaje_preview, tipo) VALUES (?, ?, ?, ?, ?)',
                   (message_id, timestamp, mensaje, mensaje_preview, tipo))
    conn.commit()
    conn.close()

 

def mensaje_ya_procesado(mensaje_preview, timestamp_actual):
    """Verifica si un mensaje similar ha sido procesado en los últimos 5 minutos."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    tiempo_limite = timestamp_actual - 5 * 60  # 5 minutos en segundos
    cursor.execute('''
        SELECT timestamp FROM mensajes
        WHERE tipo = 'user' AND mensaje_preview = ? AND timestamp >= ?
        ORDER BY timestamp DESC LIMIT 1
    ''', (mensaje_preview, tiempo_limite))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None  # Devuelve True si ya fue procesado

def generar_nuevo_message_id():
    """Genera un nuevo message_id incremental."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(message_id) FROM mensajes')
    resultado = cursor.fetchone()
    conn.close()
    if resultado and resultado[0]:
        return resultado[0] + 1
    else:
        return 1