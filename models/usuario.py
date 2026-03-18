class Usuario:
    """Representa los atributos del usuario en el sistema de libreria"""
    def __init__(self,id,nombre,email):
        """Inicializa los datos del usuario en el sistema de libreria"""
        self._id=id
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacio")
        self._nombre=nombre
        self._email=None
        self.email=email
    @property
    def id(self):
        """Devuelve el valor de id del usuario"""
        return self._id
    @property
    def nombre(self):
        """Devuelve el nombre del usuario"""
        return self._nombre
    @property
    def email(self):
        """Devuelve el email del usuario"""
        return self._email
    @email.setter
    def email(self,email):
        """Metodo que permite actualizar el email del usuario"""
        if "@" not in email:
            raise ValueError("Email invalido")
        self._email=email
    def __str__(self):
        """Devuelve los datos del usuario de manera legible"""
        return f"Usuario: {self._nombre} ({self._id}) Email:{self._email}"
    def __repr__(self):
        """Devuelve la informacion del usuario de manera tecnica"""
        return f"Usuario(id={self._id},nombre={self._nombre},email={self._email})"