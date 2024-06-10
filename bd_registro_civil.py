import sqlite3

# Conectar a la base de datos (se crea si no existe)
conexion = sqlite3.connect('bd_registro_civil.db')

# Crear un cursor
cursor = conexion.cursor()

# Crear la tabla tb_defunciones
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tb_defunciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rut TEXT NOT NULL,
        ejecutado INTEGER CHECK(ejecutado IN (0, 1)),
        certificado TEXT CHECK(certificado IN ('si', 'no')),
        fecha_inicio DATE,
        fecha_fin DATE
    )
''')

# Confirmar los cambios
conexion.commit()

# Cerrar la conexión
conexion.close()
