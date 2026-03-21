from database.connection import managed_connection
from models.cliente import Cliente

class ClienteRepository:
    """Repositorio que maneja la persistencia de clientes en PostgreSQL."""

    def guardar(self, cliente, connection=None):
        """Guarda o actualiza un cliente en la base de datos."""
        with managed_connection(connection) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO clientes (dni, nombre, correo, direccion, frecuente)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (dni) DO UPDATE SET
                        nombre = EXCLUDED.nombre,
                        correo = EXCLUDED.correo,
                        direccion = EXCLUDED.direccion,
                        frecuente = EXCLUDED.frecuente
                """, (cliente.dni, cliente.nombre, cliente.correo, cliente.direccion, cliente.frecuente))

    def obtener_todos(self, connection=None):
        """Retorna una lista de todos los clientes de la base de datos."""
        with managed_connection(connection) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT dni, nombre, correo, direccion, frecuente FROM clientes")
                filas = cursor.fetchall()
        return [Cliente(f[0], f[1], f[2], f[3], f[4]) for f in filas]

    def buscar_por_dni(self, dni, connection=None):
        """Busca y retorna un cliente por su DNI, o None si no existe."""
        with managed_connection(connection) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT dni, nombre, correo, direccion, frecuente FROM clientes WHERE dni = %s", (dni,))
                fila = cursor.fetchone()
        if fila:
            return Cliente(fila[0], fila[1], fila[2], fila[3], fila[4])
        return None
