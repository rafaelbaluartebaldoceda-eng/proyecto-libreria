"""Dependencias reutilizables para la capa HTTP de FastAPI."""

from repositories.cliente_repository import ClienteRepository
from repositories.libro_repository import LibroRepository
from services.libreria_service import LibreriaService


def get_libreria_service():
    """Construye y retorna el servicio principal de catalogo para la API."""
    libro_repo = LibroRepository()
    cliente_repo = ClienteRepository()
    return LibreriaService(libro_repo, cliente_repo)
