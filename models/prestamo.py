import datetime
class Prestamo:
    def __init__(self,id,libro_id,usuario_id,fecha_prestamo,fecha_devolucion=None):
        self._id=id
        self._libro_id=libro_id
        self._usuario_id=usuario_id
        self._fecha_prestamo=fecha_prestamo
        self._fecha_devolucion=fecha_devolucion
    @property
    def id(self):
        return self._id
    @property
    def libro_id(self):
        return self._libro_id
    @property
    def usuario_id(self):
        return self._usuario_id
    @property
    def fecha_prestamo(self):
        return self._fecha_prestamo
    @property
    def fecha_devolucion(self):
        return self._fecha_devolucion
    @fecha_devolucion.setter
    def fecha_devolucion(self,nueva_fecha):
        if nueva_fecha is not None and not isinstance(nueva_fecha, datetime.datetime):
            raise TypeError("La fecha debe ser un objeto datetime o None")
        self._fecha_devolucion=nueva_fecha
    def __str__(self):
        return f"Prestamo #{self._id} | Libro:{self._libro_id} | Usuario: {self._usuario_id} | Fecha:{self._fecha_prestamo}"
    def __repr__(self):
        return f"Prestamo(id={self._id}, libro_id={self._libro_id}, usuario_id={self._usuario_id}, fecha_prestamo={self._fecha_prestamo}, fecha_devolucion={self._fecha_devolucion})"