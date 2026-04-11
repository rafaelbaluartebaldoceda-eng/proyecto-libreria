"""Schemas Pydantic usados por los endpoints de pedidos."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PedidoResponse(BaseModel):
    """Representa la estructura HTTP de salida para un pedido."""

    model_config = ConfigDict(from_attributes=True)

    id: int | None
    cantidad: int
    metodo_entrega: str
    estado: str
    fecha: datetime


class PedidoCreate(BaseModel):
    """Representa la estructura HTTP de entrada para registrar un pedido."""

    libro_id: int = Field(gt=0)
    cliente_dni: str = Field(min_length=8, max_length=8, pattern=r"^\d{8}$")
    cantidad: int = Field(gt=0)
    metodo_entrega: Literal["tienda", "domicilio"]

    model_config = {
        "json_schema_extra": {
            "example": {
                "libro_id": 101,
                "cliente_dni": "12345678",
                "cantidad": 2,
                "metodo_entrega": "domicilio",
            }
        }
    }


class PedidoEstadoUpdate(BaseModel):
    """Representa la estructura HTTP para cambiar el estado de un pedido."""

    estado: Literal["pendiente", "entregado", "cancelado"]

    model_config = {
        "json_schema_extra": {
            "example": {
                "estado": "entregado",
            }
        }
    }
