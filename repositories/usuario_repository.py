"""Repositorio de usuarios implementado con SQLAlchemy ORM."""

from sqlalchemy import exists, select

from database.connection import managed_connection
from database.orm_models import UsuarioORM
from models.usuario import Usuario


class UsuarioRepository:
    """Acceso a datos para entidades de autenticacion."""

    def guardar(self, usuario, connection=None):
        """Inserta un usuario y actualiza su id persistente."""
        with managed_connection(connection) as session:
            orm_usuario = UsuarioORM(
                username=usuario.username,
                email=usuario.email,
                hashed_password=usuario.hashed_password,
                role=usuario.role,
                activo=usuario.activo,
            )
            session.add(orm_usuario)
            session.flush()
            usuario._id = orm_usuario.id
        return usuario

    def buscar_por_username(self, username, connection=None):
        """Busca y retorna un usuario por username."""
        with managed_connection(connection) as session:
            fila = session.scalar(
                select(UsuarioORM).where(UsuarioORM.username == username)
            )
        return self._build_usuario(fila)

    def buscar_por_email(self, email, connection=None):
        """Busca y retorna un usuario por correo."""
        with managed_connection(connection) as session:
            fila = session.scalar(select(UsuarioORM).where(UsuarioORM.email == email))
        return self._build_usuario(fila)

    def buscar_por_id(self, user_id, connection=None):
        """Busca y retorna un usuario por id."""
        with managed_connection(connection) as session:
            fila = session.get(UsuarioORM, user_id)
        return self._build_usuario(fila)

    def obtener_todos(self, connection=None):
        """Retorna la lista completa de usuarios."""
        with managed_connection(connection) as session:
            filas = session.scalars(select(UsuarioORM).order_by(UsuarioORM.id)).all()
        return [self._build_usuario(fila) for fila in filas]

    def existe_admin_activo(self, connection=None):
        """Indica si ya existe al menos un usuario administrador activo."""
        with managed_connection(connection) as session:
            return bool(
                session.scalar(
                    select(
                        exists().where(
                            UsuarioORM.role == "admin",
                            UsuarioORM.activo.is_(True),
                        )
                    )
                )
            )

    @staticmethod
    def _build_usuario(fila):
        """Reconstruye un usuario a partir de una fila persistida."""
        if not fila:
            return None
        return Usuario(
            username=fila.username,
            email=fila.email,
            hashed_password=fila.hashed_password,
            role=fila.role,
            activo=fila.activo,
            user_id=fila.id,
        )
