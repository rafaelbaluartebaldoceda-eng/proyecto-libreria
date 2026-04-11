"""Schemas Pydantic usados por los endpoints de usuarios y auth."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UsuarioRegister(BaseModel):
    """Representa el body publico para registrar un usuario comun."""

    username: str = Field(min_length=3, max_length=50, pattern=r"^[A-Za-z0-9_]+$")
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        """Evita usernames con espacios externos o contenido vacio."""
        if value.strip() != value:
            raise ValueError("El username no debe iniciar ni terminar con espacios.")
        return value

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value):
        """Exige una password basica con letras y numeros."""
        if value.strip() != value:
            raise ValueError(
                "La contrasena no debe iniciar ni terminar con espacios."
            )
        if not any(char.isalpha() for char in value):
            raise ValueError("La contrasena debe incluir al menos una letra.")
        if not any(char.isdigit() for char in value):
            raise ValueError("La contrasena debe incluir al menos un numero.")
        return value


class UsuarioCreate(UsuarioRegister):
    """Representa el body administrativo para crear usuarios con rol explicito."""

    role: Literal["admin", "user"] = "user"


class AdminBootstrapRequest(UsuarioRegister):
    """Representa el body usado para crear el primer admin del sistema."""

    bootstrap_token: str = Field(min_length=16, max_length=255)

    @field_validator("bootstrap_token")
    @classmethod
    def validate_bootstrap_token(cls, value):
        """Evita tokens de bootstrap con espacios externos."""
        if value.strip() != value:
            raise ValueError(
                "El bootstrap token no debe iniciar ni terminar con espacios."
            )
        return value


class UsuarioResponse(BaseModel):
    """Representa la estructura HTTP de salida para un usuario autenticable."""

    model_config = ConfigDict(from_attributes=True)

    id: int | None
    username: str
    email: EmailStr
    role: Literal["admin", "user"]
    activo: bool
