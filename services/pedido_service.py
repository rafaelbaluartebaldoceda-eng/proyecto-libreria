from models.pedido import Pedido

class PedidoService:
    """Servicio que gestiona la logica de negocio de los pedidos."""

    def __init__(self, storage, libros, clientes):
        """Inicializa el servicio con storage y datos de libros y clientes."""
        self._storage = storage
        self._libros = libros
        self._clientes = clientes
        self._pedidos = self._cargar_pedidos()

    def registrar_pedido(self, libro, cliente, cantidad, metodo_entrega):
        """Crea y registra un nuevo pedido en el sistema."""
        if libro is None or cliente is None:
            raise ValueError("Libro y cliente son requeridos")
        pedido = Pedido(libro, cliente, cantidad, metodo_entrega)
        self._pedidos.append(pedido)
        self.guardar_pedidos()
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
        if pedido.estado != "entregado" and nuevo_estado == "entregado":
            pedido.libro.reducir_stock(pedido.cantidad)
        pedido.estado = nuevo_estado
        self.guardar_pedidos()
        return pedido

    def pedidos_por_estado(self, estado):
        """Retorna lista de pedidos filtrados por estado."""
        return [p for p in self._pedidos if p.estado == estado.lower()]

    def guardar_pedidos(self):
        """Guarda todos los pedidos en el storage."""
        self._storage.guardar([p.to_dict() for p in self._pedidos])

    def _cargar_pedidos(self):
        """Carga los pedidos desde el storage."""
        data = self._storage.cargar()
        if data:
            Pedido._contador_pedido = max(p["id"] for p in data)
        pedidos = []
        for p in data:
            libro = next((l for l in self._libros if l.id == p["libro_id"]), None)
            cliente = next((c for c in self._clientes if c.dni == p["cliente_dni"]), None)
            if libro and cliente:
                pedido = Pedido.from_dict(p, libro, cliente)
                pedidos.append(pedido)
        return pedidos