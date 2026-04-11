"""Pruebas basicas de la capa FastAPI para el recurso pedidos."""

from datetime import datetime
import unittest

from fastapi.testclient import TestClient

from app.dependencies import get_auth_service, get_pedido_service
from app.main import app
from auth_test_utils import FakeAuthService, build_auth_headers


class FakePedidoData:
    """Representa un pedido simple para serializacion de pruebas."""

    def __init__(self, pedido_id, cantidad, metodo_entrega, estado, fecha):
        self.id = pedido_id
        self.cantidad = cantidad
        self.metodo_entrega = metodo_entrega
        self.estado = estado
        self.fecha = fecha


class FakePedidoService:
    """Doble de prueba del servicio de pedidos para endpoints HTTP."""

    def __init__(self):
        self._pedidos = [
            FakePedidoData(1, 2, "domicilio", "pendiente", datetime(2026, 3, 30, 10, 0, 0)),
            FakePedidoData(2, 1, "tienda", "entregado", datetime(2026, 3, 30, 11, 0, 0)),
        ]

    def listar_pedidos(self):
        """Retorna la lista simulada de pedidos."""
        return self._pedidos

    def buscar_pedido_por_id(self, pedido_id):
        """Busca un pedido por id en el catalogo simulado."""
        for pedido in self._pedidos:
            if pedido.id == pedido_id:
                return pedido
        return None

    def registrar_pedido(self, libro_id, cliente_dni, cantidad, metodo_entrega):
        """Registra un nuevo pedido simulado con datos minimos."""
        if libro_id == 999:
            raise ValueError("Libro no encontrado")
        if cliente_dni == "00000000":
            raise ValueError("Cliente no encontrado")
        nuevo_pedido = FakePedidoData(
            len(self._pedidos) + 1,
            cantidad,
            metodo_entrega,
            "pendiente",
            datetime(2026, 3, 30, 12, 0, 0),
        )
        self._pedidos.append(nuevo_pedido)
        return nuevo_pedido

    def cambiar_estado(self, pedido_id, nuevo_estado):
        """Actualiza el estado de un pedido simulado."""
        for pedido in self._pedidos:
            if pedido.id == pedido_id:
                if pedido.estado == nuevo_estado:
                    raise ValueError("El estado no puede ser el mismo")
                pedido.estado = nuevo_estado
                return pedido
        raise ValueError("Pedido no encontrado")


class PedidosApiTests(unittest.TestCase):
    """Valida el comportamiento basico del router de pedidos."""

    def setUp(self):
        self.fake_service = FakePedidoService()
        self.fake_auth_service = FakeAuthService()
        app.dependency_overrides[get_pedido_service] = lambda: self.fake_service
        app.dependency_overrides[get_auth_service] = lambda: self.fake_auth_service
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()

    def test_listar_pedidos(self):
        """Verifica que el endpoint de listado responda con pedidos simulados."""
        response = self.client.get("/pedidos/", headers=build_auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_crear_pedido(self):
        """Valida que se pueda registrar un pedido con datos correctos."""
        response = self.client.post(
            "/pedidos/",
            json={
                "libro_id": 101,
                "cliente_dni": "12345678",
                "cantidad": 2,
                "metodo_entrega": "domicilio",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["estado"], "pendiente")

    def test_crear_pedido_con_libro_inexistente(self):
        """Valida que la API retorne 404 si el libro no existe."""
        response = self.client.post(
            "/pedidos/",
            json={
                "libro_id": 999,
                "cliente_dni": "12345678",
                "cantidad": 1,
                "metodo_entrega": "tienda",
            },
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Libro no encontrado")

    def test_actualizar_estado_pedido(self):
        """Verifica que el estado del pedido se actualice correctamente."""
        response = self.client.patch(
            "/pedidos/1/estado",
            json={"estado": "entregado"},
            headers=build_auth_headers(),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["estado"], "entregado")

    def test_actualizar_estado_pedido_inexistente(self):
        """Valida que la API retorne 404 al actualizar un pedido inexistente."""
        response = self.client.patch(
            "/pedidos/999/estado",
            json={"estado": "cancelado"},
            headers=build_auth_headers(),
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Pedido no encontrado")
    
    def test_obtener_pedido_existente(self):
        """Verifica que la API retorne un pedido existente por id."""
        response = self.client.get("/pedidos/1", headers=build_auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], 1)

    def test_obtener_pedido_inexistente(self):
        """Verifica que la API retorne 404 para un pedido inexistente."""
        response = self.client.get("/pedidos/999", headers=build_auth_headers())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Pedido no encontrado")

if __name__ == "__main__":
    unittest.main()
