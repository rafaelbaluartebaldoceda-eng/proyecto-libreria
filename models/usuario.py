"""Entidad de dominio para autenticacion y autorizacion."""


class Usuario:
    """Representa un usuario autenticable del sistema."""

    def __init__(self, username, email, hashed_password, role="user", activo=True, user_id=None):
        """Inicializa un usuario validando sus atributos principales."""
        if not isinstance(username, str) or not username.strip():
            raise ValueError("Username invalido")
        if not isinstance(email, str) or "@" not in email or "." not in email:
            raise ValueError("Correo invalido")
        if not isinstance(hashed_password, str) or len(hashed_password.strip()) < 20:
            raise ValueError("Hash de contrasena invalido")
        if role not in ("admin", "user"):
            raise ValueError("Rol invalido")
        if not isinstance(activo, bool):
            raise ValueError("Estado activo invalido")

        self._id = user_id
        self._username = username
        self._email = email
        self._hashed_password = hashed_password
        self._role = role
        self._activo = activo

    @property
    def id(self):
        """Retorna el identificador persistente del usuario."""
        return self._id

    @property
    def username(self):
        """Retorna el username unico del usuario."""
        return self._username

    @property
    def email(self):
        """Retorna el correo del usuario."""
        return self._email

    @property
    def hashed_password(self):
        """Retorna la contrasena hasheada del usuario."""
        return self._hashed_password

    @property
    def role(self):
        """Retorna el rol del usuario."""
        return self._role

    @property
    def activo(self):
        """Indica si el usuario esta habilitado para autenticarse."""
        return self._activo

    def __repr__(self):
        """Retorna una representacion tecnica del usuario."""
        return (
            f"Usuario(id={self._id}, username='{self._username}', "
            f"email='{self._email}', role='{self._role}', activo={self._activo})"
        )
