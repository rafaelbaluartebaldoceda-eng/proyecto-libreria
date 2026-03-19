class Cliente:
    """Entidad que representa un cliente en el sistema de libreria."""
    def __init__(self,dni,nombre,correo,direccion,frecuente=False):
        """Inicializa los datos el usuario en el sistema"""
        if not isinstance(dni,str) or len(dni)!= 8 or not dni.isdigit():
            raise ValueError("Valor de DNI invalido, ingrese nuevamente")
        if not isinstance(nombre,str) or not nombre.strip():
            raise ValueError("Nombre invalido, ingrese nuevamente")
        if not isinstance(correo,str) or "@" not in correo or "." not in correo:
            raise ValueError("Direccion de correo invalida") 
        if not isinstance(direccion,str) or not direccion.strip():
            raise ValueError("Direccion invalida")
        if not isinstance(frecuente,bool):
            raise ValueError("Estado del cliente invalido")
        self._dni=dni
        self._nombre=nombre
        self._correo=correo
        self._direccion=direccion
        self._frecuente=frecuente
    @property
    def dni(self):
        """Devuelve el numero de DNI del ciente"""
        return self._dni
    @property
    def nombre(self):
        """Devuelve el nombre del cliente registrado"""
        return self._nombre
    @property
    def correo(self):
        """Devuelve la direccion de correo registrada del cliente"""
        return self._correo
    @property
    def direccion(self):
        """Devuelve la direccion de vivienda del cliente"""
        return self._direccion
    @property
    def frecuente(self):
        """Devuelve el estado del cliente, si es frecuente o no"""
        return self._frecuente
    @correo.setter
    def correo(self,nuevo_correo):
        """Actualiza el correo del cliente"""
        if not isinstance(nuevo_correo,str) or "@" not in nuevo_correo or "." not in nuevo_correo:
            raise ValueError("Nueva direccion de correo invalida")
        self._correo=nuevo_correo
    @direccion.setter
    def direccion(self,nueva_direccion):
        """Actualiza la direccion del cliente"""
        if not isinstance(nueva_direccion,str) or not nueva_direccion.strip():
            raise ValueError("Nueva direccion invalida")
        self._direccion=nueva_direccion
    @frecuente.setter
    def frecuente(self,es_frecuente):
        """Actualiza el estado frecuente del cliente"""
        if not isinstance(es_frecuente,bool):
            raise ValueError("El estado frecuente debe ser booleano")
        self._frecuente=es_frecuente
    def marcar_como_frecuente(self):
        """Marca al cliente como frecuente."""
        self._frecuente = True
    def to_dict(self):
        """Convierte el objeto Cliente a diccionario."""
        return {
            "dni": self._dni,
            "nombre": self._nombre,
            "correo": self._correo,
            "direccion": self._direccion,
            "frecuente": self._frecuente
        }
    @classmethod
    def from_dict(cls, data):
        """Crea una instancia de Cliente desde un diccionario."""
        return cls(
            data["dni"],
            data["nombre"],
            data["correo"],
            data["direccion"],
            data["frecuente"]
        )
    def __str__(self):
        """Devuelve los datos del cliente de forma legible"""
        frecuente="Si" if self._frecuente else "No"
        return f"Nombre: {self._nombre} ({self._dni}) | Correo: {self._correo} | Direccion: {self._direccion} | Cliente Frecuente: {frecuente}"
    def __repr__(self):
        """Devuelve los datos del cliente de forma tecnica"""
        return f"Cliente(dni='{self._dni}', nombre='{self._nombre}', correo='{self._correo}', direccion='{self._direccion}', frecuente={self._frecuente})"
