class Libro:
    def __init__(self,id,titulo,autor,disponible=True):
        self._id=id
        self._titulo=titulo
        self._autor=autor
        self._disponible=disponible
    @property
    def id(self):
        return self._id
    @property
    def titulo(self):
        return self._titulo
    @property
    def autor(self):
        return self._autor
    @property
    def disponible(self):
        return self._disponible