from models.pedido import Pedido
class PedidoService:
    """Servicio que gestiona la logica de negocio de los pedidos."""
    def __init__(self):
        """Inicializa el servicio con una lista vacia de pedidos."""
        self._pedidos = []
    def registrar_pedido(self, libro, cliente, cantidad, metodo_entrega):
        """Crea y registra un nuevo pedido en el sistema."""
        if libro is None or cliente is None:
            raise ValueError("Libro y cliente son requeridos")
        pedido = Pedido(libro, cliente, cantidad, metodo_entrega)
        self._pedidos.append(pedido)
        return pedido
    def listar_pedidos(self):
        """Retorna una copia de la lista de pedidos registrados."""
        return list(self._pedidos)
    def buscar_pedido_por_id(self, id_pedido):
        """Busca y retorna un pedido por su id, o None si no existe."""
        return next((p for p in self._pedidos if p.id == id_pedido), None)
    def cambiar_estado(self, id_pedido, nuevo_estado):
        """Cambia el estado de un pedido existente."""
        pedido = self.buscar_pedido_por_id(id_pedido)
        if pedido is None:
            raise ValueError("Pedido no encontrado")
        nuevo_estado = nuevo_estado.lower()
        if nuevo_estado == "entregado":
            pedido.libro.reducir_stock(pedido.cantidad)
        pedido.estado = nuevo_estado
        return pedido
    def pedidos_por_estado(self, estado):
        """Retorna lista de pedidos filtrados por estado."""
        return [p for p in self._pedidos if p.estado == estado.lower()]