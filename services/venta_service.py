from models.venta import Venta
class VentaService:
    """Servicio que gestiona la logica de negocio de las ventas."""
    def __init__(self):
        """Inicializa el servicio con una lista vacia de ventas."""
        self._ventas=[]
    def registrar_venta(self,libro,cliente,cantidad):
        """Crea y registra una nueva venta en el sistema."""
        venta=Venta(libro,cliente,cantidad)
        self._ventas.append(venta)
        return venta
    def listar_ventas(self):
        """Retorna la lista completa de ventas registradas."""
        return list(self._ventas)
    def buscar_venta_por_id(self,id_venta):
        """Busca y retorna una venta por su id."""
        for venta in self._ventas:
            if venta.id ==id_venta:
                return venta
        return None