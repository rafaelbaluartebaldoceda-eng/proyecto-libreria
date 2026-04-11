"""Pruebas basicas de la capa FastAPI para autenticacion y autorizacion."""

import unittest

from fastapi.testclient import TestClient

from app.dependencies import get_auth_service, get_libreria_service
from app.main import app
from models.libro import Libro
from auth_test_utils import FakeAuthService, build_auth_headers


class FakeLibreriaAdminService:
    """Doble de prueba minimo para validar rutas administrativas protegidas."""

    def registrar_libro(self, libro_id, titulo, autor, categoria, precio, stock):
        """Retorna un libro simulado cuando el admin crea catalogo."""
        return Libro(libro_id, titulo, autor, categoria, precio, stock)


class AuthApiTests(unittest.TestCase):
    """Valida el comportamiento de auth y de la autorizacion por rol."""

    def setUp(self):
        self.fake_auth_service = FakeAuthService()
        self.fake_libreria_service = FakeLibreriaAdminService()
        app.dependency_overrides[get_auth_service] = lambda: self.fake_auth_service
        app.dependency_overrides[get_libreria_service] = lambda: self.fake_libreria_service
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()

    def test_register_user(self):
        """Valida el registro publico de un usuario comun."""
        response = self.client.post(
            "/auth/register",
            json={
                "username": "nuevo_usuario",
                "email": "nuevo@example.com",
                "password": "clave1234",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["role"], "user")

    def test_register_user_with_duplicate_username(self):
        """Verifica que el registro falle si el username ya existe."""
        response = self.client.post(
            "/auth/register",
            json={
                "username": "admin",
                "email": "otro@example.com",
                "password": "clave1234",
            },
        )
        self.assertEqual(response.status_code, 409)

    def test_register_user_with_weak_password(self):
        """Verifica que el registro rechace passwords sin numeros o letras."""
        response = self.client.post(
            "/auth/register",
            json={
                "username": "debil",
                "email": "debil@example.com",
                "password": "sololetras",
            },
        )
        self.assertEqual(response.status_code, 422)

    def test_login_success(self):
        """Valida que el login correcto retorne un Bearer token."""
        response = self.client.post(
            "/token",
            data={"username": "admin", "password": "admin123"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["token_type"], "bearer")
        self.assertIn("access_token", response.json())

    def test_login_invalid_credentials(self):
        """Verifica que el login falle con credenciales incorrectas."""
        response = self.client.post(
            "/token",
            data={"username": "admin", "password": "incorrecta"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Incorrect username or password")

    def test_read_current_user(self):
        """Valida que el perfil del usuario autenticado sea accesible con token."""
        response = self.client.get("/users/me", headers=build_auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "admin")

    def test_read_current_user_without_token(self):
        """Verifica que una ruta protegida exija autenticacion."""
        response = self.client.get("/users/me")
        self.assertEqual(response.status_code, 401)

    def test_read_current_user_with_invalid_token(self):
        """Verifica que una ruta protegida rechace tokens invalidos."""
        response = self.client.get(
            "/users/me",
            headers={"Authorization": "Bearer token-invalido"},
        )
        self.assertEqual(response.status_code, 401)

    def test_admin_route_forbids_user_role(self):
        """Verifica que un usuario comun no pueda ejecutar acciones admin."""
        response = self.client.post(
            "/libros/",
            json={
                "id": 999,
                "titulo": "Libro Protegido",
                "autor": "Autor",
                "categoria": "Prueba",
                "precio": 20,
                "stock": 4,
            },
            headers=build_auth_headers("usuario", "user"),
        )
        self.assertEqual(response.status_code, 403)

    def test_admin_can_create_users_with_role(self):
        """Verifica que un admin pueda crear usuarios con rol explicito."""
        response = self.client.post(
            "/auth/users",
            json={
                "username": "nuevo_admin",
                "email": "nuevo_admin@example.com",
                "password": "admin1234",
                "role": "admin",
            },
            headers=build_auth_headers(),
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["role"], "admin")

    def test_bootstrap_admin_creates_first_admin(self):
        """Permite crear el primer admin cuando el sistema aun no tiene uno."""
        app.dependency_overrides[get_auth_service] = lambda: FakeAuthService(
            include_default_admin=False
        )

        response = self.client.post(
            "/auth/bootstrap-admin",
            json={
                "username": "primer_admin",
                "email": "primer_admin@example.com",
                "password": "primeradmin123",
                "bootstrap_token": "bootstrap-admin-token-123",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["role"], "admin")

    def test_bootstrap_admin_rejects_invalid_bootstrap_token(self):
        """Rechaza el bootstrap si el token especial no coincide."""
        app.dependency_overrides[get_auth_service] = lambda: FakeAuthService(
            include_default_admin=False
        )

        response = self.client.post(
            "/auth/bootstrap-admin",
            json={
                "username": "primer_admin",
                "email": "primer_admin@example.com",
                "password": "primeradmin123",
                "bootstrap_token": "token-incorrecto-1234",
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_bootstrap_admin_rejects_when_admin_already_exists(self):
        """Bloquea el bootstrap si ya hay un administrador activo."""
        response = self.client.post(
            "/auth/bootstrap-admin",
            json={
                "username": "otro_admin",
                "email": "otro_admin@example.com",
                "password": "otroadmin123",
                "bootstrap_token": "bootstrap-admin-token-123",
            },
        )
        self.assertEqual(response.status_code, 409)


if __name__ == "__main__":
    unittest.main()
