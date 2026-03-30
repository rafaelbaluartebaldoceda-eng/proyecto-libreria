"""Schemas Pydantic usados por los endpoints de ventas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class VentaCreate(BaseModel):
    """Representa la estructura HTTP de entrada para registrar una venta."""

    libro_id: int = Field(gt=0)
    cliente_dni: str = Field(min_length=8, max_length=8)
    cantidad: int = Field(gt=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "libro_id": 101,
                "cliente_dni": "12345678",
                "cantidad": 2,
            }
        }
    }


class VentaResponse(BaseModel):
    """Representa la estructura HTTP de salida para una venta."""

    model_config = ConfigDict(from_attributes=True)

    id: int | None
    cantidad: int
    total: int
    fecha: datetime