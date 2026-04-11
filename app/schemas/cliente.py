"""Schemas Pydantic usados por los endpoints de clientes."""

from pydantic import BaseModel, ConfigDict, Field


class ClienteResponse(BaseModel):
    """Representa la estructura HTTP de salida para un cliente."""

    model_config = ConfigDict(from_attributes=True)

    dni: str
    nombre: str
    direccion: str
    correo: str
    frecuente: bool


class ClienteCreate(BaseModel):
    """Representa la estructura HTTP de entrada para registrar un cliente."""

    dni: str = Field(min_length=8, max_length=8, pattern=r"^\d{8}$")
    nombre: str = Field(min_length=1, max_length=100)
    direccion: str = Field(min_length=1, max_length=150)
    correo: str = Field(min_length=1, max_length=100)
    frecuente: bool = False

    model_config = {
        "json_schema_extra": {
            "example": {
                "dni": "12345678",
                "nombre": "Nuevo Cliente",
                "direccion": "Ate Vitarte",
                "correo": "cliente@gmail.com",
                "frecuente": False,
            }
        }
    }
