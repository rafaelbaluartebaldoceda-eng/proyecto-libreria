import unittest

from models.cliente import Cliente
from models.libro import Libro
from models.pedido import Pedido
from models.venta import Venta


class DomainModelTests(unittest.TestCase):
    def test_venta_reduce_stock_and_leave_id_pending_until_persisted(self):
        libro = Libro(1, "Clean Code", "Robert C. Martin", "Software", 80, 5)
        cliente = Cliente("12345678", "Ana", "ana@mail.com", "Lima")

        venta = Venta(libro, cliente, 2)

        self.assertIsNone(venta.id)
        self.assertEqual(venta.total, 160)
        self.assertEqual(libro.stock, 3)

    def test_venta_rejects_stock_insuficiente(self):
        libro = Libro(1, "1984", "George Orwell", "Distopia", 50, 1)
        cliente = Cliente("12345678", "Ana", "ana@mail.com", "Lima")

        with self.assertRaises(ValueError):
            Venta(libro, cliente, 2)

    def test_pedido_valida_metodo_entrega(self):
        libro = Libro(1, "1984", "George Orwell", "Distopia", 50, 4)
        cliente = Cliente("12345678", "Ana", "ana@mail.com", "Lima")

        with self.assertRaises(ValueError):
            Pedido(libro, cliente, 1, "drone")

    def test_cliente_valida_dni(self):
        with self.assertRaises(ValueError):
            Cliente("1234", "Ana", "ana@mail.com", "Lima")


if __name__ == "__main__":
    unittest.main()

