"""Pruebas basicas de la capa FastAPI para el recurso clientes."""

import unittest

from fastapi.testclient import TestClient

from app.dependencies import get_libreria_service
from app.main import app
from models.cliente import Cliente


class FakeLibreriaClientesService:
    """Doble de prueba del servicio de libreria para endpoints de clientes."""

    def __init__(self):
        self._clientes = [
            Cliente("12345678", "Ana Torres", "ana@gmail.com", "Lima", True),
            Cliente("23456789", "Carlos Ruiz", "carlos@gmail.com", "Cusco", False),
        ]

    def listar_clientes_frecuentes(self):
        """Retorna la lista simulada de clientes frecuentes."""
        return [cliente for cliente in self._clientes if cliente.frecuente]

    def registrar_cliente(self, dni, nombre, correo, direccion, frecuente=False):
        """Registra un cliente si no existe un DNI repetido."""
        for cliente in self._clientes:
            if cliente.dni == dni:
                raise ValueError("Ya existe un cliente con ese DNI.")
        nuevo_cliente = Cliente(dni, nombre, correo, direccion, frecuente)
        self._clientes.append(nuevo_cliente)
        return nuevo_cliente


class ClientesApiTests(unittest.TestCase):
    """Valida el comportamiento basico del router de clientes."""

    def setUp(self):
        self.fake_service = FakeLibreriaClientesService()
        app.dependency_overrides[get_libreria_service] = lambda: self.fake_service
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()

    def test_obtener_clientes_frecuentes(self):
        """Verifica que el endpoint retorne solo clientes frecuentes."""
        response = self.client.get("/clientes/frecuentes")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["dni"], "12345678")

    def test_crear_cliente(self):
        """Valida que se pueda registrar un cliente con datos correctos."""
        response = self.client.post(
            "/clientes/",
            json={
                "dni": "34567890",
                "nombre": "Lucia Vega",
                "direccion": "Arequipa",
                "correo": "lucia@gmail.com",
                "frecuente": False,
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["dni"], "34567890")

    def test_crear_cliente_con_dni_repetido(self):
        """Verifica que la API retorne conflicto si el DNI ya existe."""
        response = self.client.post(
            "/clientes/",
            json={
                "dni": "12345678",
                "nombre": "Duplicado",
                "direccion": "Lima",
                "correo": "duplicado@gmail.com",
                "frecuente": False,
            },
        )
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["detail"], "Ya existe un cliente con ese DNI.")


if __name__ == "__main__":
    unittest.main()
