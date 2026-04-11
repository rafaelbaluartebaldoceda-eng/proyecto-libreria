"""Pruebas basicas de la capa FastAPI para el recurso ventas."""

from datetime import datetime
import unittest

from fastapi.testclient import TestClient

from app.dependencies import get_auth_service, get_venta_service
from app.main import app
from auth_test_utils import FakeAuthService, build_auth_headers


class FakeVentaData:
    """Representa una venta simple para serializacion de pruebas."""

    def __init__(self, venta_id, cantidad, total, fecha):
        self.id = venta_id
        self.cantidad = cantidad
        self.total = total
        self.fecha = fecha


class FakeVentaService:
    """Doble de prueba del servicio de ventas para endpoints HTTP."""

    def __init__(self):
        self._ventas = [
            FakeVentaData(1, 2, 70, datetime(2026, 3, 29, 10, 0, 0)),
            FakeVentaData(2, 1, 45, datetime(2026, 3, 29, 11, 0, 0)),
        ]

    def listar_ventas(self):
        """Retorna la lista simulada de ventas."""
        return self._ventas

    def buscar_venta_por_id(self, venta_id):
        """Busca una venta por id en el catalogo simulado."""
        for venta in self._ventas:
            if venta.id == venta_id:
                return venta
        return None

    def registrar_venta(self, libro_id, cliente_dni, cantidad):
        """Registra una nueva venta simulada con datos minimos."""
        if libro_id == 999:
            raise ValueError("Libro no encontrado")
        if cliente_dni == "00000000":
            raise ValueError("Cliente no encontrado")
        nueva_venta = FakeVentaData(
            len(self._ventas) + 1,
            cantidad,
            cantidad * 35,
            datetime(2026, 3, 29, 12, 0, 0),
        )
        self._ventas.append(nueva_venta)
        return nueva_venta


class VentasApiTests(unittest.TestCase):
    """Valida el comportamiento basico del router de ventas."""

    def setUp(self):
        self.fake_service = FakeVentaService()
        self.fake_auth_service = FakeAuthService()
        app.dependency_overrides[get_venta_service] = lambda: self.fake_service
        app.dependency_overrides[get_auth_service] = lambda: self.fake_auth_service
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()

    def test_listar_ventas(self):
        response = self.client.get("/ventas/", headers=build_auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_obtener_venta_existente(self):
        response = self.client.get("/ventas/1", headers=build_auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], 1)

    def test_obtener_venta_inexistente(self):
        response = self.client.get("/ventas/999", headers=build_auth_headers())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Venta no encontrada")

    def test_crear_venta(self):
        response = self.client.post(
            "/ventas/",
            json={
                "libro_id": 101,
                "cliente_dni": "12345678",
                "cantidad": 3,
            },
            headers=build_auth_headers(),
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["cantidad"], 3)

    def test_crear_venta_con_libro_inexistente(self):
        response = self.client.post(
            "/ventas/",
            json={
                "libro_id": 999,
                "cliente_dni": "12345678",
                "cantidad": 1,
            },
            headers=build_auth_headers(),
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Libro no encontrado")


if __name__ == "__main__":
    unittest.main()
