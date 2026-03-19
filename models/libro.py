class Libro:
    """Representa los atributos del libro en el sistema de inventario de libreria"""
    def __init__(self,id,titulo,autor,categoria,precio,stock):
        """Inicializa un libro con los atributos basicos."""
        if not isinstance(id,int) or id<=0:
            raise ValueError("Valor de id invalido")
        if not isinstance(titulo,str) or not titulo.strip():
            raise ValueError("Valor de titulo invalido")
        if not isinstance(autor,str) or not autor.strip():
            raise ValueError("Valor de nombre de autor invalido")
        if not isinstance(categoria,str) or not categoria.strip():
            raise ValueError("Valor de categoria incorrecto")
        if not isinstance(precio,int) or precio<=0:
            raise ValueError("Valor de precio invalido")
        if not isinstance(stock,int) or stock<0:
            raise ValueError("Valor de stock invalido")
        self._id=id
        self._titulo=titulo
        self._autor=autor
        self._categoria=categoria
        self._precio=precio
        self._stock=stock
    @property
    def id(self):
        """Devuelve el valor asignado al id del libro"""
        return self._id
    @property
    def titulo(self):
        """Retorna el titulo del libro"""
        return self._titulo
    @property
    def autor(self):
        """Retorna el nombre del autor del libro"""
        return self._autor
    @property
    def categoria(self):
        """Retorna el nombre de la categoria del libro"""
        return self._categoria
    @property
    def precio(self):
        """Retorna el valor del precio del libro"""
        return self._precio
    @property
    def stock(self):
        """Retorna la cantidad de stock del libro"""
        return self._stock
    @property
    def disponible(self):
        """Retorna el estado de disponibilidad del libro"""
        return self._stock > 0
    @precio.setter
    def precio(self,nuevo_precio):
        """Actualiza el precio del libro"""
        if not isinstance(nuevo_precio,int) or nuevo_precio<=0:
            raise ValueError("Valor de precio invalido")
        self._precio=nuevo_precio
    def aumentar_stock(self,cantidad):
        """Metodo para aumentar el stock del libro"""
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("Cantidad invalida")
        self._stock+=cantidad
    def reducir_stock(self, cantidad):
        """Reduce el stock del libro al realizar una venta."""
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("Cantidad invalida")
        if cantidad > self._stock:
            raise ValueError("Stock insuficiente")
        self._stock -= cantidad
    def to_dict(self):
        """Convierte el objeto Libro a diccionario."""
        return {
            "id": self._id,
            "titulo": self._titulo,
            "autor": self._autor,
            "categoria": self._categoria,
            "precio": self._precio,
            "stock": self._stock
        }
    @classmethod
    def from_dict(cls, data):
        """Crea una instancia de Libro desde un diccionario."""
        return cls(
            data["id"],
            data["titulo"],
            data["autor"],
            data["categoria"],
            data["precio"],
            data["stock"]
        )
    def __str__(self):
        """Retorna la informacion completa del libro para el usuario"""
        estado= "Disponible" if self.disponible else "No Disponible"
        return f"Libro {self._titulo} - {self._autor} | Categoria: {self._categoria}, Precio: S/.{self._precio}, Stock: {self._stock}, Estado: {estado}"
    def __repr__(self):
        """Retorna la informacion tecnica de los atributos del libro"""
        return f"Libro(id={self._id}, titulo='{self._titulo}', autor='{self._autor}', categoria='{self._categoria}', precio={self._precio}, stock={self._stock}, disponible={self.disponible})"