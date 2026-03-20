from database.connection import get_connection
from models.pedido import Pedido

class PedidoRepository:
    """Repositorio que maneja la persistencia de pedidos en PostgreSQL."""

    def guardar(self, pedido):
        """Guarda o actualiza un pedido en la base de datos."""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO pedidos (libro_id, cliente_dni, cantidad, metodo_entrega, estado, fecha)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        estado = EXCLUDED.estado
                    RETURNING id
                """, (pedido.libro.id, pedido.cliente.dni, pedido.cantidad,
                      pedido.metodo_entrega, pedido.estado, pedido.fecha))
                pedido._id = cursor.fetchone()[0]

    def obtener_todos(self, libros, clientes):
        """Retorna una lista de todos los pedidos de la base de datos."""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, libro_id, cliente_dni, cantidad, metodo_entrega, estado, fecha FROM pedidos")
                filas = cursor.fetchall()
        pedidos = []
        for f in filas:
            libro = next((l for l in libros if l.id == f[1]), None)
            cliente = next((c for c in clientes if c.dni == f[2]), None)
            if libro and cliente:
                pedido = Pedido.from_dict({
                    "id": f[0],
                    "libro_id": f[1],
                    "cliente_dni": f[2],
                    "cantidad": f[3],
                    "metodo_entrega": f[4],
                    "estado": f[5],
                    "fecha": f[6].isoformat()
                }, libro, cliente)
                pedidos.append(pedido)
        return pedidos

    def actualizar_estado(self, pedido_id, nuevo_estado):
        """Actualiza el estado de un pedido en la base de datos."""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE pedidos SET estado = %s WHERE id = %s
                """, (nuevo_estado, pedido_id))