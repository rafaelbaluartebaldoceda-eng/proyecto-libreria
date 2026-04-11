"""Dependencias reutilizables para la capa HTTP de FastAPI."""

from repositories.cliente_repository import ClienteRepository
from repositories.libro_repository import LibroRepository
from repositories.pedido_repository import PedidoRepository
from repositories.usuario_repository import UsuarioRepository
from repositories.venta_repository import VentaRepository
from services.pedido_service import PedidoService
from services.auth_service import AuthService
from services.libreria_service import LibreriaService
from services.venta_service import VentaService


def get_libreria_service():
    """Construye y retorna el servicio principal de catalogo para la API."""
    libro_repo = LibroRepository()
    cliente_repo = ClienteRepository()
    return LibreriaService(libro_repo, cliente_repo)


def get_venta_service():
    """Construye y retorna el servicio principal de ventas para la API."""
    libro_repo = LibroRepository()
    cliente_repo = ClienteRepository()
    venta_repo = VentaRepository()
    return VentaService(venta_repo, libro_repo, cliente_repo)


def get_pedido_service():
    """Construye y retorna el servicio principal de pedidos para la API."""
    pedido_repo = PedidoRepository()
    libro_repo = LibroRepository()
    cliente_repo = ClienteRepository()
    return PedidoService(pedido_repo, libro_repo, cliente_repo)


def get_auth_service():
    """Construye y retorna el servicio principal de autenticacion para la API."""
    usuario_repo = UsuarioRepository()
    return AuthService(usuario_repo)
