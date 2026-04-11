import unittest
from contextlib import contextmanager

from models.cliente import Cliente
from models.libro import Libro
from models.pedido import Pedido
from models.usuario import Usuario
from services.auth_service import AuthService
from services.libreria_service import LibreriaService
from services.pedido_service import PedidoService
from services.venta_service import VentaService


class FakeLibroRepo:
    def __init__(self, libro=None):
        self.libro = libro
        self.calls = []
        self.saved_books = []

    def buscar_por_id(self, libro_id, connection=None):
        self.calls.append(("buscar_por_id", connection))
        return self.libro

    def guardar(self, libro, connection=None):
        self.calls.append(("guardar", connection))
        self.saved_books.append(libro)

    def obtener_todos(self, connection=None):
        self.calls.append(("obtener_todos", connection))
        return [self.libro] if self.libro else []


class FakeClienteRepo:
    def __init__(self, cliente=None):
        self.cliente = cliente
        self.calls = []
        self.saved_clients = []

    def buscar_por_dni(self, dni, connection=None):
        self.calls.append(("buscar_por_dni", connection))
        return self.cliente

    def guardar(self, cliente, connection=None):
        self.calls.append(("guardar", connection))
        self.saved_clients.append(cliente)

    def obtener_todos(self, connection=None):
        self.calls.append(("obtener_todos", connection))
        return [self.cliente] if self.cliente else []


class FakeVentaRepo:
    def __init__(self, should_fail=False):
        self.should_fail = should_fail
        self.calls = []

    def guardar(self, venta, connection=None):
        self.calls.append(("guardar", connection))
        if self.should_fail:
            raise RuntimeError("db failure")
        venta._id = 99


class FakePedidoRepo:
    def __init__(self, pedido=None):
        self.pedido = pedido
        self.calls = []
        self.updated_states = []

    def guardar(self, pedido, connection=None):
        self.calls.append(("guardar", connection))
        pedido._id = 10

    def obtener_todos(self, libros, clientes, connection=None):
        self.calls.append(("obtener_todos", connection))
        return [self.pedido] if self.pedido else []

    def buscar_por_id(self, pedido_id, libros, clientes, connection=None):
        self.calls.append(("buscar_por_id", connection))
        return self.pedido

    def actualizar_estado(self, pedido_id, nuevo_estado, connection=None):
        self.calls.append(("actualizar_estado", connection))
        self.updated_states.append((pedido_id, nuevo_estado))


class FakeUsuarioRepo:
    def __init__(self):
        self.users_by_username = {}
        self.users_by_email = {}
        self.saved_users = []

    def buscar_por_username(self, username, connection=None):
        return self.users_by_username.get(username)

    def buscar_por_email(self, email, connection=None):
        return self.users_by_email.get(email)

    def guardar(self, usuario, connection=None):
        usuario._id = len(self.saved_users) + 1
        self.saved_users.append(usuario)
        self.users_by_username[usuario.username] = usuario
        self.users_by_email[usuario.email] = usuario
        return usuario

    def existe_admin_activo(self, connection=None):
        return any(
            usuario.role == "admin" and usuario.activo
            for usuario in self.saved_users
        )


class ServiceTests(unittest.TestCase):
    def test_libreria_service_registra_libro_nuevo(self):
        libro_repo = FakeLibroRepo()
        cliente_repo = FakeClienteRepo()
        service = LibreriaService(libro_repo, cliente_repo)

        libro = service.registrar_libro(1, "DDD", "Evans", "Software", 120, 6)

        self.assertEqual(libro.id, 1)
        self.assertEqual(len(libro_repo.saved_books), 1)

    def test_venta_service_usa_una_sola_transaccion(self):
        libro = Libro(1, "DDD", "Evans", "Software", 120, 5)
        cliente = Cliente("12345678", "Ana", "ana@mail.com", "Lima")
        libro_repo = FakeLibroRepo(libro)
        cliente_repo = FakeClienteRepo(cliente)
        venta_repo = FakeVentaRepo()
        service = VentaService(venta_repo, libro_repo, cliente_repo)
        token = object()

        @contextmanager
        def fake_transaction():
            yield token

        from unittest.mock import patch

        with patch("services.venta_service.managed_connection", fake_transaction):
            venta = service.registrar_venta(1, "12345678", 2)

        self.assertEqual(venta.id, 99)
        self.assertTrue(all(call[1] is token for call in libro_repo.calls))
        self.assertTrue(all(call[1] is token for call in cliente_repo.calls))
        self.assertTrue(all(call[1] is token for call in venta_repo.calls))

    def test_venta_service_no_actualiza_stock_persistido_si_falla_la_venta(self):
        libro = Libro(1, "DDD", "Evans", "Software", 120, 5)
        cliente = Cliente("12345678", "Ana", "ana@mail.com", "Lima")
        libro_repo = FakeLibroRepo(libro)
        cliente_repo = FakeClienteRepo(cliente)
        venta_repo = FakeVentaRepo(should_fail=True)
        service = VentaService(venta_repo, libro_repo, cliente_repo)
        rollback_state = {"rolled_back": False}

        @contextmanager
        def fake_transaction():
            try:
                yield object()
            except RuntimeError:
                rollback_state["rolled_back"] = True
                raise

        from unittest.mock import patch

        with patch("services.venta_service.managed_connection", fake_transaction):
            with self.assertRaises(RuntimeError):
                service.registrar_venta(1, "12345678", 2)

        self.assertTrue(rollback_state["rolled_back"])
        self.assertEqual(libro_repo.saved_books, [])

    def test_pedido_service_entrega_descuenta_stock_y_actualiza_estado(self):
        libro = Libro(1, "DDD", "Evans", "Software", 120, 5)
        cliente = Cliente("12345678", "Ana", "ana@mail.com", "Lima")
        pedido = Pedido(libro, cliente, 2, "tienda", pedido_id=7)
        libro_repo = FakeLibroRepo(libro)
        cliente_repo = FakeClienteRepo(cliente)
        pedido_repo = FakePedidoRepo(pedido)
        service = PedidoService(pedido_repo, libro_repo, cliente_repo)
        token = object()

        @contextmanager
        def fake_transaction():
            yield token

        from unittest.mock import patch

        with patch("services.pedido_service.managed_connection", fake_transaction):
            resultado = service.cambiar_estado(7, "entregado")

        self.assertEqual(resultado.estado, "entregado")
        self.assertEqual(libro.stock, 3)
        self.assertEqual(pedido_repo.updated_states, [(7, "entregado")])
        self.assertTrue(all(call[1] is token for call in libro_repo.calls))
        self.assertTrue(all(call[1] is token for call in cliente_repo.calls))
        self.assertTrue(all(call[1] is token for call in pedido_repo.calls))

    def test_auth_service_registra_y_autentica_usuario(self):
        usuario_repo = FakeUsuarioRepo()
        service = AuthService(usuario_repo)
        token = object()

        @contextmanager
        def fake_transaction():
            yield token

        from unittest.mock import patch

        with patch("services.auth_service.managed_connection", fake_transaction):
            usuario = service.registrar_usuario(
                "admin",
                "admin@example.com",
                "admin1234",
                role="admin",
            )
            autenticado = service.autenticar_usuario("admin", "admin1234")

        self.assertIsNotNone(usuario.id)
        self.assertNotEqual(usuario.hashed_password, "admin1234")
        self.assertEqual(autenticado.username, "admin")

    def test_auth_service_rechaza_username_duplicado(self):
        usuario_repo = FakeUsuarioRepo()
        service = AuthService(usuario_repo)
        existente = Usuario("admin", "admin@example.com", "x" * 30, role="admin")
        usuario_repo.guardar(existente)
        token = object()

        @contextmanager
        def fake_transaction():
            yield token

        from unittest.mock import patch

        with patch("services.auth_service.managed_connection", fake_transaction):
            with self.assertRaises(ValueError):
                service.registrar_usuario("admin", "otro@example.com", "admin1234")

    def test_auth_service_detecta_admin_activo(self):
        usuario_repo = FakeUsuarioRepo()
        service = AuthService(usuario_repo)
        usuario_repo.guardar(
            Usuario("admin", "admin@example.com", "x" * 30, role="admin")
        )
        token = object()

        @contextmanager
        def fake_transaction():
            yield token

        from unittest.mock import patch

        with patch("services.auth_service.managed_connection", fake_transaction):
            self.assertTrue(service.existe_admin_activo())


if __name__ == "__main__":
    unittest.main()
