import sqlite3
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
     # Crear la tabla 'mensajes' si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            mensaje TEXT NOT NULL
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
            print("resultados de la consulta:", sql_statement, "\n", resultados)
            conn.close()
            return resultados
        else:
            print("resultados de la consulta:", sql_statement, "\n", "Operación realizada con éxito.")
            conn.commit()
            conn.close()
            return "Operación realizada con éxito."
    except sqlite3.Error as e:
        print
        conn.close()
        return f"Error al ejecutar la consulta: {e}"
     