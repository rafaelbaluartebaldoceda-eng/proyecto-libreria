"""Endpoints HTTP para operaciones relacionadas con pedidos."""

from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.dependencies import get_pedido_service
from app.schemas.pedido import PedidoCreate, PedidoEstadoUpdate, PedidoResponse
from services.pedido_service import PedidoService


router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.get("/", response_model=list[PedidoResponse])
def listar_pedidos(service: PedidoService = Depends(get_pedido_service)):
    """Lista todos los pedidos registrados en el sistema."""
    return service.listar_pedidos()


@router.post("/", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def crear_pedido(
    pedido: PedidoCreate,
    service: PedidoService = Depends(get_pedido_service),
):
    """Registra un nuevo pedido usando la logica existente de la aplicacion."""
    try:
        return service.registrar_pedido(
            pedido.libro_id,
            pedido.cliente_dni,
            pedido.cantidad,
            pedido.metodo_entrega,
        )
    except ValueError as error:
        detail = str(error)
        status_code = (
            status.HTTP_404_NOT_FOUND
            if "no encontrado" in detail.lower()
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=status_code, detail=detail) from error


@router.patch("/{pedido_id}/estado", response_model=PedidoResponse)
def actualizar_estado_pedido(
    datos: PedidoEstadoUpdate,
    pedido_id: int = Path(gt=0),
    service: PedidoService = Depends(get_pedido_service),
):
    """Actualiza el estado de un pedido existente."""
    try:
        return service.cambiar_estado(pedido_id, datos.estado)
    except ValueError as error:
        detail = str(error)
        status_code = (
            status.HTTP_404_NOT_FOUND
            if "no encontrado" in detail.lower()
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=status_code, detail=detail) from error
