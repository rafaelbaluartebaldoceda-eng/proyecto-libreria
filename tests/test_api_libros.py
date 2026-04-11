"""Pruebas basicas de la capa FastAPI para el recurso libros."""

import unittest

from fastapi.testclient import TestClient

from app.dependencies import get_auth_service, get_libreria_service
from app.main import app
from models.libro import Libro
from auth_test_utils import FakeAuthService, build_auth_headers


class FakeLibreriaService:
    """Doble de prueba del servicio de libreria para endpoints de libros."""

    def __init__(self):
        self._libros = [
            Libro(101, "El Principito", "Antoine de Saint-Exupery", "Ficcion", 35, 10),
            Libro(102, "1984", "George Orwell", "Distopia", 50, 6),
        ]

    def listar_libros(self):
        """Retorna el catalogo simulado."""
        return self._libros

    def buscar_libro(self, libro_id):
        """Busca un libro por id en el catalogo simulado."""
        for libro in self._libros:
            if libro.id == libro_id:
                return libro
        return None

    def registrar_libro(self, libro_id, titulo, autor, categoria, precio, stock):
        """Registra un libro si no existe un id repetido."""
        if self.buscar_libro(libro_id):
            raise ValueError("Ya existe un libro con ese ID.")
        libro = Libro(libro_id, titulo, autor, categoria, precio, stock)
        self._libros.append(libro)
        return libro


class LibrosApiTests(unittest.TestCase):
    """Valida el comportamiento basico del router de libros."""

    def setUp(self):
        self.fake_service = FakeLibreriaService()
        self.fake_auth_service = FakeAuthService()
        app.dependency_overrides[get_libreria_service] = lambda: self.fake_service
        app.dependency_overrides[get_auth_service] = lambda: self.fake_auth_service
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Bienvenido a la API de libreria"})

    def test_listar_libros(self):
        response = self.client.get("/libros/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_obtener_libro_existente(self):
        response = self.client.get("/libros/101")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["titulo"], "El Principito")

    def test_obtener_libro_inexistente(self):
        response = self.client.get("/libros/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Libro no encontrado")

    def test_crear_libro(self):
        response = self.client.post(
            "/libros/",
            json={
                "id": 200,
                "titulo": "Dune",
                "autor": "Frank Herbert",
                "categoria": "Ciencia Ficcion",
                "precio": 90,
                "stock": 7,
            },
            headers=build_auth_headers(),
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["id"], 200)

    def test_crear_libro_con_id_repetido(self):
        response = self.client.post(
            "/libros/",
            json={
                "id": 101,
                "titulo": "Duplicado",
                "autor": "Autor",
                "categoria": "Prueba",
                "precio": 20,
                "stock": 1,
            },
            headers=build_auth_headers(),
        )
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["detail"], "Ya existe un libro con ese ID.")


if __name__ == "__main__":
    unittest.main()
