from models.pedido import Pedido

class PedidoService:
    """Servicio que gestiona la logica de negocio de los pedidos."""

    def __init__(self, pedido_repo, libro_repo, cliente_repo):
        """Inicializa el servicio con los repositories necesarios."""
        self._pedido_repo = pedido_repo
        self._libro_repo = libro_repo
        self._cliente_repo = cliente_repo

    def registrar_pedido(self, libro_id, cliente_dni, cantidad, metodo_entrega):
        """Crea y registra un nuevo pedido en el sistema."""
        libro = self._libro_repo.buscar_por_id(libro_id)
        cliente = self._cliente_repo.buscar_por_dni(cliente_dni)
        if not libro:
            raise ValueError("Libro no encontrado")
        if not cliente:
            raise ValueError("Cliente no encontrado")
        pedido = Pedido(libro, cliente, cantidad, metodo_entrega)
        self._pedido_repo.guardar(pedido)
        return pedido

    def listar_pedidos(self):
        """Retorna una lista de todos los pedidos registrados."""
        libros = self._libro_repo.obtener_todos()
        clientes = self._cliente_repo.obtener_todos()
        return self._pedido_repo.obtener_todos(libros, clientes)

    def buscar_pedido_por_id(self, id_pedido):
        """Busca y retorna un pedido por su id."""
        libros = self._libro_repo.obtener_todos()
        clientes = self._cliente_repo.obtener_todos()
        return self._pedido_repo.buscar_por_id(id_pedido, libros, clientes)

    def cambiar_estado(self, id_pedido, nuevo_estado):
        """Cambia el estado de un pedido existente."""
        libros = self._libro_repo.obtener_todos()
        clientes = self._cliente_repo.obtener_todos()
        pedido = self._pedido_repo.buscar_por_id(id_pedido, libros, clientes)
        if pedido is None:
            raise ValueError("Pedido no encontrado")
        nuevo_estado = nuevo_estado.lower()
        if pedido.estado != "entregado" and nuevo_estado == "entregado":
            pedido.libro.reducir_stock(pedido.cantidad)
            self._libro_repo.guardar(pedido.libro)
        pedido.estado = nuevo_estado
        self._pedido_repo.actualizar_estado(id_pedido, nuevo_estado)
        return pedido

    def pedidos_por_estado(self, estado):
        """Retorna lista de pedidos filtrados por estado."""
        return [p for p in self.listar_pedidos() if p.estado == estado.lower()]