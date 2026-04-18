"""Repositorio de clientes implementado con SQLAlchemy ORM."""

from sqlalchemy import select

from database.connection import managed_connection
from database.orm_models import ClienteORM
from models.cliente import Cliente


class ClienteRepository:
    """Repositorio que maneja la persistencia de clientes en PostgreSQL."""

    def guardar(self, cliente, connection=None):
        """Guarda o actualiza un cliente en la base de datos."""
        with managed_connection(connection) as session:
            orm_cliente = session.get(ClienteORM, cliente.dni)
            if orm_cliente is None:
                orm_cliente = ClienteORM(
                    dni=cliente.dni,
                    nombre=cliente.nombre,
                    correo=cliente.correo,
                    direccion=cliente.direccion,
                    frecuente=cliente.frecuente,
                )
                session.add(orm_cliente)
            else:
                orm_cliente.nombre = cliente.nombre
                orm_cliente.correo = cliente.correo
                orm_cliente.direccion = cliente.direccion
                orm_cliente.frecuente = cliente.frecuente
        return cliente

    def obtener_todos(self, connection=None):
        """Retorna una lista de todos los clientes de la base de datos."""
        with managed_connection(connection) as session:
            filas = session.scalars(select(ClienteORM).order_by(ClienteORM.dni)).all()
        return [self._build_cliente(fila) for fila in filas]

    def buscar_por_dni(self, dni, connection=None):
        """Busca y retorna un cliente por su DNI, o None si no existe."""
        with managed_connection(connection) as session:
            fila = session.get(ClienteORM, dni)
        return self._build_cliente(fila)

    @staticmethod
    def _build_cliente(fila):
        """Reconstruye una entidad Cliente a partir del modelo ORM."""
        if fila is None:
            return None
        return Cliente(
            fila.dni,
            fila.nombre,
            fila.correo,
            fila.direccion,
            fila.frecuente,
        )
