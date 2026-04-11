"""Utilidades compartidas para probar autenticacion y autorizacion."""

import os

from app.auth_utils import create_access_token, hash_password, verify_password
from models.usuario import Usuario


os.environ.setdefault("SECRET_KEY", "test-secret-key-for-codex")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
os.environ.setdefault("ADMIN_BOOTSTRAP_TOKEN", "bootstrap-admin-token-123")


class FakeAuthService:
    """Doble de prueba del servicio de autenticacion para endpoints HTTP."""

    def __init__(self, include_default_admin=True):
        self._users = {}
        next_id = 1

        if include_default_admin:
            self._users["admin"] = Usuario(
                username="admin",
                email="admin@example.com",
                hashed_password=hash_password("admin123"),
                role="admin",
                activo=True,
                user_id=next_id,
            )
            next_id += 1

        self._users["usuario"] = Usuario(
            username="usuario",
            email="usuario@example.com",
            hashed_password=hash_password("usuario123"),
            role="user",
            activo=True,
            user_id=next_id,
        )

    def registrar_usuario(self, username, email, password, role="user"):
        """Registra un usuario nuevo si username y correo no existen."""
        if username in self._users:
            raise ValueError("Ya existe un usuario con ese username.")
        if any(user.email == email for user in self._users.values()):
            raise ValueError("Ya existe un usuario con ese correo.")
        nuevo_usuario = Usuario(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            role=role,
            activo=True,
            user_id=len(self._users) + 1,
        )
        self._users[username] = nuevo_usuario
        return nuevo_usuario

    def autenticar_usuario(self, username, password):
        """Autentica un usuario segun username y password."""
        user = self._users.get(username)
        if not user or not user.activo:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def obtener_usuario_por_username(self, username):
        """Busca un usuario por username dentro del doble de prueba."""
        return self._users.get(username)

    def existe_admin_activo(self):
        """Indica si ya existe un administrador activo en el sistema simulado."""
        return any(
            user.role == "admin" and user.activo for user in self._users.values()
        )


def build_auth_headers(username="admin", role="admin"):
    """Construye headers Authorization validos para pruebas HTTP."""
    token = create_access_token({"sub": username, "role": role})
    return {"Authorization": f"Bearer {token}"}
