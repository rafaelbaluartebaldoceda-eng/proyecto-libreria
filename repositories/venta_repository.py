from database.connection import managed_connection
from models.venta import Venta

class VentaRepository:
    """Repositorio que maneja la persistencia de ventas en PostgreSQL."""

    def guardar(self, venta, connection=None):
        """Guarda una venta en la base de datos."""
        with managed_connection(connection) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO ventas (libro_id, cliente_dni, cantidad, fecha)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (venta.libro.id, venta.cliente.dni, venta.cantidad, venta.fecha))
                venta._id = cursor.fetchone()[0]

    def obtener_todos(self, libros, clientes, connection=None):
        """Retorna una lista de todas las ventas de la base de datos."""
        with managed_connection(connection) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, libro_id, cliente_dni, cantidad, fecha FROM ventas")
                filas = cursor.fetchall()
        ventas = []
        for f in filas:
            libro = next((l for l in libros if l.id == f[1]), None)
            cliente = next((c for c in clientes if c.dni == f[2]), None)
            if libro and cliente:
                venta = Venta.from_dict({
                    "id": f[0],
                    "libro_id": f[1],
                    "cliente_dni": f[2],
                    "cantidad": f[3],
                    "fecha": f[4].isoformat()
                }, libro, cliente)
                ventas.append(venta)
        return ventas
    def buscar_por_id(self, id, libros, clientes, connection=None):
        """Busca una venta por su id."""
        with managed_connection(connection) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, libro_id, cliente_dni, cantidad, fecha FROM ventas WHERE id = %s", (id,))
                f = cursor.fetchone()
        if not f:
            return None
        libro = next((l for l in libros if l.id == f[1]), None)
        cliente = next((c for c in clientes if c.dni == f[2]), None)
        if libro and cliente:
            return Venta.from_dict({"id": f[0], "libro_id": f[1], "cliente_dni": f[2], "cantidad": f[3], "fecha": f[4].isoformat()}, libro, cliente)
        return None

    def total_ventas(self, connection=None):
        """Retorna el total acumulado de todas las ventas directamente desde SQL."""
        with managed_connection(connection) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT SUM(v.cantidad * l.precio)
                    FROM ventas v
                    JOIN libros l ON v.libro_id = l.id
                """)
                resultado = cursor.fetchone()[0]
        return resultado or 0
