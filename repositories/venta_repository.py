"""Repositorio de ventas implementado con SQLAlchemy ORM."""

from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from database.connection import managed_connection
from database.orm_models import LibroORM, VentaORM
from models.cliente import Cliente
from models.libro import Libro
from models.venta import Venta


class VentaRepository:
    """Repositorio que maneja la persistencia de ventas en PostgreSQL."""

    def guardar(self, venta, connection=None):
        """Guarda una venta en la base de datos."""
        with managed_connection(connection) as session:
            orm_venta = VentaORM(
                libro_id=venta.libro.id,
                cliente_dni=venta.cliente.dni,
                cantidad=venta.cantidad,
                fecha=venta.fecha,
            )
            session.add(orm_venta)
            session.flush()
            venta._id = orm_venta.id
        return venta

    def obtener_todos(self, libros=None, clientes=None, connection=None):
        """Retorna una lista de todas las ventas de la base de datos."""
        with managed_connection(connection) as session:
            filas = session.scalars(
                select(VentaORM)
                .options(
                    joinedload(VentaORM.libro),
                    joinedload(VentaORM.cliente),
                )
                .order_by(VentaORM.id)
            ).all()
        return [self._build_venta(fila) for fila in filas]

    def buscar_por_id(self, id, libros=None, clientes=None, connection=None):
        """Busca una venta por su id."""
        with managed_connection(connection) as session:
            fila = session.scalar(
                select(VentaORM)
                .options(
                    joinedload(VentaORM.libro),
                    joinedload(VentaORM.cliente),
                )
                .where(VentaORM.id == id)
            )
        return self._build_venta(fila)

    def total_ventas(self, connection=None):
        """Retorna el total acumulado de todas las ventas directamente desde SQL."""
        with managed_connection(connection) as session:
            total = session.scalar(
                select(func.coalesce(func.sum(VentaORM.cantidad * LibroORM.precio), 0))
                .join(LibroORM, VentaORM.libro_id == LibroORM.id)
            )
        return total or 0

    @staticmethod
    def _build_venta(fila):
        """Reconstruye una entidad Venta a partir del modelo ORM."""
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
        return Venta.from_dict(
            {
                "id": fila.id,
                "libro_id": fila.libro_id,
                "cliente_dni": fila.cliente_dni,
                "cantidad": fila.cantidad,
                "fecha": fila.fecha.isoformat(),
            },
            libro,
            cliente,
        )
