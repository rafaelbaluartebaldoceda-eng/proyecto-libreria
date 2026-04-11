"""Repositorio que maneja la persistencia de usuarios en PostgreSQL."""

from database.connection import managed_connection
from models.usuario import Usuario


class UsuarioRepository:
    """Acceso a datos para entidades de autenticacion."""

    def guardar(self, usuario, connection=None):
        """Inserta un usuario y actualiza su id persistente."""
        with managed_connection(connection) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO usuarios (username, email, hashed_password, role, activo)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        usuario.username,
                        usuario.email,
                        usuario.hashed_password,
                        usuario.role,
                        usuario.activo,
                    ),
                )
                usuario._id = cursor.fetchone()[0]
        return usuario

    def buscar_por_username(self, username, connection=None):
        """Busca y retorna un usuario por username."""
        with managed_connection(connection) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, username, email, hashed_password, role, activo
                    FROM usuarios
                    WHERE username = %s
                    """,
                    (username,),
                )
                fila = cursor.fetchone()
        return self._build_usuario(fila)

    def buscar_por_email(self, email, connection=None):
        """Busca y retorna un usuario por correo."""
        with managed_connection(connection) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, username, email, hashed_password, role, activo
                    FROM usuarios
                    WHERE email = %s
                    """,
                    (email,),
                )
                fila = cursor.fetchone()
        return self._build_usuario(fila)

    def buscar_por_id(self, user_id, connection=None):
        """Busca y retorna un usuario por id."""
        with managed_connection(connection) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, username, email, hashed_password, role, activo
                    FROM usuarios
                    WHERE id = %s
                    """,
                    (user_id,),
                )
                fila = cursor.fetchone()
        return self._build_usuario(fila)

    def obtener_todos(self, connection=None):
        """Retorna la lista completa de usuarios."""
        with managed_connection(connection) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, username, email, hashed_password, role, activo
                    FROM usuarios
                    ORDER BY id
                    """
                )
                filas = cursor.fetchall()
        return [self._build_usuario(fila) for fila in filas]

    def existe_admin_activo(self, connection=None):
        """Indica si ya existe al menos un usuario administrador activo."""
        with managed_connection(connection) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT EXISTS(
                        SELECT 1
                        FROM usuarios
                        WHERE role = 'admin' AND activo = TRUE
                    )
                    """
                )
                return cursor.fetchone()[0]

    @staticmethod
    def _build_usuario(fila):
        """Reconstruye un usuario a partir de una fila de PostgreSQL."""
        if not fila:
            return None
        return Usuario(
            username=fila[1],
            email=fila[2],
            hashed_password=fila[3],
            role=fila[4],
            activo=fila[5],
            user_id=fila[0],
        )
