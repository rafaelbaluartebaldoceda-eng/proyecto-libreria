"""Schemas Pydantic usados por los endpoints de libros."""

from pydantic import BaseModel, ConfigDict, Field


class LibroResponse(BaseModel):
    """Representa la estructura HTTP de salida para un libro."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    autor: str
    categoria: str
    precio: int
    stock: int
    disponible: bool


class LibroCreate(BaseModel):
    """Representa la estructura HTTP de entrada para registrar un libro."""

    id: int = Field(gt=0)
    titulo: str = Field(min_length=1, max_length=100)
    autor: str = Field(min_length=1, max_length=100)
    categoria: str = Field(min_length=1, max_length=50)
    precio: int = Field(gt=0)
    stock: int = Field(ge=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 104,
                "titulo": "Clean Code",
                "autor": "Robert C. Martin",
                "categoria": "Software",
                "precio": 80,
                "stock": 5,
            }
        }
    }
