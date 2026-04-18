"""Repositorio de pedidos implementado con SQLAlchemy ORM."""

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database.connection import managed_connection
from database.orm_models import PedidoORM
from models.cliente import Cliente
from models.libro import Libro
from models.pedido import Pedido


class PedidoRepository:
    """Repositorio que maneja la persistencia de pedidos en PostgreSQL."""

    def guardar(self, pedido, connection=None):
        """Guarda un pedido en la base de datos."""
        with managed_connection(connection) as session:
            orm_pedido = PedidoORM(
                libro_id=pedido.libro.id,
                cliente_dni=pedido.cliente.dni,
                cantidad=pedido.cantidad,
                metodo_entrega=pedido.metodo_entrega,
                estado=pedido.estado,
                fecha=pedido.fecha,
            )
            session.add(orm_pedido)
            session.flush()
            pedido._id = orm_pedido.id
        return pedido

    def obtener_todos(self, libros=None, clientes=None, connection=None):
        """Retorna una lista de todos los pedidos de la base de datos."""
        with managed_connection(connection) as session:
            filas = session.scalars(
                select(PedidoORM)
                .options(
                    joinedload(PedidoORM.libro),
                    joinedload(PedidoORM.cliente),
                )
                .order_by(PedidoORM.id)
            ).all()
        return [self._build_pedido(fila) for fila in filas]

    def actualizar_estado(self, pedido_id, nuevo_estado, connection=None):
        """Actualiza el estado de un pedido en la base de datos."""
        with managed_connection(connection) as session:
            orm_pedido = session.get(PedidoORM, pedido_id)
            if orm_pedido is not None:
                orm_pedido.estado = nuevo_estado

    def buscar_por_id(self, id_pedido, libros=None, clientes=None, connection=None):
        """Busca un pedido por su id."""
        with managed_connection(connection) as session:
            fila = session.scalar(
                select(PedidoORM)
                .options(
                    joinedload(PedidoORM.libro),
                    joinedload(PedidoORM.cliente),
                )
                .where(PedidoORM.id == id_pedido)
            )
        return self._build_pedido(fila)

    @staticmethod
    def _build_pedido(fila):
        """Reconstruye una entidad Pedido a partir del modelo ORM."""
        if fila is None or fila.libro is None or fila.cliente is None:
            return None

        libro = Libro(
            fila.libro.id,
            fila.libro.titulo,
            fila.libro.autor,
            fila.libro.categoria,
            fila.libro.precio,
            fila.libro.stock,
        )
        cliente = Cliente(
            fila.cliente.dni,
            fila.cliente.nombre,
            fila.cliente.correo,
            fila.cliente.direccion,
            fila.cliente.frecuente,
        )
        return Pedido.from_dict(
            {
                "id": fila.id,
                "libro_id": fila.libro_id,
                "cliente_dni": fila.cliente_dni,
                "cantidad": fila.cantidad,
                "metodo_entrega": fila.metodo_entrega,
                "estado": fila.estado,
                "fecha": fila.fecha.isoformat(),
            },
            libro,
            cliente,
        )
