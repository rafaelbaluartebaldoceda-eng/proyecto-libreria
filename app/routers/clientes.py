"""Endpoints HTTP para operaciones relacionadas con clientes."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_libreria_service
from app.schemas.cliente import ClienteCreate, ClienteResponse
from services.libreria_service import LibreriaService


router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("/frecuentes", response_model=list[ClienteResponse])
def obtener_clientes_frecuentes(
    service: LibreriaService = Depends(get_libreria_service),
):
    """Retorna la lista de clientes marcados como frecuentes."""
    return service.listar_clientes_frecuentes()


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def crear_cliente(
    cliente: ClienteCreate,
    service: LibreriaService = Depends(get_libreria_service),
):
    """Registra un nuevo cliente usando la logica existente de la aplicacion."""
    try:
        return service.registrar_cliente(
            cliente.dni,
            cliente.nombre,
            cliente.correo,
            cliente.direccion,
            cliente.frecuente,
        )
    except ValueError as error:
        detail = str(error)
        status_code = (
            status.HTTP_409_CONFLICT
            if "Ya existe un cliente" in detail
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=status_code, detail=detail) from error
