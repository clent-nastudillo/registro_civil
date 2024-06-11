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

# def main():
#     db_name = 'bd_registro_civil.db'
#     connection = connect_to_db(db_name)
    
#     if connection:
#         defunciones_no_ejecutadas = get_defunciones_no_ejecutadas(connection)
#         if defunciones_no_ejecutadas:
#             for defuncion in defunciones_no_ejecutadas:
#                 print(defuncion)
        
#         close_connection(connection)

# if __name__ == "__main__":
#     main()
