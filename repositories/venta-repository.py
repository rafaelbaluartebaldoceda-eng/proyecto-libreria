from database.connection import get_connection
from models.venta import Venta

class VentaRepository:
    """Repositorio que maneja la persistencia de ventas en PostgreSQL."""

    def guardar(self, venta):
        """Guarda una venta en la base de datos."""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO ventas (libro_id, cliente_dni, cantidad, fecha)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (venta.libro.id, venta.cliente.dni, venta.cantidad, venta.fecha))
                venta._id = cursor.fetchone()[0]

    def obtener_todos(self, libros, clientes):
        """Retorna una lista de todas las ventas de la base de datos."""
        with get_connection() as conn:
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