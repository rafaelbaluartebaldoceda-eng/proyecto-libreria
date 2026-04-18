"""Repositorio de libros implementado con SQLAlchemy ORM."""

from sqlalchemy import select

from database.connection import managed_connection
from database.orm_models import LibroORM
from models.libro import Libro


class LibroRepository:
    """Repositorio que maneja la persistencia de libros en PostgreSQL."""

    def guardar(self, libro, connection=None):
        """Guarda o actualiza un libro en la base de datos."""
        with managed_connection(connection) as session:
            orm_libro = session.get(LibroORM, libro.id)
            if orm_libro is None:
                orm_libro = LibroORM(
                    id=libro.id,
                    titulo=libro.titulo,
                    autor=libro.autor,
                    categoria=libro.categoria,
                    precio=libro.precio,
                    stock=libro.stock,
                )
                session.add(orm_libro)
            else:
                orm_libro.titulo = libro.titulo
                orm_libro.autor = libro.autor
                orm_libro.categoria = libro.categoria
                orm_libro.precio = libro.precio
                orm_libro.stock = libro.stock
        return libro

    def obtener_todos(self, connection=None):
        """Retorna una lista de todos los libros de la base de datos."""
        with managed_connection(connection) as session:
            filas = session.scalars(select(LibroORM).order_by(LibroORM.id)).all()
        return [self._build_libro(fila) for fila in filas]

    def buscar_por_id(self, id, connection=None):
        """Busca y retorna un libro por su id, o None si no existe."""
        with managed_connection(connection) as session:
            fila = session.get(LibroORM, id)
        return self._build_libro(fila)

    @staticmethod
    def _build_libro(fila):
        """Reconstruye una entidad Libro a partir del modelo ORM."""
        if fila is None:
            return None
        return Libro(
            fila.id,
            fila.titulo,
            fila.autor,
            fila.categoria,
            fila.precio,
            fila.stock,
        )
