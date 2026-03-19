from models.venta import Venta
class VentaService:
    """Servicio que gestiona la logica de negocio de las ventas."""
    def __init__(self):
        """Inicializa el servicio con una lista vacia de ventas."""
        self._ventas = []
    def registrar_venta(self, libro, cliente, cantidad):
        """Crea y registra una nueva venta en el sistema."""
        if libro is None or cliente is None:
            raise ValueError("Libro y cliente son requeridos")
        venta = Venta(libro, cliente, cantidad)
        self._ventas.append(venta)
        return venta
    def listar_ventas(self):
        """Retorna una copia de la lista de ventas registradas."""
        return list(self._ventas)
    def buscar_venta_por_id(self, id):
        """Busca y retorna una venta por su id, o None si no existe."""
        return next((v for v in self._ventas if v.id == id), None)
    def total_ventas(self):
        """Retorna el monto total acumulado de todas las ventas."""
        return sum(v.total for v in self._ventas)