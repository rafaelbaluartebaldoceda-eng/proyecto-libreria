from models.venta import Venta

class VentaService:
    """Servicio que gestiona la logica de negocio de las ventas."""

    def __init__(self, venta_repo, libro_repo, cliente_repo):
        """Inicializa el servicio con los repositories necesarios."""
        self._venta_repo = venta_repo
        self._libro_repo = libro_repo
        self._cliente_repo = cliente_repo

    def registrar_venta(self, libro_id, cliente_dni, cantidad):
        """Crea y registra una nueva venta en el sistema."""
        libro = self._libro_repo.buscar_por_id(libro_id)
        cliente = self._cliente_repo.buscar_por_dni(cliente_dni)
        if not libro:
            raise ValueError("Libro no encontrado")
        if not cliente:
            raise ValueError("Cliente no encontrado")
        venta = Venta(libro, cliente, cantidad)
        self._venta_repo.guardar(venta)
        self._libro_repo.guardar(libro)
        return venta

    def listar_ventas(self):
        """Retorna una lista de todas las ventas registradas."""
        libros = self._libro_repo.obtener_todos()
        clientes = self._cliente_repo.obtener_todos()
        return self._venta_repo.obtener_todos(libros, clientes)

    def buscar_venta_por_id(self, id):
        """Busca y retorna una venta por su id."""
        libros = self._libro_repo.obtener_todos()
        clientes = self._cliente_repo.obtener_todos()
        return self._venta_repo.buscar_por_id(id, libros, clientes)

    def total_ventas(self):
        """Retorna el monto total acumulado de todas las ventas."""
        return self._venta_repo.total_ventas()