from datetime import datetime
from models.libro import Libro
from models.cliente import Cliente

class Venta:
    """Entidad que representa una venta en el sistema de libreria."""
    _contador_de_venta = 0
    def __init__(self, libro, cliente, cantidad):
        """Inicializa una venta con libro, cliente y cantidad."""
        if not isinstance(libro, Libro):
            raise TypeError("El libro debe ser una instancia de Libro")
        if not isinstance(cliente, Cliente):
            raise TypeError("El cliente debe ser una instancia de Cliente")
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero positivo")
        if cantidad > libro.stock:
            raise ValueError("Stock insuficiente para realizar la venta")
        libro.reducir_stock(cantidad)
        Venta._contador_de_venta += 1
        self._id = Venta._contador_de_venta
        self._libro = libro
        self._cliente = cliente
        self._cantidad = cantidad
        self._fecha = datetime.now()
    @property
    def id(self):
        """Devuelve el id unico de la venta"""
        return self._id
    @property
    def libro(self):
        """Devuelve el objeto libro asociado a la venta"""
        return self._libro
    @property
    def cliente(self):
        """Devuelve el objeto cliente asociado a la venta"""
        return self._cliente
    @property
    def cantidad(self):
        """Devuelve la cantidad de libros vendidos"""
        return self._cantidad
    @property
    def total(self):
        """Calcula y devuelve el monto total de la venta dinamicamente"""
        return self._libro.precio * self._cantidad
    @property
    def fecha(self):
        """Devuelve la fecha y hora de la venta"""
        return self._fecha
    def to_dict(self):
        """Convierte el objeto Venta a diccionario."""
        return {
            "id": self._id,
            "libro_id": self._libro.id,
            "cliente_dni": self._cliente.dni,
            "cantidad": self._cantidad,
            "total": self.total,
            "fecha": self._fecha.isoformat()
        }
    @classmethod
    def from_dict(cls, data, libro, cliente):
        """Reconstruye una Venta desde un diccionario."""
        venta = cls.__new__(cls)
        venta._id = data["id"]
        venta._libro = libro
        venta._cliente = cliente
        venta._cantidad = data["cantidad"]
        venta._fecha = datetime.fromisoformat(data["fecha"])
        return venta
    def __str__(self):
        """Retorna la informacion de la venta de forma legible"""
        return (f"Venta #{self._id} | "
                f"Libro: {self._libro.titulo} | "
                f"Cliente: {self._cliente.nombre} | "
                f"Cantidad: {self._cantidad} | "
                f"Total: S/.{self.total} | "
                f"Fecha: {self._fecha.strftime('%Y-%m-%d %H:%M')}")
    def __repr__(self):
        """Retorna la informacion tecnica de la venta"""
        return (f"Venta(id={self._id}, "
                f"libro={repr(self._libro)}, "
                f"cliente={repr(self._cliente)}, "
                f"cantidad={self._cantidad}, "
                f"total={self.total}, "
                f"fecha='{self._fecha}')")