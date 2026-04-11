"""Servicio de autenticacion y administracion de usuarios."""

import re

from email_validator import EmailNotValidError, validate_email

from database.connection import managed_connection
from models.usuario import Usuario
from app.auth_utils import hash_password, verify_password


class AuthService:
    """Coordina registro, autenticacion y consulta de usuarios."""

    USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")

    def __init__(self, usuario_repo):
        self._usuario_repo = usuario_repo

    def registrar_usuario(self, username, email, password, role="user"):
        """Registra un nuevo usuario validando duplicados y hasheando password."""
        with managed_connection() as conn:
            username = self._validar_username(username)
            email = self._validar_email(email)
            self._validar_credenciales_basicas(password)
            if self._usuario_repo.buscar_por_username(username, connection=conn):
                raise ValueError("Ya existe un usuario con ese username.")
            if self._usuario_repo.buscar_por_email(email, connection=conn):
                raise ValueError("Ya existe un usuario con ese correo.")

            usuario = Usuario(
                username=username,
                email=email,
                hashed_password=hash_password(password),
                role=role,
            )
            self._usuario_repo.guardar(usuario, connection=conn)
            return usuario

    def autenticar_usuario(self, username, password):
        """Valida credenciales y retorna el usuario autenticado si son correctas."""
        with managed_connection() as conn:
            username = self._validar_username(username, raise_errors=False)
            if not username or not isinstance(password, str):
                return None
            usuario = self._usuario_repo.buscar_por_username(username, connection=conn)
            if not usuario or not usuario.activo:
                return None
            if not verify_password(password, usuario.hashed_password):
                return None
            return usuario

    def obtener_usuario_por_username(self, username):
        """Busca un usuario por username para autenticacion/autorizacion."""
        with managed_connection() as conn:
            username = self._validar_username(username, raise_errors=False)
            if not username:
                return None
            return self._usuario_repo.buscar_por_username(username, connection=conn)

    def existe_admin_activo(self):
        """Indica si ya existe un administrador activo en el sistema."""
        with managed_connection() as conn:
            return self._usuario_repo.existe_admin_activo(connection=conn)

    @staticmethod
    def _validar_credenciales_basicas(password):
        """Valida reglas minimas de password antes de hashearla."""
        if not isinstance(password, str) or len(password) < 8:
            raise ValueError("La contrasena debe tener al menos 8 caracteres.")
        if password.strip() != password:
            raise ValueError("La contrasena no debe iniciar ni terminar con espacios.")
        if not any(char.isalpha() for char in password):
            raise ValueError("La contrasena debe incluir al menos una letra.")
        if not any(char.isdigit() for char in password):
            raise ValueError("La contrasena debe incluir al menos un numero.")

    @classmethod
    def _validar_username(cls, username, raise_errors=True):
        """Valida username y retorna una version segura para consultas/registro."""
        if not isinstance(username, str):
            if raise_errors:
                raise ValueError("El username debe ser un texto valido.")
            return None

        username = username.strip()
        if not 3 <= len(username) <= 50:
            if raise_errors:
                raise ValueError("El username debe tener entre 3 y 50 caracteres.")
            return None
        if not cls.USERNAME_PATTERN.fullmatch(username):
            if raise_errors:
                raise ValueError(
                    "El username solo puede contener letras, numeros y guion bajo."
                )
            return None
        return username

    @staticmethod
    def _validar_email(email):
        """Valida correo y retorna una version normalizada para persistencia."""
        if not isinstance(email, str):
            raise ValueError("El correo debe ser un texto valido.")
        if email.strip() != email:
            raise ValueError("El correo no debe iniciar ni terminar con espacios.")

        try:
            result = validate_email(email, check_deliverability=False)
        except EmailNotValidError as error:
            raise ValueError("Correo invalido.") from error
        return result.normalized
