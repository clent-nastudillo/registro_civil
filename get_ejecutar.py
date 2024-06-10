import sqlite3

class RegistroCivilDB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = self.connect_to_db()
    
    def connect_to_db(self):
        try:
            connection = sqlite3.connect(self.db_name)
            print(f"Conexión exitosa a la base de datos {self.db_name}")
            return connection
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None
    
    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Conexión cerrada")
    
    def get_defunciones_no_ejecutadas(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM tb_defunciones WHERE ejecutado = 0"
            cursor.execute(query)
            resultados = cursor.fetchall()
            return resultados
        except sqlite3.Error as e:
            print(f"Error al realizar la consulta: {e}")
            return None

def main():
    db = RegistroCivilDB('bd_registro_civil.db')
    
    defunciones_no_ejecutadas = db.get_defunciones_no_ejecutadas()
    if defunciones_no_ejecutadas:
        for defuncion in defunciones_no_ejecutadas:
            print(defuncion)
    
    db.close_connection()

if __name__ == "__main__":
    main()
