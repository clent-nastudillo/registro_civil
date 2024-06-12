import sqlite3

def connect_to_db(db_name):
    try:
        connection = sqlite3.connect(db_name)
        print(f"Conexión exitosa a la base de datos {db_name}")
        return connection
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def close_connection(connection):
    if connection:
        connection.close()
        print("Conexión cerrada")

def get_defunciones_no_ejecutadas(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM tb_defunciones WHERE ejecutado = 0"
        cursor.execute(query)
        resultados = cursor.fetchall()
        return resultados
    except sqlite3.Error as e:
        print(f"Error al realizar la consulta: {e}")
        return None

def update_row(connection, defuncion, data):
    try:
        cursor = connection.cursor()
        query = "UPDATE tb_defunciones SET ejecutado = ?, certificado = ?, fecha_inicio = ?, fecha_fin = ? WHERE id = ?"
        cursor.execute(query, (data[0], data[1], data[2], data[3], defuncion[0]))
        connection.commit()
        print("DATOS ACTUALIZADOS")
    except sqlite3.Error as e:
        print(f"Error al actualizar la fila: {e}")