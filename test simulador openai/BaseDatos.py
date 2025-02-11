import sqlite3

class BaseDatos:
    def __init__(self):
        """Inicializa la base de datos y crea la tabla si no existe."""
        self.conn = sqlite3.connect("interacciones.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS interacciones
                               (id INTEGER PRIMARY KEY, prompt TEXT, respuesta TEXT)''')
        self.conn.commit()

    def guardar_interaccion(self, prompt, respuesta):
        """Guarda la interacción del usuario en la base de datos."""
        self.cursor.execute("INSERT INTO interacciones (prompt, respuesta) VALUES (?, ?)", (prompt, respuesta))
        self.conn.commit()

    def ver_historial(self):
        """Muestra todas las interacciones almacenadas en la base de datos."""
        self.cursor.execute("SELECT * FROM interacciones")
        interacciones = self.cursor.fetchall()

        if interacciones:
            print("\n📜 Historial de Conversaciones:")
            for id_, prompt, respuesta in interacciones:
                print(f"\n🗣️ Tú: {prompt}\n🤖 Amigo: {respuesta}\n{'-' * 40}")
        else:
            print("\n🔍 No hay historial de conversaciones aún.")

    def cerrar_conexion(self):
        """Cierra la conexión con la base de datos."""
        self.conn.close()

if __name__ == "__main__":
    db = BaseDatos()
    db.ver_historial()
    db.cerrar_conexion()
