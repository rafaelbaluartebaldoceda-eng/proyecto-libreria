from models.cliente import Cliente
from models.libro import Libro


class LibreriaService:
    """Coordina operaciones base de catalogo y clientes."""

    def __init__(self, libro_repo, cliente_repo):
        self._libro_repo = libro_repo
        self._cliente_repo = cliente_repo

    def inicializar_datos_base(self):
        """Carga datos iniciales si la base aun esta vacia."""
        libros = self._libro_repo.obtener_todos()
        if not libros:
            libros = [
                Libro(101, "El Principito", "Antoine de Saint-Exupery", "Ficcion", 35, 10),
                Libro(102, "Cien Anios de Soledad", "Gabriel Garcia Marquez", "Realismo Magico", 45, 8),
                Libro(103, "1984", "George Orwell", "Distopia", 50, 6),
            ]
            for libro in libros:
                self._libro_repo.guardar(libro)

        clientes = self._cliente_repo.obtener_todos()
        if not clientes:
            clientes = [
                Cliente("12345678", "Ana Torres", "ana@gmail.com", "Lima"),
                Cliente("23456789", "Carlos Ruiz", "carlos@gmail.com", "Cusco"),
                Cliente("34567890", "Lucia Vega", "lucia@gmail.com", "Arequipa"),
                Cliente("45678901", "Marco Rios", "marco@gmail.com", "Piura"),
            ]
            for cliente in clientes:
                self._cliente_repo.guardar(cliente)

    def registrar_libro(self, libro_id, titulo, autor, categoria, precio, stock):
        """Registra un nuevo libro si el identificador aun no existe."""
        if self._libro_repo.buscar_por_id(libro_id):
            raise ValueError("Ya existe un libro con ese ID.")
        libro = Libro(libro_id, titulo, autor, categoria, precio, stock)
        self._libro_repo.guardar(libro)
        return libro

    def registrar_cliente(self, dni, nombre, correo, direccion, frecuente=False):
        """Registra un nuevo cliente si el DNI aun no existe."""
        if self._cliente_repo.buscar_por_dni(dni):
            raise ValueError("Ya existe un cliente con ese DNI.")
        cliente = Cliente(dni, nombre, correo, direccion, frecuente)
        self._cliente_repo.guardar(cliente)
        return cliente

    def listar_libros(self):
        """Retorna todos los libros registrados."""
        return self._libro_repo.obtener_todos()

    def buscar_libro(self, libro_id):
        """Busca un libro por su identificador."""
        return self._libro_repo.buscar_por_id(libro_id)

    def listar_clientes_frecuentes(self):
        """Retorna solo los clientes marcados como frecuentes."""
        return [cliente for cliente in self._cliente_repo.obtener_todos() if cliente.frecuente]
