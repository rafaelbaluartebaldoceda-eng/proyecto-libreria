class Libro:
    """Representa los atributos del libro en el sistema de inventario de libreria"""
    def __init__(self,id,titulo,autor,disponible=True):
        """Inicializa un libro con los atributos basicos."""
        self._id=id
        if not titulo.strip():
            raise ValueError("El titulo no puede estar vacio")
        self._titulo=titulo
        if not autor.strip():
            raise ValueError("El nombre del autor no puede estar vacio")
        self._autor=autor
        self._disponible=disponible
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
    def disponible(self):
        """Retorna el estado de disponibilidad del libro"""
        return self._disponible
    @disponible.setter
    def disponible(self,disponible):
        """Se añade metodo que actualiza el estado de disponibilidad del libro"""
        if not isinstance(disponible,bool):
            raise TypeError("Valor incorrecto, no esta definido como booleano")
        self._disponible=disponible
    def __str__(self):
        """Retorna la informacion completa del libro para el usuario"""
        estado= "Disponible" if self._disponible else "No Disponible"
        return f"Libro {self._titulo} - {self._autor} ({estado})"
    def __repr__(self):
        """Retorna la informacion tecnica de los atributos del libro"""
        return f"Libro(id={self._id}, titulo={self._titulo}, autor={self._autor}, disponible={self._disponible})"