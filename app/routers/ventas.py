"""Endpoints HTTP para operaciones relacionadas con ventas."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.dependencies import get_venta_service
from app.schemas.venta import VentaCreate, VentaResponse
from app.security import require_admin
from services.venta_service import VentaService


router = APIRouter(prefix="/ventas", tags=["Ventas"])


@router.get("/", response_model=list[VentaResponse])
def listar_ventas(
    admin_user: Annotated[object, Depends(require_admin)],
    service: VentaService = Depends(get_venta_service),
):
    """Lista todas las ventas registradas en el sistema."""
    _ = admin_user
    return service.listar_ventas()


@router.get("/{venta_id}", response_model=VentaResponse)
def obtener_venta(
    admin_user: Annotated[object, Depends(require_admin)],
    venta_id: int = Path(gt=0),
    service: VentaService = Depends(get_venta_service),
):
    """Busca y retorna una venta por su identificador."""
    _ = admin_user
    venta = service.buscar_venta_por_id(venta_id)
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada"
        )
    return venta


@router.post("/", response_model=VentaResponse, status_code=status.HTTP_201_CREATED)
def crear_venta(
    venta: VentaCreate,
    admin_user: Annotated[object, Depends(require_admin)],
    service: VentaService = Depends(get_venta_service),
):
    """Registra una nueva venta usando la logica existente de la aplicacion."""
    _ = admin_user
    try:
        return service.registrar_venta(
            venta.libro_id,
            venta.cliente_dni,
            venta.cantidad,
        )
    except ValueError as error:
        detail = str(error)
        status_code = (
            status.HTTP_404_NOT_FOUND
            if "no encontrado" in detail.lower()
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=status_code, detail=detail) from error
