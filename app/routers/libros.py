"""Endpoints HTTP para operaciones relacionadas con libros."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.dependencies import get_libreria_service
from app.schemas.libro import LibroCreate, LibroResponse
from app.security import require_admin
from services.libreria_service import LibreriaService


router = APIRouter(prefix="/libros", tags=["Libros"])


@router.get("/", response_model=list[LibroResponse])
def listar_libros(service: LibreriaService = Depends(get_libreria_service)):
    """Lista todos los libros registrados en el sistema."""
    return service.listar_libros()


@router.get("/{libro_id}", response_model=LibroResponse)
def obtener_libro(
    libro_id: int = Path(gt=0),
    service: LibreriaService = Depends(get_libreria_service),
):
    """Busca y retorna un libro por su identificador."""
    libro = service.buscar_libro(libro_id)
    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Libro no encontrado",
        )
    return libro


@router.post("/", response_model=LibroResponse, status_code=status.HTTP_201_CREATED)
def crear_libro(
    libro: LibroCreate,
    admin_user: Annotated[object, Depends(require_admin)],
    service: LibreriaService = Depends(get_libreria_service),
):
    """Registra un nuevo libro usando la logica existente de la aplicacion."""
    _ = admin_user
    try:
        return service.registrar_libro(
            libro.id,
            libro.titulo,
            libro.autor,
            libro.categoria,
            libro.precio,
            libro.stock,
        )
    except ValueError as error:
        detail = str(error)
        status_code = (
            status.HTTP_409_CONFLICT
            if "Ya existe un libro" in detail
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=status_code, detail=detail) from error
