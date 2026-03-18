import datetime
class Prestamo:
    """Representa los atributos necesarios para prestamo de libro"""
    def __init__(self,id,libro_id,usuario_id,fecha_prestamo,fecha_devolucion=None):
        self._id=id
        self._libro_id=libro_id
        self._usuario_id=usuario_id
        self._fecha_prestamo=fecha_prestamo
        self._fecha_devolucion=fecha_devolucion
    @property
    def id(self):
        """Devuelve el valor del id del prestamo"""
        return self._id
    @property
    def libro_id(self):
        """Devuelve el valor del libro para el prestamo"""
        return self._libro_id
    @property
    def usuario_id(self):
        """Devuelve el valor del usuario que pide el prestamo"""
        return self._usuario_id
    @property
    def fecha_prestamo(self):
        """Devuelve el valor de la fecha de solicitud del prestamo"""
        return self._fecha_prestamo
    @property
    def fecha_devolucion(self):
        """Devuelve el valor de la fecha de devolucion del prestamo"""
        return self._fecha_devolucion
    @fecha_devolucion.setter
    def fecha_devolucion(self,nueva_fecha):
        """Permite cambiar la fecha de devolucion del prestamo"""
        if nueva_fecha is not None and not isinstance(nueva_fecha, datetime.datetime):
            raise TypeError("La fecha debe ser un objeto datetime o None")
        self._fecha_devolucion=nueva_fecha
    def __str__(self):
        """Muestra los valores de los atributos de manera legible"""
        return f"Prestamo #{self._id} | Libro:{self._libro_id} | Usuario: {self._usuario_id} | Fecha:{self._fecha_prestamo}"
    def __repr__(self):
        """Muestra los valores de los atributos de manera tecnica"""
        return f"Prestamo(id={self._id}, libro_id={self._libro_id}, usuario_id={self._usuario_id}, fecha_prestamo={self._fecha_prestamo}, fecha_devolucion={self._fecha_devolucion})"