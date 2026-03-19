from models.venta import Venta
class VentaService:
    """Servicio que gestiona la logica de negocio de las ventas."""
    def __init__(self, storage, libros, clientes):
        """Inicializa el servicio con storage y datos de libros y clientes."""
        self._storage = storage
        self._libros = libros
        self._clientes = clientes
        self._ventas = self._cargar_ventas()
    def registrar_venta(self, libro, cliente, cantidad):
        """Crea y registra una nueva venta en el sistema."""
        if libro is None or cliente is None:
            raise ValueError("Libro y cliente son requeridos")
        venta = Venta(libro, cliente, cantidad)
        self._ventas.append(venta)
        self.guardar_ventas()
        return venta
    def guardar_ventas(self):
        """Guarda todas las ventas en el storage."""
        self._storage.guardar([v.to_dict() for v in self._ventas])
    def listar_ventas(self):
        """Retorna una copia de la lista de ventas registradas."""
        return list(self._ventas)
    def buscar_venta_por_id(self, id):
        """Busca y retorna una venta por su id, o None si no existe."""
        return next((v for v in self._ventas if v.id == id), None)
    def total_ventas(self):
        """Retorna el monto total acumulado de todas las ventas."""
        return sum(v.total for v in self._ventas)
    def _cargar_ventas(self):
        """Carga las ventas desde el storage."""
        data = self._storage.cargar()
        if data:
            Venta._contador_de_venta = max(v["id"] for v in data)
        ventas = []
        for v in data:
            libro = next((l for l in self._libros if l.id == v["libro_id"]), None)
            cliente = next((c for c in self._clientes if c.dni == v["cliente_dni"]), None)
            if libro and cliente:
                venta = Venta.from_dict(v, libro, cliente)
                ventas.append(venta)
        return ventas