from datetime import datetime
from models.libro import Libro
from models.cliente import Cliente

class Pedido:
    """Entidad que representa un pedido en el sistema de libreria."""
    _contador_pedido = 0
    def __init__(self, libro, cliente, cantidad, metodo_entrega, estado="pendiente"):
        """Inicializa un pedido con libro, cliente, cantidad y metodo de entrega."""
        if not isinstance(libro, Libro):
            raise TypeError("El libro debe ser una instancia de Libro")
        if not isinstance(cliente, Cliente):
            raise TypeError("El cliente debe ser una instancia de Cliente")
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero positivo")
        metodo_entrega = metodo_entrega.lower()
        if metodo_entrega not in ("tienda", "domicilio"):
            raise ValueError("El metodo de entrega debe ser 'tienda' o 'domicilio'")
        if estado not in ("pendiente", "entregado", "cancelado"):
            raise ValueError("El estado debe ser 'pendiente', 'entregado' o 'cancelado'")
        Pedido._contador_pedido += 1
        self._id = Pedido._contador_pedido
        self._libro = libro
        self._cliente = cliente
        self._cantidad = cantidad
        self._metodo_entrega = metodo_entrega
        self._estado = estado
        self._fecha = datetime.now()
    @property
    def id(self):
        """Devuelve el id unico del pedido"""
        return self._id
    @property
    def libro(self):
        """Devuelve el objeto libro asociado al pedido"""
        return self._libro
    @property
    def cliente(self):
        """Devuelve el objeto cliente asociado al pedido"""
        return self._cliente
    @property
    def cantidad(self):
        """Devuelve la cantidad de libros del pedido"""
        return self._cantidad
    @property
    def metodo_entrega(self):
        """Devuelve el metodo de entrega del pedido"""
        return self._metodo_entrega
    @property
    def estado(self):
        """Devuelve el estado actual del pedido"""
        return self._estado
    @property
    def fecha(self):
        """Devuelve la fecha y hora del pedido"""
        return self._fecha
    @estado.setter
    def estado(self, nuevo_estado):
        """Actualiza el estado del pedido"""
        if not isinstance(nuevo_estado, str) or nuevo_estado not in ("pendiente", "entregado", "cancelado"):
            raise ValueError("El estado debe ser 'pendiente', 'entregado' o 'cancelado'")
        if nuevo_estado == self._estado:
            raise ValueError("El estado no puede ser el mismo")
        self._estado = nuevo_estado
    @property
    def total(self):
        """Calcula y devuelve el total del pedido dinamicamente"""
        return self._libro.precio * self._cantidad
    def to_dict(self):
        """Convierte el objeto Pedido a diccionario."""
        return {
            "id": self._id,
            "libro_id": self._libro.id,
            "cliente_dni": self._cliente.dni,
            "cantidad": self._cantidad,
            "metodo_entrega": self._metodo_entrega,
            "estado": self._estado,
            "fecha": self._fecha.isoformat()
        }

    @classmethod
    def from_dict(cls, data, libro, cliente):
        """Reconstruye un Pedido desde un diccionario."""
        pedido = cls.__new__(cls)
        pedido._id = data["id"]
        pedido._libro = libro
        pedido._cliente = cliente
        pedido._cantidad = data["cantidad"]
        pedido._metodo_entrega = data["metodo_entrega"]
        pedido._estado = data["estado"]
        pedido._fecha = datetime.fromisoformat(data["fecha"])
        return pedido
    def __str__(self):
        """Retorna la informacion del pedido de forma legible"""
        return (f"Pedido #{self._id} | "
                f"Libro: {self._libro.titulo} | "
                f"Cliente: {self._cliente.nombre} | "
                f"Cantidad: {self._cantidad} | "
                f"Total: S/.{self.total} | "
                f"Entrega: {self._metodo_entrega} | "
                f"Estado: {self._estado} | "
                f"Fecha: {self._fecha.strftime('%Y-%m-%d %H:%M')}")
    def __repr__(self):
        """Retorna la informacion tecnica del pedido"""
        return (f"Pedido(id={self._id}, "
                f"libro={repr(self._libro)}, "
                f"cliente={repr(self._cliente)}, "
                f"cantidad={self._cantidad}, "
                f"total={self.total}, "
                f"metodo_entrega='{self._metodo_entrega}', "
                f"estado='{self._estado}', "
                f"fecha='{self._fecha}')")